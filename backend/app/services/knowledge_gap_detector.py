from typing import List, Dict, Any
from app.models.answer_evaluation import AnswerEvaluationModel
from app.core.logging_config import logger


class KnowledgeGapDetector:
    """
    Identifies missing technical concepts, incomplete explanations, and knowledge gaps
    to recommend future review areas for candidate feedback.
    """

    @classmethod
    def detect_gaps(
        cls,
        evaluation: AnswerEvaluationModel,
        topic_title: str,
        learning_objectives: List[str],
    ) -> Dict[str, Any]:
        detected_gaps = list(evaluation.gaps)
        review_recommendations = []

        if evaluation.score < 60:
            detected_gaps.append(f"Incomplete explanation of {topic_title} fundamentals.")
            for obj in learning_objectives:
                review_recommendations.append(f"Review: {obj}")
            logger.info(f"Knowledge gap detected: Highlighted {len(detected_gaps)} gap(s) for topic '{topic_title}'.")
        else:
            logger.info(f"Knowledge gap check: Candidate demonstrated adequate comprehension of '{topic_title}'.")

        return {
            "topic_title": topic_title,
            "score": evaluation.score,
            "detected_gaps": detected_gaps,
            "review_recommendations": review_recommendations,
        }
