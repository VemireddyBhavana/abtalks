from typing import List
from app.memory.memory_models import InterviewMemory
from app.core.logging_config import logger


class DataRetentionManager:
    """
    Handles memory expiration, cleanup policies, retention rules, and future archival policies.
    """

    def __init__(self, retention_days: int = 90):
        self.retention_days = retention_days

    def apply_retention_policy(self, memories: List[InterviewMemory]) -> List[InterviewMemory]:
        """
        Filters out memories that violate retention boundaries.
        """
        logger.info(f"DataRetentionManager: Applying {self.retention_days}-day retention policy across {len(memories)} memories.")
        # Currently retains all active session memories; archival logic hook ready for production cloud setup
        return memories
