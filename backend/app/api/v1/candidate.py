from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from app.services.candidate_service import CandidateService, get_candidate_service
from app.models.candidate import CandidateModel, ProgressModel, CandidateSummaryModel

router = APIRouter(prefix="/candidate", tags=["Candidate"])


@router.get(
    "",
    response_model=CandidateModel,
    summary="Get Candidate Profile",
    description="Returns the full cached candidate profile details including progress and learning signals.",
    status_code=200,
)
@router.get(
    "/",
    response_model=CandidateModel,
    summary="Get Candidate Profile (Trailing Slash)",
    description="Returns the full cached candidate profile details including progress and learning signals.",
    status_code=200,
)
def get_candidate(
    service: CandidateService = Depends(get_candidate_service),
):
    return service.get_candidate()


@router.get(
    "/progress",
    response_model=ProgressModel,
    summary="Get Candidate Progress",
    description="Returns candidate progress metrics (completed days, total days, percentage).",
    status_code=200,
)
def get_candidate_progress(
    service: CandidateService = Depends(get_candidate_service),
):
    return service.get_candidate().progress


@router.get(
    "/analytics",
    response_model=Dict[str, Any],
    summary="Get Candidate Analytics",
    description="Returns computed analytics metrics including completion rate, strongest topics, and areas for growth.",
    status_code=200,
)
def get_candidate_analytics(
    service: CandidateService = Depends(get_candidate_service),
):
    return {
        "candidate_id": service.get_candidate().candidate_id,
        "completion_rate": service.get_completion_rate(),
        "total_completed_days": service.get_total_completed_days(),
        "total_remaining_days": service.get_total_remaining_days(),
        "strongest_topics": service.get_strongest_topics(),
        "weakest_topics": service.get_weakest_topics(),
    }
