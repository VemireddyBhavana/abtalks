from app.models.candidate import CandidateModel, ProgressModel
from app.models.curriculum import TopicModel, DayModel, CurriculumModel
from app.models.interview_engine import QuestionPlaceholderModel


class MockDataFactory:
    """
    Factory creating standardized mock instances for backend unit and integration testing.
    """

    @staticmethod
    def create_candidate(candidate_id: str = "cand_test_99", full_name: str = "Test Candidate") -> CandidateModel:
        return CandidateModel(
            candidate_id=candidate_id,
            full_name=full_name,
            email="test@example.com",
            target_role="AI Engineer",
            experience_level="Senior",
            progress=ProgressModel(
                completed_days=[1],
                incomplete_days=[2],
                total_days=2,
                progress_percentage=50.0,
            ),
            completed_topics=["top_1"],
            skipped_topics=[],
            learning_signals=[],
            recent_activity=[],
        )

    @staticmethod
    def create_question(question_id: str = "q_mock_1", topic_id: str = "top_mock") -> QuestionPlaceholderModel:
        return QuestionPlaceholderModel(
            id=question_id,
            day_number=1,
            topic_id=topic_id,
            topic_title="Mock Topic",
            question_text="Sample technical question text?",
            difficulty="Intermediate",
        )
