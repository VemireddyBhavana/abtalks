from typing import Any, Callable, Dict, Optional
from app.core.logging_config import logger


class InMemoryCacheManager:
    """
    Centralized In-Memory Cache Manager for intelligence layer services.
    Supports lazy loading, atomic cache retrieval, cache refresh, and status inspection.
    """

    _instance: Optional["InMemoryCacheManager"] = None

    def __init__(self):
        self._store: Dict[str, Any] = {}

    @classmethod
    def get_instance(cls) -> "InMemoryCacheManager":
        if cls._instance is None:
            cls._instance = InMemoryCacheManager()
        return cls._instance

    def load(self, key: str, loader_fn: Callable[[], Any]) -> Any:
        """
        Loads data using loader_fn if key is absent from cache, stores it, and returns the result.
        """
        if key not in self._store:
            data = loader_fn()
            self._store[key] = data
            logger.info(f"Cache Created: Populated cache for key '{key}'.")
        return self._store[key]

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieves cached data for key, returning None if absent.
        """
        return self._store.get(key)

    def refresh(self, key: str, loader_fn: Callable[[], Any]) -> Any:
        """
        Forces re-execution of loader_fn, updates cache store, and logs event.
        """
        data = loader_fn()
        self._store[key] = data
        logger.info(f"Cache Refreshed: Updated cache for key '{key}'.")
        return data

    def clear(self, key: Optional[str] = None) -> None:
        """
        Clears a specific cache key or resets entire cache store.
        """
        if key:
            if key in self._store:
                del self._store[key]
                logger.info(f"Cache cleared for key '{key}'.")
        else:
            self._store.clear()
            logger.info("Cache cleared for all keys.")

    def is_ready(self, key: Optional[str] = None) -> bool:
        """
        Returns True if a specific key (or any key) exists in cache store.
        """
        if key:
            return key in self._store and self._store[key] is not None
        return len(self._store) > 0


# Singleton provider helper
def get_cache_manager() -> InMemoryCacheManager:
    return InMemoryCacheManager.get_instance()
