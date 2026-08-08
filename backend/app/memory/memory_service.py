from typing import Optional, List, Dict, Any
from app.repositories.memory_repository import MemoryRepository
from app.memory.memory_cache import MemoryCache
from app.memory.memory_validator import MemoryValidator
from app.memory.memory_serializer import MemorySerializer
from app.memory.memory_migration import MemoryMigrationManager
from app.memory.memory_metrics import get_memory_metrics, MemoryMetricsTracker
from app.memory.memory_retry_manager import MemoryRetryManager
from app.memory.session_snapshot import SessionSnapshotManager
from app.memory.memory_search import MemorySearchEngine
from app.memory.retention_manager import DataRetentionManager
from app.memory.memory_security import MemorySecurity
from app.memory.memory_models import (
    InterviewMemory,
    SessionMemory,
    CandidateMemory,
    EvaluationMemory,
    FeedbackMemory,
)
from app.models.feedback_report import FeedbackReportModel
from app.services.interview_state import InterviewSessionState
from app.services.candidate_service import CandidateService, get_candidate_service
from app.utils.helpers import get_utc_now
from app.core.logging_config import logger


class MemoryService:
    """
    Production-grade Service Layer for managing persistent interview memories.
    Communicates with MemoryRepository (decoupled from providers) and integrates
    MemoryCache, MemoryValidator, SessionSnapshotManager, MemorySearchEngine,
    DataRetentionManager, MemorySecurity, and Telemetry Metrics.
    """

    def __init__(
        self,
        repository: Optional[MemoryRepository] = None,
        cache: Optional[MemoryCache] = None,
        snapshot_manager: Optional[SessionSnapshotManager] = None,
        retention_manager: Optional[DataRetentionManager] = None,
        metrics_tracker: Optional[MemoryMetricsTracker] = None,
        candidate_service: Optional[CandidateService] = None,
    ):
        self.repository = repository or MemoryRepository()
        self.cache = cache or MemoryCache()
        self.snapshot_manager = snapshot_manager or SessionSnapshotManager()
        self.retention_manager = retention_manager or DataRetentionManager()
        self.metrics_tracker = metrics_tracker or get_memory_metrics()
        self.candidate_service = candidate_service or get_candidate_service()

    def initialize_session_memory(self, session: InterviewSessionState) -> InterviewMemory:
        """
        Creates, validates, caches, snapshots, and persists initial InterviewMemory document upon session start.
        """
        candidate = self.candidate_service.get_candidate()

        sess_mem = SessionMemory(
            session_id=session.session_id,
            candidate_id=session.candidate_id,
            started_at=session.started_at,
            done=session.done,
            total_questions=len(session.plan.questions),
            current_question_index=session.current_question_index,
        )

        curr_day = candidate.progress.completed_days[-1] + 1 if candidate.progress.completed_days else 1
        cand_mem = CandidateMemory(
            candidate_id=candidate.candidate_id,
            full_name=candidate.full_name,
            target_role=candidate.target_role,
            current_day=curr_day,
            completed_topics=candidate.completed_topics,
        )

        memory = InterviewMemory(
            memory_id=session.session_id,
            session=sess_mem,
            candidate=cand_mem,
            turns=[],
            knowledge_gaps=[],
            feedback=None,
            updated_at=get_utc_now(),
        )

        # Pre-flight Validation
        MemoryValidator.validate(memory)

        # Snapshot Milestone
        self.snapshot_manager.create_snapshot(session.session_id, "Interview started", memory)

        # Encrypt sensitive fields before persistence
        sec_memory = MemorySecurity.encrypt_sensitive_fields(memory)

        # Persist via RetryManager & Repository
        MemoryRetryManager.execute_with_retry(lambda: self.repository.save(sec_memory))
        
        # Cache plaintext in memory
        plain_memory = MemorySecurity.decrypt_sensitive_fields(sec_memory)
        self.cache.put(memory.memory_id, plain_memory)
        self.metrics_tracker.record_write()

        logger.info(f"Memory write: Session memory initialized for '{session.session_id}'.")
        return plain_memory

    def record_turn_memory(
        self,
        session: InterviewSessionState,
        question_id: str,
        topic_id: str,
        topic_title: str,
        question_text: str,
        candidate_answer: str,
        score: int,
        classification: str,
        confidence_score: int,
        action_type: str,
        difficulty: str,
    ) -> Optional[InterviewMemory]:
        """
        Appends turn answer and evaluation result to persistent memory.
        """
        mem = self.get_session_memory(session.session_id)
        if not mem:
            mem = self.initialize_session_memory(session)

        turn_index = len(mem.turns)
        eval_mem = EvaluationMemory(
            turn_index=turn_index,
            question_id=question_id,
            topic_id=topic_id,
            topic_title=topic_title,
            question_text=question_text,
            candidate_answer=candidate_answer,
            score=score,
            classification=classification,
            confidence_score=confidence_score,
            action_type=action_type,
            difficulty=difficulty,
        )

        mem.turns.append(eval_mem)
        mem.session.current_question_index = session.current_question_index
        mem.session.done = session.done
        mem.updated_at = get_utc_now()

        MemoryValidator.validate(mem)
        
        # Create Snapshot Milestone
        self.snapshot_manager.create_snapshot(session.session_id, "Question answered", mem)

        sec_memory = MemorySecurity.encrypt_sensitive_fields(mem)
        MemoryRetryManager.execute_with_retry(lambda: self.repository.update(session.session_id, sec_memory))
        
        plain_memory = MemorySecurity.decrypt_sensitive_fields(sec_memory)
        self.cache.put(session.session_id, plain_memory)
        self.metrics_tracker.record_update()

        logger.info(f"Memory update: Recorded turn {turn_index + 1} memory for session '{session.session_id}'.")
        return plain_memory

    def record_feedback_memory(
        self, session_id: str, feedback_report: FeedbackReportModel
    ) -> Optional[InterviewMemory]:
        """
        Stores final completed feedback report in persistent memory.
        """
        mem = self.get_session_memory(session_id)
        if not mem:
            logger.warning(f"Memory failure: Cannot attach feedback report to missing memory '{session_id}'.")
            return None

        mem.session.done = True
        mem.session.completed_at = get_utc_now()
        mem.feedback = FeedbackMemory(
            overall_score=feedback_report.overall_score.overall_score,
            grade=feedback_report.overall_score.grade,
            rating_label=feedback_report.overall_score.rating_label,
            report_json=feedback_report.model_dump(),
        )
        mem.updated_at = get_utc_now()

        MemoryValidator.validate(mem)
        
        # Create Snapshot Milestone
        self.snapshot_manager.create_snapshot(session_id, "Interview finished", mem)

        sec_memory = MemorySecurity.encrypt_sensitive_fields(mem)
        MemoryRetryManager.execute_with_retry(lambda: self.repository.update(session_id, sec_memory))
        
        plain_memory = MemorySecurity.decrypt_sensitive_fields(sec_memory)
        self.cache.put(session_id, plain_memory)
        self.metrics_tracker.record_update()

        logger.info(f"Memory update: Attached final feedback report to memory '{session_id}'.")
        return plain_memory

    def get_session_memory(self, session_id: str) -> Optional[InterviewMemory]:
        """
        Retrieves session memory document by ID (checking Cache first, then Repository).
        """
        cached = self.cache.get(session_id)
        if cached:
            self.metrics_tracker.record_read(hit_cache=True)
            return cached

        mem = self.repository.find_by_id(session_id)
        self.metrics_tracker.record_read(hit_cache=False)
        if mem:
            # Migration check
            payload = MemorySerializer.serialize(mem)
            migrated_payload = MemoryMigrationManager.migrate_if_needed(payload)
            migrated_mem = MemorySerializer.deserialize(migrated_payload)
            
            plain_mem = MemorySecurity.decrypt_sensitive_fields(migrated_mem)
            self.cache.put(session_id, plain_mem)
            return plain_mem

        return None

    def search_candidate_history(self, candidate_id: str) -> List[InterviewMemory]:
        """Retrieves all past interview memories for a candidate."""
        raw_results = self.repository.search_by_keyword(candidate_id)
        retained = self.retention_manager.apply_retention_policy(raw_results)
        return [MemorySecurity.decrypt_sensitive_fields(m) for m in retained]

    def filter_memories(
        self,
        session_id: Optional[str] = None,
        candidate_id: Optional[str] = None,
        topic_title: Optional[str] = None,
        day_number: Optional[int] = None,
        classification: Optional[str] = None,
    ) -> List[InterviewMemory]:
        """Multi-criteria search filtering using MemorySearchEngine."""
        raw_results = self.repository.search_by_keyword(candidate_id or "")
        return MemorySearchEngine.filter_memories(
            memories=raw_results,
            session_id=session_id,
            candidate_id=candidate_id,
            topic_title=topic_title,
            day_number=day_number,
            classification=classification,
        )


# Singleton helper
_memory_service_instance: Optional[MemoryService] = None


def get_memory_service() -> MemoryService:
    global _memory_service_instance
    if _memory_service_instance is None:
        _memory_service_instance = MemoryService()
    return _memory_service_instance
