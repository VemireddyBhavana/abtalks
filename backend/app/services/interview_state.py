from typing import List, Dict, Optional, Any
from app.models.interview_engine import QuestionPlaceholderModel, InterviewPlanModel, InterviewStateModel
from app.utils.helpers import get_utc_now
from app.core.logging_config import logger


class InterviewSessionState:
    """
    In-memory state tracker for an active interview session.
    """

    def __init__(self, session_id: str, candidate_id: str, plan: InterviewPlanModel):
        self.session_id = session_id
        self.candidate_id = candidate_id
        self.plan = plan
        self.current_question_index = 0
        self.done = False
        self.started_at = get_utc_now()
        self.completed_at: Optional[str] = None
        self.candidate_answers: List[Dict[str, Any]] = []

    @property
    def current_question(self) -> Optional[QuestionPlaceholderModel]:
        """Returns the active question model or None if completed."""
        if self.done or self.current_question_index >= len(self.plan.questions):
            return None
        return self.plan.questions[self.current_question_index]

    @property
    def asked_question_ids(self) -> List[str]:
        """Returns list of question IDs that have been presented so far."""
        return [q.id for q in self.plan.questions[: self.current_question_index + 1]]

    @property
    def topics_covered(self) -> List[str]:
        """Returns distinct topic IDs covered so far."""
        covered = set()
        for q in self.plan.questions[: self.current_question_index + 1]:
            covered.add(q.topic_id)
        return sorted(list(covered))

    @property
    def days_covered(self) -> List[int]:
        """Returns distinct curriculum day indices covered so far."""
        covered = set()
        for q in self.plan.questions[: self.current_question_index + 1]:
            covered.add(q.day_number)
        return sorted(list(covered))

    def record_answer(self, answer_text: str) -> bool:
        """
        Records the candidate's answer for the current question and advances the index.
        Returns True if interview is completed after this answer, else False.
        """
        if self.done:
            return True

        current_q = self.current_question
        if current_q:
            self.candidate_answers.append({
                "question_id": current_q.id,
                "day_number": current_q.day_number,
                "topic_id": current_q.topic_id,
                "question_text": current_q.question_text,
                "candidate_answer": answer_text,
                "answered_at": get_utc_now(),
            })
            logger.info(f"Answer Stored: Session '{self.session_id}', Q{self.current_question_index + 1} ({current_q.id})")

        self.current_question_index += 1

        if self.current_question_index >= len(self.plan.questions):
            self.done = True
            self.completed_at = get_utc_now()
            logger.info(f"Interview Completed: Session '{self.session_id}' finished all {len(self.plan.questions)} questions.")

        return self.done

    def to_state_model(self) -> InterviewStateModel:
        """Serializes current state into InterviewStateModel Pydantic model."""
        return InterviewStateModel(
            session_id=self.session_id,
            candidate_id=self.candidate_id,
            current_question_index=self.current_question_index,
            done=self.done,
            total_questions=len(self.plan.questions),
            asked_question_ids=self.asked_question_ids,
            candidate_answers=self.candidate_answers,
            days_covered=self.days_covered,
            topics_covered=self.topics_covered,
            started_at=self.started_at,
            completed_at=self.completed_at,
        )


class InterviewStateManager:
    """
    Central repository for tracking active interview session states.
    """

    def __init__(self):
        self._sessions: Dict[str, InterviewSessionState] = {}

    def create_session(self, session_id: str, candidate_id: str, plan: InterviewPlanModel) -> InterviewSessionState:
        session = InterviewSessionState(session_id, candidate_id, plan)
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[InterviewSessionState]:
        return self._sessions.get(session_id)

    def has_session(self, session_id: str) -> bool:
        return session_id in self._sessions


# Singleton helper
_state_manager_instance: Optional[InterviewStateManager] = None


def get_interview_state_manager() -> InterviewStateManager:
    global _state_manager_instance
    if _state_manager_instance is None:
        _state_manager_instance = InterviewStateManager()
    return _state_manager_instance
