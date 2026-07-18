"""Shared helpers for Student Digital Twin domain tests."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from app.domain.student_twin.digital_twin import DigitalTwin
from app.domain.student_twin.evidence_event import EvidenceEvent
from app.domain.student_twin.evidence_type import EvidenceType
from app.domain.student_twin.learner import Learner


def make_learner(learner_id: str = "learner-1", **kwargs) -> Learner:
    return Learner.create(learner_id, **kwargs)


def make_twin(
    twin_id: str = "twin-1",
    learner_id: str = "learner-1",
    *,
    subject_code: str | None = "CS1",
) -> DigitalTwin:
    return DigitalTwin.create(
        twin_id,
        make_learner(learner_id),
        subject_code=subject_code,
        created_at=datetime(2026, 1, 1, tzinfo=UTC),
    )


def make_event(
    event_id: str = "e1",
    evidence_type: EvidenceType | str = EvidenceType.PRACTICE_RESULT,
    *,
    day: int = 1,
    topic_id: str | None = "topic-1",
    outcome: str | None = "success",
    score: float | None = None,
    confidence_rating: float | None = None,
    duration_seconds: int | None = None,
) -> EvidenceEvent:
    when = datetime(2026, 7, day, 12, 0, tzinfo=UTC)
    return EvidenceEvent.create(
        event_id,
        evidence_type,
        when,
        topic_id=topic_id,
        outcome=outcome,
        score=score,
        confidence_rating=confidence_rating,
        duration_seconds=duration_seconds,
    )


def make_events(
    count: int,
    *,
    topic_id: str = "topic-1",
    outcome: str = "success",
    evidence_type: EvidenceType = EvidenceType.PRACTICE_RESULT,
) -> list[EvidenceEvent]:
    return [
        make_event(
            f"e{i}",
            evidence_type,
            day=1 + (i % 28),
            topic_id=topic_id,
            outcome=outcome,
        )
        for i in range(count)
    ]


def staggered_events(
    outcomes: list[str],
    *,
    topic_id: str = "topic-1",
) -> list[EvidenceEvent]:
    base = datetime(2026, 6, 1, tzinfo=UTC)
    return [
        EvidenceEvent.create(
            f"s{i}",
            EvidenceType.ASSESSMENT_OUTCOME,
            base + timedelta(days=i),
            topic_id=topic_id,
            outcome=outcome,
        )
        for i, outcome in enumerate(outcomes)
    ]
