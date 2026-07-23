"""UpcomingMilestoneCard — next milestone projection."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from application.student_experience.home.enums import MilestoneKind
from application.student_experience.home.errors import HomeInvariantViolation


@dataclass(frozen=True, slots=True)
class UpcomingMilestoneCard:
    """Immutable upcoming milestone card."""

    title: str
    kind: MilestoneKind
    milestone_date: date | None
    days_until: int | None
    detail: str
    has_milestone: bool = False

    def __post_init__(self) -> None:
        title = (self.title or "").strip()
        if not title:
            raise HomeInvariantViolation(
                "title must be a non-empty string",
                invariant="UpcomingMilestoneCard.title.required",
            )
        object.__setattr__(self, "title", title)
        if not isinstance(self.kind, MilestoneKind):
            raise HomeInvariantViolation(
                "kind must be a MilestoneKind",
                invariant="UpcomingMilestoneCard.kind.type",
            )
        if self.milestone_date is not None and not isinstance(
            self.milestone_date, date
        ):
            raise HomeInvariantViolation(
                "milestone_date must be a date when provided",
                invariant="UpcomingMilestoneCard.milestone_date.type",
            )
        if self.days_until is not None:
            if isinstance(self.days_until, bool) or not isinstance(
                self.days_until, int
            ):
                raise HomeInvariantViolation(
                    "days_until must be an integer when provided",
                    invariant="UpcomingMilestoneCard.days_until.type",
                )
        detail = (self.detail or "").strip()
        if not detail:
            raise HomeInvariantViolation(
                "detail must be a non-empty string",
                invariant="UpcomingMilestoneCard.detail.required",
            )
        object.__setattr__(self, "detail", detail)
