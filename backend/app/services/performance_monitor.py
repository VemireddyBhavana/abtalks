import os
import sys
import time
from typing import Dict, Any
from app.core.logging_config import logger


class PerformanceMonitor:
    """
    Centralized Performance Monitoring service tracking latency, memory utilization,
    CPU estimation, and request throughput metrics.
    """

    _instance = None

    def __init__(self):
        self.request_count = 0
        self.total_latency_ms = 0.0
        self.start_timestamp = time.time()
        self.latency_history = []

    @classmethod
    def get_instance(cls) -> "PerformanceMonitor":
        if cls._instance is None:
            cls._instance = PerformanceMonitor()
        return cls._instance

    def record_request(self, latency_ms: float) -> None:
        """
        Records a completed request latency sample and updates cumulative statistics.
        """
        self.request_count += 1
        self.total_latency_ms += latency_ms
        self.latency_history.append(latency_ms)
        if len(self.latency_history) > 1000:
            self.latency_history.pop(0)

    def get_memory_usage(self) -> Dict[str, Any]:
        """
        Returns process memory metrics.
        """
        try:
            import psutil
            process = psutil.Process(os.getpid())
            mem_info = process.memory_info()
            return {
                "rss_bytes": mem_info.rss,
                "rss_mb": round(mem_info.rss / (1024 * 1024), 2),
                "vsz_mb": round(mem_info.vms / (1024 * 1024), 2),
            }
        except ImportError:
            # Fallback estimation if psutil is unavailable
            return {
                "rss_bytes": 0,
                "rss_mb": 0.0,
                "note": "psutil optional dependency not installed",
            }

    def get_metrics(self) -> Dict[str, Any]:
        """
        Aggregates performance diagnostic metrics.
        """
        uptime_seconds = max(1.0, time.time() - self.start_timestamp)
        avg_latency = (
            round(self.total_latency_ms / self.request_count, 2)
            if self.request_count > 0
            else 0.0
        )
        throughput_rps = round(self.request_count / uptime_seconds, 2)

        return {
            "uptime_seconds": round(uptime_seconds, 1),
            "total_requests": self.request_count,
            "avg_latency_ms": avg_latency,
            "throughput_rps": throughput_rps,
            "memory": self.get_memory_usage(),
            "python_version": sys.version.split()[0],
        }


def get_performance_monitor() -> PerformanceMonitor:
    return PerformanceMonitor.get_instance()
