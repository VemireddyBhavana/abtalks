from fastapi import APIRouter
from app.core.config import settings
from app.core.cache import get_cache_manager
from app.services.curriculum_service import CurriculumService
from app.services.candidate_service import CandidateService

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "",
    summary="V1 Health Check",
    description="Returns detailed health status and readiness of cached intelligence services."
)
@router.get(
    "/",
    summary="V1 Health Check (Trailing Slash)",
    description="Returns detailed health status and readiness of cached intelligence services."
)
def get_v1_health():
    cache_mgr = get_cache_manager()
    curriculum_ready = cache_mgr.is_ready(CurriculumService.CACHE_KEY)
    candidate_ready = cache_mgr.is_ready(CandidateService.CACHE_KEY)

    return {
        "status": "running",
        "service": settings.PROJECT_NAME,
        "api_version": "v1",
        "curriculumLoaded": curriculum_ready,
        "candidateLoaded": candidate_ready,
        "cacheReady": cache_mgr.is_ready(),
    }
