from typing import Dict, Any, List
from app.services.evaluation_history import EvaluationHistory


class EvaluationMetricsTracker:
    """
    Computes evaluation metrics across the session:
    - Average evaluation score
    - Confidence trend
    - Action distribution
    - Difficulty progression
    - Topic mastery summary
    """

    @classmethod
    def compute_summary_metrics(cls, history: EvaluationHistory) -> Dict[str, Any]:
        turns = history.turns
        if not turns:
            return {
                "average_score": 0.0,
                "confidence_trend": [],
                "total_turns": 0,
                "mastered_topics": [],
            }

        avg_score = history.get_average_score()
        confidence_trend = history.get_confidence_trend()
        
        action_dist: Dict[str, int] = {}
        mastered_topics = []

        for t in turns:
            act = t.get("action_type", "Unknown")
            action_dist[act] = action_dist.get(act, 0) + 1
            if t.get("score", 0) >= 85:
                mastered_topics.append(t.get("topic_id"))

        return {
            "average_score": avg_score,
            "confidence_trend": confidence_trend,
            "total_turns": len(turns),
            "action_distribution": action_dist,
            "mastered_topics_count": len(set(mastered_topics)),
        }
