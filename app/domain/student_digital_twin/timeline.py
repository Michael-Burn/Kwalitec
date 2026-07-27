"""Educational timeline — chronologically ordered Twin events."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum


class TimelineEventKind(StrEnum):
    """Kinds of timeline entries for Twin history diagnostics."""

    OBSERVATION = "observation"
    REASONING = "reasoning"
    MASTERY_UPDATE = "mastery_update"
    GAP_IDENTIFIED = "gap_identified"
    RECOMMENDATION = "recommendation"
    PREDICTION = "prediction"
    STATE_SNAPSHOT = "state_snapshot"


@dataclass(frozen=True)
class TimelineEvent:
    """One chronologically ordered Twin history entry."""

    event_id: str
    twin_id: str
    kind: TimelineEventKind
    occurred_at: datetime
    summary: str
    reference_id: str = ""
    metadata_json: str = "{}"

    def __post_init__(self) -> None:
        if not (self.event_id or "").strip():
            raise ValueError("event_id is required")
        kind = (
            self.kind
            if isinstance(self.kind, TimelineEventKind)
            else TimelineEventKind(str(self.kind))
        )
        object.__setattr__(self, "kind", kind)
        when = self.occurred_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "occurred_at", when.astimezone(UTC).replace(tzinfo=None)
            )


@dataclass(frozen=True)
class Timeline:
    """Ordered Twin history (newest last for append semantics)."""

    events: tuple[TimelineEvent, ...] = ()

    def append(self, event: TimelineEvent) -> Timeline:
        return Timeline(events=(*self.events, event))

    def chronological(self) -> tuple[TimelineEvent, ...]:
        return tuple(sorted(self.events, key=lambda e: (e.occurred_at, e.event_id)))
