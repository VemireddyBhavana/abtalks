from abc import ABC, abstractmethod
from typing import Optional
from app.models.interview_engine import InterviewPlanModel, QuestionPlaceholderModel
from app.services.curriculum_service import CurriculumService
from app.services.candidate_service import CandidateService


class AbstractInterviewStrategy(ABC):
    """
    Abstract Strategy interface for planning and executing interview turn logic.
    Supports future dynamic/adaptive LLM strategies (Gemini, Claude, OpenAI) without changing InterviewEngine.
    """

    @abstractmethod
    def generate_plan(
        self,
        candidate_id: str,
        session_id: str,
        curriculum_service: CurriculumService,
        candidate_service: CandidateService,
    ) -> InterviewPlanModel:
        """Generates an InterviewPlanModel according to strategy rules."""
        pass

    @abstractmethod
    def determine_next_question(
        self,
        plan: InterviewPlanModel,
        current_index: int,
    ) -> Optional[QuestionPlaceholderModel]:
        """Determines next question or returns None if interview is completed."""
        pass
