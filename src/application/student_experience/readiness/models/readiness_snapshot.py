"""ReadinessSnapshot — compact durable projection of a composed readiness view."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.student_experience.readiness.enums import (
    AssessmentConfidenceCategory,
    ReadinessCategory,
    ReadinessDirection,
)
from application.student_experience.readiness.errors import (
    ReadinessInvariantViolation,
)
from application.student_experience.readiness.ids import ReadinessSnapshotId


@dataclass(frozen=True, slots=True)
class ReadinessSnapshot:
    """Compact immutable snapshot of the exam readiness surface.

    Suitable for refresh comparisons and outbound publishing. Never carries
    raw Education OS aggregates.
    """

    snapshot_id: ReadinessSnapshotId
    student_id: str
    captured_at: datetime
    readiness_available: bool
    readiness_percent: float | None
    readiness_category: ReadinessCategory
    readiness_label: str
    direction: ReadinessDirection
    direction_message: str
    assessment_confidence: AssessmentConfidenceCategory
    assessment_confidence_label: str
    strength_count: int
    risk_count: int
    action_count: int
    milestone_count: int
    days_remaining: int | None
    target_exam_label: str | None
    home_focus_headline: str | None = None
    journey_trajectory_message: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.snapshot_id, ReadinessSnapshotId):
            raise ReadinessInvariantViolation(
                "snapshot_id must be a ReadinessSnapshotId",
                invariant="ReadinessSnapshot.snapshot_id.type",
            )
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise ReadinessInvariantViolation(
                "student_id must be a non-empty string",
                invariant="ReadinessSnapshot.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        if not isinstance(self.captured_at, datetime):
            raise ReadinessInvariantViolation(
                "captured_at must be a datetime",
                invariant="ReadinessSnapshot.captured_at.type",
            )
        if not isinstance(self.readiness_category, ReadinessCategory):
            raise ReadinessInvariantViolation(
                "readiness_category must be a ReadinessCategory",
                invariant="ReadinessSnapshot.readiness_category.type",
            )
        if not isinstance(self.direction, ReadinessDirection):
            raise ReadinessInvariantViolation(
                "direction must be a ReadinessDirection",
                invariant="ReadinessSnapshot.direction.type",
            )
        if not isinstance(
            self.assessment_confidence, AssessmentConfidenceCategory
        ):
            raise ReadinessInvariantViolation(
                "assessment_confidence must be an AssessmentConfidenceCategory",
                invariant="ReadinessSnapshot.assessment_confidence.type",
            )
        for name in (
            "readiness_label",
            "direction_message",
            "assessment_confidence_label",
        ):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise ReadinessInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"ReadinessSnapshot.{name}.required",
                )
            object.__setattr__(self, name, value)
        if self.readiness_percent is not None:
            if isinstance(self.readiness_percent, bool) or not isinstance(
                self.readiness_percent, int | float
            ):
                raise ReadinessInvariantViolation(
                    "readiness_percent must be a real number when provided",
                    invariant="ReadinessSnapshot.readiness_percent.type",
                )
            object.__setattr__(
                self, "readiness_percent", round(float(self.readiness_percent), 2)
            )
        for name in (
            "strength_count",
            "risk_count",
            "action_count",
            "milestone_count",
        ):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise ReadinessInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"ReadinessSnapshot.{name}.type",
                )
            if value < 0:
                raise ReadinessInvariantViolation(
                    f"{name} must be >= 0",
                    invariant=f"ReadinessSnapshot.{name}.range",
                )
        object.__setattr__(
            self,
            "target_exam_label",
            (self.target_exam_label or "").strip() or None,
        )
        object.__setattr__(
            self,
            "home_focus_headline",
            (self.home_focus_headline or "").strip() or None,
        )
        object.__setattr__(
            self,
            "journey_trajectory_message",
            (self.journey_trajectory_message or "").strip() or None,
        )
