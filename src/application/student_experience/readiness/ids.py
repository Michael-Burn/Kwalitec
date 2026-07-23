"""Typed identifiers for Exam Readiness Experience artefacts."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.readiness.errors import (
    ReadinessInvariantViolation,
)


@dataclass(frozen=True, slots=True)
class ReadinessId:
    """Opaque identifier for a composed exam readiness view."""

    value: str

    def __post_init__(self) -> None:
        value = (self.value or "").strip()
        if not value:
            raise ReadinessInvariantViolation(
                "ReadinessId value must be a non-empty string",
                invariant="ReadinessId.value.required",
            )
        object.__setattr__(self, "value", value)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class ReadinessSnapshotId:
    """Opaque identifier for a ReadinessSnapshot."""

    value: str

    def __post_init__(self) -> None:
        value = (self.value or "").strip()
        if not value:
            raise ReadinessInvariantViolation(
                "ReadinessSnapshotId value must be a non-empty string",
                invariant="ReadinessSnapshotId.value.required",
            )
        object.__setattr__(self, "value", value)

    def __str__(self) -> str:
        return self.value
