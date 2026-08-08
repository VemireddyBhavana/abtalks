import pytest
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
from app.memory.memory_models import SessionMemory, CandidateMemory, InterviewMemory
from app.exceptions.memory_exception import MemoryValidationError, MemoryRetryExhaustedError
from app.services.interview_engine import InterviewEngine
from app.utils.helpers import get_utc_now


def test_memory_factory_instantiation():
    """Verifies MemoryFactory creates requested or default providers."""
    mock_prov = MemoryFactory.create_provider("mock")
    assert isinstance(mock_prov, MockMemoryProvider)

    breeth_prov = MemoryFactory.create_provider("breeth")
    assert isinstance(breeth_prov, BreethProvider)


def test_mock_memory_repository_crud_operations():
    """Verifies CRUD operations on MockMemoryProvider implementing AbstractMemoryRepository."""
    repo = MockMemoryProvider()

    sess = SessionMemory(
        session_id="sess_repo_1",
        candidate_id="cand_alex",
        started_at=get_utc_now(),
        done=False,
        total_questions=8,
        current_question_index=0,
    )
    cand = CandidateMemory(
        candidate_id="cand_alex",
        full_name="Alex Mercer",
        current_day=1,
    )
    mem = InterviewMemory(
        memory_id="sess_repo_1",
        session=sess,
        candidate=cand,
        turns=[],
        knowledge_gaps=[],
        feedback=None,
        updated_at=get_utc_now(),
    )

    # 1. Save
    assert repo.save(mem) is True

    # 2. Find by ID
    retrieved = repo.find_by_id("sess_repo_1")
    assert retrieved is not None
    assert retrieved.candidate.full_name == "Alex Mercer"

    # 3. Search by Keyword
    results = repo.search_by_keyword("Alex")
    assert len(results) == 1
    assert results[0].memory_id == "sess_repo_1"

    # 4. Update
    mem.session.done = True
    assert repo.update("sess_repo_1", mem) is True
    assert repo.find_by_id("sess_repo_1").session.done is True

    # 5. Delete
    assert repo.delete("sess_repo_1") is True
    assert repo.find_by_id("sess_repo_1") is None


def test_memory_cache_operations():
    """Verifies MemoryCache get, put, hit, and eviction logic."""
    cache = MemoryCache(max_entries=2)
    sess = SessionMemory(session_id="s1", candidate_id="c1", started_at=get_utc_now(), done=False, total_questions=8, current_question_index=0)
    cand = CandidateMemory(candidate_id="c1", full_name="Name", current_day=1)
    mem1 = InterviewMemory(memory_id="s1", session=sess, candidate=cand, turns=[], updated_at=get_utc_now())
    mem2 = InterviewMemory(memory_id="s2", session=sess, candidate=cand, turns=[], updated_at=get_utc_now())

    cache.put("s1", mem1)
    assert cache.get("s1") is not None
    assert cache.get("s2") is None

    cache.put("s2", mem2)
    assert cache.get("s1") is not None
    assert cache.get("s2") is not None


def test_memory_serializer_and_validator():
    """Verifies MemorySerializer and MemoryValidator integrity rules."""
    sess = SessionMemory(session_id="s_val", candidate_id="c_val", started_at=get_utc_now(), done=False, total_questions=8, current_question_index=0)
    cand = CandidateMemory(candidate_id="c_val", full_name="Valid Candidate", current_day=1)
    mem = InterviewMemory(memory_id="s_val", session=sess, candidate=cand, turns=[], updated_at=get_utc_now())

    # Pre-flight validation success
    assert MemoryValidator.validate(mem) is True

    # Serialization & Deserialization
    serialized = MemorySerializer.serialize(mem)
    deserialized = MemorySerializer.deserialize(serialized)
    assert deserialized.memory_id == "s_val"

    # Validation failure on empty ID
    mem.memory_id = ""
    with pytest.raises(MemoryValidationError):
        MemoryValidator.validate(mem)


def test_memory_migration_and_metrics():
    """Verifies MemoryMigrationManager and MemoryMetricsTracker."""
    payload = {"schema_version": "0.9.0", "memory_id": "m1"}
    migrated = MemoryMigrationManager.migrate_if_needed(payload)
    assert migrated["schema_version"] == "1.0.0"

    tracker = MemoryMetricsTracker()
    tracker.record_read(hit_cache=True)
    tracker.record_read(hit_cache=False)
    tracker.record_write()
    summary = tracker.get_summary()

    assert summary["total_reads"] == 2
    assert summary["cache_hits"] == 1
    assert summary["cache_misses"] == 1
    assert summary["cache_hit_ratio_percentage"] == 50.0


def test_memory_retry_manager():
    """Verifies MemoryRetryManager retries failed operations and raises MemoryRetryExhaustedError."""
    attempts = 0

    def failing_op():
        nonlocal attempts
        attempts += 1
        raise ValueError("Simulated network failure")

    with pytest.raises(MemoryRetryExhaustedError):
        MemoryRetryManager.execute_with_retry(failing_op, max_retries=2, backoff_sec=0.01)

    assert attempts == 3


def test_breeth_provider_graceful_fallback():
    """Verifies BreethProvider falls back to MockMemoryProvider when API key is missing."""
    breeth_prov = BreethProvider(api_key="", project_id="abtalks", collection="memories")
    sess = SessionMemory(session_id="sess_fb_1", candidate_id="cand_alex", started_at=get_utc_now(), done=False, total_questions=8, current_question_index=0)
    cand = CandidateMemory(candidate_id="cand_alex", full_name="Alex", current_day=1)
    mem = InterviewMemory(memory_id="sess_fb_1", session=sess, candidate=cand, turns=[], updated_at=get_utc_now())

    assert breeth_prov.save(mem) is True
    assert breeth_prov.find_by_id("sess_fb_1") is not None


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

    # Verify complete InterviewMemory document in Breeth Memory service
    final_mem = engine.memory_service.get_session_memory("sess_mem_test")
    assert final_mem is not None
    assert final_mem.session.done is True
    assert len(final_mem.turns) == 8
    assert final_mem.feedback is not None
    assert final_mem.feedback.overall_score > 0.0
