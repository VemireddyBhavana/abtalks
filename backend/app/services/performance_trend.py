from typing import List, Dict, Any


class PerformanceTrendAnalyzer:
    """
    Tracks turn-by-turn score progression, confidence trends, difficulty trajectory,
    and topic mastery trends using Phase 6 evaluation history data.
    """

    @classmethod
    def analyze_trends(cls, turn_answers: List[Dict[str, Any]]) -> Dict[str, Any]:
        scores = []
        confidences = []
        difficulties = []

        for turn in turn_answers:
            eval_data = turn.get("evaluation", {})
            scores.append(eval_data.get("score", 70))
            confidences.append(eval_data.get("confidence_score", 70))
            difficulties.append(turn.get("difficulty", "Intermediate"))

        # Calculate slope/trend (improving, steady, declining)
        if len(scores) >= 2:
            trend_val = scores[-1] - scores[0]
            trajectory = "Improving" if trend_val > 5 else ("Declining" if trend_val < -5 else "Steady")
        else:
            trajectory = "Steady"

        return {
            "score_progression": scores,
            "confidence_trend": confidences,
            "difficulty_trajectory": difficulties,
            "performance_trajectory": trajectory,
        }
