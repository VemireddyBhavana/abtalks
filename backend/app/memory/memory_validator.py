from app.memory.memory_models import InterviewMemory
from app.exceptions.memory_exception import MemoryValidationError
from app.core.logging_config import logger


class MemoryValidator:
    """
    Pre-flight validator verifying InterviewMemory schema integrity before persistence.
    """

    @classmethod
    def validate(cls, memory: InterviewMemory) -> bool:
        if not memory.memory_id or len(memory.memory_id.strip()) == 0:
            logger.error("MemoryValidationError: memory_id cannot be empty.")
            raise MemoryValidationError("memory_id cannot be empty.")

        if not memory.session.session_id:
            logger.error("MemoryValidationError: session_id cannot be empty.")
            raise MemoryValidationError("session_id cannot be empty.")

        if not memory.candidate.candidate_id:
            logger.error("MemoryValidationError: candidate_id cannot be empty.")
            raise MemoryValidationError("candidate_id cannot be empty.")

        logger.info(f"MemoryValidator: InterviewMemory '{memory.memory_id}' passed pre-flight schema validation.")
        return True
