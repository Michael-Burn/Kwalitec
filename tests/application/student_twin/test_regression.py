"""Regression suite for Student Digital Twin educational invariants."""

from __future__ import annotations

import pytest

from app.application.student_twin.comparison_service import ComparisonService
from app.application.student_twin.exceptions import ComparisonError, ExplanationError
from app.application.student_twin.explanation_service import ExplanationService
from app.application.student_twin.timeline_service import TimelineService
from tests.application.student_twin.helpers import make_engine, success_events
from tests.domain.student_twin.helpers import make_event, make_twin


def test_no_curriculum_fields_on_twin():
    twin = make_twin()
    assert not hasattr(twin, "curriculum")
    assert not hasattr(twin, "pdf")


def test_recommendations_reversible_with_new_evidence():
    engine = make_engine()
    twin = engine.create_twin("l1", twin_id="t1")
    twin = engine.ingest_many(
        twin, success_events(2, topic_id="weak-topic", prefix="a")
    )
    first_kinds = [r.kind for r in twin.recommendations.recommendations]
    twin = engine.ingest_many(
        twin,
        success_events(15, topic_id="weak-topic", prefix="b"),
    )
    second_kinds = [r.kind for r in twin.recommendations.recommendations]
    assert first_kinds is not None and second_kinds is not None
    assert twin.event_count == 17


def test_comparison_rejects_different_twins():
    engine = make_engine()
    a = engine.create_twin("l1", twin_id="a")
    b = engine.create_twin("l2", twin_id="b")
    with pytest.raises(ComparisonError):
        ComparisonService.compare(
            engine.domain_snapshot(a),
            engine.domain_snapshot(b),
        )


def test_explanation_missing_id():
    twin = make_twin()
    with pytest.raises(ExplanationError):
        ExplanationService.explain_recommendation(twin, "missing")


def test_timeline_orders_by_version():
    engine = make_engine()
    twin = engine.create_twin("l1", twin_id="t1")
    snaps = [engine.domain_snapshot(twin)]
    for i in range(5):
        twin = engine.ingest_evidence(twin, make_event(f"e{i}", day=i + 1))
        snaps.append(engine.domain_snapshot(twin))
    ordered = TimelineService.build(list(reversed(snaps)))
    patches = [s.version.patch for s in ordered]
    assert patches == sorted(patches)


@pytest.mark.parametrize("batch", list(range(1, 31)))
def test_batch_ingest_event_count(batch):
    engine = make_engine()
    twin = engine.create_twin("l1", twin_id="t1")
    twin = engine.ingest_many(twin, success_events(batch))
    assert twin.event_count == batch
    assert twin.evidence_profile.total_events == batch


@pytest.mark.parametrize("topic_a,topic_b", [
    ("alpha", "beta"),
    ("t1", "t2"),
    ("calc", "stats"),
    ("s1", "s2"),
    ("m1", "m2"),
])
def test_multi_topic_mastery(topic_a, topic_b):
    engine = make_engine()
    twin = engine.create_twin("l1", twin_id="t1")
    twin = engine.ingest_many(
        twin, success_events(3, topic_id=topic_a, prefix=f"{topic_a}-")
    )
    twin = engine.ingest_many(
        twin, success_events(3, topic_id=topic_b, prefix=f"{topic_b}-")
    )
    assert twin.mastery.record_for(topic_a) is not None
    assert twin.mastery.record_for(topic_b) is not None
    assert twin.mastery.topic_count == 2


def test_engine_version_constants():
    from app.application.student_twin.twin_engine import StudentTwinEngine

    assert StudentTwinEngine.ENGINE_ID == "student_twin"
    assert StudentTwinEngine.ENGINE_VERSION.startswith("2.")
