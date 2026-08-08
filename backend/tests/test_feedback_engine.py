import pytest
from app.services.score_calculator import ScoreCalculator
from app.services.summary_generator import SummaryGenerator
from app.services.recommendation_engine import RecommendationEngine
from app.services.report_generator import ReportGenerator
from app.services.feedback_engine import FeedbackEngine
from app.services.interview_engine import InterviewEngine
from app.models.feedback_report import KnowledgeGapModel


def test_score_calculator_weights_loading_and_calculation():
    """Verifies ScoreCalculator loads external score_weights.json and computes weighted scores."""
    turn_answers = [
        {
            "question_id": "q1",
            "topic_id": "top_react_19",
            "evaluation": {
                "score": 90,
                "confidence_score": 88,
                "rubric": {
                    "technical_accuracy": 95,
                    "concept_coverage": 90,
                    "terminology": 90,
                    "reasoning": 85,
                    "examples": 80,
                    "completeness": 90,
                },
                "metrics": {"communication_clarity": 90},
            },
        }
    ]

    overall = ScoreCalculator.calculate_overall_score(turn_answers)
    assert overall.overall_score > 80.0
    assert overall.grade in ["A+", "A"]
    assert len(overall.breakdown) == 7

    # Verify category weight sum equals 1.0
    total_weight = sum(cat.weight for cat in overall.breakdown)
    assert round(total_weight, 2) == 1.0


def test_summary_generator_format():
    """Verifies SummaryGenerator produces narrative summary and performance highlights."""
    turn_answers = [{"evaluation": {"score": 85}}]
    overall = ScoreCalculator.calculate_overall_score(turn_answers)

    summary = SummaryGenerator.generate_summary(overall, turn_answers, candidate_name="Alex Mercer")
    assert "Alex Mercer" in summary.overall_performance
    assert len(summary.interview_highlights) >= 1
    assert len(summary.areas_for_improvement) >= 1


def test_recommendation_engine_curriculum_mapping():
    """Verifies RecommendationEngine maps knowledge gaps to curriculum days and objectives."""
    rec_engine = RecommendationEngine()
    gap = KnowledgeGapModel(
        topic_id="top_fastapi_core",
        topic_title="FastAPI ASGI & OpenAPI Specs",
        day_number=1,
        description="Lacks understanding of ASGI loop.",
        severity="High",
    )

    recs = rec_engine.generate_recommendations([gap], overall_score=65.0)
    assert len(recs) == 1
    assert recs[0].curriculum_day == 1
    assert "Day 1" in recs[0].recommended_action


def test_feedback_engine_end_to_end_completion():
    """Integration test: verifies InterviewEngine generates feedback_report on Question 8 completion."""
    engine = InterviewEngine()
    start_resp = engine.start_interview(candidate_id="cand_feedback_test", session_id="sess_feedback_test")
    assert start_resp.session_id == "sess_feedback_test"

    # Answer Questions 1 to 7
    for i in range(7):
        resp = engine.submit_answer("sess_feedback_test", f"Candidate technical answer {i + 1}")
        assert resp.done is False
        assert resp.feedback_report is None

    # Answer Question 8 (final question)
    final_resp = engine.submit_answer("sess_feedback_test", "Final answer 8 with React and FastAPI details")
    assert final_resp.done is True
    assert final_resp.feedback_report is not None
    assert final_resp.feedback_report.session_id == "sess_feedback_test"
    assert final_resp.feedback_report.overall_score.overall_score > 0.0
    assert len(final_resp.feedback_report.overall_score.breakdown) == 7
    assert final_resp.feedback_report.summary.overall_performance is not None
