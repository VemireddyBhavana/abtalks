from typing import List, Optional
from app.memory.memory_models import InterviewMemory


class MemorySearchEngine:
    """
    Multi-criteria search engine for InterviewMemory documents.
    Supports filtering by: Session ID, Candidate ID, Topic, Curriculum Day, Knowledge Gap, Classification, Date.
    """

    @classmethod
    def filter_memories(
        cls,
        memories: List[InterviewMemory],
        session_id: Optional[str] = None,
        candidate_id: Optional[str] = None,
        topic_title: Optional[str] = None,
        day_number: Optional[int] = None,
        classification: Optional[str] = None,
    ) -> List[InterviewMemory]:
        filtered = list(memories)

        if session_id:
            filtered = [m for m in filtered if m.session.session_id == session_id]

        if candidate_id:
            filtered = [m for m in filtered if m.candidate.candidate_id == candidate_id]

        if topic_title:
            t_lower = topic_title.lower()
            filtered = [m for m in filtered if any(t_lower in t.topic_title.lower() for t in m.turns)]

        if day_number:
            filtered = [m for m in filtered if any(t.turn_index + 1 == day_number for t in m.turns)]

        if classification:
            c_lower = classification.lower()
            filtered = [m for m in filtered if any(t.classification.lower() == c_lower for t in m.turns)]

        return filtered
