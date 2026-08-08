import pytest
from app.memory.memory_factory import MemoryFactory
from app.memory.mock_provider import MockMemoryProvider
from app.memory.breeth_provider import BreethProvider
from app.memory.memory_service import MemoryService
from app.memory.memory_models import SessionMemory, CandidateMemory, InterviewMemory
from app.services.interview_engine import InterviewEngine
from app.utils.helpers import get_utc_now


def test_memory_factory_instantiation():
    """Verifies MemoryFactory creates requested or default providers."""
    mock_prov = MemoryFactory.create_provider("mock")
    assert isinstance(mock_prov, MockMemoryProvider)

    breeth_prov = MemoryFactory.create_provider("breeth")
    assert isinstance(breeth_prov, BreethProvider)


def test_mock_memory_provider_crud_operations():
    """Verifies CRUD operations on MockMemoryProvider."""
    provider = MockMemoryProvider()

    sess = SessionMemory(
        session_id="sess_crud_1",
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
        memory_id="sess_crud_1",
        session=sess,
        candidate=cand,
        turns=[],
        knowledge_gaps=[],
        feedback=None,
        updated_at=get_utc_now(),
    )

    # 1. Save
    assert provider.save_memory(mem) is True

    # 2. Get
    retrieved = provider.get_memory("sess_crud_1")
    assert retrieved is not None
    assert retrieved.candidate.full_name == "Alex Mercer"

    # 3. Search
    results = provider.search_memory("Alex")
    assert len(results) == 1
    assert results[0].memory_id == "sess_crud_1"

    # 4. Update
    mem.session.done = True
    assert provider.update_memory("sess_crud_1", mem) is True
    assert provider.get_memory("sess_crud_1").session.done is True

    # 5. Delete
    assert provider.delete_memory("sess_crud_1") is True
    assert provider.get_memory("sess_crud_1") is None


def test_breeth_provider_graceful_fallback():
    """Verifies BreethProvider falls back to MockMemoryProvider when API key is missing."""
    breeth_prov = BreethProvider(api_key="", project_id="abtalks", collection="memories")
    sess = SessionMemory(
        session_id="sess_fb_1",
        candidate_id="cand_alex",
        started_at=get_utc_now(),
        done=False,
        total_questions=8,
        current_question_index=0,
    )
    cand = CandidateMemory(candidate_id="cand_alex", full_name="Alex", current_day=1)
    mem = InterviewMemory(memory_id="sess_fb_1", session=sess, candidate=cand, turns=[], updated_at=get_utc_now())

    assert breeth_prov.save_memory(mem) is True
    assert breeth_prov.get_memory("sess_fb_1") is not None


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
