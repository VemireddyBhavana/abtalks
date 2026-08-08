from typing import Dict, Any, List
from app.models.interview_engine import InterviewPlanModel
from app.services.question_bank import QuestionBank
from app.services.candidate_service import CandidateService, get_candidate_service
from app.exceptions.interview_exception import InterviewPlanError, QuestionBankError
from app.core.logging_config import logger


class InterviewValidator:
    """
    Pre-flight validator for interview plans and candidate readiness.
    Verifies:
    1. Exactly 8 questions
    2. Minimum 4 curriculum days covered
    3. Zero duplicate topics
    4. QuestionBank integrity
    5. Candidate profile readiness
    """

    def __init__(self, candidate_service: CandidateService = None):
        self.candidate_service = candidate_service or get_candidate_service()

    def validate_plan(self, plan: InterviewPlanModel) -> Dict[str, Any]:
        """
        Validates an InterviewPlanModel and returns a detailed validation report.
        Raises InterviewPlanError if critical constraints are violated.
        """
        questions = plan.questions

        # 1. Question count check
        if len(questions) != 8:
            logger.error(f"Validation Failed: Plan has {len(questions)} questions (expected 8).")
            raise InterviewPlanError(f"Interview plan must contain exactly 8 questions, got {len(questions)}.")

        # 2. Distinct days check
        days_covered = set(q.day_number for q in questions)
        if len(days_covered) < 4:
            logger.error(f"Validation Failed: Plan covers {len(days_covered)} days (expected >= 4).")
            raise InterviewPlanError(f"Interview plan must cover at least 4 curriculum days, got {len(days_covered)}.")

        # 3. Topic uniqueness check
        topic_ids = [q.topic_id for q in questions]
        if len(topic_ids) != len(set(topic_ids)):
            logger.error("Validation Failed: Duplicate topics found in interview plan.")
            raise InterviewPlanError("Interview plan contains duplicate topics.")

        # 4. QuestionBank integrity check
        if QuestionBank.get_question_count() < 8:
            logger.error("Validation Failed: QuestionBank has insufficient questions.")
            raise QuestionBankError("QuestionBank has fewer than 8 total questions.")

        # 5. Candidate readiness check
        candidate = self.candidate_service.get_candidate()
        if not candidate or not candidate.candidate_id:
            logger.error("Validation Failed: Candidate profile uninitialized.")
            raise InterviewPlanError("Candidate profile unavailable for interview planning.")

        logger.info(f"Validation Passed: Interview plan '{plan.session_id}' verified successfully (8 Qs, {len(days_covered)} days).")

        return {
            "session_id": plan.session_id,
            "candidate_id": plan.candidate_id,
            "valid": True,
            "total_questions": len(questions),
            "days_covered_count": len(days_covered),
            "days_covered": sorted(list(days_covered)),
            "topics_count": len(topic_ids),
            "candidate_name": candidate.full_name,
        }
