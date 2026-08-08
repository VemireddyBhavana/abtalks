import time
from typing import Callable, Any
from app.core.logging_config import logger
from app.exceptions.llm_exception import LLMProviderError, LLMTimeoutError


class RetryManager:
    """
    Executes operations with exponential backoff retries for transient failures.
    """

    @classmethod
    def execute_with_retry(
        cls,
        operation: Callable[[], Any],
        max_retries: int = 3,
        backoff_factor: float = 1.5,
    ) -> Any:
        attempt = 0
        last_exception = None

        while attempt < max_retries:
            try:
                attempt += 1
                return operation()
            except (LLMProviderError, LLMTimeoutError, ConnectionError) as exc:
                last_exception = exc
                logger.warning(
                    f"Retry Triggered: Attempt {attempt}/{max_retries} failed ({str(exc)}). Retrying in {backoff_factor ** attempt:.1f}s..."
                )
                time.sleep(backoff_factor ** attempt)
            except Exception as exc:
                # Non-retriable error
                logger.error(f"Non-retriable exception in operation: {str(exc)}")
                raise exc

        logger.error(f"Fallback Activated: Max retries ({max_retries}) exhausted.")
        raise LLMProviderError(f"Operation failed after {max_retries} retry attempts.") from last_exception
