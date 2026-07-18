"""Learning velocity service — rate of progress from evidence chronology."""

from __future__ import annotations

from datetime import UTC, datetime

from app.application.student_twin.policies.confidence_policy import ConfidencePolicy
from app.application.student_twin.policies.mastery_policy import MasteryPolicy
from app.domain.student_twin.digital_twin import DigitalTwin
from app.domain.student_twin.evidence_event import EvidenceEvent
from app.domain.student_twin.learning_velocity import LearningVelocity


class LearningVelocityService:
    """Compute LearningVelocity from evidence timing and mastery deltas."""

    @staticmethod
    def calculate(
        events: list[EvidenceEvent] | tuple[EvidenceEvent, ...],
        *,
        as_of: datetime,
        window_days: float = 7.0,
    ) -> LearningVelocity:
        """Calculate velocity over a trailing window ending at ``as_of``."""
        if as_of.tzinfo is None:
            as_of = as_of.replace(tzinfo=UTC)
        if window_days <= 0:
            window_days = 7.0
        window_seconds = window_days * 86400.0
        def _age_seconds(event: EvidenceEvent) -> float:
            occurred = event.occurred_at
            if occurred.tzinfo is None:
                occurred = occurred.replace(tzinfo=UTC)
            return (as_of - occurred).total_seconds()

        in_window = [
            e
            for e in events
            if 0 <= _age_seconds(e) <= window_seconds
        ]
        events_per_day = len(in_window) / window_days if window_days else 0.0
        mastery_delta = 0.0
        knowledge_delta = 0.0
        for event in in_window:
            delta = MasteryPolicy.delta_for(event)
            mastery_delta += delta
            knowledge_delta += delta * 0.8
        mastery_delta = max(-1.0, min(1.0, mastery_delta))
        knowledge_delta = max(-1.0, min(1.0, knowledge_delta))
        return LearningVelocity.create(
            events_per_day=events_per_day,
            mastery_delta=mastery_delta,
            knowledge_delta=knowledge_delta,
            window_days=window_days,
            confidence=ConfidencePolicy.band_for(in_window),
            evidence_ids=[e.event_id for e in in_window],
        )

    @staticmethod
    def from_twin(
        twin: DigitalTwin,
        *,
        as_of: datetime,
        window_days: float = 7.0,
    ) -> LearningVelocity:
        """Calculate velocity from Twin history."""
        return LearningVelocityService.calculate(
            twin.history.events,
            as_of=as_of,
            window_days=window_days,
        )
