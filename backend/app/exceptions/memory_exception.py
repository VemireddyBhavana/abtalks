class MemoryError(Exception):
    """Base exception for all Breeth Memory subsystem errors."""
    pass


class MemoryReadError(MemoryError):
    """Raised when memory retrieval fails."""
    pass


class MemoryWriteError(MemoryError):
    """Raised when memory persistence fails."""
    pass


class MemoryConnectionError(MemoryError):
    """Raised when connecting to Breeth Memory API fails."""
    pass


class MemoryCredentialsMissingError(MemoryError):
    """Raised when BREETH_API_KEY or project credentials are missing."""
    pass


class MemoryValidationError(MemoryError):
    """Raised when InterviewMemory schema validation fails before persistence."""
    pass


class MemoryMigrationError(MemoryError):
    """Raised when memory document schema migration fails."""
    pass


class MemoryCacheError(MemoryError):
    """Raised when MemoryCache operations fail."""
    pass


class MemoryRetryExhaustedError(MemoryError):
    """Raised when memory retries are exhausted."""
    pass
