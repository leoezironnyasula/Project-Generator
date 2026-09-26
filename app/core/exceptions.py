"""
Custom exceptions for the app.
app/core/exceptions.py

Using our own exception types (instead of generic Exception) makes it
possible to catch specific failure modes later — e.g. the API layer
can catch LLMConnectionError and return a clean error message instead
of a raw stack trace.
"""


class ProjectGeneratorError(Exception):
    """Base class for all custom errors in this app."""
    pass


class LLMConnectionError(ProjectGeneratorError):
    """Raised when the local LLM server (Ollama/LM Studio) can't be reached."""
    pass


class LLMResponseError(ProjectGeneratorError):
    """Raised when the LLM responds, but the output can't be parsed into a Project."""
    pass


class ScaffoldError(ProjectGeneratorError):
    """Raised when creating the project folder/files on disk fails."""
    pass


class UnsupportedDomainError(ProjectGeneratorError):
    """Raised when a Domain has no scaffold template and no generic fallback applies."""
    pass