from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging_config import logger
from app.core.cache import get_cache_manager
from app.api.v1.health import router as v1_health_router
from app.api.v1.curriculum import router as v1_curriculum_router
from app.api.v1.candidate import router as v1_candidate_router
from app.api.v1.interview import router as v1_interview_router
from app.services.curriculum_service import get_curriculum_service, CurriculumService
from app.services.candidate_service import get_candidate_service, CandidateService
from app.services.interview_engine import get_interview_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info(f"Starting {settings.PROJECT_NAME} (v{settings.VERSION}) backend server...")
    try:
        curriculum_svc = get_curriculum_service()
        candidate_svc = get_candidate_service()
        engine_svc = get_interview_engine()
        logger.info("Phase 4 Interview Engine successfully initialized.")
    except Exception as exc:
        logger.error(f"Error during Phase 4 startup initialization: {str(exc)}")
    yield
    # Shutdown logic
    logger.info(f"Shutting down {settings.PROJECT_NAME} backend server...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FastAPI Backend Foundation & Interview Engine for ABTalks AI Interview Agent",
    version=settings.VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

from app.core.security_middleware import SecurityHeadersMiddleware, RequestSizeLimitMiddleware

# Configure Middleware
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestSizeLimitMiddleware, max_content_length=2 * 1024 * 1024)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

from app.api.v1.hackathon_api import router as hackathon_router

# Include Versioned API Routers
app.include_router(v1_health_router, prefix="/api/v1")
app.include_router(v1_curriculum_router, prefix="/api/v1")
app.include_router(v1_candidate_router, prefix="/api/v1")
app.include_router(v1_interview_router, prefix="/api/v1")
app.include_router(hackathon_router, prefix="/api/v1")

# Official Hackathon API Route Aliases (/api/interview & /health)
app.include_router(hackathon_router)
app.include_router(v1_health_router)


@app.get("/", tags=["Root"], summary="Root Health Check", description="Returns health diagnostics for server and intelligence layer caches.")
def root_health_check():
    """
    Root Health Diagnostics Endpoint
    Returns health status and cache readiness metrics.
    """
    cache_mgr = get_cache_manager()
    curriculum_ready = cache_mgr.is_ready(CurriculumService.CACHE_KEY)
    candidate_ready = cache_mgr.is_ready(CandidateService.CACHE_KEY)

    return {
        "status": "running",
        "project": settings.PROJECT_NAME,
        "curriculumLoaded": curriculum_ready,
        "candidateLoaded": candidate_ready,
        "cacheReady": cache_mgr.is_ready(),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
