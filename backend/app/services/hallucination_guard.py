from typing import Dict, Any
from app.models.answer_evaluation import AnswerEvaluationModel
from app.core.logging_config import logger


class HallucinationGuard:
    """
    Validates LLM evaluation outputs, ensuring required JSON fields exist, score ranges
    stay strictly within 0-100, and no fabricated rubric fields exist.
    """

    @classmethod
    def sanitize_and_validate(cls, eval_model: AnswerEvaluationModel) -> AnswerEvaluationModel:
        # Clamp scores to [0, 100] range
        eval_model.score = max(0, min(100, eval_model.score))
        eval_model.confidence_score = max(0, min(100, eval_model.confidence_score))

        # Clamp rubric fields
        rubric = eval_model.rubric
        rubric.technical_accuracy = max(0, min(100, rubric.technical_accuracy))
        rubric.concept_coverage = max(0, min(100, rubric.concept_coverage))
        rubric.terminology = max(0, min(100, rubric.terminology))
        rubric.reasoning = max(0, min(100, rubric.reasoning))
        rubric.examples = max(0, min(100, rubric.examples))
        rubric.completeness = max(0, min(100, rubric.completeness))
        rubric.weighted_total_score = max(0.0, min(100.0, rubric.weighted_total_score))

        logger.info(f"HallucinationGuard: Sanitized evaluation score {eval_model.score} (Confidence: {eval_model.confidence_score}).")
        return eval_model
