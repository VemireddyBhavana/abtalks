from typing import Dict, Any
from app.memory.memory_models import InterviewMemory
from app.core.logging_config import logger


class MemoryMigrationManager:
    """
    Manages schema version migrations for backward/forward compatibility of stored memory payloads.
    """

    CURRENT_SCHEMA_VERSION = "1.0.0"

    @classmethod
    def migrate_if_needed(cls, payload: Dict[str, Any]) -> Dict[str, Any]:
        version = payload.get("schema_version", "0.9.0")
        if version != cls.CURRENT_SCHEMA_VERSION:
            logger.info(f"Migration executed: Upgrading memory schema payload from version {version} to {cls.CURRENT_SCHEMA_VERSION}.")
            payload["schema_version"] = cls.CURRENT_SCHEMA_VERSION
        return payload
