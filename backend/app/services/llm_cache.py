from typing import Dict, Optional
from app.models.interview_engine import QuestionPlaceholderModel
from app.core.logging_config import logger


class LLMCache:
    """
    Caches LLM-generated questions during the interview session to prevent duplicate API requests
    for identical prompt signatures.
    """

    def __init__(self):
        self._cache: Dict[str, QuestionPlaceholderModel] = {}

    def get(self, signature: str) -> Optional[QuestionPlaceholderModel]:
        """Retrieves cached question by signature."""
        if signature in self._cache:
            logger.info(f"LLMCache Hit: Retrieved cached question for signature '{signature}'.")
            return self._cache[signature]
        return None

    def put(self, signature: str, question: QuestionPlaceholderModel) -> None:
        """Stores question in cache under signature."""
        self._cache[signature] = question
        logger.info(f"LLMCache Put: Stored question in cache for signature '{signature}'.")

    def clear(self) -> None:
        self._cache.clear()


# Singleton instance
_llm_cache_instance = LLMCache()


def get_llm_cache() -> LLMCache:
    return _llm_cache_instance
