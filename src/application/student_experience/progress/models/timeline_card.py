"""TimelineCard — chronological educational event projection."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.student_experience.progress.enums import TimelineEventKind
from application.student_experience.progress.errors import JourneyInvariantViolation


@dataclass(frozen=True, slots=True)
class TimelineEvent:
    """One descriptive educational timeline event — never explanatory."""

    kind: TimelineEventKind
    occurred_at: datetime
    title: str
    message: str

    def __post_init__(self) -> None:
        if not isinstance(self.kind, TimelineEventKind):
            raise JourneyInvariantViolation(
                "kind must be a TimelineEventKind",
                invariant="TimelineEvent.kind.type",
            )
        if not isinstance(self.occurred_at, datetime):
            raise JourneyInvariantViolation(
                "occurred_at must be a datetime",
                invariant="TimelineEvent.occurred_at.type",
            )
        title = (self.title or "").strip()
        if not title:
            raise JourneyInvariantViolation(
                "title must be a non-empty string",
                invariant="TimelineEvent.title.required",
            )
        object.__setattr__(self, "title", title)
        message = (self.message or "").strip()
        if not message:
            raise JourneyInvariantViolation(
                "message must be a non-empty string",
                invariant="TimelineEvent.message.required",
            )
        object.__setattr__(self, "message", message)


@dataclass(frozen=True, slots=True)
class TimelineCard:
    """Immutable chronological educational timeline."""

    events: tuple[TimelineEvent, ...] = ()
    headline: str = "Your learning timeline"
    has_events: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "events", tuple(self.events))
        for event in self.events:
            if not isinstance(event, TimelineEvent):
                raise JourneyInvariantViolation(
                    "events must contain TimelineEvent values",
                    invariant="TimelineCard.events.type",
                )
        headline = (self.headline or "").strip()
        if not headline:
            raise JourneyInvariantViolation(
                "headline must be a non-empty string",
                invariant="TimelineCard.headline.required",
            )
        object.__setattr__(self, "headline", headline)
        object.__setattr__(self, "has_events", bool(self.events))
