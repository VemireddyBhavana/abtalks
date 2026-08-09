from typing import Dict, Any
from app.monitoring.metrics import get_metrics_registry


class HealthMetricsCollector:
    """
    Collects and computes system health readiness indicators.
    """

    @staticmethod
    def collect_health_metrics() -> Dict[str, Any]:
        registry = get_metrics_registry()
        snapshot = registry.get_metrics_snapshot()
        
        error_rate = 0.0
        if snapshot["total_requests"] > 0:
            error_rate = round(snapshot["total_errors"] / snapshot["total_requests"], 4)

        return {
            "health_status": "healthy" if error_rate < 0.05 else "degraded",
            "error_rate": error_rate,
            "active_sessions": snapshot["active_sessions"],
            "total_serviced_requests": snapshot["total_requests"],
        }
