from app.core.logging_config import logger


class AnswerClassifier:
    """
    Classifies candidate answers into quality tiers:
    - Excellent (90 - 100)
    - Good (75 - 89)
    - Average (60 - 74)
    - Weak (40 - 59)
    - Incorrect (0 - 39)
    - Unclear (unparseable / off-topic)
    """

    EXCELLENT = "Excellent"
    GOOD = "Good"
    AVERAGE = "Average"
    WEAK = "Weak"
    INCORRECT = "Incorrect"
    UNCLEAR = "Unclear"

    @classmethod
    def classify_score(cls, score: int, answer_text: str = "") -> str:
        """
        Maps a 0-100 score and text features to a classification tier.
        """
        if not answer_text or len(answer_text.strip()) < 5:
            logger.info("Classification: Marked as 'Unclear' due to short/empty response.")
            return cls.UNCLEAR

        if score >= 90:
            classification = cls.EXCELLENT
        elif score >= 75:
            classification = cls.GOOD
        elif score >= 60:
            classification = cls.AVERAGE
        elif score >= 40:
            classification = cls.WEAK
        else:
            classification = cls.INCORRECT

        logger.info(f"Classification: Score {score} classified as '{classification}'.")
        return classification
