from typing import List
from app.models.feedback_report import RecommendationModel


class RecommendationPriorityEngine:
    """
    Ranks recommendations into Critical, High, Medium, Low priority tiers
    based on overall score severity and knowledge gap impact.
    """

    @classmethod
    def prioritize_recommendations(
        cls,
        recommendations: List[RecommendationModel],
        overall_score: float,
    ) -> List[RecommendationModel]:
        prioritized = []

        for rec in recommendations:
            if overall_score < 50:
                rec.priority = "Critical"
            elif overall_score < 70:
                rec.priority = "High"
            elif overall_score < 85:
                rec.priority = "Medium"
            else:
                rec.priority = "Low"
            prioritized.append(rec)

        # Sort: Critical -> High -> Medium -> Low
        priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        return sorted(prioritized, key=lambda r: priority_order.get(r.priority, 2))
