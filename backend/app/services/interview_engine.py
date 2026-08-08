from typing import Optional, Dict, Any
from app.strategies.base_strategy import AbstractInterviewStrategy
from app.strategies.standard_strategy import StandardInterviewStrategy
from app.models.interview_engine import (
    QuestionPlaceholderModel,
    InterviewPlanModel,
    StartInterviewRequestModel,
    StartInterviewResponseModel,
    AnswerSubmissionModel,
    AnswerInterviewResponseModel,
    InterviewStateModel,
    InterviewSummaryModel,
)
from app.models.curriculum import TopicModel
from app.services.interview_planner import InterviewPlanner
from app.services.interview_validator import InterviewValidator
from app.services.interview_state import get_interview_state_manager, InterviewSessionState
from app.services.curriculum_service import CurriculumService, get_curriculum_service
from app.services.candidate_service import CandidateService, get_candidate_service
from app.services.answer_evaluator import AnswerEvaluator
from app.services.followup_engine import FollowUpEngine
from app.services.feedback_engine import FeedbackEngine, get_feedback_engine
from app.exceptions.interview_exception import (
    InterviewAlreadyCompletedError,
    InvalidInterviewStateError,
    QuestionNotFoundError,
)
from app.utils.helpers import generate_unique_id
from app.core.logging_config import logger


