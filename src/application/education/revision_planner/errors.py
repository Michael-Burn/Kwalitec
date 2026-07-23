"""Application errors for Adaptive Revision Planning.

Coordination and scheduling failures — not educational domain invariants.
"""

from __future__ import annotations

from application.errors import ApplicationError


class RevisionPlanningError(ApplicationError):
    """Raised when revision planning cannot proceed from its inputs."""

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.code = (code or "").strip() or None


class ScheduleInvariantViolation(RevisionPlanningError):  # noqa: N818
    """Raised when a schedule model invariant is breached at construction."""

    def __init__(self, message: str, *, invariant: str | None = None) -> None:
        super().__init__(message, code="schedule_invariant")
        self.invariant = (invariant or "").strip() or None


class ScheduleValidationError(RevisionPlanningError):
    """Raised when a schedule fails structural or policy validation."""

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message, code=code or "schedule_validation")
