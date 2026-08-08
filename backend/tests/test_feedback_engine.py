import pytest
from app.services.score_calculator import ScoreCalculator
from app.services.summary_generator import SummaryGenerator
from app.services.recommendation_engine import RecommendationEngine
from app.services.report_generator import ReportGenerator
from app.services.feedback_engine import FeedbackEngine
from app.services.interview_engine import InterviewEngine
from app.services.strength_analyzer import StrengthAnalyzer
from app.services.weakness_analyzer import WeaknessAnalyzer
from app.services.curriculum_coverage import CurriculumCoverageAnalyzer
from app.services.recommendation_priority import RecommendationPriorityEngine
from app.services.performance_trend import PerformanceTrendAnalyzer
from app.services.report_validator import ReportValidator
from app.services.feedback_metrics import get_feedback_metrics
from app.strategies.feedback.technical_feedback_strategy import TechnicalFeedbackStrategy
from app.strategies.feedback.behavioral_feedback_strategy import BehavioralFeedbackStrategy
from app.strategies.feedback.summary_feedback_strategy import SummaryFeedbackStrategy
from app.exporters.pdf_exporter import PDFExporterPlaceholder
from app.exporters.markdown_exporter import MarkdownExporterPlaceholder
from app.exporters.html_exporter import HTMLExporterPlaceholder
from app.models.feedback_report import KnowledgeGapModel, RecommendationModel


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


def test_analyzers_and_priority_engine():
    """Verifies StrengthAnalyzer, WeaknessAnalyzer, and RecommendationPriorityEngine."""
    turn_answers = [
        {
            "evaluation": {
                "score": 90,
                "strengths": ["Solid React 19 knowledge"],
                "weaknesses": [],
                "gaps": [],
            }
        },
        {
            "evaluation": {
                "score": 45,
                "strengths": [],
                "weaknesses": ["Incomplete ASGI loop"],
                "gaps": ["Missing FastAPI OpenAPI concept"],
            }
        },
    ]

    strengths = StrengthAnalyzer.analyze_strengths(turn_answers)
    assert len(strengths) >= 1
    assert "Solid React 19 knowledge" in strengths

    weaknesses = WeaknessAnalyzer.analyze_weaknesses(turn_answers)
    assert len(weaknesses) >= 1
    assert "Incomplete ASGI loop" in weaknesses

    rec = RecommendationModel(
        topic_title="FastAPI ASGI",
        curriculum_day=1,
        learning_objectives=["Build ASGI microservices"],
        recommended_action="Study Day 1",
        priority="Medium",
    )
    prioritized = RecommendationPriorityEngine.prioritize_recommendations([rec], overall_score=45.0)
    assert prioritized[0].priority == "Critical"


def test_performance_trend_and_coverage():
    """Verifies PerformanceTrendAnalyzer and CurriculumCoverageAnalyzer."""
    turn_answers = [
        {"evaluation": {"score": 60, "confidence_score": 65}, "difficulty": "Intermediate"},
        {"evaluation": {"score": 85, "confidence_score": 85}, "difficulty": "Advanced"},
    ]

    trend = PerformanceTrendAnalyzer.analyze_trends(turn_answers)
    assert trend["performance_trajectory"] == "Improving"
    assert trend["score_progression"] == [60, 85]

    coverage_analyzer = CurriculumCoverageAnalyzer()
    cov = coverage_analyzer.analyze_coverage(days_covered=[1, 2], topics_covered=["top_1", "top_2"])
    assert cov["distinct_days_covered"] == 2
    assert cov["day_coverage_percentage"] > 0.0


def test_report_validator_and_exporters():
    """Verifies ReportValidator and exporter placeholders."""
    engine = FeedbackEngine()
    # Create minimal session state test
    session_engine = InterviewEngine()
    session_engine.start_interview(candidate_id="cand_exp_test", session_id="sess_exp_test")
    session = session_engine.state_manager.get_session("sess_exp_test")
    
    report = engine.generate_feedback_report(session)
    assert ReportValidator.validate_report(report) is True

    pdf_exporter = PDFExporterPlaceholder()
    assert "sess_exp_test" in pdf_exporter.export(report)

    md_exporter = MarkdownExporterPlaceholder()
    assert "# Interview Feedback Report" in md_exporter.export(report)

    html_exporter = HTMLExporterPlaceholder()
    assert "<html>" in html_exporter.export(report)


def test_feedback_strategies():
    """Verifies Feedback Strategy Pattern (Technical, Behavioral, Summary)."""
    tech_engine = FeedbackEngine(strategy=TechnicalFeedbackStrategy())
    beh_engine = FeedbackEngine(strategy=BehavioralFeedbackStrategy())
    sum_engine = FeedbackEngine(strategy=SummaryFeedbackStrategy())

    session_engine = InterviewEngine()
    session_engine.start_interview(candidate_id="cand_strat_test", session_id="sess_strat_test")
    session = session_engine.state_manager.get_session("sess_strat_test")

    report_tech = tech_engine.generate_feedback_report(session)
    assert report_tech.session_id == "sess_strat_test"

    report_beh = beh_engine.generate_feedback_report(session)
    assert report_beh.summary.communication_assessment is not None

    report_sum = sum_engine.generate_feedback_report(session)
    assert report_sum.session_id == "sess_strat_test"


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
