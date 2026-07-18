"""Entity construction and invariant tests for student_twin domain."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.domain.student_twin.confidence_band import (
    ConfidenceBand,
    confidence_band_from_score,
    confidence_score_from_band,
    resolve_confidence_band,
)
from app.domain.student_twin.confidence_state import (
    ConfidenceState,
    TopicConfidenceRecord,
)
from app.domain.student_twin.evidence_event import EvidenceEvent
from app.domain.student_twin.evidence_profile import EvidenceProfile
from app.domain.student_twin.evidence_type import EvidenceType, resolve_evidence_type
from app.domain.student_twin.knowledge_state import KnowledgeState, TopicKnowledgeRecord
from app.domain.student_twin.learner import Learner
from app.domain.student_twin.learning_history import LearningHistory
from app.domain.student_twin.learning_velocity import LearningVelocity
from app.domain.student_twin.mastery_state import MasteryState, TopicMasteryRecord
from app.domain.student_twin.readiness_state import ReadinessState
from app.domain.student_twin.recommendation_state import (
    Recommendation,
    RecommendationKind,
    RecommendationState,
)
from app.domain.student_twin.retention_state import RetentionState, TopicRetentionRecord
from app.domain.student_twin.twin_identity import TwinIdentity
from app.domain.student_twin.twin_snapshot import TwinSnapshot
from app.domain.student_twin.twin_version import TwinVersion
from app.domain.student_twin.weakness_profile import (
    WeaknessItem,
    WeaknessKind,
    WeaknessProfile,
)
from tests.domain.student_twin.helpers import make_event, make_learner, make_twin


def test_learner_create_and_with_subject():
    learner = make_learner("L1", display_name="Ada", subject_codes=["CS1"])
    assert learner.subject_count == 1
    expanded = learner.with_subject("CM1")
    assert expanded.subject_count == 2
    with pytest.raises(ValueError):
        expanded.with_subject("CM1")


def test_learner_rejects_blank():
    with pytest.raises(ValueError):
        Learner.create("  ")


def test_twin_identity():
    ident = TwinIdentity.create("t1", "l1", subject_code="CS1")
    assert ident.with_subject(None).subject_code is None
    assert ident.with_subject("CM1").subject_code == "CM1"


def test_twin_version_bumps():
    v = TwinVersion.initial()
    assert v.label == "1.0.0"
    assert v.bump_patch().label == "1.0.1"
    assert v.bump_minor().label == "1.1.0"
    assert v.bump_major().label == "2.0.0"
    assert TwinVersion.create(1, 0, 0).precedes(TwinVersion.create(1, 0, 1))


def test_twin_version_rejects_negative():
    with pytest.raises(ValueError):
        TwinVersion.create(-1, 0, 0)


def test_evidence_type_resolve():
    assert resolve_evidence_type("practice_result") is EvidenceType.PRACTICE_RESULT
    with pytest.raises(ValueError):
        resolve_evidence_type("not_a_type")


def test_evidence_event_create():
    event = make_event("e1", score=0.8, confidence_rating=0.5, duration_seconds=120)
    assert event.is_topic_scoped
    assert event.score == 0.8


@pytest.mark.parametrize(
    "field,kwargs",
    [
        ("score", {"score": 1.5}),
        ("confidence_rating", {"confidence_rating": -0.1}),
        ("duration_seconds", {"duration_seconds": -1}),
        ("event_id", {"event_id": "  "}),
    ],
)
def test_evidence_event_rejects_invalid(field, kwargs):
    base = dict(
        event_id="e1",
        evidence_type=EvidenceType.PRACTICE_RESULT,
        occurred_at=datetime(2026, 7, 1, tzinfo=UTC),
        topic_id="t1",
    )
    base.update(kwargs)
    if field == "event_id":
        with pytest.raises(ValueError):
            EvidenceEvent.create(**base)
    else:
        with pytest.raises(ValueError):
            EvidenceEvent.create(**base)


def test_learning_history_append_and_duplicate():
    h = LearningHistory.empty()
    e1 = make_event("e1")
    h2 = h.append(e1)
    assert h2.event_count == 1
    assert h.is_empty
    with pytest.raises(ValueError):
        h2.append(e1)
    h3 = h2.append_many([make_event("e2"), make_event("e3")])
    assert h3.event_count == 3
    assert h3.event_by_id("e2") is not None
    assert len(h3.events_for_topic("topic-1")) == 3


def test_evidence_profile_from_events():
    events = [
        make_event("a"),
        make_event("b", EvidenceType.REFLECTION, topic_id="topic-2"),
    ]
    profile = EvidenceProfile.from_events(events)
    assert profile.total_events == 2
    assert profile.topic_count == 2
    assert profile.count_for(EvidenceType.PRACTICE_RESULT) == 1


def test_confidence_band_mapping():
    assert confidence_band_from_score(0.9) is ConfidenceBand.VERY_HIGH
    assert confidence_band_from_score(0.1) is ConfidenceBand.VERY_LOW
    assert resolve_confidence_band("high") is ConfidenceBand.HIGH
    assert 0.0 <= confidence_score_from_band(ConfidenceBand.MEDIUM) <= 1.0


def test_topic_states_create():
    k = TopicKnowledgeRecord.create("t1", 0.5, confidence_score=0.6)
    m = TopicMasteryRecord.create("t1", 0.4, confidence=ConfidenceBand.LOW)
    r = TopicRetentionRecord.create("t1", 0.3, confidence_score=0.4)
    c = TopicConfidenceRecord.create("t1", 0.55)
    assert KnowledgeState.create([k]).topic_count == 1
    assert MasteryState.create([m]).record_for("t1") is not None
    assert RetentionState.create([r]).overall_score == 0.3
    assert ConfidenceState.create(topic_records=[c]).record_for("t1") is not None


def test_duplicate_topic_rejected():
    m1 = TopicMasteryRecord.create("t1", 0.2)
    m2 = TopicMasteryRecord.create("t1", 0.3)
    with pytest.raises(ValueError):
        MasteryState.create([m1, m2])


def test_readiness_and_velocity():
    ready = ReadinessState.create(0.7, confidence=ConfidenceBand.HIGH)
    assert ready.is_ready
    vel = LearningVelocity.create(
        events_per_day=2.0, mastery_delta=0.1, window_days=7.0
    )
    assert vel.is_active and vel.is_improving


def test_weakness_and_recommendation():
    item = WeaknessItem.create("t1", WeaknessKind.LOW_MASTERY, 0.8, rationale="low")
    profile = WeaknessProfile.create([item])
    assert profile.topic_ids == ("t1",)
    rec = Recommendation.create(
        "r1",
        RecommendationKind.PRACTICE_TOPIC,
        topic_id="t1",
        rationale="weak",
        expected_benefit="raise_mastery",
    )
    state = RecommendationState.create([rec])
    assert state.primary is rec
    assert not state.is_empty


def test_digital_twin_lifecycle():
    twin = make_twin()
    assert twin.version.label == "1.0.0"
    event = make_event("e1")
    twin2 = twin.with_evidence(event)
    assert twin2.event_count == 1
    assert twin2.version.label == "1.0.1"
    assert twin.event_count == 0
    snap = twin2.to_snapshot()
    assert snap.history_event_ids == ("e1",)
    assert isinstance(snap, TwinSnapshot)


def test_twin_snapshot_create():
    twin = make_twin()
    snap = TwinSnapshot.create(
        twin.identity,
        twin.version,
        datetime(2026, 7, 1, tzinfo=UTC),
    )
    assert snap.twin_id == "twin-1"
