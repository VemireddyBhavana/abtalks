from typing import Optional, List
from app.memory.memory_repository import AbstractMemoryRepository
from app.memory.memory_factory import MemoryFactory
from app.memory.memory_models import InterviewMemory
from app.core.logging_config import logger


class MemoryRepository:
    """
    Repository class decoupling MemoryService from direct provider implementations.
    Communicates with underlying AbstractMemoryRepository providers (Breeth, Mock, etc.).
    """

    def __init__(self, provider: Optional[AbstractMemoryRepository] = None):
        self.provider = provider or MemoryFactory.create_provider()

    def save(self, memory: InterviewMemory) -> bool:
        logger.info(f"Memory saved: Repository storing InterviewMemory '{memory.memory_id}'.")
        return self.provider.save(memory)

    def find_by_id(self, memory_id: str) -> Optional[InterviewMemory]:
        logger.info(f"Memory read: Repository querying InterviewMemory '{memory_id}'.")
        return self.provider.find_by_id(memory_id)

    def update(self, memory_id: str, memory: InterviewMemory) -> bool:
        logger.info(f"Memory updated: Repository updating InterviewMemory '{memory_id}'.")
        return self.provider.update(memory_id, memory)

    def delete(self, memory_id: str) -> bool:
        logger.info(f"Memory deleted: Repository deleting InterviewMemory '{memory_id}'.")
        return self.provider.delete(memory_id)

    def search_by_keyword(self, keyword: str) -> List[InterviewMemory]:
        logger.info(f"Memory search: Repository searching for keyword '{keyword}'.")
        return self.provider.search_by_keyword(keyword)
