"""Typed identifiers for Student Home Experience artefacts."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.home.errors import HomeInvariantViolation


@dataclass(frozen=True, slots=True)
class HomeId:
    """Opaque identifier for a composed home view."""

    value: str

    def __post_init__(self) -> None:
        value = (self.value or "").strip()
        if not value:
            raise HomeInvariantViolation(
                "HomeId value must be a non-empty string",
                invariant="HomeId.value.required",
            )
        object.__setattr__(self, "value", value)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class SnapshotId:
    """Opaque identifier for a HomeSnapshot."""

    value: str

    def __post_init__(self) -> None:
        value = (self.value or "").strip()
        if not value:
            raise HomeInvariantViolation(
                "SnapshotId value must be a non-empty string",
                invariant="SnapshotId.value.required",
            )
        object.__setattr__(self, "value", value)

    def __str__(self) -> str:
        return self.value
