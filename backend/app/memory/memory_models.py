from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from app.models.feedback_report import FeedbackReportModel


class SessionMemory(BaseModel):
    """Session metadata memory model."""
    session_id: str = Field(description="Unique interview session ID")
    candidate_id: str = Field(description="Candidate identifier")
    started_at: str = Field(description="ISO timestamp when started")
    completed_at: Optional[str] = Field(default=None, description="ISO timestamp when finished")
    done: bool = Field(default=False, description="True if completed")
    total_questions: int = Field(default=8, description="Total planned questions")
    current_question_index: int = Field(default=0, description="Current question index")


class CandidateMemory(BaseModel):
    """Candidate profile snapshot memory model."""
    candidate_id: str = Field(description="Candidate ID")
    full_name: str = Field(description="Candidate Name")
    target_role: str = Field(default="Full Stack AI Engineer", description="Target Application Position")
    current_day: int = Field(default=1, description="Candidate current curriculum day")
    completed_topics: List[str] = Field(default_factory=list)


class EvaluationMemory(BaseModel):
    """Per-turn answer evaluation memory model."""
    turn_index: int = Field(description="Turn index (0-indexed)")
    question_id: str = Field(description="Question ID")
    topic_id: str = Field(description="Topic ID")
    topic_title: str = Field(description="Topic Title")
    question_text: str = Field(description="Question text")
    candidate_answer: str = Field(description="Candidate answer text")
    score: int = Field(description="Answer evaluation score (0-100)")
    classification: str = Field(description="Quality classification")
    confidence_score: int = Field(description="Confidence metric")
    action_type: str = Field(description="Chosen follow-up strategy action")
    difficulty: str = Field(description="Active question difficulty level")


class FeedbackMemory(BaseModel):
    """Final feedback report memory model wrapper."""
    overall_score: float = Field(ge=0.0, le=100.0)
    grade: str = Field(description="Grade designation")
    rating_label: str = Field(description="Rating label")
    report_json: Dict[str, Any] = Field(default_factory=dict, description="Full serialized FeedbackReportModel")


class InterviewMemory(BaseModel):
    """
    Root Interview Memory document representing complete persistent interview state.
    """
    memory_id: str = Field(description="Unique memory document ID")
    session: SessionMemory = Field(description="Session metadata memory")
    candidate: CandidateMemory = Field(description="Candidate profile memory")
    turns: List[EvaluationMemory] = Field(default_factory=list, description="All turn evaluations")
    knowledge_gaps: List[Dict[str, Any]] = Field(default_factory=list, description="Detected knowledge gaps")
    feedback: Optional[FeedbackMemory] = Field(default=None, description="Final feedback report memory")
    updated_at: str = Field(description="ISO timestamp when updated")
