from typing import Optional, List, Dict, Any
from app.memory.memory_provider import AbstractMemoryProvider
from app.memory.memory_factory import MemoryFactory
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
    Service Layer for managing persistent interview memories across sessions.
    Provides methods to store session metadata, questions, candidate answers, evaluations,
    knowledge gaps, and final feedback reports.
    """

    def __init__(
        self,
        provider: Optional[AbstractMemoryProvider] = None,
        candidate_service: Optional[CandidateService] = None,
    ):
        self.provider = provider or MemoryFactory.create_provider()
        self.candidate_service = candidate_service or get_candidate_service()

    def initialize_session_memory(self, session: InterviewSessionState) -> InterviewMemory:
        """
        Creates and stores initial InterviewMemory document upon session start.
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

        self.provider.save_memory(memory)
        logger.info(f"Memory write: Session memory initialized for '{session.session_id}'.")
        return memory

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
        mem = self.provider.get_memory(session.session_id)
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

        self.provider.update_memory(session.session_id, mem)
        logger.info(f"Memory update: Recorded turn {turn_index + 1} memory for session '{session.session_id}'.")
        return mem

    def record_feedback_memory(
        self, session_id: str, feedback_report: FeedbackReportModel
    ) -> Optional[InterviewMemory]:
        """
        Stores final completed feedback report in persistent memory.
        """
        mem = self.provider.get_memory(session_id)
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

        self.provider.update_memory(session_id, mem)
        logger.info(f"Memory update: Attached final feedback report to memory '{session_id}'.")
        return mem

    def get_session_memory(self, session_id: str) -> Optional[InterviewMemory]:
        """Retrieves session memory document by ID."""
        return self.provider.get_memory(session_id)

    def search_candidate_history(self, candidate_id: str) -> List[InterviewMemory]:
        """Retrieves all past interview memories for a candidate."""
        return self.provider.search_memory(candidate_id)


# Singleton helper
_memory_service_instance: Optional[MemoryService] = None


def get_memory_service() -> MemoryService:
    global _memory_service_instance
    if _memory_service_instance is None:
        _memory_service_instance = MemoryService()
    return _memory_service_instance
