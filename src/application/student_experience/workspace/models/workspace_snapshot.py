"""WorkspaceSnapshot — compact durable projection of a composed workspace."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.student_experience.workspace.enums import (
    FocusPromptKind,
    SessionPresence,
)
from application.student_experience.workspace.errors import WorkspaceInvariantViolation
from application.student_experience.workspace.ids import WorkspaceSnapshotId


@dataclass(frozen=True, slots=True)
class WorkspaceSnapshot:
    """Compact immutable snapshot of the Adaptive Study Workspace surface.

    Suitable for refresh comparisons and outbound publishing. Never carries
    raw Education OS aggregates.
    """

    snapshot_id: WorkspaceSnapshotId
    student_id: str
    captured_at: datetime
    session_available: bool
    session_presence: SessionPresence
    mission_title: str | None
    completion_percent: float | None
    remaining_minutes: int | None
    current_objective_label: str | None
    primary_focus_kind: FocusPromptKind
    primary_focus_prompt: str
    objective_count: int
    completed_objective_count: int
    remaining_objective_count: int
    resource_count: int
    next_session_preview: str
    readiness_impact_summary: str

    def __post_init__(self) -> None:
        if not isinstance(self.snapshot_id, WorkspaceSnapshotId):
            raise WorkspaceInvariantViolation(
                "snapshot_id must be a WorkspaceSnapshotId",
                invariant="WorkspaceSnapshot.snapshot_id.type",
            )
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise WorkspaceInvariantViolation(
                "student_id must be a non-empty string",
                invariant="WorkspaceSnapshot.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        if not isinstance(self.captured_at, datetime):
            raise WorkspaceInvariantViolation(
                "captured_at must be a datetime",
                invariant="WorkspaceSnapshot.captured_at.type",
            )
        if not isinstance(self.session_presence, SessionPresence):
            raise WorkspaceInvariantViolation(
                "session_presence must be a SessionPresence",
                invariant="WorkspaceSnapshot.session_presence.type",
            )
        if not isinstance(self.primary_focus_kind, FocusPromptKind):
            raise WorkspaceInvariantViolation(
                "primary_focus_kind must be a FocusPromptKind",
                invariant="WorkspaceSnapshot.primary_focus_kind.type",
            )
        for name in (
            "primary_focus_prompt",
            "next_session_preview",
            "readiness_impact_summary",
        ):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise WorkspaceInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"WorkspaceSnapshot.{name}.required",
                )
            object.__setattr__(self, name, value)
        object.__setattr__(
            self, "mission_title", (self.mission_title or "").strip() or None
        )
        object.__setattr__(
            self,
            "current_objective_label",
            (self.current_objective_label or "").strip() or None,
        )
        if self.completion_percent is not None:
            if isinstance(self.completion_percent, bool) or not isinstance(
                self.completion_percent, int | float
            ):
                raise WorkspaceInvariantViolation(
                    "completion_percent must be a real number when provided",
                    invariant="WorkspaceSnapshot.completion_percent.type",
                )
            object.__setattr__(
                self, "completion_percent", round(float(self.completion_percent), 2)
            )
        if self.remaining_minutes is not None:
            if isinstance(self.remaining_minutes, bool) or not isinstance(
                self.remaining_minutes, int
            ):
                raise WorkspaceInvariantViolation(
                    "remaining_minutes must be an integer when provided",
                    invariant="WorkspaceSnapshot.remaining_minutes.type",
                )
            if self.remaining_minutes < 0:
                raise WorkspaceInvariantViolation(
                    "remaining_minutes must be >= 0",
                    invariant="WorkspaceSnapshot.remaining_minutes.range",
                )
        for name in (
            "objective_count",
            "completed_objective_count",
            "remaining_objective_count",
            "resource_count",
        ):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise WorkspaceInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"WorkspaceSnapshot.{name}.type",
                )
            if value < 0:
                raise WorkspaceInvariantViolation(
                    f"{name} must be >= 0",
                    invariant=f"WorkspaceSnapshot.{name}.range",
                )
