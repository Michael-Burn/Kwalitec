"""Retention estimator — durability from mastery and evidence recency."""

from __future__ import annotations

import math
from datetime import UTC, datetime

from app.application.student_twin.policies.confidence_policy import ConfidencePolicy
from app.domain.student_twin.digital_twin import DigitalTwin
from app.domain.student_twin.evidence_event import EvidenceEvent
from app.domain.student_twin.mastery_state import MasteryState
from app.domain.student_twin.retention_state import RetentionState, TopicRetentionRecord

# Half-life in days for retention decay (deterministic constant).
_RETENTION_HALF_LIFE_DAYS = 14.0


class RetentionEstimator:
    """Estimate retention from mastery and time since last evidence."""

    @staticmethod
    def calculate(
        events: list[EvidenceEvent] | tuple[EvidenceEvent, ...],
        mastery: MasteryState,
        *,
        as_of: datetime,
    ) -> RetentionState:
        """Estimate retention for each mastered topic as of ``as_of``."""
        if as_of.tzinfo is None:
            as_of = as_of.replace(tzinfo=UTC)
        by_topic: dict[str, list[EvidenceEvent]] = {}
        for event in events:
            if event.topic_id is None:
                continue
            by_topic.setdefault(event.topic_id, []).append(event)

        records: list[TopicRetentionRecord] = []
        all_ids = [e.event_id for e in events]
        for record in mastery.topic_records:
            topic_events = by_topic.get(record.topic_id, [])
            last_at = max((e.occurred_at for e in topic_events), default=None)
            if last_at is None:
                retention = 0.0
            else:
                if last_at.tzinfo is None:
                    last_at = last_at.replace(tzinfo=UTC)
                days = max(0.0, (as_of - last_at).total_seconds() / 86400.0)
                decay = math.exp(
                    -math.log(2.0) * days / _RETENTION_HALF_LIFE_DAYS
                )
                retention = record.mastery_score * decay
                if retention > 1.0:
                    retention = 1.0
            conf = ConfidencePolicy.score_for(topic_events)
            records.append(
                TopicRetentionRecord.create(
                    record.topic_id,
                    retention,
                    confidence_score=conf,
                    last_evidence_at=last_at,
                    evidence_ids=[e.event_id for e in topic_events],
                )
            )
        return RetentionState.create(
            records,
            overall_confidence=ConfidencePolicy.band_for(events),
            evidence_ids=all_ids,
        )

    @staticmethod
    def from_twin(twin: DigitalTwin, *, as_of: datetime) -> RetentionState:
        """Estimate retention from Twin mastery and history."""
        return RetentionEstimator.calculate(
            twin.history.events,
            twin.mastery,
            as_of=as_of,
        )
