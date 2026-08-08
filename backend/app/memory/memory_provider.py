from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from app.memory.memory_models import InterviewMemory


class AbstractMemoryProvider(ABC):
    """Abstract interface contract for persistent Memory Providers (Breeth, Mock, etc.)."""

    @abstractmethod
    def save_memory(self, memory: InterviewMemory) -> bool:
        """Saves a new or updated InterviewMemory document."""
        pass

    @abstractmethod
    def get_memory(self, memory_id: str) -> Optional[InterviewMemory]:
        """Retrieves an InterviewMemory document by ID."""
        pass

    @abstractmethod
    def update_memory(self, memory_id: str, memory: InterviewMemory) -> bool:
        """Updates an existing InterviewMemory document."""
        pass

    @abstractmethod
    def delete_memory(self, memory_id: str) -> bool:
        """Deletes an InterviewMemory document by ID."""
        pass

    @abstractmethod
    def search_memory(self, query_keyword: str) -> List[InterviewMemory]:
        """Searches memory documents matching keyword query."""
        pass
