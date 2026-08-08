from app.services.answer_classifier import AnswerClassifier


class BloomsTaxonomyManager:
    """
    Maps candidate answer quality and technical depth to Bloom's Taxonomy cognitive levels:
    - Remember (0-39: Recall facts)
    - Understand (40-59: Explain concepts)
    - Apply (60-74: Implement solutions)
    - Analyze (75-84: Compare architectures)
    - Evaluate (85-94: Critique trade-offs)
    - Create (95-100: Design novel systems)
    """

    LEVELS = {
        "Remember": (0, 39),
        "Understand": (40, 59),
        "Apply": (60, 74),
        "Analyze": (75, 84),
        "Evaluate": (85, 94),
        "Create": (95, 100),
    }

    @classmethod
    def get_cognitive_level(cls, score: int) -> str:
        for level, (low, high) in cls.LEVELS.items():
            if low <= score <= high:
                return level
        return "Understand"
