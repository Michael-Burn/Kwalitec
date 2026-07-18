"""Parametrized domain matrix for student_twin."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.domain.student_twin.confidence_band import (
    ConfidenceBand,
    confidence_band_from_score,
)
from app.domain.student_twin.evidence_event import EvidenceEvent
from app.domain.student_twin.evidence_type import resolve_evidence_type
from app.domain.student_twin.mastery_state import TopicMasteryRecord
from app.domain.student_twin.recommendation_state import (
    Recommendation,
    RecommendationKind,
)
from app.domain.student_twin.twin_version import TwinVersion
from app.domain.student_twin.weakness_profile import WeaknessItem, WeaknessKind
from tests.domain.student_twin.helpers import make_event, make_twin

EVIDENCE_TYPES = [
    "activity_completed",
    "assessment_outcome",
    "practice_result",
    "reflection",
    "self_assessment",
    "recall_performance",
    "confidence_rating",
    "time_on_task",
    "session_completion",
    "mission_completion",
    "revision_outcome",
]

TOPICS = [f"topic-{i}" for i in range(1, 31)]
OUTCOMES = [
    "pass",
    "fail",
    "success",
    "incorrect",
    "partial",
    "strong",
    "weak",
    None,
]


@pytest.mark.parametrize("token", EVIDENCE_TYPES)
def test_resolve_all_evidence_types(token):
    assert resolve_evidence_type(token).value == token


@pytest.mark.parametrize("token", EVIDENCE_TYPES)
def test_create_event_for_each_type(token):
    event = EvidenceEvent.create(
        f"ev-{token}",
        token,
        datetime(2026, 7, 1, tzinfo=UTC),
        topic_id="t1",
        outcome="success",
    )
    assert event.evidence_type.value == token


@pytest.mark.parametrize("topic_id", TOPICS)
def test_topic_mastery_records(topic_id):
    record = TopicMasteryRecord.create(
        topic_id, 0.42, confidence=ConfidenceBand.MEDIUM
    )
    assert record.topic_id == topic_id


@pytest.mark.parametrize("outcome", OUTCOMES)
def test_events_with_outcomes(outcome):
    event = make_event("e1", outcome=outcome)
    assert event.outcome == (outcome.lower() if isinstance(outcome, str) else None)


@pytest.mark.parametrize("major", list(range(1, 21)))
def test_version_major_labels(major):
    v = TwinVersion.create(major, 0, 0)
    assert v.label.startswith(f"{major}.")


@pytest.mark.parametrize("patch", list(range(0, 40)))
def test_version_patch_sequence(patch):
    v = TwinVersion.create(1, 0, patch)
    assert v.bump_patch().patch == patch + 1


@pytest.mark.parametrize("score", [i / 20 for i in range(0, 21)])
def test_confidence_scores_cover_unit_interval(score):
    band = confidence_band_from_score(score)
    assert isinstance(band, ConfidenceBand)


@pytest.mark.parametrize("kind", list(RecommendationKind))
def test_all_recommendation_kinds(kind):
    rec = Recommendation.create(f"r-{kind.value}", kind, priority=0.5)
    assert rec.kind is kind


@pytest.mark.parametrize("kind", list(WeaknessKind))
def test_all_weakness_kinds(kind):
    item = WeaknessItem.create("t1", kind, 0.5)
    assert item.kind is kind


@pytest.mark.parametrize("learner_id", [f"learner-{i}" for i in range(1, 41)])
def test_many_learners(learner_id):
    twin = make_twin(twin_id=f"twin-{learner_id}", learner_id=learner_id)
    assert twin.learner_id == learner_id


@pytest.mark.parametrize("n", list(range(1, 26)))
def test_twin_accumulates_n_events(n):
    twin = make_twin()
    for i in range(n):
        twin = twin.with_evidence(make_event(f"e{i}", day=1 + (i % 28)))
    assert twin.event_count == n
    assert twin.version.patch == n
