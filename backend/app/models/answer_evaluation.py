from typing import List, Optional
from pydantic import BaseModel, Field


class RubricScoreModel(BaseModel):
    """Weighted rubric score breakdown model."""
    technical_accuracy: int = Field(ge=0, le=100, default=75)
    concept_coverage: int = Field(ge=0, le=100, default=75)
    terminology: int = Field(ge=0, le=100, default=70)
    reasoning: int = Field(ge=0, le=100, default=70)
    examples: int = Field(ge=0, le=100, default=60)
    completeness: int = Field(ge=0, le=100, default=70)
    weighted_total_score: float = Field(ge=0.0, le=100.0, default=72.5)


class ConfidenceMetricsModel(BaseModel):
    """Metrics model evaluating candidate answer confidence and depth."""
    confidence: int = Field(ge=0, le=100, default=75)
    technical_depth: int = Field(ge=0, le=100, default=70)
    conceptual_understanding: int = Field(ge=0, le=100, default=75)
    completeness: int = Field(ge=0, le=100, default=70)
    communication_clarity: int = Field(ge=0, le=100, default=80)


class AnswerEvaluationModel(BaseModel):
    """Complete evaluation report model for a candidate turn response."""
    score: int = Field(ge=0, le=100, description="Overall score out of 100")
    confidence_score: int = Field(ge=0, le=100, description="Confidence rating out of 100")
    classification: str = Field(description="Classification: Excellent | Good | Average | Weak | Incorrect | Unclear")
    rubric: RubricScoreModel = Field(default_factory=RubricScoreModel)
    metrics: ConfidenceMetricsModel = Field(default_factory=ConfidenceMetricsModel)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    gaps: List[str] = Field(default_factory=list)
    recommended_action: str = Field(default="Medium Followup")


class FollowUpDecisionModel(BaseModel):
    """Adaptive follow-up action model."""
    action_type: str = Field(description="Action type: Deeper Probe | Medium Followup | Clarification | Simpler Explanation | Transition")
    follow_up_question_text: Optional[str] = Field(default=None, description="Generated follow-up question text")
    rationale: str = Field(default="Adaptive question selected based on classification.")
    topic_transition: bool = Field(default=False, description="True if advancing to next curriculum topic")
