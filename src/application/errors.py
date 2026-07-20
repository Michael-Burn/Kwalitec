"""Application-layer errors (coordination failures, not educational rules)."""

from __future__ import annotations


class ApplicationError(Exception):
    """Base error for application coordination failures."""

    def __init__(self, message: str) -> None:
        cleaned = (message or "").strip() or "application error"
        super().__init__(cleaned)
        self.message = cleaned


class NotFoundError(ApplicationError):
    """Raised when a required aggregate cannot be loaded."""

    def __init__(self, resource: str, identity: str) -> None:
        super().__init__(f"{resource} not found: {identity}")
        self.resource = resource
        self.identity = identity


class ConflictError(ApplicationError):
    """Raised when a command conflicts with current aggregate state."""
