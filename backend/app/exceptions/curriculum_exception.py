class CurriculumError(Exception):
    """Base exception class for Curriculum domain errors."""
    pass


class CurriculumNotFoundError(CurriculumError):
    """Raised when the curriculum JSON file or requested day/module item is missing."""
    pass


class CurriculumValidationError(CurriculumError):
    """Raised when curriculum JSON schema validation fails or JSON is corrupted."""
    pass
