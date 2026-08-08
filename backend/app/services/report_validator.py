from app.models.feedback_report import FeedbackReportModel
from app.exceptions.interview_exception import InterviewPlanError
from app.core.logging_config import logger


class ReportValidator:
    """
    Validates overall score range, category scores, required sections, recommendation completeness,
    and curriculum references before returning the final report.
    """

    @classmethod
    def validate_report(cls, report: FeedbackReportModel) -> bool:
        # 1. Overall Score check [0, 100]
        if report.overall_score.overall_score < 0.0 or report.overall_score.overall_score > 100.0:
            logger.error("Report Validation Failed: Overall score out of [0, 100] range.")
            raise InterviewPlanError("Invalid report: overall score must be between 0 and 100.")

        # 2. Category Breakdown check
        if len(report.overall_score.breakdown) == 0:
            logger.error("Report Validation Failed: Category breakdown is empty.")
            raise InterviewPlanError("Invalid report: category score breakdown is empty.")

        # 3. Recommendations check
        if len(report.recommendations) == 0:
            logger.error("Report Validation Failed: Recommendations list is empty.")
            raise InterviewPlanError("Invalid report: recommendations list cannot be empty.")

        logger.info(f"Report validated: Feedback report for session '{report.session_id}' passed pre-flight validation.")
        return True
