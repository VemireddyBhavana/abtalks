from typing import Any
from app.exporters.base_exporter import AbstractReportExporter
from app.models.feedback_report import FeedbackReportModel


class PDFExporterPlaceholder(AbstractReportExporter):
    """
    Placeholder for future PDF Export functionality.
    """

    def export(self, report: FeedbackReportModel) -> Any:
        # TODO: Implement PDF binary export using WeasyPrint / ReportLab in future releases
        return f"PDF_PLACEHOLDER_BYTES_FOR_SESSION_{report.session_id}"
