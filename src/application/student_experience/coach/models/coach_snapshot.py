"""CoachSnapshot — compact durable projection of a composed coach context."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.student_experience.coach.errors import CoachInvariantViolation
from application.student_experience.coach.ids import CoachSnapshotId


@dataclass(frozen=True, slots=True)
class CoachSnapshot:
    """Compact immutable snapshot of the AI Learning Coach surface.

    Suitable for refresh comparisons and outbound publishing. Never carries
    raw Education OS aggregates.
    """

    snapshot_id: CoachSnapshotId
    student_id: str
    captured_at: datetime
    focus_headline: str
    mission_title: str | None
    readiness_label: str
    journey_message: str
    explanation_card_count: int
    suggested_question_count: int
    reflection_prompt_count: int
    celebration_count: int
    improvement_count: int
    risk_count: int
    milestone_count: int

    def __post_init__(self) -> None:
        if not isinstance(self.snapshot_id, CoachSnapshotId):
            raise CoachInvariantViolation(
                "snapshot_id must be a CoachSnapshotId",
                invariant="CoachSnapshot.snapshot_id.type",
            )
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise CoachInvariantViolation(
                "student_id must be a non-empty string",
                invariant="CoachSnapshot.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        if not isinstance(self.captured_at, datetime):
            raise CoachInvariantViolation(
                "captured_at must be a datetime",
                invariant="CoachSnapshot.captured_at.type",
            )
        for name in ("focus_headline", "readiness_label", "journey_message"):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise CoachInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"CoachSnapshot.{name}.required",
                )
            object.__setattr__(self, name, value)
        object.__setattr__(
            self, "mission_title", (self.mission_title or "").strip() or None
        )
        for name in (
            "explanation_card_count",
            "suggested_question_count",
            "reflection_prompt_count",
            "celebration_count",
            "improvement_count",
            "risk_count",
            "milestone_count",
        ):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise CoachInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"CoachSnapshot.{name}.type",
                )
            if value < 0:
                raise CoachInvariantViolation(
                    f"{name} must be >= 0",
                    invariant=f"CoachSnapshot.{name}.range",
                )
