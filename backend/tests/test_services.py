from app.services.curriculum_service import CurriculumService
from app.services.candidate_service import CandidateService
from app.core.cache import get_cache_manager


def test_curriculum_service_loading():
    svc = CurriculumService()
    assert svc is not None
    days = svc.get_all_days()
    assert days is not None
    assert len(days) > 0


def test_candidate_service_loading():
    svc = CandidateService()
    assert svc is not None
    cand = svc.get_candidate()
    assert cand is not None
    assert cand.candidate_id is not None


def test_cache_manager_behavior():
    cache = get_cache_manager()
    res = cache.load("test_key", lambda: {"data": 123})
    assert res == {"data": 123}
    cached_val = cache.get("test_key")
    assert cached_val == {"data": 123}
