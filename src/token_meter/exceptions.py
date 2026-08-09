class TokenMeterError(Exception):
    """Base exception for Token Meter."""


class AuthenticationError(TokenMeterError):
    """Raised when the provider rejects the API key."""


class ModelNotFoundError(TokenMeterError):
    """Raised when the requested model is invalid or unavailable."""


class RateLimitError(TokenMeterError):
    """Raised when the provider rate-limits the request."""


class NetworkError(TokenMeterError):
    """Raised when the provider cannot be reached."""


class ContextWindowError(TokenMeterError):
    """Raised when the prompt exceeds the model context window."""
