from typing import List, Dict, Any, Optional


class ConversationContextManager:
    """
    Maintains and formats multi-turn interview conversation context including previous questions,
    answers, current day, and topic metadata.
    """

    @classmethod
    def format_history(
        cls,
        session_id: str,
        current_question_index: int,
        asked_questions: Optional[List[str]] = None,
        candidate_answers: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Formats history into a structured string context.
        """
        questions_str = "\n".join([f"- {q}" for q in (asked_questions or [])]) or "None yet"
        
        answers_summary = []
        for idx, ans in enumerate(candidate_answers or []):
            answers_summary.append(
                f"Turn {idx + 1} ({ans.get('topic_id', 'topic')}): {ans.get('question_text')} => Answer: {ans.get('candidate_answer', '')[:100]}..."
            )
        answers_str = "\n".join(answers_summary) or "No previous turns completed."

        return f"""Session ID: {session_id}
Active Question Index: {current_question_index + 1}
Asked Questions:
{questions_str}

Candidate Turn History:
{answers_str}"""
