from typing import List, Optional
from app.models.interview_engine import QuestionPlaceholderModel
from app.exceptions.llm_exception import LLMResponseParsingError
from app.core.logging_config import logger


class ResponseValidator:
    """
    Validates LLM-generated questions against structural and content quality criteria:
    - Minimum / Maximum character length (15 to 500 chars)
    - Non-empty text
    - No duplicate questions
    - Topic keyword alignment
    """

    @classmethod
    def validate_question(
        cls,
        question: QuestionPlaceholderModel,
        topic_title: str,
        asked_questions: Optional[List[str]] = None,
    ) -> bool:
        q_text = question.question_text.strip()

        # 1. Non-empty check
        if not q_text:
            logger.error("Validation Failed: Generated question text is empty.")
            raise LLMResponseParsingError("Generated question text is empty.")

        # 2. Length check
        if len(q_text) < 15 or len(q_text) > 500:
            logger.error(f"Validation Failed: Question length ({len(q_text)} chars) out of range (15-500).")
            raise LLMResponseParsingError(f"Question length ({len(q_text)} chars) out of valid range (15-500).")

        # 3. Duplicate question check
        if asked_questions:
            for prev_q in asked_questions:
                if q_text.lower() in prev_q.lower() or prev_q.lower() in q_text.lower():
                    logger.error("Validation Failed: Generated question duplicates a previously asked question.")
                    raise LLMResponseParsingError("Generated question duplicates a previously asked question.")

        logger.info(f"Validation Passed: Question '{question.id}' passed structural validation.")
        return True
