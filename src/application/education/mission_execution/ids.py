"""Identity tokens for Mission Execution.

Opaque, immutable identifiers scoped to this application package.
Identities are not database keys and carry no persistence semantics.
"""

from __future__ import annotations

from dataclasses import dataclass

from application.education.mission_execution.errors import (
    MissionExecutionInvariantViolation,
)


def _require_identity(value: str | None, type_name: str) -> str:
    if value is None:
        raise MissionExecutionInvariantViolation(
            f"{type_name} is required",
            invariant=f"{type_name}.required",
        )
    cleaned = value.strip()
    if not cleaned:
        raise MissionExecutionInvariantViolation(
            f"{type_name} must be non-empty",
            invariant=f"{type_name}.non_empty",
        )
    if any(ch.isspace() for ch in cleaned):
        raise MissionExecutionInvariantViolation(
            f"{type_name} must not contain whitespace",
            invariant=f"{type_name}.no_whitespace",
        )
    return cleaned


@dataclass(frozen=True, slots=True)
class ExecutionId:
    """Identity of a single MissionExecution runtime instance."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "value", _require_identity(self.value, "ExecutionId")
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class StudentId:
    """Identity of the student owning a MissionExecution."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "value", _require_identity(self.value, "StudentId")
        )

    def __str__(self) -> str:
        return self.value
