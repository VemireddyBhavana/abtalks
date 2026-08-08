from app.strategies.feedback.base_feedback_strategy import AbstractFeedbackStrategy
from app.models.feedback_report import FeedbackReportModel
from app.services.interview_state import InterviewSessionState
from app.strategies.feedback.technical_feedback_strategy import TechnicalFeedbackStrategy
from app.core.logging_config import logger


class SummaryFeedbackStrategy(AbstractFeedbackStrategy):
    """
    Summary Feedback Strategy generating high-level executive report overviews.
    """

    def generate_report(self, session: InterviewSessionState) -> FeedbackReportModel:
        logger.info(f"SummaryFeedbackStrategy: Generating executive summary feedback report for '{session.session_id}'...")
        return TechnicalFeedbackStrategy().generate_report(session)
