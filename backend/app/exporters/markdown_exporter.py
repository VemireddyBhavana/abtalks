from app.exporters.base_exporter import AbstractReportExporter
from app.models.feedback_report import FeedbackReportModel


class MarkdownExporterPlaceholder(AbstractReportExporter):
    """
    Placeholder for future Markdown Export functionality.
    """

    def export(self, report: FeedbackReportModel) -> str:
        return f"# Interview Feedback Report: {report.session_id}\n\nOverall Score: {report.overall_score.overall_score}/100"
