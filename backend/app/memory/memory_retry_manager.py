import time
from typing import Callable, Any, Type, Tuple
from app.exceptions.memory_exception import MemoryError, MemoryRetryExhaustedError
from app.core.logging_config import logger


class MemoryRetryManager:
    """
    Retries transient memory persistence operations with exponential backoff.
    """

    @classmethod
    def execute_with_retry(
        cls,
        func: Callable[[], Any],
        max_retries: int = 2,
        backoff_sec: float = 0.1,
        catch_exceptions: Tuple[Type[Exception], ...] = (Exception,),
    ) -> Any:
        attempt = 0
        while attempt <= max_retries:
            try:
                return func()
            except catch_exceptions as e:
                attempt += 1
                if attempt > max_retries:
                    logger.error(f"MemoryRetryExhaustedError: Memory operation failed after {max_retries} retries: {e}")
                    raise MemoryRetryExhaustedError(f"Memory operation exhausted {max_retries} retries: {e}") from e
                
                delay = backoff_sec * (2 ** (attempt - 1))
                logger.warning(f"Memory operation attempt {attempt} failed: {e}. Retrying in {delay:.2f}s...")
                time.sleep(delay)
