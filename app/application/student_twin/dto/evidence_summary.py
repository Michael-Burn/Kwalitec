"""Immutable evidence summary DTO."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.student_twin.evidence_profile import EvidenceProfile


@dataclass(frozen=True)
class EvidenceSummary:
    """Evidence volume and type distribution projection."""

    total_events: int = 0
    topic_count: int = 0
    by_type: tuple[tuple[str, int], ...] = field(default_factory=tuple)
    event_ids: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_domain(cls, profile: EvidenceProfile) -> EvidenceSummary:
        """Project EvidenceProfile to a DTO."""
        return cls(
            total_events=profile.total_events,
            topic_count=profile.topic_count,
            by_type=profile.by_type,
            event_ids=profile.event_ids,
        )
