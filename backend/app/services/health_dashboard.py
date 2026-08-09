from typing import Dict, Any
from app.core.cache import get_cache_manager
from app.services.curriculum_service import CurriculumService
from app.services.candidate_service import CandidateService
from app.services.performance_monitor import get_performance_monitor
from app.utils.security_audit import SecurityAudit


class HealthDashboardService:
    """
    Centralized Health Dashboard service aggregating backend, intelligence cache,
    provider readiness, and performance metrics into a single unified diagnostic report.
    """

    @staticmethod
    def get_dashboard_status() -> Dict[str, Any]:
        cache_mgr = get_cache_manager()
        curriculum_ready = cache_mgr.is_ready(CurriculumService.CACHE_KEY)
        candidate_ready = cache_mgr.is_ready(CandidateService.CACHE_KEY)
        
        perf_monitor = get_performance_monitor()
        perf_metrics = perf_monitor.get_metrics()
        
        sec_audit = SecurityAudit.run_audit()

        return {
            "status": "healthy" if (curriculum_ready and candidate_ready) else "degraded",
            "components": {
                "curriculum_service": "ready" if curriculum_ready else "not_loaded",
                "candidate_service": "ready" if candidate_ready else "not_loaded",
                "memory_provider": "ready",
                "llm_provider": "ready (mock)",
            },
            "performance": perf_metrics,
            "security_compliance": {
                "compliant": sec_audit["compliant"],
                "warnings": sec_audit["warnings"],
            },
        }


def get_health_dashboard_service() -> HealthDashboardService:
    return HealthDashboardService()
