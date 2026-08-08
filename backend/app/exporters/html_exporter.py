from app.exporters.base_exporter import AbstractReportExporter
from app.models.feedback_report import FeedbackReportModel


class HTMLExporterPlaceholder(AbstractReportExporter):
    """
    Placeholder for future HTML Export functionality.
    """

    def export(self, report: FeedbackReportModel) -> str:
        return f"<html><body><h1>Feedback Report for Session {report.session_id}</h1></body></html>"
