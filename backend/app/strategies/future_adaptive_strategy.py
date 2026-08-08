from typing import Optional
from app.strategies.base_strategy import AbstractInterviewStrategy
from app.models.interview_engine import InterviewPlanModel, QuestionPlaceholderModel
from app.services.curriculum_service import CurriculumService
from app.services.candidate_service import CandidateService
from app.services.interview_planner import InterviewPlanner


class FutureAdaptiveStrategy(AbstractInterviewStrategy):
    """
    Placeholder for Future Adaptive AI Strategy (Gemini / Claude / OpenAI).
    Will dynamically adapt difficulty tiers and follow-up probes based on real-time candidate scores.
    """

    def __init__(self, planner: Optional[InterviewPlanner] = None):
        self.planner = planner or InterviewPlanner()

    def generate_plan(
        self,
        candidate_id: str,
        session_id: str,
        curriculum_service: CurriculumService,
        candidate_service: CandidateService,
    ) -> InterviewPlanModel:
        # TODO: Implement adaptive plan generation with LLM provider in Phase 5
        return self.planner.generate_plan(candidate_id=candidate_id, session_id=session_id)

    def determine_next_question(
        self,
        plan: InterviewPlanModel,
        current_index: int,
    ) -> Optional[QuestionPlaceholderModel]:
        # TODO: Implement dynamic follow-up selection with adaptive difficulty engine in Phase 5
        if current_index >= len(plan.questions):
            return None
        return plan.questions[current_index]
