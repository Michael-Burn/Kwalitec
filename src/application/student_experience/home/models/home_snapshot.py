"""HomeSnapshot — compact durable projection of a composed home view."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.student_experience.home.errors import HomeInvariantViolation
from application.student_experience.home.ids import SnapshotId


@dataclass(frozen=True, slots=True)
class HomeSnapshot:
    """Compact immutable snapshot of the student home surface.

    Suitable for refresh comparisons and outbound publishing. Never carries
    raw Education OS aggregates.
    """

    snapshot_id: SnapshotId
    student_id: str
    captured_at: datetime
    focus_headline: str
    focus_mission_title: str | None
    focus_action_label: str
    progress_message: str
    momentum_message: str
    completed_missions: int
    current_streak_days: int
    hours_studied: float
    exam_available: bool
    exam_days_remaining: int | None
    exam_readiness_label: str | None
    insight_count: int
    quick_action_count: int
    achievement_count: int

    def __post_init__(self) -> None:
        if not isinstance(self.snapshot_id, SnapshotId):
            raise HomeInvariantViolation(
                "snapshot_id must be a SnapshotId",
                invariant="HomeSnapshot.snapshot_id.type",
            )
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise HomeInvariantViolation(
                "student_id must be a non-empty string",
                invariant="HomeSnapshot.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        if not isinstance(self.captured_at, datetime):
            raise HomeInvariantViolation(
                "captured_at must be a datetime",
                invariant="HomeSnapshot.captured_at.type",
            )
        for name in (
            "focus_headline",
            "focus_action_label",
            "progress_message",
            "momentum_message",
        ):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise HomeInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"HomeSnapshot.{name}.required",
                )
            object.__setattr__(self, name, value)
        object.__setattr__(
            self,
            "focus_mission_title",
            (self.focus_mission_title or "").strip() or None,
        )
        for name in (
            "completed_missions",
            "current_streak_days",
            "insight_count",
            "quick_action_count",
            "achievement_count",
        ):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise HomeInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"HomeSnapshot.{name}.type",
                )
            if value < 0:
                raise HomeInvariantViolation(
                    f"{name} must be >= 0",
                    invariant=f"HomeSnapshot.{name}.range",
                )
        if isinstance(self.hours_studied, bool) or not isinstance(
            self.hours_studied, int | float
        ):
            raise HomeInvariantViolation(
                "hours_studied must be a real number",
                invariant="HomeSnapshot.hours_studied.type",
            )
        object.__setattr__(self, "hours_studied", round(float(self.hours_studied), 2))
        object.__setattr__(
            self,
            "exam_readiness_label",
            (self.exam_readiness_label or "").strip() or None,
        )
