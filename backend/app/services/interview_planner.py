from typing import List, Set, Optional
from app.models.interview_engine import QuestionPlaceholderModel, InterviewPlanModel
from app.services.question_bank import QuestionBank
from app.services.question_selector import QuestionSelector
from app.services.curriculum_service import CurriculumService, get_curriculum_service
from app.services.candidate_service import CandidateService, get_candidate_service
from app.services.llm_service import LLMService, get_llm_service
from app.exceptions.llm_exception import LLMError
from app.utils.helpers import get_utc_now, generate_unique_id
from app.core.logging_config import logger


class InterviewPlanner:
    """
    Generates a structured 8-question interview plan covering at least 4 distinct curriculum days.
    Uses LLMService to dynamically generate questions for selected topics with QuestionBank fallback.
    """

    def __init__(
        self,
        question_selector: Optional[QuestionSelector] = None,
        llm_service: Optional[LLMService] = None,
        curriculum_service: Optional[CurriculumService] = None,
        candidate_service: Optional[CandidateService] = None,
    ):
        self.curriculum_service = curriculum_service or get_curriculum_service()
        self.candidate_service = candidate_service or get_candidate_service()
        self.question_selector = question_selector or QuestionSelector(
            curriculum_service=self.curriculum_service,
            candidate_service=self.candidate_service,
        )
        self.llm_service = llm_service or get_llm_service()

    def generate_plan(self, candidate_id: str, session_id: Optional[str] = None) -> InterviewPlanModel:
        """
        Generates an 8-question InterviewPlanModel dynamically using LLMService / QuestionBank fallback.
        """
        session_id = session_id or generate_unique_id("session")
        selected_topics = self.question_selector.select_topics(min_days=4, target_topic_count=8)
        candidate = self.candidate_service.get_candidate()

        planned_questions: List[QuestionPlaceholderModel] = []
        used_question_ids: Set[str] = set()
        used_topic_ids: Set[str] = set()

        for idx, topic in enumerate(selected_topics):
            if len(planned_questions) >= 8:
                break

            q_id = f"q_idx_{idx + 1}_{topic.id}"
            day = self.curriculum_service.get_day(
                self._find_day_number_for_topic(topic.id)
            )

            # Try generating dynamic LLM question
            question_model = None
            try:
                question_model = self.llm_service.generate_question(
                    candidate=candidate,
                    topic=topic,
                    day=day,
                    question_id=q_id,
                    difficulty="Intermediate",
                    asked_questions=[q.question_text for q in planned_questions],
                    session_id=session_id,
                )
            except (LLMError, Exception) as exc:
                logger.warning(f"Generation Failed for topic '{topic.id}': {str(exc)}. Falling back to QuestionBank.")
                # Fallback to QuestionBank
                topic_bank_questions = QuestionBank.get_questions_by_topic(topic.id)
                if topic_bank_questions:
                    question_model = topic_bank_questions[0]
                else:
                    question_model = QuestionPlaceholderModel(
                        id=q_id,
                        day_number=day.day_number if day else 1,
                        topic_id=topic.id,
                        topic_title=topic.title,
                        question_text=f"How do you implement {topic.title} in scalable full stack AI applications?",
                        difficulty="Intermediate"
                    )

            if question_model and question_model.topic_id not in used_topic_ids:
                planned_questions.append(question_model)
                used_question_ids.add(question_model.id)
                used_topic_ids.add(question_model.topic_id)

        # Fallback fill if fewer than 8 questions were generated
        if len(planned_questions) < 8:
            all_questions = QuestionBank.get_all_questions()
            for q in all_questions:
                if len(planned_questions) >= 8:
                    break
                if q.topic_id not in used_topic_ids:
                    planned_questions.append(q)
                    used_topic_ids.add(q.topic_id)

        days_covered = set(q.day_number for q in planned_questions)
        logger.info(
            f"Interview Plan Created: Session '{session_id}' with {len(planned_questions)} LLM/Bank questions covering {len(days_covered)} distinct days."
        )

        return InterviewPlanModel(
            session_id=session_id,
            candidate_id=candidate_id,
            created_at=get_utc_now(),
            questions=planned_questions,
        )

    def _find_day_number_for_topic(self, topic_id: str) -> int:
        for day in self.curriculum_service.get_all_days():
            for top in day.topics:
                if top.id == topic_id:
                    return day.day_number
        return 1
