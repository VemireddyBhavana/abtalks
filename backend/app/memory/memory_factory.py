from typing import Optional
from app.memory.memory_provider import AbstractMemoryProvider
from app.memory.mock_provider import MockMemoryProvider
from app.memory.breeth_provider import BreethProvider
from app.core.config import settings
from app.core.logging_config import logger


class MemoryFactory:
    """
    Factory class for instantiating persistent memory providers based on configuration.
    """

    @classmethod
    def create_provider(cls, provider_type: Optional[str] = None) -> AbstractMemoryProvider:
        provider = (provider_type or settings.MEMORY_PROVIDER).lower()

        if provider == "breeth":
            logger.info("Memory initialized: Instantiating BreethProvider.")
            return BreethProvider()
        elif provider == "mock":
            logger.info("Memory initialized: Instantiating MockMemoryProvider.")
            return MockMemoryProvider()
        else:
            logger.warning(f"Unknown memory provider '{provider}'. Falling back to MockMemoryProvider.")
            return MockMemoryProvider()
