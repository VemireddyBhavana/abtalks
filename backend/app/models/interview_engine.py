from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class QuestionPlaceholderModel(BaseModel):
    id: str = Field(..., description="Unique question identifier e.g. q_day1_react")
    day_number: int = Field(..., ge=1, description="Curriculum day index")
    topic_id: str = Field(..., description="Curriculum topic ID")
    topic_title: str = Field(..., description="Curriculum topic title")
    question_text: str = Field(..., description="Placeholder question prompt text")
    difficulty: str = Field(default="Intermediate", description="Question difficulty tier: Fundamental, Intermediate, Advanced")


class InterviewPlanModel(BaseModel):
    session_id: str = Field(..., description="Unique session identifier")
    candidate_id: str = Field(..., description="Candidate ID")
    created_at: str = Field(..., description="ISO formatted creation timestamp")
    questions: List[QuestionPlaceholderModel] = Field(..., min_length=8, max_length=8, description="Ordered 8-question sequence")


class StartInterviewRequestModel(BaseModel):
    candidate_id: Optional[str] = Field(default="cand_alex_dev_99", description="Candidate ID to initiate session")
    session_id: Optional[str] = Field(default=None, description="Optional custom session ID; auto-generated if omitted")


class StartInterviewResponseModel(BaseModel):
    session_id: str = Field(..., description="Unique session identifier")
    message: str = Field(default="Interview session started successfully.")
    total_questions: int = Field(default=8, description="Total questions planned")
    current_question_index: int = Field(default=0, description="Current question zero-based index")
    question: QuestionPlaceholderModel = Field(..., description="First placeholder question")


class AnswerSubmissionModel(BaseModel):
    session_id: str = Field(..., description="Active session ID")
    answer_text: str = Field(..., min_length=1, description="Candidate response text")


class AnswerInterviewResponseModel(BaseModel):
    session_id: str = Field(..., description="Active session ID")
    message: str = Field(..., description="Status message")
    done: bool = Field(..., description="True if interview is completed (after Q8)")
    current_question_index: int = Field(..., description="Next zero-based question index")
    total_questions: int = Field(default=8, description="Total questions in plan")
    next_question: Optional[QuestionPlaceholderModel] = Field(default=None, description="Next question model (None if done)")


class InterviewStateModel(BaseModel):
    session_id: str
    candidate_id: str
    current_question_index: int
    done: bool
    total_questions: int
    asked_question_ids: List[str]
    candidate_answers: List[Dict[str, Any]]
    days_covered: List[int]
    topics_covered: List[str]
    started_at: str
    completed_at: Optional[str] = None


class InterviewSummaryModel(BaseModel):
    session_id: str
    candidate_id: str
    total_questions_asked: int
    distinct_days_covered_count: int
    distinct_topics_covered_count: int
    days_covered: List[int]
    topics_covered: List[str]
    started_at: str
    completed_at: Optional[str] = None
    done: bool
