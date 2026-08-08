from app.models.answer_evaluation import ConfidenceMetricsModel
from app.core.logging_config import logger


class ConfidenceAnalyzer:
    """
    Analyzes candidate turn responses to estimate confidence rating, technical depth,
    conceptual understanding, completeness, and communication clarity.
    """

    @classmethod
    def analyze_confidence(cls, answer_text: str, base_score: int) -> ConfidenceMetricsModel:
        text = answer_text.strip()
        length = len(text)

        # Baseline metrics calculated from answer structure and base score
        clarity = min(100, max(50, 60 + (length // 20)))
        depth = min(100, max(30, base_score - 5 + (10 if "because" in text.lower() or "for example" in text.lower() else 0)))
        understanding = min(100, max(40, base_score + 5))
        completeness = min(100, max(35, base_score - 2))
        confidence = min(100, max(40, int((depth * 0.4) + (understanding * 0.4) + (clarity * 0.2))))

        logger.info(f"Confidence Score: Estimated confidence {confidence}% (Depth: {depth}%, Clarity: {clarity}%).")

        return ConfidenceMetricsModel(
            confidence=confidence,
            technical_depth=depth,
            conceptual_understanding=understanding,
            completeness=completeness,
            communication_clarity=clarity,
        )
