import json
import re
from typing import Dict, Any
from app.models.interview_engine import QuestionPlaceholderModel
from app.models.curriculum import TopicModel
from app.exceptions.llm_exception import LLMResponseParsingError
from app.core.logging_config import logger


class ResponseParser:
    """
    Parses and validates raw LLM output text into structured QuestionPlaceholderModel instances.
    """

    @classmethod
    def parse_question_response(
        cls,
        raw_response: str,
        topic: TopicModel,
        day_number: int,
        question_id: str,
        fallback_difficulty: str = "Intermediate",
    ) -> QuestionPlaceholderModel:
        """
        Extracts JSON payload from raw_response text and converts it into QuestionPlaceholderModel.
        """
        logger.info("Parsing Completed: Beginning extraction of JSON question payload.")
        if not raw_response or not raw_response.strip():
            logger.error("LLMResponseParsingError: Received empty response from LLM provider.")
            raise LLMResponseParsingError("Empty response string received from LLM provider.")

        try:
            # Strip potential markdown code block wrappers ```json ... ```
            cleaned = raw_response.strip()
            if cleaned.startswith("```"):
                cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned)
                cleaned = re.sub(r"\n?```$", "", cleaned)
                cleaned = cleaned.strip()

            parsed = json.loads(cleaned)

            question_text = parsed.get("question_text") or parsed.get("question")
            if not question_text:
                raise ValueError("JSON response missing required 'question_text' field.")

            difficulty = parsed.get("difficulty") or fallback_difficulty

            logger.info(f"Parsing Completed: Successfully parsed question '{question_id}'.")
            return QuestionPlaceholderModel(
                id=question_id,
                day_number=day_number,
                topic_id=topic.id,
                topic_title=topic.title,
                question_text=question_text.strip(),
                difficulty=difficulty,
            )
        except (json.JSONDecodeError, ValueError) as exc:
            logger.error(f"LLMResponseParsingError: Failed to parse LLM JSON output: {str(exc)}")
            raise LLMResponseParsingError(f"Failed to parse valid JSON question from LLM output: {str(exc)}") from exc
