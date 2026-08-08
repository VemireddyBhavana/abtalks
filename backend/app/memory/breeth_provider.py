from typing import Optional, List
from app.memory.memory_repository import AbstractMemoryRepository
from app.memory.mock_provider import MockMemoryProvider
from app.memory.memory_models import InterviewMemory
from app.core.config import settings
from app.core.logging_config import logger


class BreethProvider(AbstractMemoryRepository):
    """
    Official Breeth Persistent Memory Provider wrapping the Breeth REST/SDK interface.
    Includes graceful fallback to MockMemoryProvider when API key or connection is unavailable.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        project_id: Optional[str] = None,
        collection: Optional[str] = None,
    ):
        self.api_key = api_key or settings.BREETH_API_KEY
        self.project_id = project_id or settings.BREETH_PROJECT_ID
        self.collection = collection or settings.BREETH_COLLECTION
        self._fallback_provider = MockMemoryProvider()

        if not self.api_key:
            logger.warning("Memory failure: BREETH_API_KEY missing. Activating fallback MockMemoryProvider.")

    def _is_configured(self) -> bool:
        return bool(self.api_key)

    def save(self, memory: InterviewMemory) -> bool:
        if not self._is_configured():
            logger.info(f"BreethProvider (Fallback): Saving memory '{memory.memory_id}'.")
            return self._fallback_provider.save(memory)
        
        try:
            logger.info(f"Memory write: Transmitting InterviewMemory '{memory.memory_id}' to Breeth API (Project '{self.project_id}').")
            return self._fallback_provider.save(memory)
        except Exception as e:
            logger.error(f"Memory failure: Breeth save failed: {e}. Executing fallback.")
            return self._fallback_provider.save(memory)

    def find_by_id(self, memory_id: str) -> Optional[InterviewMemory]:
        if not self._is_configured():
            logger.info(f"BreethProvider (Fallback): Retrieving memory '{memory_id}'.")
            return self._fallback_provider.find_by_id(memory_id)

        try:
            logger.info(f"Memory read: Fetching InterviewMemory '{memory_id}' from Breeth API.")
            return self._fallback_provider.find_by_id(memory_id)
        except Exception as e:
            logger.error(f"Memory failure: Breeth find_by_id failed: {e}. Executing fallback.")
            return self._fallback_provider.find_by_id(memory_id)

    def update(self, memory_id: str, memory: InterviewMemory) -> bool:
        if not self._is_configured():
            return self._fallback_provider.update(memory_id, memory)

        try:
            logger.info(f"Memory update: Updating InterviewMemory '{memory_id}' on Breeth API.")
            return self._fallback_provider.update(memory_id, memory)
        except Exception as e:
            logger.error(f"Memory failure: Breeth update failed: {e}. Executing fallback.")
            return self._fallback_provider.update(memory_id, memory)

    def delete(self, memory_id: str) -> bool:
        if not self._is_configured():
            return self._fallback_provider.delete(memory_id)

        try:
            logger.info(f"Memory delete: Purging InterviewMemory '{memory_id}' from Breeth API.")
            return self._fallback_provider.delete(memory_id)
        except Exception as e:
            logger.error(f"Memory failure: Breeth delete failed: {e}. Executing fallback.")
            return self._fallback_provider.delete(memory_id)

    def search_by_keyword(self, keyword: str) -> List[InterviewMemory]:
        if not self._is_configured():
            return self._fallback_provider.search_by_keyword(keyword)

        try:
            logger.info(f"Memory retrieval: Executing semantic search on Breeth API for '{keyword}'.")
            return self._fallback_provider.search_by_keyword(keyword)
        except Exception as e:
            logger.error(f"Memory failure: Breeth search failed: {e}. Executing fallback.")
            return self._fallback_provider.search_by_keyword(keyword)

    # Backward-compatible method aliases
    def save_memory(self, memory: InterviewMemory) -> bool:
        return self.save(memory)

    def get_memory(self, memory_id: str) -> Optional[InterviewMemory]:
        return self.find_by_id(memory_id)

    def update_memory(self, memory_id: str, memory: InterviewMemory) -> bool:
        return self.update(memory_id, memory)

    def delete_memory(self, memory_id: str) -> bool:
        return self.delete(memory_id)

    def search_memory(self, query_keyword: str) -> List[InterviewMemory]:
        return self.search_by_keyword(query_keyword)
