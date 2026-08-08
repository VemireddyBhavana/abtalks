from typing import List, Dict, Any, Optional
from app.models.feedback_report import (
    FeedbackReportModel,
    OverallScoreModel,
    KnowledgeGapModel,
    RecommendationModel,
    FeedbackSummaryModel,
)
from app.models.candidate import CandidateModel
from app.utils.helpers import get_utc_now
from app.core.logging_config import logger


class ReportGenerator:
    """
    Assembles structured FeedbackReportModel JSON payloads combining scores, strengths,
    weaknesses, knowledge gaps, curriculum coverage, recommendations, and executive summaries.
    """

    @classmethod
    def assemble_report(
        cls,
        session_id: str,
        candidate: CandidateModel,
        overall_score: OverallScoreModel,
        strengths: List[str],
        weaknesses: List[str],
        knowledge_gaps: List[KnowledgeGapModel],
        topics_covered: List[str],
        days_covered: List[int],
        recommendations: List[RecommendationModel],
        summary: FeedbackSummaryModel,
    ) -> FeedbackReportModel:
        logger.info(f"Feedback report completed: Assembling report for session '{session_id}'...")

        curriculum_coverage = {
            "distinct_days_count": len(set(days_covered)),
            "days_covered": sorted(list(set(days_covered))),
            "distinct_topics_count": len(set(topics_covered)),
            "topics_covered": sorted(list(set(topics_covered))),
        }

        return FeedbackReportModel(
            session_id=session_id,
            candidate_id=candidate.candidate_id,
            generated_at=get_utc_now(),
            overall_score=overall_score,
            strengths=list(set(strengths)),
            weaknesses=list(set(weaknesses)),
            knowledge_gaps=knowledge_gaps,
            topics_covered=sorted(list(set(topics_covered))),
            curriculum_coverage=curriculum_coverage,
            recommendations=recommendations,
            summary=summary,
        )
