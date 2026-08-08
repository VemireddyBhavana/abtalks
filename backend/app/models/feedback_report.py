from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class CategoryScoreModel(BaseModel):
    """Category weighted score detail model."""
    category_name: str = Field(description="Category name (e.g. Technical Accuracy)")
    score: float = Field(ge=0.0, le=100.0, description="Raw category score out of 100")
    weight: float = Field(ge=0.0, le=1.0, description="Category weight factor")
    weighted_score: float = Field(ge=0.0, le=100.0, description="Weighted contribution")
    evaluation_notes: str = Field(default="")


class OverallScoreModel(BaseModel):
    """Overall score summary model."""
    overall_score: float = Field(ge=0.0, le=100.0, description="Final weighted score out of 100")
    grade: str = Field(description="Grade designation (A+, A, B, C, D, F)")
    rating_label: str = Field(description="Rating label (e.g. Exceptional, Strong, Proficient, Developing)")
    breakdown: List[CategoryScoreModel] = Field(default_factory=list)


class KnowledgeGapModel(BaseModel):
    """Identified knowledge gap model."""
    topic_id: str = Field(description="Topic ID")
    topic_title: str = Field(description="Topic Title")
    day_number: int = Field(description="Curriculum Day Number")
    description: str = Field(description="Description of detected knowledge gap")
    severity: str = Field(default="Medium", description="Severity: High | Medium | Low")


class RecommendationModel(BaseModel):
    """Actionable candidate study recommendation model."""
    topic_title: str = Field(description="Topic Title")
    curriculum_day: int = Field(description="Curriculum Day Number")
    learning_objectives: List[str] = Field(default_factory=list, description="Objectives to revisit")
    recommended_action: str = Field(description="Specific study/practice recommendation")
    priority: str = Field(default="Medium", description="Priority: High | Medium | Low")


class FeedbackSummaryModel(BaseModel):
    """Executive narrative summary model."""
    overall_performance: str = Field(description="Overall performance narrative")
    interview_highlights: List[str] = Field(default_factory=list, description="Key technical highlights")
    areas_for_improvement: List[str] = Field(default_factory=list, description="Targeted growth areas")
    learning_progress: str = Field(description="Assessment of learning progression")
    communication_assessment: str = Field(description="Clarity and articulation assessment")


class FeedbackReportModel(BaseModel):
    """Complete, structured final interview feedback report model."""
    session_id: str = Field(description="Interview session ID")
    candidate_id: str = Field(description="Candidate ID")
    generated_at: str = Field(description="ISO timestamp of report generation")
    overall_score: OverallScoreModel = Field(description="Overall score metrics")
    strengths: List[str] = Field(default_factory=list, description="Key candidate strengths")
    weaknesses: List[str] = Field(default_factory=list, description="Identified candidate weaknesses")
    knowledge_gaps: List[KnowledgeGapModel] = Field(default_factory=list, description="Detected knowledge gaps")
    topics_covered: List[str] = Field(default_factory=list, description="Topics asked during session")
    curriculum_coverage: Dict[str, Any] = Field(default_factory=dict, description="Day & topic coverage statistics")
    recommendations: List[RecommendationModel] = Field(default_factory=list, description="Curriculum-aligned study recommendations")
    summary: FeedbackSummaryModel = Field(description="Executive narrative summary")
