from typing import Dict, Any, Optional
from datetime import datetime, timezone
from app.services.interview_state import InterviewSessionState


class ProgressTracker:
    """
    Computes real-time progress metrics for an active interview session:
    - Active Question Index
    - Questions Remaining
    - Completion Percentage
    - Elapsed Time (seconds)
    - Current Curriculum Day & Topic
    """

    @classmethod
    def get_progress(cls, session: InterviewSessionState) -> Dict[str, Any]:
        total = len(session.plan.questions)
        current_idx = session.current_question_index
        remaining = max(0, total - current_idx)
        completion_pct = round((current_idx / total) * 100.0, 2) if total > 0 else 0.0

        current_q = session.current_question
        current_day = current_q.day_number if current_q else None
        current_topic = current_q.topic_title if current_q else None

        elapsed_seconds = 0
        if session.started_at:
            start_dt = datetime.fromisoformat(session.started_at)
            now_dt = datetime.now(timezone.utc)
            elapsed_seconds = int((now_dt - start_dt).total_seconds())

        return {
            "session_id": session.session_id,
            "current_question_number": min(current_idx + 1, total),
            "total_questions": total,
            "questions_remaining": remaining,
            "completion_percentage": completion_pct,
            "done": session.done,
            "elapsed_seconds": elapsed_seconds,
            "current_curriculum_day": current_day,
            "current_topic": current_topic,
            "days_covered": session.days_covered,
            "topics_covered": session.topics_covered,
        }
