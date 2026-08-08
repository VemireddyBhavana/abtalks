from app.strategies.evaluation.base_evaluation_strategy import AbstractEvaluationStrategy
from app.models.answer_evaluation import AnswerEvaluationModel
from app.services.rubric_engine import RubricEngine
from app.services.confidence_analyzer import ConfidenceAnalyzer
from app.services.answer_classifier import AnswerClassifier
from app.core.logging_config import logger


class RuleBasedEvaluationStrategy(AbstractEvaluationStrategy):
    """
    Deterministic Rule-Based Evaluation Strategy for offline environments.
    """

    def evaluate(
        self,
        candidate_answer: str,
        question_text: str,
        topic_title: str,
        day_number: int = 1,
        difficulty: str = "Intermediate",
    ) -> AnswerEvaluationModel:
        logger.info(f"RuleBasedEvaluationStrategy: Evaluating answer deterministically for '{topic_title}'...")

        ans_len = len(candidate_answer.strip())
        score = 80 if ans_len >= 30 else (50 if ans_len >= 10 else 25)

        rubric = RubricEngine.evaluate_rubric(
            accuracy=score,
            coverage=score,
            terminology=score,
            reasoning=score,
            examples=score,
            completeness=score,
        )

        classification = AnswerClassifier.classify_score(score, candidate_answer)
        metrics = ConfidenceAnalyzer.analyze_confidence(candidate_answer, score)

        return AnswerEvaluationModel(
            score=score,
            confidence_score=metrics.confidence,
            classification=classification,
            rubric=rubric,
            metrics=metrics,
            strengths=[f"Deterministic check for {topic_title}."],
            weaknesses=[],
            gaps=[],
            recommended_action="Medium Followup",
        )
