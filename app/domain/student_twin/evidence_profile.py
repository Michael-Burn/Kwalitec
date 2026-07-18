"""Evidence profile — aggregated counts derived solely from evidence events."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.student_twin.evidence_event import EvidenceEvent
from app.domain.student_twin.evidence_type import EvidenceType


@dataclass(frozen=True)
class EvidenceProfile:
    """Immutable aggregation of evidence volume and type distribution.

    No inference beyond counting. Does not invent mastery or readiness.
    """

    total_events: int = 0
    by_type: tuple[tuple[str, int], ...] = field(default_factory=tuple)
    topic_ids: tuple[str, ...] = field(default_factory=tuple)
    event_ids: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def empty(cls) -> EvidenceProfile:
        """Return an empty evidence profile."""
        return cls()

    @classmethod
    def from_events(
        cls,
        events: list[EvidenceEvent] | tuple[EvidenceEvent, ...],
    ) -> EvidenceProfile:
        """Build a profile by counting events deterministically."""
        ordered = tuple(events)
        counts: dict[str, int] = {}
        topics: list[str] = []
        seen_topics: set[str] = set()
        event_ids: list[str] = []
        for event in ordered:
            key = event.evidence_type.value
            counts[key] = counts.get(key, 0) + 1
            event_ids.append(event.event_id)
            if event.topic_id and event.topic_id not in seen_topics:
                seen_topics.add(event.topic_id)
                topics.append(event.topic_id)
        by_type = tuple(sorted(counts.items(), key=lambda item: item[0]))
        return cls(
            total_events=len(ordered),
            by_type=by_type,
            topic_ids=tuple(topics),
            event_ids=tuple(event_ids),
        )

    def count_for(self, evidence_type: EvidenceType | str) -> int:
        """Return count for an evidence type (0 when absent)."""
        token = (
            evidence_type.value
            if isinstance(evidence_type, EvidenceType)
            else str(evidence_type).strip().lower()
        )
        for key, count in self.by_type:
            if key == token:
                return count
        return 0

    @property
    def topic_count(self) -> int:
        """Number of distinct topic ids observed."""
        return len(self.topic_ids)

    @property
    def is_empty(self) -> bool:
        """True when no evidence has been observed."""
        return self.total_events == 0
