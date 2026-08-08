from app.strategies.followup.base_followup_strategy import AbstractFollowUpStrategy
from app.models.answer_evaluation import AnswerEvaluationModel, FollowUpDecisionModel
from app.models.interview_engine import QuestionPlaceholderModel
from app.models.curriculum import TopicModel
from app.core.logging_config import logger


class DeepDiveStrategy(AbstractFollowUpStrategy):
    """Generates deeper technical probe questions for Excellent or Good answers."""

    def generate(
        self,
        evaluation: AnswerEvaluationModel,
        current_question: QuestionPlaceholderModel,
        topic: TopicModel,
        candidate_answer: str,
    ) -> FollowUpDecisionModel:
        logger.info(f"DeepDiveStrategy: Generating deeper technical probe for topic '{topic.title}'.")
        q_text = f"Taking that a step further into architectural design, how would you scale {topic.title} under high concurrency production environments?"
        return FollowUpDecisionModel(
            action_type="Deeper Probe",
            follow_up_question_text=q_text,
            rationale="Candidate demonstrated strong technical mastery; probing deeper architectural knowledge.",
            topic_transition=False,
        )
