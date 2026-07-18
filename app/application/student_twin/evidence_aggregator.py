"""Evidence aggregator — builds EvidenceProfile from Twin history."""

from __future__ import annotations

from app.domain.student_twin.digital_twin import DigitalTwin
from app.domain.student_twin.evidence_event import EvidenceEvent
from app.domain.student_twin.evidence_profile import EvidenceProfile
from app.domain.student_twin.learning_history import LearningHistory


class EvidenceAggregator:
    """Deterministic aggregation of evidence events into a profile."""

    @staticmethod
    def aggregate(
        events: list[EvidenceEvent] | tuple[EvidenceEvent, ...] | LearningHistory,
    ) -> EvidenceProfile:
        """Aggregate events into an EvidenceProfile."""
        if isinstance(events, LearningHistory):
            return EvidenceProfile.from_events(events.events)
        return EvidenceProfile.from_events(events)

    @staticmethod
    def from_twin(twin: DigitalTwin) -> EvidenceProfile:
        """Aggregate evidence from a Twin's learning history."""
        return EvidenceProfile.from_events(twin.history.events)

    @staticmethod
    def topic_events(
        twin: DigitalTwin,
        topic_id: str,
    ) -> tuple[EvidenceEvent, ...]:
        """Return topic-scoped events in chronicle order."""
        return twin.history.events_for_topic(topic_id)
