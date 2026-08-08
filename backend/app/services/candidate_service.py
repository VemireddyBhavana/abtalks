import json
from typing import List, Optional
from pydantic import ValidationError
from app.interfaces.candidate_interface import AbstractCandidateService
from app.models.candidate import (
    CandidateModel,
    LearningSignalModel,
    RecentActivityModel,
    CandidateSummaryModel,
)
from app.core.config import settings
from app.core.logging_config import logger
from app.core.cache import get_cache_manager, InMemoryCacheManager
from app.utils.json_loader import load_json_file
from app.utils.validators import validate_model
from app.exceptions.candidate_exception import (
    CandidateNotFoundError,
    CandidateValidationError,
)


class CandidateService(AbstractCandidateService):
    """
    Concrete implementation of Candidate Intelligence Service.
    Utilizes Centralized InMemoryCacheManager, Pydantic validation, and custom domain exceptions.
    """

    CACHE_KEY = "candidate_data"

    def __init__(self, data_path: Optional[str] = None):
        self.data_path = data_path or settings.CANDIDATE_PATH
        self.cache_manager: InMemoryCacheManager = get_cache_manager()
        self.load_candidate(self.data_path)

    def load_candidate(self, file_path: str) -> CandidateModel:
        """
        Loads candidate JSON from disk, validates via CandidateModel, updates cache, and logs event.
        """
        try:
            raw_data = load_json_file(file_path)
            candidate = validate_model(CandidateModel, raw_data)
            self.cache_manager.refresh(self.CACHE_KEY, lambda: candidate)
            logger.info(f"Candidate Loaded Successfully: Loaded profile for '{candidate.full_name}' ({candidate.candidate_id})")
            return candidate
        except FileNotFoundError as exc:
            logger.error(f"JSON Missing: Candidate file not found at '{file_path}'")
            raise CandidateNotFoundError(f"Candidate JSON missing at path: {file_path}") from exc
        except json.JSONDecodeError as exc:
            logger.error(f"JSON Corrupted: Failed to parse JSON at '{file_path}': {str(exc)}")
            raise CandidateValidationError(f"Candidate JSON corrupted: {str(exc)}") from exc
        except ValidationError as exc:
            logger.error(f"Validation Failed: Candidate schema invalid: {str(exc)}")
            raise CandidateValidationError(f"Candidate schema validation failed: {str(exc)}") from exc

    def refresh_cache(self) -> CandidateModel:
        """
        Forces cache refresh from disk.
        """
        return self.load_candidate(self.data_path)

    def _get_cache(self) -> CandidateModel:
        candidate = self.cache_manager.get(self.CACHE_KEY)
        if candidate is None:
            candidate = self.load_candidate(self.data_path)
        return candidate

    def get_candidate(self) -> CandidateModel:
        return self._get_cache()

    def get_completed_days(self) -> List[int]:
        return self._get_cache().progress.completed_days

    def get_incomplete_days(self) -> List[int]:
        return self._get_cache().progress.incomplete_days

    def get_progress_percentage(self) -> float:
        return self._get_cache().progress.progress_percentage

    def get_completed_topics(self) -> List[str]:
        return self._get_cache().completed_topics

    def get_skipped_topics(self) -> List[str]:
        return self._get_cache().skipped_topics

    def get_learning_signals(self) -> List[LearningSignalModel]:
        return self._get_cache().learning_signals

    def get_recent_activity(self) -> List[RecentActivityModel]:
        return self._get_cache().recent_activity

    def get_candidate_summary(self) -> CandidateSummaryModel:
        cand = self._get_cache()
        return CandidateSummaryModel(
            candidate_id=cand.candidate_id,
            full_name=cand.full_name,
            target_role=cand.target_role,
            progress_percentage=cand.progress.progress_percentage,
            completed_days_count=len(cand.progress.completed_days),
            total_days_count=cand.progress.total_days,
            completed_topics_count=len(cand.completed_topics),
            learning_signals_count=len(cand.learning_signals),
        )

    def get_completion_rate(self) -> float:
        return round(self.get_progress_percentage() / 100.0, 4)

    def get_total_completed_days(self) -> int:
        return len(self.get_completed_days())

    def get_total_remaining_days(self) -> int:
        return len(self.get_incomplete_days())

    def get_strongest_topics(self) -> List[LearningSignalModel]:
        signals = self.get_learning_signals()
        return [s for s in signals if "strength" in s.category.lower() or s.score >= 80]

    def get_weakest_topics(self) -> List[LearningSignalModel]:
        signals = self.get_learning_signals()
        return [s for s in signals if "growth" in s.category.lower() or "weak" in s.category.lower() or s.score < 80]


# Singleton instance helper
_candidate_service_instance: Optional[CandidateService] = None


def get_candidate_service() -> CandidateService:
    global _candidate_service_instance
    if _candidate_service_instance is None:
        _candidate_service_instance = CandidateService()
    return _candidate_service_instance
