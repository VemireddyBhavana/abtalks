from app.strategies.followup.base_followup_strategy import AbstractFollowUpStrategy
from app.models.answer_evaluation import AnswerEvaluationModel, FollowUpDecisionModel
from app.models.interview_engine import QuestionPlaceholderModel
from app.models.curriculum import TopicModel
from app.core.logging_config import logger


class ClarificationStrategy(AbstractFollowUpStrategy):
    """Generates clarification questions for Average or Unclear answers."""

    def generate(
        self,
        evaluation: AnswerEvaluationModel,
        current_question: QuestionPlaceholderModel,
        topic: TopicModel,
        candidate_answer: str,
    ) -> FollowUpDecisionModel:
        logger.info(f"ClarificationStrategy: Generating clarification question for topic '{topic.title}'.")
        q_text = f"Could you elaborate a bit more on how {topic.title} handles errors and data validation in full stack applications?"
        return FollowUpDecisionModel(
            action_type="Clarification",
            follow_up_question_text=q_text,
            rationale="Candidate answer was average or unclear; seeking technical clarification on gaps.",
            topic_transition=False,
        )
