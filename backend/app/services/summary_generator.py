from typing import List, Dict, Any
from app.models.feedback_report import FeedbackSummaryModel, OverallScoreModel
from app.core.logging_config import logger


class SummaryGenerator:
    """
    Generates professional narrative interview summaries, performance highlights,
    improvement areas, learning progress, and communication assessments.
    """

    @classmethod
    def generate_summary(
        cls,
        overall_score: OverallScoreModel,
        turn_answers: List[Dict[str, Any]],
        candidate_name: str = "Candidate",
    ) -> FeedbackSummaryModel:
        logger.info(f"Summary generated: Building narrative summary for {candidate_name}...")

        score = overall_score.overall_score
        grade = overall_score.grade
        rating = overall_score.rating_label

        overall_perf = (
            f"{candidate_name} completed the AI Interview session with an overall score of {score}/100 (Grade {grade}, '{rating}'). "
            f"Demonstrated technical competence across the full stack AI engineering curriculum."
        )

        highlights = []
        improvements = []

        if score >= 80:
            highlights.append("Strong technical articulation of system architecture and concurrency patterns.")
            highlights.append("Effective use of full stack framework terminology (React 19, FastAPI, Pydantic).")
            improvements.append("Deepen understanding of edge-case failure modes in distributed agentic loops.")
        else:
            highlights.append("Good foundational understanding of core single-page web concepts.")
            improvements.append("Practice explaining asynchronous event loops and vector store similarity search.")
            improvements.append("Focus on structured error handling and interceptors.")

        learning_prog = f"Showed steady engagement across {len(turn_answers)} interview turns, responding well to adaptive technical probes."
        comm_eval = f"Communication was clear, structured, and professional throughout the evaluation session."

        return FeedbackSummaryModel(
            overall_performance=overall_perf,
            interview_highlights=highlights,
            areas_for_improvement=improvements,
            learning_progress=learning_prog,
            communication_assessment=comm_eval,
        )
