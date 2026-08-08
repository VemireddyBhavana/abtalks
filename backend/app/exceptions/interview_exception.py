class InterviewError(Exception):
    """Base exception for Interview domain errors."""
    pass


class InterviewAlreadyCompletedError(InterviewError):
    """Raised when an action is attempted on an already finished interview session."""
    pass


class InterviewPlanError(InterviewError):
    """Raised when interview plan generation or topic selection fails."""
    pass


class QuestionNotFoundError(InterviewError):
    """Raised when a requested question ID is missing from QuestionBank or plan."""
    pass


class InvalidInterviewStateError(InterviewError):
    """Raised when invalid state transitions or uninitialized sessions are accessed."""
    pass


class QuestionBankError(InterviewError):
    """Raised when QuestionBank integrity checks fail."""
    pass
