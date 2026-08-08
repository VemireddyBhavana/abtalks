class LLMError(Exception):
    """Base exception for LLM service domain errors."""
    pass


class LLMProviderError(LLMError):
    """Raised when an LLM provider fails to generate a response or encounters an API error."""
    pass


class LLMApiKeyMissingError(LLMError):
    """Raised when the required API key for the selected LLM provider is missing or empty."""
    pass


class LLMResponseParsingError(LLMError):
    """Raised when parsing or validating the LLM's response JSON output fails."""
    pass


class LLMTimeoutError(LLMError):
    """Raised when the LLM provider API request times out."""
    pass
