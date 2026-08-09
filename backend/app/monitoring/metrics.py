import time
from typing import Dict, Any


class MetricsRegistry:
    """
    Centralized Observability Metrics Registry tracking API request counts, error counts,
    active interview sessions, and latency distribution.
    """

    _instance = None

    def __init__(self):
        self._request_counter: Dict[str, int] = {}
        self._error_counter: Dict[str, int] = {}
        self._active_sessions: int = 0
        self._total_requests: int = 0
        self._total_errors: int = 0

    @classmethod
    def get_instance(cls) -> "MetricsRegistry":
        if cls._instance is None:
            cls._instance = MetricsRegistry()
        return cls._instance

    def increment_request(self, endpoint: str) -> None:
        self._total_requests += 1
        self._request_counter[endpoint] = self._request_counter.get(endpoint, 0) + 1

    def increment_error(self, endpoint: str) -> None:
        self._total_errors += 1
        self._error_counter[endpoint] = self._error_counter.get(endpoint, 0) + 1

    def increment_active_session(self) -> None:
        self._active_sessions += 1

    def decrement_active_session(self) -> None:
        self._active_sessions = max(0, self._active_sessions - 1)

    def get_metrics_snapshot(self) -> Dict[str, Any]:
        return {
            "total_requests": self._total_requests,
            "total_errors": self._total_errors,
            "active_sessions": self._active_sessions,
            "endpoint_requests": self._request_counter,
            "endpoint_errors": self._error_counter,
        }


def get_metrics_registry() -> MetricsRegistry:
    return MetricsRegistry.get_instance()
