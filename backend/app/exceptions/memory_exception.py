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
