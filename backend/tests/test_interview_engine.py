import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.factories.interview_factory import InterviewFactory
from app.strategies.standard_strategy import StandardInterviewStrategy
from app.strategies.future_adaptive_strategy import FutureAdaptiveStrategy
from app.services.difficulty_manager import DifficultyManager
from app.services.topic_coverage import TopicCoverageAnalyzer
from app.services.progress_tracker import ProgressTracker
from app.services.question_history import QuestionHistory
from app.services.interview_validator import InterviewValidator
from app.services.interview_metrics import InterviewMetricsCalculator
from app.services.interview_engine import InterviewEngine
from app.exceptions.interview_exception import (
    InterviewAlreadyCompletedError,
    InvalidInterviewStateError,
    InterviewPlanError,
)

client = TestClient(app)


def test_interview_factory_and_strategy():
    """Verifies InterviewFactory constructs engine with StandardInterviewStrategy."""
    engine = InterviewFactory.create_engine()
    assert isinstance(engine.strategy, StandardInterviewStrategy)

    adaptive_engine = InterviewFactory.create_engine(strategy=FutureAdaptiveStrategy())
    assert isinstance(adaptive_engine.strategy, FutureAdaptiveStrategy)


def test_difficulty_manager():
    """Verifies DifficultyManager mappings, score calculations, and tier suggestions."""
    assert DifficultyManager.get_difficulty_score("Fundamental") == 1
    assert DifficultyManager.get_difficulty_score("Intermediate") == 2
    assert DifficultyManager.get_difficulty_score("Advanced") == 3

    assert DifficultyManager.suggest_next_difficulty(90.0) == "Advanced"
    assert DifficultyManager.suggest_next_difficulty(70.0) == "Intermediate"
    assert DifficultyManager.suggest_next_difficulty(40.0) == "Fundamental"


def test_topic_coverage_analyzer():
    """Verifies TopicCoverageAnalyzer calculates statistics and flags validity."""
    engine = InterviewFactory.create_engine()
    resp = engine.start_interview(candidate_id="cand_coverage_test", session_id="sess_coverage_test")
    session = engine.state_manager.get_session("sess_coverage_test")

    analysis = TopicCoverageAnalyzer.analyze_plan(session.plan)
    assert analysis["total_questions"] == 8
    assert analysis["distinct_days_count"] >= 4
    assert analysis["is_multi_day_compliant"] is True
    assert analysis["is_topic_unique"] is True
    assert analysis["valid"] is True


def test_question_history():
    """Verifies QuestionHistory tracking and duplicate detection."""
    history = QuestionHistory()
    history.record_question("q1", "top1", 1)

    assert history.is_question_asked("q1") is True
    assert history.is_question_asked("q2") is False
    assert history.is_topic_asked("top1") is True
    assert history.get_asked_days() == [1]

    history.clear()
    assert history.is_question_asked("q1") is False


def test_progress_tracker_and_metrics():
    """Verifies ProgressTracker and InterviewMetricsCalculator."""
    engine = InterviewFactory.create_engine()
    engine.start_interview(candidate_id="cand_prog_test", session_id="sess_prog_test")
    session = engine.state_manager.get_session("sess_prog_test")

    progress = ProgressTracker.get_progress(session)
    assert progress["total_questions"] == 8
    assert progress["questions_remaining"] == 8
    assert progress["completion_percentage"] == 0.0

    engine.submit_answer("sess_prog_test", "Test Answer 1")

    progress_after = ProgressTracker.get_progress(session)
    assert progress_after["questions_remaining"] == 7
    assert progress_after["completion_percentage"] == 12.5

    metrics = InterviewMetricsCalculator.calculate_metrics(session)
    assert metrics["questions_asked_count"] == 1
    assert metrics["average_difficulty_score"] > 0.0


def test_interview_validator_success_and_failure():
    """Verifies InterviewValidator pre-flight plan checks."""
    validator = InterviewValidator()
    engine = InterviewFactory.create_engine()
    engine.start_interview(candidate_id="cand_val_test", session_id="sess_val_test")
    session = engine.state_manager.get_session("sess_val_test")

    report = validator.validate_plan(session.plan)
    assert report["valid"] is True
    assert report["days_covered_count"] >= 4

    # Test invalid plan (less than 8 questions)
    bad_plan = session.plan.model_copy()
    bad_plan.questions = bad_plan.questions[:5]
    with pytest.raises(InterviewPlanError, match="exactly 8 questions"):
        validator.validate_plan(bad_plan)


def test_custom_exception_handling():
    """Verifies custom exceptions raised during invalid state transitions."""
    engine = InterviewFactory.create_engine()

    # Invalid session ID
    with pytest.raises(InvalidInterviewStateError):
        engine.get_session_state("non_existent_sess")

    # Double completion
    engine.start_interview(candidate_id="cand_exc_test", session_id="sess_exc_test")
    for i in range(8):
        engine.submit_answer("sess_exc_test", f"Answer {i + 1}")

    with pytest.raises(InterviewAlreadyCompletedError):
        engine.submit_answer("sess_exc_test", "Extra answer after completion")


def test_api_validation_endpoint():
    """Integration test for GET /api/v1/interview/{session_id}/validate."""
    start_res = client.post("/api/v1/interview/start", json={"candidate_id": "cand_api_val", "session_id": "sess_api_val"})
    assert start_res.status_code == 200

    val_res = client.get("/api/v1/interview/sess_api_val/validate")
    assert val_res.status_code == 200
    val_data = val_res.json()
    assert val_data["valid"] is True
    assert val_data["days_covered_count"] >= 4
