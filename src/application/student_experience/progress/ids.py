"""Typed identifiers for Learning Journey Experience artefacts."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.progress.errors import JourneyInvariantViolation


@dataclass(frozen=True, slots=True)
class JourneyId:
    """Opaque identifier for a composed learning journey view."""

    value: str

    def __post_init__(self) -> None:
        value = (self.value or "").strip()
        if not value:
            raise JourneyInvariantViolation(
                "JourneyId value must be a non-empty string",
                invariant="JourneyId.value.required",
            )
        object.__setattr__(self, "value", value)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class JourneySnapshotId:
    """Opaque identifier for a JourneySnapshot."""

    value: str

    def __post_init__(self) -> None:
        value = (self.value or "").strip()
        if not value:
            raise JourneyInvariantViolation(
                "JourneySnapshotId value must be a non-empty string",
                invariant="JourneySnapshotId.value.required",
            )
        object.__setattr__(self, "value", value)

    def __str__(self) -> str:
        return self.value
