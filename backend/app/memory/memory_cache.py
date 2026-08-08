from typing import Optional, Dict
from app.memory.memory_models import InterviewMemory
from app.core.logging_config import logger


class MemoryCache:
    """
    In-memory cache for InterviewMemory documents to eliminate redundant external reads.
    """

    def __init__(self, max_entries: int = 100):
        self.max_entries = max_entries
        self._cache: Dict[str, InterviewMemory] = {}

    def get(self, memory_id: str) -> Optional[InterviewMemory]:
        if memory_id in self._cache:
            logger.info(f"Cache hit: Retrieved InterviewMemory '{memory_id}' from MemoryCache.")
            return self._cache[memory_id]
        logger.info(f"Cache miss: InterviewMemory '{memory_id}' not found in MemoryCache.")
        return None

    def put(self, memory_id: str, memory: InterviewMemory) -> None:
        if len(self._cache) >= self.max_entries:
            # Evict oldest entry
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        self._cache[memory_id] = memory
        logger.info(f"MemoryCache put: Cached InterviewMemory '{memory_id}'.")

    def invalidate(self, memory_id: str) -> None:
        if memory_id in self._cache:
            del self._cache[memory_id]
            logger.info(f"MemoryCache invalidate: Evicted InterviewMemory '{memory_id}'.")

    def clear(self) -> None:
        self._cache.clear()
