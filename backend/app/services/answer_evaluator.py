from typing import Optional
from app.strategies.evaluation.base_evaluation_strategy import AbstractEvaluationStrategy
from app.strategies.evaluation.llm_evaluation_strategy import LLMEvaluationStrategy
from app.models.answer_evaluation import AnswerEvaluationModel
from app.services.hallucination_guard import HallucinationGuard
from app.core.logging_config import logger


class AnswerEvaluator:
    """
    AnswerEvaluator using Evaluation Strategy Pattern and HallucinationGuard.
    """

    def __init__(self, strategy: Optional[AbstractEvaluationStrategy] = None):
        self.strategy = strategy or LLMEvaluationStrategy()

    def evaluate_answer(
        self,
        candidate_answer: str,
        question_text: str,
        topic_title: str,
        topic_category: str = "General",
        day_number: int = 1,
        difficulty: str = "Intermediate",
    ) -> AnswerEvaluationModel:
        """
        Evaluates a candidate answer via the configured strategy and passes result through HallucinationGuard.
        """
        logger.info(f"Evaluation completed: Running strategy '{type(self.strategy).__name__}' for topic '{topic_title}'.")
        raw_eval = self.strategy.evaluate(
            candidate_answer=candidate_answer,
            question_text=question_text,
            topic_title=topic_title,
            day_number=day_number,
            difficulty=difficulty,
        )

        sanitized_eval = HallucinationGuard.sanitize_and_validate(raw_eval)
        logger.info(f"Classification selected: '{sanitized_eval.classification}' (Score {sanitized_eval.score}/100).")
        return sanitized_eval
