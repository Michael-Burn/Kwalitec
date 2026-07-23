"""Identity tokens for Adaptive Revision Planning.

Opaque, immutable identifiers scoped to this application package.
Identities are not database keys and carry no persistence semantics.
"""

from __future__ import annotations

from dataclasses import dataclass

from application.education.revision_planner.errors import ScheduleInvariantViolation


def _require_identity(value: str | None, type_name: str) -> str:
    if value is None:
        raise ScheduleInvariantViolation(
            f"{type_name} is required",
            invariant=f"{type_name}.required",
        )
    cleaned = value.strip()
    if not cleaned:
        raise ScheduleInvariantViolation(
            f"{type_name} must be non-empty",
            invariant=f"{type_name}.non_empty",
        )
    if any(ch.isspace() for ch in cleaned):
        raise ScheduleInvariantViolation(
            f"{type_name} must not contain whitespace",
            invariant=f"{type_name}.no_whitespace",
        )
    return cleaned


@dataclass(frozen=True, slots=True)
class ScheduleId:
    """Identity of a single StudySchedule produced by the planner."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "value", _require_identity(self.value, "ScheduleId")
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class SessionId:
    """Identity of a single StudySession within a StudySchedule."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", _require_identity(self.value, "SessionId"))

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class DayId:
    """Identity of a single StudyDay within a StudySchedule."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", _require_identity(self.value, "DayId"))

    def __str__(self) -> str:
        return self.value
