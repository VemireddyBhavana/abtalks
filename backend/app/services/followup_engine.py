from typing import Dict
from app.models.answer_evaluation import AnswerEvaluationModel, FollowUpDecisionModel
from app.models.interview_engine import QuestionPlaceholderModel
from app.models.curriculum import TopicModel
from app.services.answer_classifier import AnswerClassifier
from app.strategies.followup.base_followup_strategy import AbstractFollowUpStrategy
from app.strategies.followup.deep_dive_strategy import DeepDiveStrategy
from app.strategies.followup.clarification_strategy import ClarificationStrategy
from app.strategies.followup.simplification_strategy import SimplificationStrategy
from app.strategies.followup.topic_transition_strategy import TopicTransitionStrategy
from app.core.logging_config import logger


class FollowUpEngine:
    """
    Adaptive Follow-up Engine using Strategy Pattern.
    Chooses appropriate strategy (DeepDiveStrategy, ClarificationStrategy, SimplificationStrategy,
    TopicTransitionStrategy) based on evaluation result.
    """

    _STRATEGY_MAP: Dict[str, AbstractFollowUpStrategy] = {
        AnswerClassifier.EXCELLENT: DeepDiveStrategy(),
        AnswerClassifier.GOOD: DeepDiveStrategy(),
        AnswerClassifier.AVERAGE: ClarificationStrategy(),
        AnswerClassifier.UNCLEAR: ClarificationStrategy(),
        AnswerClassifier.WEAK: SimplificationStrategy(),
        AnswerClassifier.INCORRECT: SimplificationStrategy(),
    }

    @classmethod
    def generate_followup(
        cls,
        evaluation: AnswerEvaluationModel,
        current_question: QuestionPlaceholderModel,
        topic: TopicModel,
        candidate_answer: str,
        turn_count_on_topic: int = 1,
    ) -> FollowUpDecisionModel:
        """
        Determines and executes the appropriate follow-up strategy based on classification.
        """
        if turn_count_on_topic >= 2:
            logger.info(f"Topic transitioned: Max turn count reached on topic '{topic.title}'. Using TopicTransitionStrategy.")
            strategy = TopicTransitionStrategy()
        else:
            cls_type = evaluation.classification
            strategy = cls._STRATEGY_MAP.get(cls_type, ClarificationStrategy())
            logger.info(f"Follow-up strategy chosen: '{type(strategy).__name__}' for classification '{cls_type}'.")

        return strategy.generate(
            evaluation=evaluation,
            current_question=current_question,
            topic=topic,
            candidate_answer=candidate_answer,
        )
