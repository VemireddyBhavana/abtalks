import time
from typing import Optional, List
from app.models.candidate import CandidateModel
from app.models.curriculum import TopicModel, DayModel
from app.models.interview_engine import QuestionPlaceholderModel
from app.providers.model_provider import AbstractModelProvider, LLMProviderFactory
from app.services.prompt_builder import PromptBuilder
from app.services.response_parser import ResponseParser
from app.services.response_validator import ResponseValidator
from app.services.safety_filter import SafetyFilter
from app.services.retry_manager import RetryManager
from app.services.token_tracker import get_token_tracker, TokenTracker
from app.services.llm_metrics import get_llm_metrics, LLMMetricsTracker
from app.services.llm_cache import get_llm_cache, LLMCache
from app.core.logging_config import logger


class LLMService:
    """
    Enterprise LLM Question Generator Service.
    Coordinates PromptBuilder, ModelProvider, ResponseParser, ResponseValidator, SafetyFilter,
    RetryManager, TokenTracker, LLMCache, and LLMMetricsTracker.
    """

    def __init__(
        self,
        provider: Optional[AbstractModelProvider] = None,
        token_tracker: Optional[TokenTracker] = None,
        metrics_tracker: Optional[LLMMetricsTracker] = None,
        cache: Optional[LLMCache] = None,
    ):
        self.provider = provider or LLMProviderFactory.get_provider()
        self.token_tracker = token_tracker or get_token_tracker()
        self.metrics_tracker = metrics_tracker or get_llm_metrics()
        self.cache = cache or get_llm_cache()

    def generate_question(
        self,
        candidate: CandidateModel,
        topic: TopicModel,
        day: Optional[DayModel],
        question_id: str,
        difficulty: str = "Intermediate",
        asked_questions: Optional[List[str]] = None,
        session_id: str = "default_session",
    ) -> QuestionPlaceholderModel:
        """
        Generates a single technically accurate interview question.
        Uses LLMCache for deduplication and RetryManager for resilience.
        """
        cache_key = f"{session_id}_{topic.id}_{difficulty}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        prompt = PromptBuilder.build_question_generation_prompt(
            candidate=candidate,
            topic=topic,
            day=day,
            difficulty=difficulty,
            asked_questions=asked_questions,
            session_id=session_id,
        )

        start_time = time.time()

        def _call_provider():
            logger.info(f"API Request: Transmitting prompt to LLM provider '{type(self.provider).__name__}'.")
            return self.provider.generate(prompt)

        try:
            raw_text = RetryManager.execute_with_retry(_call_provider, max_retries=2)
            duration = time.time() - start_time
            logger.info(f"API Response: Received completion in {duration:.3f}s.")

            # Record token metrics
            self.token_tracker.record_usage(prompt, raw_text)

            # Safety filter check
            sanitized_text = SafetyFilter.filter_question_text(raw_text)

            # Response parsing
            question_model = ResponseParser.parse_question_response(
                raw_response=sanitized_text,
                topic=topic,
                day_number=day.day_number if day else 1,
                question_id=question_id,
                fallback_difficulty=difficulty,
            )

            # Response validation
            ResponseValidator.validate_question(
                question=question_model,
                topic_title=topic.title,
                asked_questions=asked_questions,
            )

            self.metrics_tracker.record_success(duration)
            self.cache.put(cache_key, question_model)
            return question_model

        except Exception as exc:
            self.metrics_tracker.record_failure()
            logger.error(f"Generation Failed: LLMService question generation error: {str(exc)}")
            raise exc


# Singleton helper
_llm_service_instance: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    global _llm_service_instance
    if _llm_service_instance is None:
        _llm_service_instance = LLMService()
    return _llm_service_instance
