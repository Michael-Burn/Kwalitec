"""Shared helpers for Student Digital Twin application tests."""

from __future__ import annotations

from datetime import UTC, datetime

from app.application.student_twin.twin_engine import StudentTwinEngine
from app.domain.student_twin.evidence_event import EvidenceEvent
from app.domain.student_twin.evidence_type import EvidenceType
from tests.domain.student_twin.helpers import make_event, make_twin


def make_engine(
    *,
    fixed_time: datetime | None = None,
) -> StudentTwinEngine:
    when = fixed_time or datetime(2026, 7, 18, 12, 0, tzinfo=UTC)
    counter = {"n": 0}

    def _ids() -> str:
        counter["n"] += 1
        return f"id{counter['n']:04d}"

    return StudentTwinEngine(clock=lambda: when, id_factory=_ids)


def seeded_twin(
    events: list[EvidenceEvent] | None = None,
    *,
    twin_id: str = "twin-1",
    learner_id: str = "learner-1",
):
    engine = make_engine()
    twin = engine.create_twin(learner_id, twin_id=twin_id, subject_code="CS1")
    if events:
        twin = engine.ingest_many(twin, events)
    return engine, twin


def success_events(
    n: int,
    topic_id: str = "topic-1",
    *,
    prefix: str = "ok",
) -> list[EvidenceEvent]:
    return [
        make_event(
            f"{prefix}{i}",
            EvidenceType.PRACTICE_RESULT,
            day=1 + (i % 28),
            topic_id=topic_id,
            outcome="success",
            score=0.85,
        )
        for i in range(n)
    ]


def mixed_events(topic_id: str = "topic-1") -> list[EvidenceEvent]:
    return [
        make_event(
            "m1",
            EvidenceType.ASSESSMENT_OUTCOME,
            day=1,
            topic_id=topic_id,
            outcome="pass",
            score=0.9,
        ),
        make_event(
            "m2",
            EvidenceType.RECALL_PERFORMANCE,
            day=2,
            topic_id=topic_id,
            outcome="fail",
            score=0.2,
        ),
        make_event(
            "m3",
            EvidenceType.REVISION_OUTCOME,
            day=3,
            topic_id=topic_id,
            outcome="success",
            score=0.7,
        ),
        make_event(
            "m4",
            EvidenceType.SESSION_COMPLETION,
            day=4,
            topic_id=None,
            outcome=None,
        ),
    ]


# Re-export make_twin for application tests.
__all__ = [
    "make_engine",
    "make_event",
    "make_twin",
    "mixed_events",
    "seeded_twin",
    "success_events",
]
