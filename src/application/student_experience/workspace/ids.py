"""Typed identifiers for Adaptive Study Workspace artefacts."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.workspace.errors import WorkspaceInvariantViolation


@dataclass(frozen=True, slots=True)
class WorkspaceId:
    """Opaque identifier for a composed study workspace view."""

    value: str

    def __post_init__(self) -> None:
        value = (self.value or "").strip()
        if not value:
            raise WorkspaceInvariantViolation(
                "WorkspaceId value must be a non-empty string",
                invariant="WorkspaceId.value.required",
            )
        object.__setattr__(self, "value", value)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class WorkspaceSnapshotId:
    """Opaque identifier for a WorkspaceSnapshot."""

    value: str

    def __post_init__(self) -> None:
        value = (self.value or "").strip()
        if not value:
            raise WorkspaceInvariantViolation(
                "WorkspaceSnapshotId value must be a non-empty string",
                invariant="WorkspaceSnapshotId.value.required",
            )
        object.__setattr__(self, "value", value)

    def __str__(self) -> str:
        return self.value
