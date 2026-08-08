from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from app.services.curriculum_service import CurriculumService, get_curriculum_service
from app.models.curriculum import CurriculumModel, DayModel, TopicModel

router = APIRouter(prefix="/curriculum", tags=["Curriculum"])


@router.get(
    "",
    response_model=CurriculumModel,
    summary="Get All Curriculum",
    description="Returns the full cached curriculum structure including modules and daily schedules.",
    status_code=200,
)
@router.get(
    "/",
    response_model=CurriculumModel,
    summary="Get All Curriculum (Trailing Slash)",
    description="Returns the full cached curriculum structure including modules and daily schedules.",
    status_code=200,
)
def get_curriculum(
    service: CurriculumService = Depends(get_curriculum_service),
):
    return service._get_cache()


@router.get(
    "/search",
    response_model=List[TopicModel],
    summary="Search Curriculum Topics",
    description="Searches curriculum topics matching a keyword across titles and categories.",
    status_code=200,
)
def search_curriculum_topics(
    keyword: str = Query(..., min_length=1, description="Search keyword for topics"),
    service: CurriculumService = Depends(get_curriculum_service),
):
    return service.search_topic(keyword)


@router.get(
    "/day/{day_number}",
    response_model=DayModel,
    summary="Get Curriculum Day",
    description="Returns detailed curriculum data for a specific day_number.",
    status_code=200,
)
def get_curriculum_day(
    day_number: int,
    service: CurriculumService = Depends(get_curriculum_service),
):
    day = service.get_day(day_number)
    if not day:
        raise HTTPException(
            status_code=404,
            detail=f"Day number {day_number} not found in curriculum."
        )
    return day
