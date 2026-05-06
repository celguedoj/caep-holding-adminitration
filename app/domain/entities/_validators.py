"""Shared entity validation helpers."""

from app.domain.exceptions import DomainValidationError
from app.domain.types import Email


def require_text(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise DomainValidationError(f"{field_name} cannot be empty.")
    return normalized


def optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None


def require_email(value: Email) -> Email:
    normalized = str(value).strip().lower()
    if "@" not in normalized or normalized.startswith("@") or normalized.endswith("@"):
        raise DomainValidationError("email must be valid.")
    return Email(normalized)
