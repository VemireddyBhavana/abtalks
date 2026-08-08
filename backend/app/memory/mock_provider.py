from typing import Optional, List, Dict
from app.memory.memory_provider import AbstractMemoryProvider
from app.memory.memory_models import InterviewMemory
from app.core.logging_config import logger


class MockMemoryProvider(AbstractMemoryProvider):
    """
    In-memory persistent repository implementation for offline/test environments.
    """

    def __init__(self):
        self._store: Dict[str, InterviewMemory] = {}

    def save_memory(self, memory: InterviewMemory) -> bool:
        logger.info(f"Memory write: Storing memory '{memory.memory_id}' in MockMemoryProvider.")
        self._store[memory.memory_id] = memory
        return True

    def get_memory(self, memory_id: str) -> Optional[InterviewMemory]:
        logger.info(f"Memory read: Retrieving memory '{memory_id}' from MockMemoryProvider.")
        return self._store.get(memory_id)

    def update_memory(self, memory_id: str, memory: InterviewMemory) -> bool:
        logger.info(f"Memory update: Updating memory '{memory_id}' in MockMemoryProvider.")
        self._store[memory_id] = memory
        return True

    def delete_memory(self, memory_id: str) -> bool:
        if memory_id in self._store:
            logger.info(f"Memory delete: Deleting memory '{memory_id}' from MockMemoryProvider.")
            del self._store[memory_id]
            return True
        return False

    def search_memory(self, query_keyword: str) -> List[InterviewMemory]:
        logger.info(f"Memory retrieval: Searching memory using keyword '{query_keyword}'.")
        query_lower = query_keyword.lower()
        results: List[InterviewMemory] = []
        for mem in self._store.values():
            if (
                query_lower in mem.session.session_id.lower()
                or query_lower in mem.candidate.candidate_id.lower()
                or any(query_lower in t.topic_title.lower() for t in mem.turns)
            ):
                results.append(mem)
        return results
