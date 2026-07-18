"""Shared identity / text validation helpers for curriculum entities."""

from __future__ import annotations


def require_non_empty(value: str, field_name: str) -> str:
    """Return stripped non-empty string or raise ValueError."""
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def optional_non_empty(value: str | None) -> str | None:
    """Return stripped string, or None when blank / absent."""
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None
