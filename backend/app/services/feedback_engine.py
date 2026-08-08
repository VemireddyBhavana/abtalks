import time
from typing import Optional
from app.models.feedback_report import FeedbackReportModel
from app.services.interview_state import InterviewSessionState
from app.strategies.feedback.base_feedback_strategy import AbstractFeedbackStrategy
from app.strategies.feedback.technical_feedback_strategy import TechnicalFeedbackStrategy
from app.services.strength_analyzer import StrengthAnalyzer
from app.services.weakness_analyzer import WeaknessAnalyzer
from app.services.recommendation_priority import RecommendationPriorityEngine
from app.services.report_validator import ReportValidator
from app.services.feedback_metrics import get_feedback_metrics, FeedbackMetricsTracker
from app.core.logging_config import logger


class FeedbackEngine:
    """
    Production-grade Feedback & Scoring Engine using Strategy Pattern, Analyzers,
    Recommendation Priority Engine, Report Validator, and Metrics Tracker.
    """

    def __init__(
        self,
        strategy: Optional[AbstractFeedbackStrategy] = None,
        metrics_tracker: Optional[FeedbackMetricsTracker] = None,
    ):
        self.strategy = strategy or TechnicalFeedbackStrategy()
        self.metrics_tracker = metrics_tracker or get_feedback_metrics()

    def generate_feedback_report(self, session: InterviewSessionState) -> FeedbackReportModel:
        """
        Generates a validated structured FeedbackReportModel for a completed session.
        """
        start_time = time.time()
        logger.info(f"Feedback generation started: Initiating report for session '{session.session_id}'...")

        # 1. Generate base report using Strategy
        report = self.strategy.generate_report(session)
        logger.info(f"Score calculated: Overall Score {report.overall_score.overall_score}/100.")

        # 2. Enrich strengths & weaknesses via analyzers
        report.strengths = StrengthAnalyzer.analyze_strengths(session.candidate_answers)
        report.weaknesses = WeaknessAnalyzer.analyze_weaknesses(session.candidate_answers)
        logger.info("Summary generated: Analyzed strengths and growth areas.")

        # 3. Prioritize recommendations
        report.recommendations = RecommendationPriorityEngine.prioritize_recommendations(
            recommendations=report.recommendations,
            overall_score=report.overall_score.overall_score,
        )
        logger.info("Recommendations generated: Ranked study recommendations by priority.")

        # 4. Pre-flight report validation
        ReportValidator.validate_report(report)
        logger.info(f"Report validated: Session '{session.session_id}' report passed validation.")

        duration = time.time() - start_time
        self.metrics_tracker.record_report(duration, report.overall_score.overall_score)

        logger.info(f"Feedback completed: Successfully generated report in {duration:.3f}s.")
        return report


# Singleton helper
_feedback_engine_instance: Optional[FeedbackEngine] = None


def get_feedback_engine() -> FeedbackEngine:
    global _feedback_engine_instance
    if _feedback_engine_instance is None:
        _feedback_engine_instance = FeedbackEngine()
    return _feedback_engine_instance
