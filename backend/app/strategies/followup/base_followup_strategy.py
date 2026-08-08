from abc import ABC, abstractmethod
from app.models.answer_evaluation import AnswerEvaluationModel, FollowUpDecisionModel
from app.models.interview_engine import QuestionPlaceholderModel
from app.models.curriculum import TopicModel


class AbstractFollowUpStrategy(ABC):
    """Abstract Strategy interface for generating adaptive follow-up questions."""

    @abstractmethod
    def generate(
        self,
        evaluation: AnswerEvaluationModel,
        current_question: QuestionPlaceholderModel,
        topic: TopicModel,
        candidate_answer: str,
    ) -> FollowUpDecisionModel:
        """Generates a FollowUpDecisionModel."""
        pass
