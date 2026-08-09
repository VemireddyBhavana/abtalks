from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from app.services.interview_engine import InterviewEngine, get_interview_engine
from app.exceptions.interview_exception import (
    InvalidInterviewStateError,
    InterviewAlreadyCompletedError,
    InterviewPlanError,
)

router = APIRouter(tags=["Hackathon API Contract"])


class HackathonFeedbackModel(BaseModel):
    summary: str
    strengths: List[str]
    gaps: List[str]
    next: List[str]


class HackathonInterviewRequest(BaseModel):
    sessionId: str = Field(..., description="Unique session identifier for the interview")
    candidate: Optional[Dict[str, Any]] = Field(None, description="Candidate profile payload provided on session start")
    message: Optional[str] = Field(None, description="Candidate response text provided on subsequent turns")


class HackathonInterviewResponse(BaseModel):
    reply: str
    done: bool = False
    feedback: Optional[HackathonFeedbackModel] = None


@router.post(
    "/api/interview",
    response_model=HackathonInterviewResponse,
    summary="Hackathon Official API Contract Endpoint",
    description="Exposes POST /api/interview accepting sessionId, candidate (on start), or message (on turn). Returns reply, done, and feedback upon completion.",
    status_code=status.HTTP_200_OK,
)
@router.post(
    "/interview",
    response_model=HackathonInterviewResponse,
    include_in_schema=False,
)
def hackathon_interview_endpoint(
    body: HackathonInterviewRequest,
    engine: InterviewEngine = Depends(get_interview_engine),
):
    session_id = body.sessionId

    # 1. Start Session Request (Candidate payload provided or first request)
    if body.candidate or not body.message:
        candidate_name = "Candidate"
        candidate_id = "CAND-001"
        
        if body.candidate:
            member = body.candidate.get("member", {})
            candidate_name = member.get("name", "Candidate")
            candidate_id = member.get("id", "CAND-001")

        try:
            start_data = engine.start_interview(
                candidate_id=candidate_id,
                session_id=session_id,
            )
            q_text = start_data.question.question_text if start_data.question else "Can you introduce yourself and discuss your recent projects?"
            reply_msg = f"Welcome {candidate_name}. Let's begin your technical interview.\n\nQuestion 1: {q_text}"
            
            return HackathonInterviewResponse(
                reply=reply_msg,
                done=False,
                feedback=None,
            )
        except Exception as exc:
            # If session is already started, treat message or continue
            pass

    # 2. Turn Answer Submission Request (Message provided)
    if body.message:
        try:
            answer_data = engine.submit_answer(session_id=session_id, answer_text=body.message)
            
            if answer_data.done:
                fb_report = answer_data.feedback_report
                
                # Format feedback object according to specification
                summary_text = "Solid technical knowledge demonstrated throughout the interview."
                strengths = ["Strong core concepts", "Clear explanations"]
                gaps = ["Could elaborate on multi-agent orchestration"]
                next_steps = ["Review advanced deployment patterns"]

                if fb_report:
                    if hasattr(fb_report.summary, "overall_assessment"):
                        summary_text = fb_report.summary.overall_assessment
                    elif isinstance(fb_report.summary, str):
                        summary_text = fb_report.summary

                    if fb_report.strengths:
                        strengths = fb_report.strengths[:5]
                    if fb_report.weaknesses:
                        gaps = fb_report.weaknesses[:5]
                    if fb_report.recommendations:
                        next_steps = [
                            f"Study {rec.topic_title} (Day {rec.curriculum_day})"
                            if hasattr(rec, "topic_title") else str(rec)
                            for rec in fb_report.recommendations[:5]
                        ]

                feedback_payload = HackathonFeedbackModel(
                    summary=summary_text,
                    strengths=strengths,
                    gaps=gaps,
                    next=next_steps,
                )

                return HackathonInterviewResponse(
                    reply="Interview completed. Thank you for participating in the technical interview.",
                    done=True,
                    feedback=feedback_payload,
                )
            else:
                next_q = answer_data.next_question
                q_text = next_q.question_text if next_q else "Next question..."
                q_num = answer_data.current_question_index + 1
                reply_msg = f"Thank you for your response.\n\nQuestion {q_num}: {q_text}"

                return HackathonInterviewResponse(
                    reply=reply_msg,
                    done=False,
                    feedback=None,
                )
        except InvalidInterviewStateError as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
        except InterviewAlreadyCompletedError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request payload. Must provide 'candidate' object or 'message' string.")
