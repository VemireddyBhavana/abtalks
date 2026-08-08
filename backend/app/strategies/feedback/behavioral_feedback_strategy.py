from app.strategies.feedback.base_feedback_strategy import AbstractFeedbackStrategy
from app.models.feedback_report import FeedbackReportModel
from app.services.interview_state import InterviewSessionState
from app.strategies.feedback.technical_feedback_strategy import TechnicalFeedbackStrategy
from app.core.logging_config import logger


class BehavioralFeedbackStrategy(AbstractFeedbackStrategy):
    """
    Behavioral Feedback Strategy focusing on communication clarity and reasoning consistency.
    """

    def generate_report(self, session: InterviewSessionState) -> FeedbackReportModel:
        logger.info(f"BehavioralFeedbackStrategy: Generating behavioral feedback report for '{session.session_id}'...")
        base_report = TechnicalFeedbackStrategy().generate_report(session)
        base_report.summary.communication_assessment = "Candidate displayed excellent verbal clarity and structured reasoning."
        return base_report
