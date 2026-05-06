"""Domain-specific exceptions."""


class DomainError(Exception):
    """Base exception for domain rule violations."""


class DomainValidationError(DomainError):
    """Raised when a domain entity receives invalid data."""
