import json
from typing import List, Optional
from pydantic import ValidationError
from app.interfaces.curriculum_interface import AbstractCurriculumService
from app.models.curriculum import CurriculumModel, ModuleModel, DayModel, TopicModel
from app.core.config import settings
from app.core.logging_config import logger
from app.core.cache import get_cache_manager, InMemoryCacheManager
from app.utils.json_loader import load_json_file
from app.utils.validators import validate_model
from app.exceptions.curriculum_exception import (
    CurriculumNotFoundError,
    CurriculumValidationError,
)


class CurriculumService(AbstractCurriculumService):
    """
    Concrete implementation of Curriculum Intelligence Service.
    Utilizes Centralized InMemoryCacheManager, Pydantic validation, and custom domain exceptions.
    """

    CACHE_KEY = "curriculum_data"

    def __init__(self, data_path: Optional[str] = None):
        self.data_path = data_path or settings.CURRICULUM_PATH
        self.cache_manager: InMemoryCacheManager = get_cache_manager()
        self.load_curriculum(self.data_path)

    def load_curriculum(self, file_path: str) -> CurriculumModel:
        """
        Loads curriculum JSON from disk, validates via CurriculumModel, updates cache, and logs event.
        """
        try:
            raw_data = load_json_file(file_path)
            curriculum = validate_model(CurriculumModel, raw_data)
            self.cache_manager.refresh(self.CACHE_KEY, lambda: curriculum)
            logger.info(f"Curriculum Loaded Successfully: Parsed '{curriculum.title}' ({len(curriculum.days)} days)")
            return curriculum
        except FileNotFoundError as exc:
            logger.error(f"JSON Missing: Curriculum file not found at '{file_path}'")
            raise CurriculumNotFoundError(f"Curriculum JSON missing at path: {file_path}") from exc
        except json.JSONDecodeError as exc:
            logger.error(f"JSON Corrupted: Failed to parse JSON at '{file_path}': {str(exc)}")
            raise CurriculumValidationError(f"Curriculum JSON corrupted: {str(exc)}") from exc
        except ValidationError as exc:
            logger.error(f"Validation Failed: Curriculum schema invalid: {str(exc)}")
            raise CurriculumValidationError(f"Curriculum schema validation failed: {str(exc)}") from exc

    def refresh_cache(self) -> CurriculumModel:
        """
        Forces cache refresh from disk.
        """
        return self.load_curriculum(self.data_path)

    def _get_cache(self) -> CurriculumModel:
        curriculum = self.cache_manager.get(self.CACHE_KEY)
        if curriculum is None:
            curriculum = self.load_curriculum(self.data_path)
        return curriculum

    def get_all_modules(self) -> List[ModuleModel]:
        return self._get_cache().modules

    def get_module(self, module_id: str) -> Optional[ModuleModel]:
        for module in self._get_cache().modules:
            if module.id == module_id:
                return module
        return None

    def get_all_days(self) -> List[DayModel]:
        return self._get_cache().days

    def get_day(self, day_number: int) -> Optional[DayModel]:
        for day in self._get_cache().days:
            if day.day_number == day_number:
                return day
        return None

    def get_topics_by_day(self, day_number: int) -> List[TopicModel]:
        day = self.get_day(day_number)
        return day.topics if day else []

    def get_learning_objectives(self, day_number: int) -> List[str]:
        day = self.get_day(day_number)
        return day.learning_objectives if day else []

    def get_tools_used(self, day_number: int) -> List[str]:
        day = self.get_day(day_number)
        return day.tools_used if day else []

    def get_days_by_module(self, module_id: str) -> List[DayModel]:
        return [day for day in self._get_cache().days if day.module_id == module_id]

    def search_topic(self, keyword: str) -> List[TopicModel]:
        kw = keyword.lower()
        results: List[TopicModel] = []
        for day in self._get_cache().days:
            for topic in day.topics:
                if kw in topic.title.lower() or kw in topic.category.lower() or kw in topic.id.lower():
                    results.append(topic)
        return results

    def search_learning_objective(self, keyword: str) -> List[str]:
        kw = keyword.lower()
        results: List[str] = []
        for day in self._get_cache().days:
            for obj in day.learning_objectives:
                if kw in obj.lower():
                    results.append(obj)
        return results

    def search_tool(self, tool_name: str) -> List[str]:
        kw = tool_name.lower()
        found = set()
        for day in self._get_cache().days:
            for tool in day.tools_used:
                if kw in tool.lower():
                    found.add(tool)
        return sorted(list(found))

    def get_days_using_tool(self, tool_name: str) -> List[DayModel]:
        kw = tool_name.lower()
        matching_days = []
        for day in self._get_cache().days:
            if any(kw in tool.lower() for tool in day.tools_used):
                matching_days.append(day)
        return matching_days


# Singleton instance helper
_curriculum_service_instance: Optional[CurriculumService] = None


def get_curriculum_service() -> CurriculumService:
    global _curriculum_service_instance
    if _curriculum_service_instance is None:
        _curriculum_service_instance = CurriculumService()
    return _curriculum_service_instance
