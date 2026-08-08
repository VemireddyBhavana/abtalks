from typing import List, Dict, Any, Optional
from app.models.feedback_report import RecommendationModel, KnowledgeGapModel
from app.services.curriculum_service import CurriculumService, get_curriculum_service
from app.core.logging_config import logger


class RecommendationEngine:
    """
    Generates actionable, curriculum-mapped study recommendations referencing curriculum days,
    learning objectives, and recommended practice areas.
    """

    def __init__(self, curriculum_service: Optional[CurriculumService] = None):
        self.curriculum_service = curriculum_service or get_curriculum_service()

    def generate_recommendations(
        self,
        knowledge_gaps: List[KnowledgeGapModel],
        overall_score: float,
    ) -> List[RecommendationModel]:
        logger.info("Recommendations generated: Mapping gaps to curriculum learning objectives...")
        recommendations: List[RecommendationModel] = []
        seen_topics = set()

        for gap in knowledge_gaps:
            if gap.topic_id in seen_topics:
                continue
            seen_topics.add(gap.topic_id)

            day = self.curriculum_service.get_day(gap.day_number)
            objectives = day.learning_objectives if day else ["Revisit foundational concepts."]

            rec = RecommendationModel(
                topic_title=gap.topic_title,
                curriculum_day=gap.day_number,
                learning_objectives=objectives,
                recommended_action=f"Revisit Curriculum Day {gap.day_number} ('{day.title if day else 'Foundations'}') and complete hands-on practice labs.",
                priority=gap.severity,
            )
            recommendations.append(rec)

        # Default fallback recommendation if candidate scored exceptionally well
        if not recommendations:
            recommendations.append(
                RecommendationModel(
                    topic_title="Advanced Production Architectures",
                    curriculum_day=5,
                    learning_objectives=["Deploy full-stack AI applications on Vercel and Render"],
                    recommended_action="Proceed to advanced production optimization and multi-agent orchestration projects.",
                    priority="Low",
                )
            )

        return recommendations


# Singleton helper
_rec_engine_instance: Optional[RecommendationEngine] = None


def get_recommendation_engine() -> RecommendationEngine:
    global _rec_engine_instance
    if _rec_engine_instance is None:
        _rec_engine_instance = RecommendationEngine()
    return _rec_engine_instance
