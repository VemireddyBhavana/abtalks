import pytest
from app.repositories.memory_repository import MemoryRepository
from app.memory.memory_factory import MemoryFactory
from app.memory.mock_provider import MockMemoryProvider
from app.memory.breeth_provider import BreethProvider
from app.memory.memory_service import MemoryService
from app.memory.memory_cache import MemoryCache
from app.memory.memory_serializer import MemorySerializer
from app.memory.memory_validator import MemoryValidator
from app.memory.memory_migration import MemoryMigrationManager
from app.memory.memory_metrics import get_memory_metrics, MemoryMetricsTracker
from app.memory.memory_retry_manager import MemoryRetryManager
from app.memory.session_snapshot import SessionSnapshotManager
from app.memory.memory_search import MemorySearchEngine
from app.memory.retention_manager import DataRetentionManager
from app.memory.memory_security import MemorySecurity
from app.memory.memory_models import SessionMemory, CandidateMemory, EvaluationMemory, InterviewMemory
from app.exceptions.memory_exception import MemoryValidationError, MemoryRetryExhaustedError
from app.services.interview_engine import InterviewEngine
from app.utils.helpers import get_utc_now


def test_memory_factory_instantiation():
    """Verifies MemoryFactory creates requested or default providers."""
    mock_prov = MemoryFactory.create_provider("mock")
    assert isinstance(mock_prov, MockMemoryProvider)

    breeth_prov = MemoryFactory.create_provider("breeth")
    assert isinstance(breeth_prov, BreethProvider)


def test_memory_repository_crud():
    """Verifies MemoryRepository wrapper operations."""
    repo = MemoryRepository(provider=MockMemoryProvider())

    sess = SessionMemory(session_id="s_repo_1", candidate_id="c1", started_at=get_utc_now(), done=False, total_questions=8, current_question_index=0)
    cand = CandidateMemory(candidate_id="c1", full_name="Name", current_day=1)
    mem = InterviewMemory(memory_id="s_repo_1", session=sess, candidate=cand, turns=[], updated_at=get_utc_now())

    assert repo.save(mem) is True
    assert repo.find_by_id("s_repo_1") is not None
    assert len(repo.search_by_keyword("Name")) == 1
    assert repo.delete("s_repo_1") is True


def test_session_snapshot_manager():
    """Verifies SessionSnapshotManager creates milestone snapshots."""
    snapshot_mgr = SessionSnapshotManager()
    sess = SessionMemory(session_id="s_snap_1", candidate_id="c1", started_at=get_utc_now(), done=False, total_questions=8, current_question_index=0)
    cand = CandidateMemory(candidate_id="c1", full_name="Name", current_day=1)
    mem = InterviewMemory(memory_id="s_snap_1", session=sess, candidate=cand, turns=[], updated_at=get_utc_now())

    snap = snapshot_mgr.create_snapshot("s_snap_1", "Interview started", mem)
    assert snap["milestone"] == "Interview started"
    assert len(snapshot_mgr.get_snapshots("s_snap_1")) == 1


def test_memory_security_encryption():
    """Verifies MemorySecurity encrypts and decrypts candidate answer fields."""
    sess = SessionMemory(session_id="s_sec_1", candidate_id="c1", started_at=get_utc_now(), done=False, total_questions=8, current_question_index=0)
    cand = CandidateMemory(candidate_id="c1", full_name="Name", current_day=1)
    eval_turn = EvaluationMemory(
        turn_index=0, question_id="q1", topic_id="t1", topic_title="Topic", question_text="Q",
        candidate_answer="Confidential technical text", score=85, classification="Good",
        confidence_score=80, action_type="Probe", difficulty="Intermediate"
    )
    mem = InterviewMemory(memory_id="s_sec_1", session=sess, candidate=cand, turns=[eval_turn], updated_at=get_utc_now())

    # Encrypt
    sec_mem = MemorySecurity.encrypt_sensitive_fields(mem)
    assert sec_mem.turns[0].candidate_answer.startswith("ENC:")

    # Decrypt
    dec_mem = MemorySecurity.decrypt_sensitive_fields(sec_mem)
    assert dec_mem.turns[0].candidate_answer == "Confidential technical text"


def test_memory_search_and_retention():
    """Verifies MemorySearchEngine and DataRetentionManager."""
    sess = SessionMemory(session_id="s_search_1", candidate_id="c_search_1", started_at=get_utc_now(), done=False, total_questions=8, current_question_index=0)
    cand = CandidateMemory(candidate_id="c_search_1", full_name="Search Candidate", current_day=1)
    eval_turn = EvaluationMemory(
        turn_index=0, question_id="q1", topic_id="top_react", topic_title="React 19", question_text="Q",
        candidate_answer="Answer", score=85, classification="Good", confidence_score=80, action_type="Probe", difficulty="Intermediate"
    )
    mem = InterviewMemory(memory_id="s_search_1", session=sess, candidate=cand, turns=[eval_turn], updated_at=get_utc_now())

    filtered = MemorySearchEngine.filter_memories([mem], session_id="s_search_1", topic_title="React 19")
    assert len(filtered) == 1

    retention_mgr = DataRetentionManager()
    retained = retention_mgr.apply_retention_policy([mem])
    assert len(retained) == 1


def test_interview_engine_memory_integration():
    """Integration test: verifies InterviewEngine automatically records session memory across all 8 turns."""
    engine = InterviewEngine()

    start_resp = engine.start_interview(candidate_id="cand_mem_test", session_id="sess_mem_test")
    assert start_resp.session_id == "sess_mem_test"

    # Check session memory initialized
    mem = engine.memory_service.get_session_memory("sess_mem_test")
    assert mem is not None
    assert mem.session.session_id == "sess_mem_test"

    # Answer all 8 questions
    for i in range(8):
        resp = engine.submit_answer("sess_mem_test", f"Technical candidate answer for turn {i + 1}")
        if i == 7:
            assert resp.done is True
            assert resp.feedback_report is not None

    # Verify complete InterviewMemory document in Memory service
    final_mem = engine.memory_service.get_session_memory("sess_mem_test")
    assert final_mem is not None
    assert final_mem.session.done is True
    assert len(final_mem.turns) == 8
    assert final_mem.feedback is not None
    assert final_mem.feedback.overall_score > 0.0
