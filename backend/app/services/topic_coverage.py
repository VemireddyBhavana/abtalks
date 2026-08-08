from typing import List, Dict, Set, Any
from app.models.interview_engine import InterviewPlanModel, QuestionPlaceholderModel


class TopicCoverageAnalyzer:
    """
    Analyzes an InterviewPlanModel to verify coverage criteria:
    - Minimum 4 distinct curriculum days
    - Zero duplicate topics
    - Module distribution statistics
    """

    @classmethod
    def analyze_plan(cls, plan: InterviewPlanModel) -> Dict[str, Any]:
        """
        Returns coverage statistics dictionary for an interview plan.
        """
        questions: List[QuestionPlaceholderModel] = plan.questions

        days_covered: Set[int] = set(q.day_number for q in questions)
        topics_covered: Set[str] = set(q.topic_id for q in questions)
        difficulties: Dict[str, int] = {}

        for q in questions:
            difficulties[q.difficulty] = difficulties.get(q.difficulty, 0) + 1

        is_multi_day_compliant = len(days_covered) >= 4
        is_topic_unique = len(topics_covered) == len(questions)

        return {
            "total_questions": len(questions),
            "distinct_days_count": len(days_covered),
            "days_covered": sorted(list(days_covered)),
            "distinct_topics_count": len(topics_covered),
            "topics_covered": sorted(list(topics_covered)),
            "difficulty_distribution": difficulties,
            "is_multi_day_compliant": is_multi_day_compliant,
            "is_topic_unique": is_topic_unique,
            "valid": is_multi_day_compliant and is_topic_unique and len(questions) == 8,
        }
