"""Determinism and regression guarantees for student_twin."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from tests.application.student_twin.helpers import (
    make_engine,
    mixed_events,
    success_events,
)
from tests.domain.student_twin.helpers import make_event, staggered_events


def _run(events):
    engine = make_engine(fixed_time=datetime(2026, 7, 18, 12, 0, tzinfo=UTC))
    twin = engine.create_twin("learner-1", twin_id="twin-1", subject_code="CS1")
    twin = engine.ingest_many(twin, events)
    return twin


def test_identical_evidence_identical_conclusions():
    events = success_events(6) + mixed_events()
    a = _run(events)
    b = _run(events)
    assert a.mastery.overall_score == b.mastery.overall_score
    assert a.knowledge.overall_score == b.knowledge.overall_score
    assert a.retention.overall_score == b.retention.overall_score
    assert a.readiness.readiness_score == b.readiness.readiness_score
    assert a.confidence.overall_score == b.confidence.overall_score
    assert [
        (r.kind, r.topic_id, r.priority, r.rationale)
        for r in a.recommendations.recommendations
    ] == [
        (r.kind, r.topic_id, r.priority, r.rationale)
        for r in b.recommendations.recommendations
    ]


@pytest.mark.parametrize("n", [1, 2, 3, 5, 8, 13])
def test_determinism_across_counts(n):
    events = success_events(n)
    assert _run(events).mastery.overall_score == _run(events).mastery.overall_score


@pytest.mark.parametrize(
    "outcomes",
    [
        ["pass", "pass", "pass"],
        ["fail", "fail", "fail"],
        ["pass", "fail", "pass"],
        ["success", "incorrect", "partial", "success"],
    ],
)
def test_determinism_outcome_patterns(outcomes):
    events = staggered_events(outcomes)
    assert _run(events).mastery.overall_score == _run(events).mastery.overall_score


def test_history_immutable_across_ingest():
    engine = make_engine()
    twin = engine.create_twin("l1", twin_id="t1")
    e1 = make_event("e1")
    twin2 = engine.ingest_evidence(twin, e1)
    assert twin.history.is_empty
    assert twin2.history.event_ids == ("e1",)
    # prior event still identical
    assert twin2.history.event_by_id("e1") == e1
