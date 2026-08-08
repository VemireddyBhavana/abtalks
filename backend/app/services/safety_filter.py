from app.core.logging_config import logger
from app.exceptions.llm_exception import LLMResponseParsingError


class SafetyFilter:
    """
    Guarantees generated questions adhere to professional, safe, and interview-focused guidelines.
    """

    UNSAFE_KEYWORDS = [
        "hack", "exploit", "password", "confidential", "illegal",
        "discriminate", "race", "gender", "religion", "political"
    ]

    @classmethod
    def filter_question_text(cls, question_text: str) -> str:
        """
        Sanitizes text and checks for forbidden keywords.
        Raises LLMResponseParsingError if unsafe content is detected.
        """
        text_lower = question_text.lower()
        for kw in cls.UNSAFE_KEYWORDS:
            if kw in text_lower and not ("hackathon" in text_lower and kw == "hack"):
                logger.error(f"Safety Filter Triggered: Detected blacklisted keyword '{kw}' in generated text.")
                raise LLMResponseParsingError(f"Generated text contains unsafe/unprofessional keyword '{kw}'.")

        return question_text.strip()
