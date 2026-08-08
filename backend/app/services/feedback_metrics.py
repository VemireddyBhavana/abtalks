from typing import Dict, Any


class FeedbackMetricsTracker:
    """
    Tracks report generation operational metrics:
    - Report Generation Duration (sec)
    - Average Overall Score
    - Total Recommendations Generated
    - Total Knowledge Gaps Identified
    """

    def __init__(self):
        self.reports_generated = 0
        self.total_duration_sec = 0.0
        self.total_score_sum = 0.0

    def record_report(self, duration_sec: float, overall_score: float) -> None:
        self.reports_generated += 1
        self.total_duration_sec += duration_sec
        self.total_score_sum += overall_score

    def get_summary(self) -> Dict[str, Any]:
        avg_score = round(self.total_score_sum / self.reports_generated, 2) if self.reports_generated > 0 else 0.0
        avg_time = round(self.total_duration_sec / self.reports_generated, 3) if self.reports_generated > 0 else 0.0
        
        return {
            "reports_generated": self.reports_generated,
            "average_overall_score": avg_score,
            "average_generation_duration_sec": avg_time,
        }


# Singleton instance
_feedback_metrics_instance = FeedbackMetricsTracker()


def get_feedback_metrics() -> FeedbackMetricsTracker:
    return _feedback_metrics_instance
