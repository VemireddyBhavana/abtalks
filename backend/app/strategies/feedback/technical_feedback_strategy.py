from app.strategies.feedback.base_feedback_strategy import AbstractFeedbackStrategy
from app.models.feedback_report import FeedbackReportModel, KnowledgeGapModel
from app.services.interview_state import InterviewSessionState
from app.services.score_calculator import ScoreCalculator
from app.services.summary_generator import SummaryGenerator
from app.services.recommendation_engine import RecommendationEngine, get_recommendation_engine
from app.services.report_generator import ReportGenerator
from app.services.candidate_service import CandidateService, get_candidate_service
from app.core.logging_config import logger


class TechnicalFeedbackStrategy(AbstractFeedbackStrategy):
    """
    Technical Feedback Strategy focusing on technical accuracy, system architecture, and API concepts.
    """

    def __init__(self):
        self.recommendation_engine = get_recommendation_engine()
        self.candidate_service = get_candidate_service()

    def generate_report(self, session: InterviewSessionState) -> FeedbackReportModel:
        logger.info(f"TechnicalFeedbackStrategy: Generating technical feedback report for '{session.session_id}'...")
        candidate = self.candidate_service.get_candidate()
        turn_answers = session.candidate_answers

        overall_score = ScoreCalculator.calculate_overall_score(turn_answers)

        strengths = []
        weaknesses = []
        knowledge_gaps = []

        for turn in turn_answers:
            eval_data = turn.get("evaluation", {})
            strengths.extend(eval_data.get("strengths", []))
            weaknesses.extend(eval_data.get("weaknesses", []))
            for gap_text in eval_data.get("gaps", []):
                knowledge_gaps.append(
                    KnowledgeGapModel(
                        topic_id=turn.get("topic_id", "top_unknown"),
                        topic_title=turn.get("question_text", "Topic")[:30],
                        day_number=turn.get("day_number", 1),
                        description=gap_text,
                        severity="High" if overall_score.overall_score < 60 else "Medium",
                    )
                )

        recommendations = self.recommendation_engine.generate_recommendations(knowledge_gaps, overall_score.overall_score)
        summary = SummaryGenerator.generate_summary(overall_score, turn_answers, candidate.full_name)

        return ReportGenerator.assemble_report(
            session_id=session.session_id,
            candidate=candidate,
            overall_score=overall_score,
            strengths=strengths,
            weaknesses=weaknesses,
            knowledge_gaps=knowledge_gaps,
            topics_covered=session.topics_covered,
            days_covered=session.days_covered,
            recommendations=recommendations,
            summary=summary,
        )
