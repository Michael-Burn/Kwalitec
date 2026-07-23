"""Application errors for Adaptive Mission Generation.

Coordination and planning failures — not educational domain invariants.
"""

from __future__ import annotations

from application.errors import ApplicationError


class MissionGenerationError(ApplicationError):
    """Raised when mission generation cannot proceed from its inputs."""

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.code = (code or "").strip() or None


class MissionInvariantViolation(MissionGenerationError):  # noqa: N818
    """Raised when a mission model invariant is breached at construction."""

    def __init__(self, message: str, *, invariant: str | None = None) -> None:
        super().__init__(message, code="mission_invariant")
        self.invariant = (invariant or "").strip() or None
