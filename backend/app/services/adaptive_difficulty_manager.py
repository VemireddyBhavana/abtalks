from typing import List
from app.services.answer_classifier import AnswerClassifier
from app.core.logging_config import logger


class AdaptiveDifficultyManager:
    """
    Manages dynamic difficulty adjustments across candidate turn responses:
    - Increase difficulty after consistently strong answers (2 consecutive Excellent/Good)
    - Maintain difficulty after Average answers
    - Reduce difficulty after Weak or Incorrect answers
    """

    DIFFICULTY_LEVELS = ["Fundamental", "Intermediate", "Advanced"]

    def __init__(self, initial_difficulty: str = "Intermediate"):
        self.current_difficulty = initial_difficulty
        self.history: List[str] = []

    def update_difficulty(self, classification: str) -> str:
        """
        Adjusts and returns the current difficulty based on latest evaluation classification.
        """
        self.history.append(classification)
        curr_idx = self.DIFFICULTY_LEVELS.index(self.current_difficulty)

        if classification in [AnswerClassifier.EXCELLENT, AnswerClassifier.GOOD]:
            # Promote if last 2 answers were strong
            if len(self.history) >= 2 and self.history[-2] in [AnswerClassifier.EXCELLENT, AnswerClassifier.GOOD]:
                if curr_idx < len(self.DIFFICULTY_LEVELS) - 1:
                    self.current_difficulty = self.DIFFICULTY_LEVELS[curr_idx + 1]
                    logger.info(f"Difficulty Adjusted: Promoted to '{self.current_difficulty}'.")
        elif classification in [AnswerClassifier.WEAK, AnswerClassifier.INCORRECT]:
            if curr_idx > 0:
                self.current_difficulty = self.DIFFICULTY_LEVELS[curr_idx - 1]
                logger.info(f"Difficulty Adjusted: Demoted to '{self.current_difficulty}'.")

        return self.current_difficulty
