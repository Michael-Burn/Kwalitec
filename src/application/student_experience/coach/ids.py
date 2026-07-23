"""Typed identifiers for AI Learning Coach artefacts."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.coach.errors import CoachInvariantViolation


@dataclass(frozen=True, slots=True)
class CoachId:
    """Opaque identifier for a composed coaching context."""

    value: str

    def __post_init__(self) -> None:
        value = (self.value or "").strip()
        if not value:
            raise CoachInvariantViolation(
                "CoachId value must be a non-empty string",
                invariant="CoachId.value.required",
            )
        object.__setattr__(self, "value", value)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class ConversationId:
    """Opaque identifier for a composed conversation context."""

    value: str

    def __post_init__(self) -> None:
        value = (self.value or "").strip()
        if not value:
            raise CoachInvariantViolation(
                "ConversationId value must be a non-empty string",
                invariant="ConversationId.value.required",
            )
        object.__setattr__(self, "value", value)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class CoachSnapshotId:
    """Opaque identifier for a CoachSnapshot."""

    value: str

    def __post_init__(self) -> None:
        value = (self.value or "").strip()
        if not value:
            raise CoachInvariantViolation(
                "CoachSnapshotId value must be a non-empty string",
                invariant="CoachSnapshotId.value.required",
            )
        object.__setattr__(self, "value", value)

    def __str__(self) -> str:
        return self.value
