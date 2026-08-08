import pytest
from app.services.answer_classifier import AnswerClassifier
from app.services.rubric_engine import RubricEngine
from app.services.confidence_analyzer import ConfidenceAnalyzer
from app.services.answer_evaluator import AnswerEvaluator
from app.services.followup_engine import FollowUpEngine
from app.services.interview_engine import InterviewEngine
from app.services.adaptive_difficulty_manager import AdaptiveDifficultyManager
from app.services.knowledge_gap_detector import KnowledgeGapDetector
from app.services.keyword_extractor import KeywordExtractor
from app.services.evaluation_history import EvaluationHistory
from app.services.hallucination_guard import HallucinationGuard
from app.services.blooms_taxonomy import BloomsTaxonomyManager
from app.services.evaluation_metrics import EvaluationMetricsTracker
from app.strategies.evaluation.rule_based_evaluation_strategy import RuleBasedEvaluationStrategy
from app.strategies.evaluation.llm_evaluation_strategy import LLMEvaluationStrategy
from app.strategies.followup.deep_dive_strategy import DeepDiveStrategy
from app.strategies.followup.clarification_strategy import ClarificationStrategy
from app.models.curriculum import TopicModel
from app.models.interview_engine import QuestionPlaceholderModel


def test_answer_classifier_tiers():
    """Verifies AnswerClassifier score mappings."""
    assert AnswerClassifier.classify_score(95, "Valid long answer") == AnswerClassifier.EXCELLENT
    assert AnswerClassifier.classify_score(80, "Valid long answer") == AnswerClassifier.GOOD
    assert AnswerClassifier.classify_score(65, "Valid long answer") == AnswerClassifier.AVERAGE
    assert AnswerClassifier.classify_score(45, "Valid long answer") == AnswerClassifier.WEAK
    assert AnswerClassifier.classify_score(20, "Valid long answer") == AnswerClassifier.INCORRECT
    assert AnswerClassifier.classify_score(80, "") == AnswerClassifier.UNCLEAR


def test_rubric_engine_weighted_scoring():
    """Verifies RubricEngine weighted score calculations."""
    rubric = RubricEngine.evaluate_rubric(
        accuracy=100,
        coverage=100,
        terminology=100,
        reasoning=100,
        examples=100,
        completeness=100,
    )
    assert rubric.weighted_total_score == 100.0


def test_confidence_analyzer_metrics():
    """Verifies ConfidenceAnalyzer metrics computation."""
    metrics = ConfidenceAnalyzer.analyze_confidence("Detailed technical response because of architecture.", 85)
    assert metrics.confidence >= 50
    assert metrics.technical_depth >= 50


def test_evaluation_strategies():
    """Verifies Evaluation Strategy Pattern (LLMEvaluationStrategy and RuleBasedEvaluationStrategy)."""
    llm_evaluator = AnswerEvaluator(strategy=LLMEvaluationStrategy())
    res1 = llm_evaluator.evaluate_answer("React 19 Server Components render on server", "Q text", "React 19")
    assert res1.score >= 70

    rule_evaluator = AnswerEvaluator(strategy=RuleBasedEvaluationStrategy())
    res2 = rule_evaluator.evaluate_answer("Short answer", "Q text", "React 19")
    assert res2.score == 50


def test_adaptive_difficulty_manager():
    """Verifies AdaptiveDifficultyManager progression."""
    mgr = AdaptiveDifficultyManager(initial_difficulty="Intermediate")
    mgr.update_difficulty(AnswerClassifier.EXCELLENT)
    new_diff = mgr.update_difficulty(AnswerClassifier.EXCELLENT)
    assert new_diff == "Advanced"

    demoted = mgr.update_difficulty(AnswerClassifier.INCORRECT)
    assert demoted == "Intermediate"


def test_knowledge_gap_detector():
    """Verifies KnowledgeGapDetector identifies missing concepts."""
    evaluator = AnswerEvaluator()
    weak_eval = evaluator.evaluate_answer("Idk", "Q text", "MCP Tools")
    gaps = KnowledgeGapDetector.detect_gaps(weak_eval, "MCP Tools", ["Learn MCP Schema"])
    assert len(gaps["detected_gaps"]) >= 1
    assert len(gaps["review_recommendations"]) == 1


def test_keyword_extractor():
    """Verifies KeywordExtractor extracts tech stack terms."""
    kw = KeywordExtractor.extract_keywords("We built a FastAPI backend microservice using Pydantic schemas and Axios.")
    assert "fastapi" in kw
    assert "pydantic" in kw
    assert "axios" in kw


def test_hallucination_guard():
    """Verifies HallucinationGuard score clamping."""
    evaluator = AnswerEvaluator()
    report = evaluator.evaluate_answer("Answer", "Q", "Topic")
    report.score = 150  # Simulate corrupted LLM output
    sanitized = HallucinationGuard.sanitize_and_validate(report)
    assert sanitized.score == 100


def test_blooms_taxonomy():
    """Verifies BloomsTaxonomyManager cognitive level mapping."""
    assert BloomsTaxonomyManager.get_cognitive_level(95) == "Create"
    assert BloomsTaxonomyManager.get_cognitive_level(90) == "Evaluate"
    assert BloomsTaxonomyManager.get_cognitive_level(80) == "Analyze"
    assert BloomsTaxonomyManager.get_cognitive_level(70) == "Apply"
    assert BloomsTaxonomyManager.get_cognitive_level(50) == "Understand"
    assert BloomsTaxonomyManager.get_cognitive_level(20) == "Remember"


def test_evaluation_history_and_metrics():
    """Verifies EvaluationHistory and EvaluationMetricsTracker."""
    history = EvaluationHistory(session_id="sess_hist")
    evaluator = AnswerEvaluator()
    dummy_q = QuestionPlaceholderModel(id="q1", day_number=1, topic_id="t1", topic_title="Title", question_text="Q", difficulty="Intermediate")
    dummy_topic = TopicModel(id="t1", title="Title", category="Gen")

    eval_report = evaluator.evaluate_answer("Answer", "Q", "Title")
    decision = FollowUpEngine.generate_followup(eval_report, dummy_q, dummy_topic, "Answer", 1)

    history.record_turn("q1", "t1", eval_report, decision, "Intermediate")
    assert history.get_turn_count() == 1
    assert history.get_average_score() > 0.0

    metrics = EvaluationMetricsTracker.compute_summary_metrics(history)
    assert metrics["total_turns"] == 1
    assert metrics["average_score"] > 0.0
