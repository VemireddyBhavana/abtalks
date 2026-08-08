from typing import Optional, List, Dict, Any
from app.models.feedback_report import FeedbackReportModel, KnowledgeGapModel
from app.services.interview_state import InterviewSessionState
from app.services.score_calculator import ScoreCalculator
from app.services.summary_generator import SummaryGenerator
from app.services.recommendation_engine import RecommendationEngine, get_recommendation_engine
from app.services.report_generator import ReportGenerator
from app.services.candidate_service import CandidateService, get_candidate_service
from app.core.logging_config import logger


class FeedbackEngine:
    """
    Main Feedback & Scoring Engine orchestrator.
    Collects turn history, evaluation history, knowledge gaps, question difficulties, and topics covered,
    and produces one final structured FeedbackReportModel JSON.
    """

    def __init__(
        self,
        recommendation_engine: Optional[RecommendationEngine] = None,
        candidate_service: Optional[CandidateService] = None,
    ):
        self.recommendation_engine = recommendation_engine or get_recommendation_engine()
        self.candidate_service = candidate_service or get_candidate_service()

    def generate_feedback_report(self, session: InterviewSessionState) -> FeedbackReportModel:
        """
        Generates final structured FeedbackReportModel for completed interview session.
        """
        logger.info(f"Report generation started: Initiating report generation for session '{session.session_id}'...")

        candidate = self.candidate_service.get_candidate()
        turn_answers = session.candidate_answers

        # 1. Calculate category and overall weighted scores
        overall_score = ScoreCalculator.calculate_overall_score(turn_answers)

        # 2. Extract strengths, weaknesses, and knowledge gaps across turns
        strengths: List[str] = []
        weaknesses: List[str] = []
        knowledge_gaps: List[KnowledgeGapModel] = []

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

        # 3. Generate actionable recommendations
        recommendations = self.recommendation_engine.generate_recommendations(
            knowledge_gaps=knowledge_gaps,
            overall_score=overall_score.overall_score,
        )

        # 4. Generate narrative summary
        summary = SummaryGenerator.generate_summary(
            overall_score=overall_score,
            turn_answers=turn_answers,
            candidate_name=candidate.full_name,
        )

        # 5. Assemble final report
        report = ReportGenerator.assemble_report(
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

        logger.info(f"Feedback report completed: Report successfully created for session '{session.session_id}'.")
        return report


# Singleton helper
_feedback_engine_instance: Optional[FeedbackEngine] = None


def get_feedback_engine() -> FeedbackEngine:
    global _feedback_engine_instance
    if _feedback_engine_instance is None:
        _feedback_engine_instance = FeedbackEngine()
    return _feedback_engine_instance
