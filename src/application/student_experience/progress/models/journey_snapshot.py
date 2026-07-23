"""JourneySnapshot — compact durable projection of a composed journey view."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.student_experience.progress.enums import (
    TrajectoryLabel,
    TrendDirection,
)
from application.student_experience.progress.errors import JourneyInvariantViolation
from application.student_experience.progress.ids import JourneySnapshotId


@dataclass(frozen=True, slots=True)
class JourneySnapshot:
    """Compact immutable snapshot of the learning journey surface.

    Suitable for refresh comparisons and outbound publishing. Never carries
    raw Education OS aggregates.
    """

    snapshot_id: JourneySnapshotId
    student_id: str
    captured_at: datetime
    trajectory: TrajectoryLabel
    trajectory_message: str
    timeline_event_count: int
    milestone_count: int
    current_streak_days: int
    longest_streak_days: int
    weekly_missions_completed: int
    monthly_missions_completed: int
    mastery_trend: TrendDirection
    consistency_message: str
    habits_message: str
    home_focus_headline: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.snapshot_id, JourneySnapshotId):
            raise JourneyInvariantViolation(
                "snapshot_id must be a JourneySnapshotId",
                invariant="JourneySnapshot.snapshot_id.type",
            )
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise JourneyInvariantViolation(
                "student_id must be a non-empty string",
                invariant="JourneySnapshot.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        if not isinstance(self.captured_at, datetime):
            raise JourneyInvariantViolation(
                "captured_at must be a datetime",
                invariant="JourneySnapshot.captured_at.type",
            )
        if not isinstance(self.trajectory, TrajectoryLabel):
            raise JourneyInvariantViolation(
                "trajectory must be a TrajectoryLabel",
                invariant="JourneySnapshot.trajectory.type",
            )
        if not isinstance(self.mastery_trend, TrendDirection):
            raise JourneyInvariantViolation(
                "mastery_trend must be a TrendDirection",
                invariant="JourneySnapshot.mastery_trend.type",
            )
        for name in (
            "trajectory_message",
            "consistency_message",
            "habits_message",
        ):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise JourneyInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"JourneySnapshot.{name}.required",
                )
            object.__setattr__(self, name, value)
        for name in (
            "timeline_event_count",
            "milestone_count",
            "current_streak_days",
            "longest_streak_days",
            "weekly_missions_completed",
            "monthly_missions_completed",
        ):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise JourneyInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"JourneySnapshot.{name}.type",
                )
            if value < 0:
                raise JourneyInvariantViolation(
                    f"{name} must be >= 0",
                    invariant=f"JourneySnapshot.{name}.range",
                )
        object.__setattr__(
            self,
            "home_focus_headline",
            (self.home_focus_headline or "").strip() or None,
        )
