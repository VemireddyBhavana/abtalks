import os
import time
from typing import Dict, Any
from app.monitoring.metrics import get_metrics_registry


class PerformanceMetricsCollector:
    """
    Collects execution latency and system resource metrics.
    """

    @staticmethod
    def collect_performance_metrics() -> Dict[str, Any]:
        registry = get_metrics_registry()
        snapshot = registry.get_metrics_snapshot()
        
        return {
            "timestamp": time.time(),
            "process_id": os.getpid(),
            "active_interview_sessions": snapshot["active_sessions"],
            "total_api_requests": snapshot["total_requests"],
            "total_api_errors": snapshot["total_errors"],
        }
