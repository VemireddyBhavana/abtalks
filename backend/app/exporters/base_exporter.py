from abc import ABC, abstractmethod
from typing import Any
from app.models.feedback_report import FeedbackReportModel


class AbstractReportExporter(ABC):
    """Abstract Interface contract for exported report formats (PDF, Markdown, HTML)."""

    @abstractmethod
    def export(self, report: FeedbackReportModel) -> Any:
        """Exports FeedbackReportModel into target format representation."""
        pass
