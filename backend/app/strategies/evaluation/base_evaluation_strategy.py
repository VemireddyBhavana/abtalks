from abc import ABC, abstractmethod
from app.models.answer_evaluation import AnswerEvaluationModel


class AbstractEvaluationStrategy(ABC):
    """Abstract Strategy interface for candidate answer evaluation."""

    @abstractmethod
    def evaluate(
        self,
        candidate_answer: str,
        question_text: str,
        topic_title: str,
        day_number: int = 1,
        difficulty: str = "Intermediate",
    ) -> AnswerEvaluationModel:
        """Evaluates candidate answer and returns an AnswerEvaluationModel."""
        pass
