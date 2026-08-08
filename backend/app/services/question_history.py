from typing import List, Set


class QuestionHistory:
    """
    Stores and tracks question IDs, topics, and curriculum days presented during an interview
    to enforce zero duplicate questions/topics.
    """

    def __init__(self):
        self._asked_question_ids: Set[str] = set()
        self._asked_topic_ids: Set[str] = set()
        self._asked_days: Set[int] = set()

    def record_question(self, question_id: str, topic_id: str, day_number: int) -> None:
        """Records a presented question."""
        self._asked_question_ids.add(question_id)
        self._asked_topic_ids.add(topic_id)
        self._asked_days.add(day_number)

    def is_question_asked(self, question_id: str) -> bool:
        """Returns True if question_id was already presented."""
        return question_id in self._asked_question_ids

    def is_topic_asked(self, topic_id: str) -> bool:
        """Returns True if topic_id was already presented."""
        return topic_id in self._asked_topic_ids

    def get_asked_question_ids(self) -> List[str]:
        return sorted(list(self._asked_question_ids))

    def get_asked_topic_ids(self) -> List[str]:
        return sorted(list(self._asked_topic_ids))

    def get_asked_days(self) -> List[int]:
        return sorted(list(self._asked_days))

    def clear(self) -> None:
        self._asked_question_ids.clear()
        self._asked_topic_ids.clear()
        self._asked_days.clear()
