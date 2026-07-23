"""UpcomingMilestoneCard — readiness milestones projection."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from application.student_experience.readiness.enums import ReadinessMilestoneKind
from application.student_experience.readiness.errors import (
    ReadinessInvariantViolation,
)


@dataclass(frozen=True, slots=True)
class ReadinessMilestone:
    """One upcoming readiness milestone."""

    kind: ReadinessMilestoneKind
    title: str
    detail: str
    milestone_date: date | None = None
    days_until: int | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.kind, ReadinessMilestoneKind):
            raise ReadinessInvariantViolation(
                "kind must be a ReadinessMilestoneKind",
                invariant="ReadinessMilestone.kind.type",
            )
        for name in ("title", "detail"):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise ReadinessInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"ReadinessMilestone.{name}.required",
                )
            object.__setattr__(self, name, value)
        if self.milestone_date is not None and not isinstance(
            self.milestone_date, date
        ):
            raise ReadinessInvariantViolation(
                "milestone_date must be a date when provided",
                invariant="ReadinessMilestone.milestone_date.type",
            )
        if self.days_until is not None:
            if isinstance(self.days_until, bool) or not isinstance(
                self.days_until, int
            ):
                raise ReadinessInvariantViolation(
                    "days_until must be an integer when provided",
                    invariant="ReadinessMilestone.days_until.type",
                )


@dataclass(frozen=True, slots=True)
class UpcomingMilestoneCard:
    """Immutable upcoming milestones for the readiness surface."""

    milestones: tuple[ReadinessMilestone, ...] = ()
    primary: ReadinessMilestone | None = None
    has_milestones: bool = False
    summary: str = "Milestones will appear as your plan develops."

    def __post_init__(self) -> None:
        object.__setattr__(self, "milestones", tuple(self.milestones))
        for item in self.milestones:
            if not isinstance(item, ReadinessMilestone):
                raise ReadinessInvariantViolation(
                    "milestones must contain ReadinessMilestone values",
                    invariant="UpcomingMilestoneCard.milestones.type",
                )
        if self.primary is not None and not isinstance(
            self.primary, ReadinessMilestone
        ):
            raise ReadinessInvariantViolation(
                "primary must be a ReadinessMilestone when provided",
                invariant="UpcomingMilestoneCard.primary.type",
            )
        summary = (self.summary or "").strip()
        if not summary:
            raise ReadinessInvariantViolation(
                "summary must be a non-empty string",
                invariant="UpcomingMilestoneCard.summary.required",
            )
        object.__setattr__(self, "summary", summary)
