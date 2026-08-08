from typing import List
from app.models.interview_engine import QuestionPlaceholderModel


class DifficultyManager:
    """
    Manages question difficulty tiers (Easy / Fundamental, Medium / Intermediate, Hard / Advanced)
    and computes difficulty progression across an interview session.
    """

    DIFFICULTY_EASY = "Fundamental"
    DIFFICULTY_MEDIUM = "Intermediate"
    DIFFICULTY_HARD = "Advanced"

    DIFFICULTY_SCORES = {
        "Fundamental": 1,
        "Intermediate": 2,
        "Advanced": 3,
    }

    @classmethod
    def get_difficulty_score(cls, difficulty: str) -> int:
        """Maps difficulty label to numeric score."""
        return cls.DIFFICULTY_SCORES.get(difficulty, 2)

    @classmethod
    def calculate_average_difficulty(cls, questions: List[QuestionPlaceholderModel]) -> float:
        """Calculates average numerical difficulty for a list of questions."""
        if not questions:
            return 0.0
        total_score = sum(cls.get_difficulty_score(q.difficulty) for q in questions)
        return round(total_score / len(questions), 2)

    @classmethod
    def suggest_next_difficulty(cls, current_score: float) -> str:
        """
        Placeholder method for dynamic difficulty adjustment based on performance score.
        """
        if current_score >= 85:
            return cls.DIFFICULTY_HARD
        elif current_score >= 60:
            return cls.DIFFICULTY_MEDIUM
        return cls.DIFFICULTY_EASY
