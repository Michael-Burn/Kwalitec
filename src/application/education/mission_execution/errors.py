"""Application errors for Mission Execution.

Coordination and lifecycle failures — not educational domain invariants.

Expected lifecycle / command violations are returned as
``MissionExecutionError`` value objects (never raised). Construction and
programming invariants may raise ``MissionExecutionInvariantViolation``.
"""

from __future__ import annotations

from dataclasses import dataclass

from application.errors import ApplicationError


@dataclass(frozen=True, slots=True)
class MissionExecutionError:
    """Deterministic application error returned (not raised) by the engine.

    Used for expected state violations such as illegal lifecycle
    transitions. Callers inspect ``code`` / ``message``; the engine never
    raises this type.
    """

    code: str
    message: str
    from_status: str | None = None
    attempted: str | None = None

    def __post_init__(self) -> None:
        code = (self.code or "").strip()
        message = (self.message or "").strip()
        if not code:
            object.__setattr__(self, "code", "mission_execution_error")
        else:
            object.__setattr__(self, "code", code)
        if not message:
            object.__setattr__(self, "message", "mission execution error")
        else:
            object.__setattr__(self, "message", message)

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


class MissionExecutionInvariantViolation(ApplicationError):  # noqa: N818
    """Raised when a mission execution model invariant is breached."""

    def __init__(self, message: str, *, invariant: str | None = None) -> None:
        super().__init__(message)
        self.invariant = (invariant or "").strip() or None
