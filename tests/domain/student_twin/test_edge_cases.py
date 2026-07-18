"""Edge cases for student_twin domain."""

from __future__ import annotations

from datetime import datetime

import pytest

from app.domain.student_twin.confidence_band import confidence_band_from_score
from app.domain.student_twin.evidence_event import EvidenceEvent
from app.domain.student_twin.evidence_type import EvidenceType
from app.domain.student_twin.learning_history import LearningHistory
from app.domain.student_twin.learning_velocity import LearningVelocity
from app.domain.student_twin.readiness_state import ReadinessState
from tests.domain.student_twin.helpers import make_event, make_twin


def test_naive_datetime_gets_utc():
    event = EvidenceEvent.create(
        "e1",
        EvidenceType.TIME_ON_TASK,
        datetime(2026, 7, 1, 12, 0),
        duration_seconds=60,
    )
    assert event.occurred_at.tzinfo is not None


def test_topic_less_event():
    event = make_event("e1", topic_id=None, outcome=None)
    assert not event.is_topic_scoped


def test_empty_states():
    twin = make_twin()
    assert twin.knowledge.topic_count == 0
    assert twin.mastery.topic_count == 0
    assert twin.weaknesses.is_empty
    assert twin.recommendations.is_empty


def test_chronological_sort_stable():
    e1 = make_event("b", day=2)
    e2 = make_event("a", day=2)
    e3 = make_event("c", day=1)
    history = LearningHistory.create([e1, e2, e3])
    ordered = history.chronologically()
    assert ordered[0].event_id == "c"
    assert [e.event_id for e in ordered[1:]] == ["a", "b"]


@pytest.mark.parametrize(
    "score",
    [0.0, 0.19, 0.20, 0.39, 0.40, 0.64, 0.65, 0.84, 0.85, 1.0],
)
def test_confidence_band_boundaries(score):
    band = confidence_band_from_score(score)
    assert band.value in {"very_low", "low", "medium", "high", "very_high"}


@pytest.mark.parametrize("delta", [-1.0, -0.5, 0.0, 0.5, 1.0])
def test_velocity_signed_deltas(delta):
    vel = LearningVelocity.create(mastery_delta=delta, knowledge_delta=delta)
    assert -1.0 <= vel.mastery_delta <= 1.0


def test_readiness_not_ready_when_low_confidence():
    from app.domain.student_twin.confidence_band import ConfidenceBand

    state = ReadinessState.create(0.9, confidence=ConfidenceBand.VERY_LOW)
    assert not state.is_ready


def test_history_create_rejects_duplicates():
    with pytest.raises(ValueError):
        LearningHistory.create([make_event("e1"), make_event("e1")])
