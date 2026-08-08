from typing import List, Dict, Any


class StrengthAnalyzer:
    """
    Identifies candidate technical strengths, communication strengths, reasoning strengths,
    consistency, and confidence metrics from evaluation history.
    """

    @classmethod
    def analyze_strengths(cls, turn_answers: List[Dict[str, Any]]) -> List[str]:
        strengths: List[str] = []
        for turn in turn_answers:
            eval_data = turn.get("evaluation", {})
            if eval_data.get("score", 0) >= 80:
                strengths.extend(eval_data.get("strengths", []))

        if not strengths:
            strengths.append("Maintained consistent participation throughout all interview turns.")
            strengths.append("Engaged actively with adaptive technical questions.")

        return sorted(list(set(strengths)))
