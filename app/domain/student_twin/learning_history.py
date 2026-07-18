"""Learning history — immutable append-only evidence timeline."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.student_twin.evidence_event import EvidenceEvent


@dataclass(frozen=True)
class LearningHistory:
    """Append-only chronicle of evidence events.

    Past events are never rewritten. Twin evolves by accumulation only.
    """

    events: tuple[EvidenceEvent, ...] = field(default_factory=tuple)

    @classmethod
    def empty(cls) -> LearningHistory:
        """Return an empty learning history."""
        return cls()

    @classmethod
    def create(
        cls,
        events: list[EvidenceEvent] | tuple[EvidenceEvent, ...] | None = None,
    ) -> LearningHistory:
        """Construct LearningHistory; rejects duplicate event ids."""
        ordered = tuple(events or ())
        seen: set[str] = set()
        for event in ordered:
            if event.event_id in seen:
                raise ValueError(f"duplicate event_id: {event.event_id!r}")
            seen.add(event.event_id)
        return cls(events=ordered)

    @property
    def event_count(self) -> int:
        """Number of recorded evidence events."""
        return len(self.events)

    @property
    def is_empty(self) -> bool:
        """True when no events have been recorded."""
        return not self.events

    @property
    def event_ids(self) -> tuple[str, ...]:
        """Ordered event identities."""
        return tuple(event.event_id for event in self.events)

    def append(self, event: EvidenceEvent) -> LearningHistory:
        """Return a new history with ``event`` appended (immutable)."""
        if event.event_id in self.event_ids:
            raise ValueError(f"duplicate event_id: {event.event_id!r}")
        return LearningHistory(events=(*self.events, event))

    def append_many(
        self,
        events: list[EvidenceEvent] | tuple[EvidenceEvent, ...],
    ) -> LearningHistory:
        """Return a new history with many events appended in order."""
        history = self
        for event in events:
            history = history.append(event)
        return history

    def event_by_id(self, event_id: str) -> EvidenceEvent | None:
        """Return an event by identity, or None."""
        token = (event_id or "").strip()
        for event in self.events:
            if event.event_id == token:
                return event
        return None

    def events_for_topic(self, topic_id: str) -> tuple[EvidenceEvent, ...]:
        """Return events scoped to ``topic_id`` in chronicle order."""
        token = (topic_id or "").strip()
        return tuple(e for e in self.events if e.topic_id == token)

    def chronologically(self) -> tuple[EvidenceEvent, ...]:
        """Return events sorted by occurred_at then event_id (stable)."""
        return tuple(
            sorted(
                self.events,
                key=lambda e: (e.occurred_at, e.event_id),
            )
        )
