"""Confidence calculator — explicit uncertainty from evidence."""

from __future__ import annotations

from app.application.student_twin.policies.confidence_policy import ConfidencePolicy
from app.domain.student_twin.confidence_band import confidence_band_from_score
from app.domain.student_twin.confidence_state import (
    ConfidenceState,
    TopicConfidenceRecord,
)
from app.domain.student_twin.digital_twin import DigitalTwin
from app.domain.student_twin.evidence_event import EvidenceEvent


class ConfidenceCalculator:
    """Compute ConfidenceState solely from evidence events."""

    @staticmethod
    def calculate(
        events: list[EvidenceEvent] | tuple[EvidenceEvent, ...],
    ) -> ConfidenceState:
        """Calculate confidence bands and per-topic scores."""
        by_topic: dict[str, list[EvidenceEvent]] = {}
        all_ids = [e.event_id for e in events]
        for event in events:
            if event.topic_id is None:
                continue
            by_topic.setdefault(event.topic_id, []).append(event)

        topic_records = [
            TopicConfidenceRecord.create(
                topic_id,
                ConfidencePolicy.score_for(topic_events),
                evidence_ids=[e.event_id for e in topic_events],
            )
            for topic_id, topic_events in sorted(by_topic.items())
        ]
        overall = ConfidencePolicy.score_for(events)
        band = confidence_band_from_score(overall)
        return ConfidenceState.create(
            topic_records=topic_records,
            knowledge_confidence=band,
            mastery_confidence=band,
            retention_confidence=band,
            recommendation_confidence=band,
            overall_score=overall,
            evidence_ids=all_ids,
        )

    @staticmethod
    def from_twin(twin: DigitalTwin) -> ConfidenceState:
        """Calculate confidence from Twin history."""
        return ConfidenceCalculator.calculate(twin.history.events)
