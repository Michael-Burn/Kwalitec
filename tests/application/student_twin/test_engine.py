"""Engine behaviour tests for StudentTwinEngine."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.application.student_twin.exceptions import DuplicateEvidence, EvidenceRejected
from app.domain.student_twin.evidence_event import EvidenceEvent
from app.domain.student_twin.evidence_type import EvidenceType
from tests.application.student_twin.helpers import (
    make_engine,
    mixed_events,
    seeded_twin,
    success_events,
)
from tests.domain.student_twin.helpers import make_event


def test_create_twin_deterministic_ids():
    engine = make_engine()
    twin = engine.create_twin("learner-1", twin_id="twin-fixed", subject_code="CS1")
    assert twin.twin_id == "twin-fixed"
    assert twin.identity.subject_code == "CS1"


def test_ingest_evidence_updates_mastery():
    engine, twin = seeded_twin(success_events(5))
    assert twin.mastery.topic_count == 1
    assert twin.mastery.overall_score > 0
    assert twin.event_count == 5


def test_duplicate_evidence_rejected():
    engine = make_engine()
    twin = engine.create_twin("l1", twin_id="t1")
    event = make_event("dup")
    twin = engine.ingest_evidence(twin, event)
    with pytest.raises((DuplicateEvidence, Exception)):
        engine.ingest_evidence(twin, event)


def test_forbidden_metadata_rejected():
    engine = make_engine()
    twin = engine.create_twin("l1", twin_id="t1")
    bad = EvidenceEvent.create(
        "bad",
        EvidenceType.PRACTICE_RESULT,
        datetime(2026, 7, 1, tzinfo=UTC),
        topic_id="t1",
        metadata=[("ai_response", "hello")],
    )
    with pytest.raises(EvidenceRejected):
        engine.ingest_evidence(twin, bad)


def test_snapshot_and_explain():
    engine, twin = seeded_twin(success_events(4))
    dto = engine.snapshot(twin)
    assert dto.twin_id == twin.twin_id
    assert dto.mastery is not None
    explanations = engine.explain_all(twin)
    assert len(explanations) >= 1
    first = explanations[0]
    explained = engine.explain(twin, first.recommendation_id)
    assert explained.rationale
    assert explained.expected_benefit


def test_compare_and_timeline():
    engine = make_engine()
    twin = engine.create_twin("l1", twin_id="t1")
    s0 = engine.domain_snapshot(twin)
    twin = engine.ingest_many(twin, success_events(3))
    s1 = engine.domain_snapshot(twin)
    comparison = engine.compare(s0, s1)
    assert comparison.evidence_added == 3
    assert comparison.mastery_improved or comparison.mastery_delta >= 0
    timeline = engine.timeline([s1, s0])
    assert timeline[0].version.patch <= timeline[1].version.patch


def test_diagnose_clean_twin():
    engine, twin = seeded_twin(mixed_events())
    report = engine.diagnose(twin)
    assert report.twin_id == twin.twin_id
    assert report.event_count == twin.event_count


def test_learner_snapshot():
    engine, twin = seeded_twin()
    snap = engine.learner_snapshot(twin)
    assert snap.learner_id == twin.learner_id


def test_recalculate_idempotent():
    engine, twin = seeded_twin(success_events(3))
    again = engine.recalculate(twin, as_of=twin.updated_at)
    assert again.mastery.overall_score == twin.mastery.overall_score
    assert again.retention.overall_score == twin.retention.overall_score
    assert again.readiness.readiness_score == twin.readiness.readiness_score
    assert [
        (r.recommendation_id, r.kind, r.priority)
        for r in again.recommendations.recommendations
    ] == [
        (r.recommendation_id, r.kind, r.priority)
        for r in twin.recommendations.recommendations
    ]
