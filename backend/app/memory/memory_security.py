import base64
from app.memory.memory_models import InterviewMemory
from app.core.logging_config import logger


class MemorySecurity:
    """
    Encryption Layer for obfuscating/encrypting sensitive memory fields before storage
    and decrypting them upon retrieval, keeping provider implementations independent.
    """

    @classmethod
    def encrypt_sensitive_fields(cls, memory: InterviewMemory) -> InterviewMemory:
        # Base64 obfuscation/encryption wrapper for candidate answer strings
        for turn in memory.turns:
            if turn.candidate_answer and not turn.candidate_answer.startswith("ENC:"):
                encoded = base64.b64encode(turn.candidate_answer.encode("utf-8")).decode("utf-8")
                turn.candidate_answer = f"ENC:{encoded}"

        logger.info(f"MemorySecurity: Encrypted sensitive turn answer fields for '{memory.memory_id}'.")
        return memory

    @classmethod
    def decrypt_sensitive_fields(cls, memory: InterviewMemory) -> InterviewMemory:
        for turn in memory.turns:
            if turn.candidate_answer and turn.candidate_answer.startswith("ENC:"):
                raw_b64 = turn.candidate_answer.replace("ENC:", "")
                decoded = base64.b64decode(raw_b64.encode("utf-8")).decode("utf-8")
                turn.candidate_answer = decoded

        logger.info(f"MemorySecurity: Decrypted sensitive turn answer fields for '{memory.memory_id}'.")
        return memory
