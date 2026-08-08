from typing import List, Dict, Any
from app.models.answer_evaluation import AnswerEvaluationModel, FollowUpDecisionModel


class EvaluationHistory:
    """
    Stores all turn evaluation results, confidence scores, difficulty changes,
    and follow-up decisions across an interview session.
    """

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.turns: List[Dict[str, Any]] = []

    def record_turn(
        self,
        question_id: str,
        topic_id: str,
        evaluation: AnswerEvaluationModel,
        decision: FollowUpDecisionModel,
        difficulty: str,
    ) -> None:
        self.turns.append({
            "question_id": question_id,
            "topic_id": topic_id,
            "score": evaluation.score,
            "confidence": evaluation.confidence_score,
            "classification": evaluation.classification,
            "action_type": decision.action_type,
            "difficulty": difficulty,
            "rubric": evaluation.rubric.model_dump(),
        })

    def get_average_score(self) -> float:
        if not self.turns:
            return 0.0
        return round(sum(t["score"] for t in self.turns) / len(self.turns), 2)

    def get_confidence_trend(self) -> List[int]:
        return [t["confidence"] for t in self.turns]

    def get_turn_count(self) -> int:
        return len(self.turns)
