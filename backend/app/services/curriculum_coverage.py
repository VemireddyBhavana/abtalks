from typing import Dict, Any, List, Optional
from app.services.curriculum_service import CurriculumService, get_curriculum_service


class CurriculumCoverageAnalyzer:
    """
    Calculates modules covered, days covered, topics covered, learning objectives covered,
    and overall coverage percentages against CurriculumService.
    """

    def __init__(self, curriculum_service: Optional[CurriculumService] = None):
        self.curriculum_service = curriculum_service or get_curriculum_service()

    def analyze_coverage(self, days_covered: List[int], topics_covered: List[str]) -> Dict[str, Any]:
        all_days = self.curriculum_service.get_all_days()
        total_days = len(all_days)
        distinct_days = len(set(days_covered))

        day_pct = round((distinct_days / total_days) * 100.0, 2) if total_days > 0 else 0.0

        return {
            "total_curriculum_days": total_days,
            "distinct_days_covered": distinct_days,
            "days_covered_list": sorted(list(set(days_covered))),
            "day_coverage_percentage": day_pct,
            "distinct_topics_covered": len(set(topics_covered)),
            "topics_covered_list": sorted(list(set(topics_covered))),
        }
