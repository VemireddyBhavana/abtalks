from typing import Dict, Any, List
from app.services.interview_state import InterviewSessionState
from app.services.difficulty_manager import DifficultyManager


class InterviewMetricsCalculator:
    """
    Computes evaluation metrics for a session:
    - Questions Asked
    - Average Difficulty Score & Tier
    - Topics Covered Count & List
    - Days Covered Count & List
    - Completion Percentage
    """

    @classmethod
    def calculate_metrics(cls, session: InterviewSessionState) -> Dict[str, Any]:
        asked_questions: List[Any] = []
        plan_questions_by_id = {q.id: q for q in session.plan.questions}

        for ans in session.candidate_answers:
            q_id = ans.get("question_id")
            q = plan_questions_by_id.get(q_id)
            if q:
                asked_questions.append(q)

        avg_diff = DifficultyManager.calculate_average_difficulty(asked_questions)
        total_q = len(session.plan.questions)
        completed_q = len(session.candidate_answers)
        completion_pct = round((completed_q / total_q) * 100.0, 2) if total_q > 0 else 0.0

        return {
            "session_id": session.session_id,
            "candidate_id": session.candidate_id,
            "total_questions_planned": total_q,
            "questions_asked_count": completed_q,
            "completion_percentage": completion_pct,
            "done": session.done,
            "average_difficulty_score": avg_diff,
            "distinct_days_covered_count": len(session.days_covered),
            "days_covered": session.days_covered,
            "distinct_topics_covered_count": len(session.topics_covered),
            "topics_covered": session.topics_covered,
            "started_at": session.started_at,
            "completed_at": session.completed_at,
        }
