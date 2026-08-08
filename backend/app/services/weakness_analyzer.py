from typing import List, Dict, Any


class WeaknessAnalyzer:
    """
    Identifies candidate weak topics, knowledge gaps, communication issues, and reasoning gaps.
    """

    @classmethod
    def analyze_weaknesses(cls, turn_answers: List[Dict[str, Any]]) -> List[str]:
        weaknesses: List[str] = []
        for turn in turn_answers:
            eval_data = turn.get("evaluation", {})
            if eval_data.get("score", 100) < 70:
                weaknesses.extend(eval_data.get("weaknesses", []))
                weaknesses.extend(eval_data.get("gaps", []))

        return sorted(list(set(weaknesses)))
