from app.models.answer_evaluation import RubricScoreModel
from app.core.logging_config import logger


class RubricEngine:
    """
    Evaluates candidate answers against weighted rubrics:
    1. Technical Accuracy (Weight 30%)
    2. Concept Coverage (Weight 25%)
    3. Terminology (Weight 15%)
    4. Reasoning (Weight 15%)
    5. Examples (Weight 10%)
    6. Completeness (Weight 5%)
    """

    @classmethod
    def evaluate_rubric(
        cls,
        accuracy: int = 75,
        coverage: int = 75,
        terminology: int = 70,
        reasoning: int = 70,
        examples: int = 60,
        completeness: int = 70,
    ) -> RubricScoreModel:
        """
        Computes weighted total rubric score.
        """
        weighted_score = (
            (accuracy * 0.30)
            + (coverage * 0.25)
            + (terminology * 0.15)
            + (reasoning * 0.15)
            + (examples * 0.10)
            + (completeness * 0.05)
        )
        total = round(weighted_score, 2)
        logger.info(f"Rubric Evaluated: Computed weighted total score {total}/100.")

        return RubricScoreModel(
            technical_accuracy=accuracy,
            concept_coverage=coverage,
            terminology=terminology,
            reasoning=reasoning,
            examples=examples,
            completeness=completeness,
            weighted_total_score=total,
        )
