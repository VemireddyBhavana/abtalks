from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.curriculum import CurriculumModel, ModuleModel, DayModel, TopicModel


class AbstractCurriculumService(ABC):
    """Abstract Interface contract for Curriculum Intelligence Service."""

    @abstractmethod
    def load_curriculum(self, file_path: str) -> CurriculumModel:
        pass

    @abstractmethod
    def get_all_modules(self) -> List[ModuleModel]:
        pass

    @abstractmethod
    def get_module(self, module_id: str) -> Optional[ModuleModel]:
        pass

    @abstractmethod
    def get_all_days(self) -> List[DayModel]:
        pass

    @abstractmethod
    def get_day(self, day_number: int) -> Optional[DayModel]:
        pass

    @abstractmethod
    def get_topics_by_day(self, day_number: int) -> List[TopicModel]:
        pass

    @abstractmethod
    def get_learning_objectives(self, day_number: int) -> List[str]:
        pass

    @abstractmethod
    def get_tools_used(self, day_number: int) -> List[str]:
        pass

    @abstractmethod
    def get_days_by_module(self, module_id: str) -> List[DayModel]:
        pass

    @abstractmethod
    def search_topic(self, keyword: str) -> List[TopicModel]:
        pass

    @abstractmethod
    def search_learning_objective(self, keyword: str) -> List[str]:
        pass

    @abstractmethod
    def search_tool(self, tool_name: str) -> List[str]:
        pass

    @abstractmethod
    def get_days_using_tool(self, tool_name: str) -> List[DayModel]:
        pass
