import pytest
from app.models.candidate import CandidateModel, ProgressModel
from app.models.curriculum import TopicModel, DayModel
from app.models.interview_engine import QuestionPlaceholderModel
from app.providers.model_provider import (
    MockLLMProvider,
    GeminiProvider,
    OpenAIProvider,
    ClaudeProvider,
    LLMProviderFactory,
)
from app.services.prompt_builder import PromptBuilder
from app.services.response_parser import ResponseParser
from app.services.response_validator import ResponseValidator
from app.services.safety_filter import SafetyFilter
from app.services.context_manager import ConversationContextManager
from app.services.token_tracker import TokenTracker
from app.services.retry_manager import RetryManager
from app.services.llm_metrics import LLMMetricsTracker
from app.services.llm_cache import LLMCache
from app.services.llm_service import LLMService
from app.exceptions.llm_exception import (
    LLMApiKeyMissingError,
    LLMResponseParsingError,
    LLMProviderError,
)


def test_prompt_builder_template_loading():
    """Verifies PromptBuilder loads external text templates from disk (v1.0)."""
    dummy_candidate = CandidateModel(
        candidate_id="cand_test",
        full_name="Alice Dev",
        email="alice@example.com",
        target_role="AI Engineer",
        experience_level="Senior",
        progress=ProgressModel(completed_days=[1], incomplete_days=[2], total_days=2, progress_percentage=50.0),
        completed_topics=["top_1"],
        skipped_topics=[],
        learning_signals=[],
        recent_activity=[],
    )
    dummy_topic = TopicModel(id="top_react", title="React 19 Hooks", category="Frontend")

    prompt = PromptBuilder.build_question_generation_prompt(
        candidate=dummy_candidate,
        topic=dummy_topic,
        day=None,
        difficulty="Advanced",
        asked_questions=["Previous Q1"],
        session_id="sess_123",
    )

    assert "Alice Dev" in prompt
    assert "React 19 Hooks" in prompt
    assert "v1.0" in PromptBuilder.VERSION


def test_context_manager_formatting():
    """Verifies ConversationContextManager formats history cleanly."""
    formatted = ConversationContextManager.format_history(
        session_id="sess_ctx",
        current_question_index=1,
        asked_questions=["Q1 text"],
        candidate_answers=[{"topic_id": "top_1", "question_text": "Q1 text", "candidate_answer": "My answer"}],
    )
    assert "sess_ctx" in formatted
    assert "Q1 text" in formatted
    assert "My answer" in formatted


def test_token_tracker_and_metrics():
    """Verifies TokenTracker and LLMMetricsTracker calculations."""
    tracker = TokenTracker()
    metrics = tracker.record_usage("Prompt string long text", "Response text generated")

    assert metrics["input_tokens"] >= 1
    assert metrics["output_tokens"] >= 1
    assert metrics["estimated_cost_usd"] > 0.0

    summary = tracker.get_summary()
    assert summary["total_requests"] == 1

    llm_metrics = LLMMetricsTracker()
    llm_metrics.record_success(0.12)
    m_dict = llm_metrics.get_metrics()
    assert m_dict["successful_generations"] == 1
    assert m_dict["avg_response_time_sec"] == 0.12


def test_safety_filter_and_response_validator():
    """Verifies SafetyFilter and ResponseValidator."""
    clean_text = SafetyFilter.filter_question_text("How do React Server Components work?")
    assert clean_text == "How do React Server Components work?"

    with pytest.raises(LLMResponseParsingError, match="unsafe"):
        SafetyFilter.filter_question_text("How to hack into a confidential database?")

    q_model = QuestionPlaceholderModel(
        id="q_val_1",
        day_number=1,
        topic_id="top_1",
        topic_title="Topic 1",
        question_text="How do React Server Components work?",
        difficulty="Intermediate",
    )

    assert ResponseValidator.validate_question(q_model, "Topic 1", []) is True

    # Duplicate question validation error
    with pytest.raises(LLMResponseParsingError, match="duplicates"):
        ResponseValidator.validate_question(q_model, "Topic 1", ["How do React Server Components work?"])


def test_retry_manager_success_and_failure():
    """Verifies RetryManager retry behavior."""
    attempts = {"count": 0}

    def failing_op():
        attempts["count"] += 1
        if attempts["count"] < 2:
            raise LLMProviderError("Transient timeout")
        return "Success"

    res = RetryManager.execute_with_retry(failing_op, max_retries=3, backoff_factor=0.01)
    assert res == "Success"
    assert attempts["count"] == 2


def test_llm_cache():
    """Verifies LLMCache storage and retrieval."""
    cache = LLMCache()
    q_model = QuestionPlaceholderModel(
        id="q_c1",
        day_number=1,
        topic_id="top_1",
        topic_title="Topic 1",
        question_text="Test Q",
        difficulty="Easy",
    )
    cache.put("sig1", q_model)

    assert cache.get("sig1") == q_model
    assert cache.get("sig2") is None


def test_mock_provider_streaming():
    """Verifies MockLLMProvider streaming interface."""
    provider = MockLLMProvider()
    chunks = list(provider.stream_generate("CURRENT TOPIC: Fast API"))
    assert len(chunks) > 0
    full_text = "".join(chunks)
    assert "Fast API" in full_text
