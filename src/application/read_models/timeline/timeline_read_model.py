"""TimelineReadModel — chronological presentation of learning activity."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TimelineEventReadModel:
    """One timeline row for dashboard / history surfaces. Display only."""

    sequence: int
    kind: str
    label: str
    occurred_at: str | None = None


@dataclass(frozen=True, slots=True)
class TimelineReadModel:
    """Ordered timeline for a student. Never carries domain aggregates."""

    student_id: str
    events: tuple[TimelineEventReadModel, ...]
    twin_id: str | None = None

    @property
    def event_count(self) -> int:
        return len(self.events)
