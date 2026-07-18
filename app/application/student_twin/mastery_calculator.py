"""Mastery calculator — deterministic mastery from evidence."""

from __future__ import annotations

from app.application.student_twin.policies.confidence_policy import ConfidencePolicy
from app.application.student_twin.policies.mastery_policy import MasteryPolicy
from app.domain.student_twin.digital_twin import DigitalTwin
from app.domain.student_twin.evidence_event import EvidenceEvent
from app.domain.student_twin.mastery_state import MasteryState, TopicMasteryRecord


class MasteryCalculator:
    """Compute MasteryState solely from evidence events."""

    @staticmethod
    def calculate(
        events: list[EvidenceEvent] | tuple[EvidenceEvent, ...],
    ) -> MasteryState:
        """Calculate mastery for all topic-scoped events."""
        by_topic: dict[str, list[EvidenceEvent]] = {}
        all_ids: list[str] = []
        for event in events:
            all_ids.append(event.event_id)
            if event.topic_id is None:
                continue
            by_topic.setdefault(event.topic_id, []).append(event)

        records: list[TopicMasteryRecord] = []
        for topic_id in sorted(by_topic.keys()):
            topic_events = by_topic[topic_id]
            score = MasteryPolicy.INITIAL_MASTERY
            evidence_ids: list[str] = []
            for event in topic_events:
                score = MasteryPolicy.apply_delta(
                    score, MasteryPolicy.delta_for(event)
                )
                evidence_ids.append(event.event_id)
            conf_score = ConfidencePolicy.score_for(topic_events)
            records.append(
                TopicMasteryRecord.create(
                    topic_id,
                    score,
                    confidence_score=conf_score,
                    evidence_ids=evidence_ids,
                )
            )
        return MasteryState.create(records, evidence_ids=all_ids)

    @staticmethod
    def from_twin(twin: DigitalTwin) -> MasteryState:
        """Calculate mastery from Twin history."""
        return MasteryCalculator.calculate(twin.history.events)
