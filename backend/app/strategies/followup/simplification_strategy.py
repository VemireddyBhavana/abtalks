from app.strategies.followup.base_followup_strategy import AbstractFollowUpStrategy
from app.models.answer_evaluation import AnswerEvaluationModel, FollowUpDecisionModel
from app.models.interview_engine import QuestionPlaceholderModel
from app.models.curriculum import TopicModel
from app.core.logging_config import logger


class SimplificationStrategy(AbstractFollowUpStrategy):
    """Generates simpler foundational questions for Weak or Incorrect answers."""

    def generate(
        self,
        evaluation: AnswerEvaluationModel,
        current_question: QuestionPlaceholderModel,
        topic: TopicModel,
        candidate_answer: str,
    ) -> FollowUpDecisionModel:
        logger.info(f"SimplificationStrategy: Generating simpler explanation question for topic '{topic.title}'.")
        q_text = f"Thank you for sharing your thoughts. To wrap up on {topic.title}, what is the fundamental core benefit it provides to developers?"
        return FollowUpDecisionModel(
            action_type="Simpler Explanation",
            follow_up_question_text=q_text,
            rationale="Answer was weak or incorrect; offering gentle technical redirection with foundational question.",
            topic_transition=False,
        )
