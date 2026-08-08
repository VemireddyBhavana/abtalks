from abc import ABC, abstractmethod
from app.models.feedback_report import FeedbackReportModel
from app.services.interview_state import InterviewSessionState


class AbstractFeedbackStrategy(ABC):
    """Abstract Strategy interface for generating structured FeedbackReportModel."""

    @abstractmethod
    def generate_report(self, session: InterviewSessionState) -> FeedbackReportModel:
        """Generates a complete FeedbackReportModel."""
        pass
