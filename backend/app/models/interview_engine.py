from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from app.models.feedback_report import FeedbackReportModel


class QuestionPlaceholderModel(BaseModel):
    """Placeholder Model representing an interview question."""
    id: str = Field(description="Unique question identifier")
    day_number: int = Field(ge=1, description="Curriculum day number (1-indexed)")
    topic_id: str = Field(description="Associated curriculum topic ID")
    topic_title: str = Field(description="Associated curriculum topic title")
    question_text: str = Field(description="The interview question text presented to candidate")
    difficulty: str = Field(default="Intermediate", description="Difficulty tier: Fundamental | Intermediate | Advanced")


class InterviewPlanModel(BaseModel):
    """Model representing an 8-question interview plan covering >=4 curriculum days."""
    session_id: str = Field(description="Unique session identifier")
    candidate_id: str = Field(description="Candidate identifier")
    created_at: str = Field(description="ISO timestamp when plan was generated")
    questions: List[QuestionPlaceholderModel] = Field(description="List of 8 planned questions")


class StartInterviewRequestModel(BaseModel):
    """Request model for starting an interview session."""
    candidate_id: Optional[str] = Field(default="cand_alex_dev_99", description="Target candidate ID")
    session_id: Optional[str] = Field(default=None, description="Optional custom session ID")


class StartInterviewResponseModel(BaseModel):
    """Response model after starting an interview session."""
    session_id: str = Field(description="Active session ID")
    message: str = Field(description="Status message")
    total_questions: int = Field(default=8, description="Total planned questions")
    current_question_index: int = Field(default=0, description="Index of active question (0-indexed)")
    question: QuestionPlaceholderModel = Field(description="Question 1 model")


class AnswerSubmissionModel(BaseModel):
    """Request model for submitting an answer."""
    session_id: str = Field(description="Active session ID")
    answer_text: str = Field(description="Candidate's technical answer text")


class AnswerInterviewResponseModel(BaseModel):
    """Response model after submitting an answer."""
    session_id: str = Field(description="Active session ID")
    message: str = Field(description="Status message")
    done: bool = Field(description="True if all 8 questions completed")
    current_question_index: int = Field(description="Active question index")
    total_questions: int = Field(description="Total planned questions")
    next_question: Optional[QuestionPlaceholderModel] = Field(default=None, description="Next question model (None if done)")
    feedback_report: Optional[FeedbackReportModel] = Field(default=None, description="Final feedback report (populated when done=true)")


class InterviewStateModel(BaseModel):
    """Full session state representation model."""
    session_id: str = Field(description="Active session ID")
    candidate_id: str = Field(description="Candidate ID")
    current_question_index: int = Field(description="Current question index")
    total_questions: int = Field(description="Total questions in plan")
    done: bool = Field(description="True if session completed")
    topics_covered: List[str] = Field(default_factory=list)
    days_covered: List[int] = Field(default_factory=list)
    candidate_answers: List[Dict[str, Any]] = Field(default_factory=list)


class InterviewSummaryModel(BaseModel):
    """High-level interview summary metadata model."""
    session_id: str = Field(description="Session ID")
    candidate_id: str = Field(description="Candidate ID")
    total_questions_asked: int = Field(description="Total questions asked")
    distinct_days_covered_count: int = Field(description="Number of distinct curriculum days covered")
    distinct_topics_covered_count: int = Field(description="Number of distinct topics covered")
    days_covered: List[int] = Field(description="List of covered curriculum day numbers")
    topics_covered: List[str] = Field(description="List of covered topic IDs")
    started_at: str = Field(description="ISO timestamp when started")
    completed_at: Optional[str] = Field(default=None, description="ISO timestamp when completed")
    done: bool = Field(description="True if session completed")
    feedback_report: Optional[FeedbackReportModel] = Field(default=None, description="Final feedback report (populated if completed)")
