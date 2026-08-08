from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends, status
from app.services.interview_engine import InterviewEngine, get_interview_engine
from app.services.interview_validator import InterviewValidator
from app.models.interview_engine import (
    StartInterviewRequestModel,
    StartInterviewResponseModel,
    AnswerSubmissionModel,
    AnswerInterviewResponseModel,
    InterviewStateModel,
    InterviewSummaryModel,
)
from app.exceptions.interview_exception import (
    InvalidInterviewStateError,
    InterviewAlreadyCompletedError,
    InterviewPlanError,
)

router = APIRouter(prefix="/interview", tags=["Interview Engine"])


@router.post(
    "/start",
    response_model=StartInterviewResponseModel,
    summary="Start Interview Session",
    description="Initializes a new interview session, creates an 8-question plan using Strategy Pattern covering >=4 curriculum days, validates plan, and returns Question 1.",
    status_code=status.HTTP_200_OK,
)
def start_interview(
    body: StartInterviewRequestModel = StartInterviewRequestModel(),
    engine: InterviewEngine = Depends(get_interview_engine),
):
    try:
        return engine.start_interview(
            candidate_id=body.candidate_id or "cand_alex_dev_99",
            session_id=body.session_id,
        )
    except InterviewPlanError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


@router.post(
    "/answer",
    response_model=AnswerInterviewResponseModel,
    summary="Submit Candidate Answer",
    description="Records candidate's answer, advances question index, and returns next question or done=true after Question 8.",
    status_code=status.HTTP_200_OK,
)
def submit_answer(
    body: AnswerSubmissionModel,
    engine: InterviewEngine = Depends(get_interview_engine),
):
    try:
        return engine.submit_answer(session_id=body.session_id, answer_text=body.answer_text)
    except InvalidInterviewStateError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InterviewAlreadyCompletedError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


@router.get(
    "/{session_id}",
    response_model=InterviewStateModel,
    summary="Get Session State",
    description="Retrieves current active session state model including answered questions and progress.",
    status_code=status.HTTP_200_OK,
)
def get_session_state(
    session_id: str,
    engine: InterviewEngine = Depends(get_interview_engine),
):
    try:
        return engine.get_session_state(session_id)
    except InvalidInterviewStateError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get(
    "/{session_id}/summary",
    response_model=InterviewSummaryModel,
    summary="Get Session Summary",
    description="Retrieves high-level summary metadata including days and topics covered.",
    status_code=status.HTTP_200_OK,
)
def get_interview_summary(
    session_id: str,
    engine: InterviewEngine = Depends(get_interview_engine),
):
    try:
        return engine.get_interview_summary(session_id)
    except InvalidInterviewStateError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get(
    "/{session_id}/validate",
    response_model=Dict[str, Any],
    summary="Validate Session Plan",
    description="Runs pre-flight validation report on session plan.",
    status_code=status.HTTP_200_OK,
)
def validate_session_plan(
    session_id: str,
    engine: InterviewEngine = Depends(get_interview_engine),
):
    try:
        session = engine.state_manager.get_session(session_id)
        if not session:
            raise InvalidInterviewStateError(f"Session '{session_id}' not found.")
        validator = InterviewValidator()
        return validator.validate_plan(session.plan)
    except InvalidInterviewStateError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
