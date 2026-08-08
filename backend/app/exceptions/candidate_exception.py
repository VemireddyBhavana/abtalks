class CandidateError(Exception):
    """Base exception class for Candidate domain errors."""
    pass


class CandidateNotFoundError(CandidateError):
    """Raised when candidate JSON file or profile data is missing."""
    pass


class CandidateValidationError(CandidateError):
    """Raised when candidate JSON schema validation fails or JSON is corrupted."""
    pass
