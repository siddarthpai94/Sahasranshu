"""Custom exceptions."""


class SahasranshuError(Exception):
    """Base exception for sahasranshu."""

    pass


class PDFProcessingError(SahasranshuError):
    """Error during PDF processing."""

    pass


class LLMError(SahasranshuError):
    """Error during LLM operations."""

    pass


class ValidationError(SahasranshuError):
    """Error during validation."""

    pass
