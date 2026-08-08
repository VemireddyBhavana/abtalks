from abc import ABC, abstractmethod
from typing import Optional, List
from app.memory.memory_models import InterviewMemory


class AbstractMemoryRepository(ABC):
    """
    Abstract Repository Interface for all persistent memory providers (Breeth, Mock, Redis, Postgres, etc.).
    """

    @abstractmethod
    def save(self, memory: InterviewMemory) -> bool:
        """Saves a new InterviewMemory document."""
        pass

    @abstractmethod
    def find_by_id(self, memory_id: str) -> Optional[InterviewMemory]:
        """Finds an InterviewMemory document by unique ID."""
        pass

    @abstractmethod
    def update(self, memory_id: str, memory: InterviewMemory) -> bool:
        """Updates an existing InterviewMemory document."""
        pass

    @abstractmethod
    def delete(self, memory_id: str) -> bool:
        """Deletes an InterviewMemory document by ID."""
        pass

    @abstractmethod
    def search_by_keyword(self, keyword: str) -> List[InterviewMemory]:
        """Searches memory documents matching keyword."""
        pass
