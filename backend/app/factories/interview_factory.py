from typing import Optional
from app.strategies.base_strategy import AbstractInterviewStrategy
from app.strategies.standard_strategy import StandardInterviewStrategy
from app.services.curriculum_service import CurriculumService, get_curriculum_service
from app.services.candidate_service import CandidateService, get_candidate_service
from app.services.question_selector import QuestionSelector
from app.services.interview_planner import InterviewPlanner
from app.services.interview_validator import InterviewValidator
from app.services.interview_engine import InterviewEngine


class InterviewFactory:
    """
    Factory Pattern implementation for constructing fully configured InterviewEngine instances
    with injected strategy, services, planner, and validator dependencies.
    """

    @classmethod
    def create_engine(
        cls,
        strategy: Optional[AbstractInterviewStrategy] = None,
        curriculum_service: Optional[CurriculumService] = None,
        candidate_service: Optional[CandidateService] = None,
    ) -> InterviewEngine:
        curriculum_svc = curriculum_service or get_curriculum_service()
        candidate_svc = candidate_service or get_candidate_service()
        chosen_strategy = strategy or StandardInterviewStrategy()

        selector = QuestionSelector(curriculum_service=curriculum_svc, candidate_service=candidate_svc)
        planner = InterviewPlanner(question_selector=selector)
        validator = InterviewValidator(candidate_service=candidate_svc)

        return InterviewEngine(strategy=chosen_strategy, planner=planner, validator=validator)
