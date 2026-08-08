from typing import List, Optional
from pydantic import BaseModel, Field


class ProgressModel(BaseModel):
    completed_days: List[int] = Field(default_factory=list, description="List of completed day numbers")
    incomplete_days: List[int] = Field(default_factory=list, description="List of incomplete day numbers")
    total_days: int = Field(default=0, ge=0, description="Total days in curriculum")
    progress_percentage: float = Field(default=0.0, ge=0.0, le=100.0, description="Computed percentage complete")


class LearningSignalModel(BaseModel):
    category: str = Field(..., description="Signal classification e.g. Strength or Area for Growth")
    signal: str = Field(..., description="Descriptive observations")
    score: int = Field(default=0, ge=0, le=100, description="Evaluated score metric")


class RecentActivityModel(BaseModel):
    day_number: int = Field(..., description="Associated day number")
    activity_type: str = Field(..., description="Action or assessment description")
    timestamp: str = Field(..., description="ISO formatted timestamp")


class CandidateModel(BaseModel):
    candidate_id: str = Field(..., description="Unique candidate ID")
    full_name: str = Field(..., description="Candidate full name")
    email: str = Field(..., description="Candidate email address")
    target_role: str = Field(..., description="Target application position")
    experience_level: str = Field(default="Mid-Level", description="Experience tier")
    progress: ProgressModel = Field(..., description="Candidate progress breakdown")
    completed_topics: List[str] = Field(default_factory=list, description="List of completed topic IDs")
    skipped_topics: List[str] = Field(default_factory=list, description="List of skipped topic IDs")
    learning_signals: List[LearningSignalModel] = Field(default_factory=list, description="Observed learning signals")
    recent_activity: List[RecentActivityModel] = Field(default_factory=list, description="Audit log of recent activity")


class CandidateSummaryModel(BaseModel):
    candidate_id: str
    full_name: str
    target_role: str
    progress_percentage: float
    completed_days_count: int
    total_days_count: int
    completed_topics_count: int
    learning_signals_count: int
