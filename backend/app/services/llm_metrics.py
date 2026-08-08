from typing import Dict, Any


class LLMMetricsTracker:
    """
    Tracks operational LLM generation metrics:
    - Successful vs Failed Generations
    - Average Response Time
    - Retry Count
    - Provider Usage Breakdown
    """

    def __init__(self):
        self.successful_generations = 0
        self.failed_generations = 0
        self.retry_count = 0
        self.total_response_time_sec = 0.0

    def record_success(self, duration_sec: float) -> None:
        self.successful_generations += 1
        self.total_response_time_sec += duration_sec

    def record_failure(self) -> None:
        self.failed_generations += 1

    def record_retry(self) -> None:
        self.retry_count += 1

    def get_metrics(self) -> Dict[str, Any]:
        total = self.successful_generations + self.failed_generations
        avg_time = round(self.total_response_time_sec / self.successful_generations, 3) if self.successful_generations > 0 else 0.0

        return {
            "total_requests": total,
            "successful_generations": self.successful_generations,
            "failed_generations": self.failed_generations,
            "retry_count": self.retry_count,
            "avg_response_time_sec": avg_time,
        }


# Singleton instance
_llm_metrics_instance = LLMMetricsTracker()


def get_llm_metrics() -> LLMMetricsTracker:
    return _llm_metrics_instance
