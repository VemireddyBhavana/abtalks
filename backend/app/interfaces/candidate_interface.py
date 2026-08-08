from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.candidate import (
    CandidateModel,
    LearningSignalModel,
    RecentActivityModel,
    CandidateSummaryModel,
)


class AbstractCandidateService(ABC):
    """Abstract Interface contract for Candidate Intelligence Service."""

    @abstractmethod
    def load_candidate(self, file_path: str) -> CandidateModel:
        pass

    @abstractmethod
    def get_candidate(self) -> CandidateModel:
        pass

    @abstractmethod
    def get_completed_days(self) -> List[int]:
        pass

    @abstractmethod
    def get_incomplete_days(self) -> List[int]:
        pass

    @abstractmethod
    def get_progress_percentage(self) -> float:
        pass

    @abstractmethod
    def get_completed_topics(self) -> List[str]:
        pass

    @abstractmethod
    def get_skipped_topics(self) -> List[str]:
        pass

    @abstractmethod
    def get_learning_signals(self) -> List[LearningSignalModel]:
        pass

    @abstractmethod
    def get_recent_activity(self) -> List[RecentActivityModel]:
        pass

    @abstractmethod
    def get_candidate_summary(self) -> CandidateSummaryModel:
        pass

    @abstractmethod
    def get_completion_rate(self) -> float:
        pass

    @abstractmethod
    def get_total_completed_days(self) -> int:
        pass

    @abstractmethod
    def get_total_remaining_days(self) -> int:
        pass

    @abstractmethod
    def get_strongest_topics(self) -> List[LearningSignalModel]:
        pass

    @abstractmethod
    def get_weakest_topics(self) -> List[LearningSignalModel]:
        pass
