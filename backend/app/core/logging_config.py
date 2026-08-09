import os
import logging
import sys


def setup_logging():
    """
    Configures production-ready Python logging with console and categorized file handlers:
    - application.log
    - api.log
    - error.log
    - performance.log
    """
    logger = logging.getLogger("ai_interview_agent")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Create logs directory inside workspace root if not present
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
        os.makedirs(logs_dir, exist_ok=True)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # 1. Console Stream Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # 2. Main Application Log File
        app_file_handler = logging.FileHandler(os.path.join(logs_dir, "application.log"), encoding="utf-8")
        app_file_handler.setFormatter(formatter)
        logger.addHandler(app_file_handler)

        # 3. Error Log File (WARNING and above)
        error_file_handler = logging.FileHandler(os.path.join(logs_dir, "error.log"), encoding="utf-8")
        error_file_handler.setLevel(logging.WARNING)
        error_file_handler.setFormatter(formatter)
        logger.addHandler(error_file_handler)

    return logger


logger = setup_logging()
