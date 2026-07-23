"""MilestoneCard — projected educational milestones."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.student_experience.progress.enums import JourneyMilestoneKind
from application.student_experience.progress.errors import JourneyInvariantViolation


@dataclass(frozen=True, slots=True)
class JourneyMilestone:
    """One projected educational milestone — never raw domain objects."""

    kind: JourneyMilestoneKind
    title: str
    message: str
    reached_at: datetime | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.kind, JourneyMilestoneKind):
            raise JourneyInvariantViolation(
                "kind must be a JourneyMilestoneKind",
                invariant="JourneyMilestone.kind.type",
            )
        title = (self.title or "").strip()
        if not title:
            raise JourneyInvariantViolation(
                "title must be a non-empty string",
                invariant="JourneyMilestone.title.required",
            )
        object.__setattr__(self, "title", title)
        message = (self.message or "").strip()
        if not message:
            raise JourneyInvariantViolation(
                "message must be a non-empty string",
                invariant="JourneyMilestone.message.required",
            )
        object.__setattr__(self, "message", message)
        if self.reached_at is not None and not isinstance(self.reached_at, datetime):
            raise JourneyInvariantViolation(
                "reached_at must be a datetime when provided",
                invariant="JourneyMilestone.reached_at.type",
            )


@dataclass(frozen=True, slots=True)
class MilestoneCard:
    """Immutable card of projected educational milestones."""

    milestones: tuple[JourneyMilestone, ...] = ()
    headline: str = "Milestones"
    has_milestones: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "milestones", tuple(self.milestones))
        for milestone in self.milestones:
            if not isinstance(milestone, JourneyMilestone):
                raise JourneyInvariantViolation(
                    "milestones must contain JourneyMilestone values",
                    invariant="MilestoneCard.milestones.type",
                )
        headline = (self.headline or "").strip()
        if not headline:
            raise JourneyInvariantViolation(
                "headline must be a non-empty string",
                invariant="MilestoneCard.headline.required",
            )
        object.__setattr__(self, "headline", headline)
        object.__setattr__(self, "has_milestones", bool(self.milestones))
