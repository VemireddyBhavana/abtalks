from app.strategies.followup.base_followup_strategy import AbstractFollowUpStrategy
from app.models.answer_evaluation import AnswerEvaluationModel, FollowUpDecisionModel
from app.models.interview_engine import QuestionPlaceholderModel
from app.models.curriculum import TopicModel
from app.core.logging_config import logger


class TopicTransitionStrategy(AbstractFollowUpStrategy):
    """Triggers advancement to the next planned curriculum topic."""

    def generate(
        self,
        evaluation: AnswerEvaluationModel,
        current_question: QuestionPlaceholderModel,
        topic: TopicModel,
        candidate_answer: str,
    ) -> FollowUpDecisionModel:
        logger.info(f"TopicTransitionStrategy: Advancing to next topic from '{topic.title}'.")
        return FollowUpDecisionModel(
            action_type="Transition",
            follow_up_question_text=None,
            rationale="Topic evaluation turn count reached; advancing to next curriculum topic.",
            topic_transition=True,
        )