class InterviewEngine:
    """
    Main Interview Engine orchestrator.
    Manages session initialization, plan generation, turn execution, answer evaluation,
    adaptive follow-up generation, and completion feedback report generation.
    """

    def __init__(
        self,
        strategy: Optional[AbstractInterviewStrategy] = None,
        planner: Optional[InterviewPlanner] = None,
        validator: Optional[InterviewValidator] = None,
        evaluator: Optional[AnswerEvaluator] = None,
        feedback_engine: Optional[FeedbackEngine] = None,
        curriculum_service: Optional[CurriculumService] = None,
        candidate_service: Optional[CandidateService] = None,
    ):
        self.strategy = strategy or StandardInterviewStrategy()
        self.planner = planner or InterviewPlanner()
        self.validator = validator or InterviewValidator()
        self.evaluator = evaluator or AnswerEvaluator()
        self.feedback_engine = feedback_engine or get_feedback_engine()
        self.curriculum_service = curriculum_service or get_curriculum_service()
        self.candidate_service = candidate_service or get_candidate_service()
        self.state_manager = get_interview_state_manager()

    def start_interview(
        self, candidate_id: str = "cand_alex_dev_99", session_id: Optional[str] = None
    ) -> StartInterviewResponseModel:
        """
        Starts an interview session, creates an 8-question plan using strategy, validates plan,
        initializes session state, and returns Question 1.
        """
        session_id = session_id or generate_unique_id("session")
        logger.info(f"Interview Created: Initiating session '{session_id}' for candidate '{candidate_id}'.")

        plan = self.strategy.generate_plan(
            candidate_id=candidate_id,
            session_id=session_id,
            curriculum_service=self.curriculum_service,
            candidate_service=self.candidate_service,
        )
        logger.info(f"Plan Generated: Created 8-question plan for session '{session_id}'.")

        self.validator.validate_plan(plan)
        logger.info(f"Validation Passed: Pre-flight plan validation succeeded for session '{session_id}'.")

        session = self.state_manager.create_session(session_id, candidate_id, plan)

        first_question = self.strategy.determine_next_question(plan, session.current_question_index)
        if not first_question:
            raise QuestionNotFoundError("First question unavailable in plan.")

        logger.info(f"Question Returned: Session '{session_id}', Q1 ({first_question.id})")

        return StartInterviewResponseModel(
            session_id=session_id,
            message="Interview session started successfully.",
            total_questions=len(plan.questions),
            current_question_index=session.current_question_index,
            question=first_question,
        )

    def submit_answer(self, session_id: str, answer_text: str) -> AnswerInterviewResponseModel:
        """
        Records the candidate's answer for the active question, evaluates answer quality,
        generates adaptive follow-ups, and produces the final FeedbackReportModel upon completion.
        """
        session = self.state_manager.get_session(session_id)
        if not session:
            logger.error(f"InvalidInterviewStateError: Session '{session_id}' not found.")
            raise InvalidInterviewStateError(f"Interview session '{session_id}' not found.")

        if session.done:
            logger.warning(f"InterviewAlreadyCompletedError: Session '{session_id}' already finished.")
            raise InterviewAlreadyCompletedError(f"Interview session '{session_id}' is already completed.")

        active_q = session.current_question
        if not active_q:
            raise QuestionNotFoundError("Active question unavailable in session.")

        # Phase 6: Evaluate candidate answer
        evaluation = self.evaluator.evaluate_answer(
            candidate_answer=answer_text,
            question_text=active_q.question_text,
            topic_title=active_q.topic_title,
            day_number=active_q.day_number,
            difficulty=active_q.difficulty,
        )

        # Record turn answer with evaluation metrics
        is_completed = session.record_answer(answer_text)
        if session.candidate_answers:
            session.candidate_answers[-1]["evaluation"] = evaluation.model_dump()

        logger.info(
            f"Answer Evaluated: Score {evaluation.score}/100 ({evaluation.classification}). Action: '{evaluation.recommended_action}'."
        )

        # Phase 6: Adaptive Follow-up Engine
        dummy_topic = TopicModel(id=active_q.topic_id, title=active_q.topic_title, category="General")
        followup_decision = FollowUpEngine.generate_followup(
            evaluation=evaluation,
            current_question=active_q,
            topic=dummy_topic,
            candidate_answer=answer_text,
            turn_count_on_topic=1 if "followup" not in active_q.id else 2,
        )

        # If adaptive follow-up is requested and session is not completed, replace next question slot
        if followup_decision.follow_up_question_text and not followup_decision.topic_transition and not is_completed:
            followup_id = f"q_followup_{active_q.id}"
            followup_q = QuestionPlaceholderModel(
                id=followup_id,
                day_number=active_q.day_number,
                topic_id=active_q.topic_id,
                topic_title=active_q.topic_title,
                question_text=followup_decision.follow_up_question_text,
                difficulty=active_q.difficulty,
            )

            next_slot = session.current_question_index
            if next_slot < len(session.plan.questions):
                session.plan.questions[next_slot] = followup_q
                logger.info(f"Follow-up Injected: Replaced slot {next_slot + 1} with adaptive follow-up '{followup_id}'.")

        next_q = self.strategy.determine_next_question(session.plan, session.current_question_index)
        feedback_report = None

        if is_completed:
            msg = "Answer recorded. Interview completed!"
            logger.info(f"Interview Completed: Session '{session_id}' completed all questions. Generating final feedback report...")
            # Phase 7: Generate final feedback report
            feedback_report = self.feedback_engine.generate_feedback_report(session)
        else:
            msg = f"Answer recorded ({evaluation.classification}). Advanced to question {session.current_question_index + 1}."
            if next_q:
                logger.info(f"Question Returned: Session '{session_id}', Q{session.current_question_index + 1} ({next_q.id})")

        return AnswerInterviewResponseModel(
            session_id=session_id,
            message=msg,
            done=is_completed,
            current_question_index=session.current_question_index,
            total_questions=len(session.plan.questions),
            next_question=next_q,
            feedback_report=feedback_report,
        )

    def get_current_question(self, session_id: str) -> Optional[QuestionPlaceholderModel]:
        """Returns current question using Strategy."""
        session = self.state_manager.get_session(session_id)
        if not session:
            raise InvalidInterviewStateError(f"Interview session '{session_id}' not found.")
        return self.strategy.determine_next_question(session.plan, session.current_question_index)

    def get_session_state(self, session_id: str) -> InterviewStateModel:
        """Returns serialized session state model."""
        session = self.state_manager.get_session(session_id)
        if not session:
            raise InvalidInterviewStateError(f"Interview session '{session_id}' not found.")
        return session.to_state_model()

    def get_interview_summary(self, session_id: str) -> InterviewSummaryModel:
        """Returns high-level interview summary metadata and feedback report if finished."""
        session = self.state_manager.get_session(session_id)
        if not session:
            raise InvalidInterviewStateError(f"Interview session '{session_id}' not found.")

        feedback_report = None
        if session.done:
            feedback_report = self.feedback_engine.generate_feedback_report(session)

        return InterviewSummaryModel(
            session_id=session.session_id,
            candidate_id=session.candidate_id,
            total_questions_asked=len(session.candidate_answers),
            distinct_days_covered_count=len(session.days_covered),
            distinct_topics_covered_count=len(session.topics_covered),
            days_covered=session.days_covered,
            topics_covered=session.topics_covered,
            started_at=session.started_at,
            completed_at=session.completed_at,
            done=session.done,
            feedback_report=feedback_report,
        )


# Singleton helper
_engine_instance: Optional[InterviewEngine] = None


def get_interview_engine() -> InterviewEngine:
    global _engine_instance
    if _engine_instance is None:
        from app.factories.interview_factory import InterviewFactory
        _engine_instance = InterviewFactory.create_engine()
    return _engine_instance
