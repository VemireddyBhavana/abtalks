import time
import functools
from typing import Callable, Any, Dict
from app.core.logging_config import logger


class BenchmarkTimer:
    """
    Context manager and utility class for timing code blocks in milliseconds.
    """
    def __init__(self, name: str = "Operation"):
        self.name = name
        self.start_time = 0.0
        self.elapsed_ms = 0.0

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed_ms = (time.perf_counter() - self.start_time) * 1000
        logger.info(f"[Benchmark] {self.name} completed in {self.elapsed_ms:.2f}ms")


def benchmark(name: str = None):
    """
    Decorator for measuring execution latency of synchronous or asynchronous functions.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        op_name = name or func.__name__

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            with BenchmarkTimer(op_name):
                return func(*args, **kwargs)

        return wrapper
    return decorator
