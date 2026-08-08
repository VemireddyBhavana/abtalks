from typing import List, Dict, Set
from app.services.curriculum_service import CurriculumService, get_curriculum_service
from app.services.candidate_service import CandidateService, get_candidate_service
from app.models.curriculum import DayModel, TopicModel
from app.core.logging_config import logger


class QuestionSelector:
    """
    Selects curriculum topics for the interview plan based on candidate progress,
    skipped topics, learning objectives, and multi-day coverage rules.
    """

    def __init__(
        self,
        curriculum_service: CurriculumService = None,
        candidate_service: CandidateService = None,
    ):
        self.curriculum_service = curriculum_service or get_curriculum_service()
        self.candidate_service = candidate_service or get_candidate_service()

    def select_topics(self, min_days: int = 4, target_topic_count: int = 8) -> List[TopicModel]:
        """
        Selects a list of distinct TopicModel objects across at least min_days curriculum days.
        """
        all_days: List[DayModel] = self.curriculum_service.get_all_days()
        candidate = self.candidate_service.get_candidate()

        completed_topic_ids: Set[str] = set(candidate.completed_topics)
        skipped_topic_ids: Set[str] = set(candidate.skipped_topics)

        selected_topics: List[TopicModel] = []
        selected_topic_ids: Set[str] = set()
        days_represented: Set[int] = set()

        # Step 1: First pass - pick topics from incomplete days / skipped topics to probe growth areas
        for day in all_days:
            for topic in day.topics:
                if len(selected_topics) >= target_topic_count:
                    break
                if topic.id not in selected_topic_ids and (topic.id in skipped_topic_ids or day.day_number in candidate.progress.incomplete_days):
                    selected_topics.append(topic)
                    selected_topic_ids.add(topic.id)
                    days_represented.add(day.day_number)
                    logger.info(f"Topic Selected: '{topic.title}' (Day {day.day_number}) [Priority: Growth/Incomplete]")

        # Step 2: Second pass - pick topics to ensure coverage of at least min_days distinct curriculum days
        for day in all_days:
            if len(days_represented) >= min_days and len(selected_topics) >= target_topic_count:
                break
            for topic in day.topics:
                if len(selected_topics) >= target_topic_count and len(days_represented) >= min_days:
                    break
                if topic.id not in selected_topic_ids:
                    selected_topics.append(topic)
                    selected_topic_ids.add(topic.id)
                    days_represented.add(day.day_number)
                    logger.info(f"Topic Selected: '{topic.title}' (Day {day.day_number}) [Priority: Day Coverage]")

        # Step 3: Fallback fill if target count not reached
        if len(selected_topics) < target_topic_count:
            for day in all_days:
                for topic in day.topics:
                    if len(selected_topics) >= target_topic_count:
                        break
                    if topic.id not in selected_topic_ids:
                        selected_topics.append(topic)
                        selected_topic_ids.add(topic.id)
                        days_represented.add(day.day_number)

        logger.info(
            f"QuestionSelector completed: Selected {len(selected_topics)} topics covering {len(days_represented)} distinct days (Target >= {min_days} days)."
        )
        return selected_topics
