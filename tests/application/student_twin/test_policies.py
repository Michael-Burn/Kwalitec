"""Policy unit tests for student_twin."""

from __future__ import annotations

import pytest

from app.application.student_twin.exceptions import EvidenceRejected, PolicyViolation
from app.application.student_twin.policies.confidence_policy import ConfidencePolicy
from app.application.student_twin.policies.evidence_policy import EvidencePolicy
from app.application.student_twin.policies.mastery_policy import MasteryPolicy
from app.application.student_twin.policies.recommendation_policy import (
    RecommendationPolicy,
)
from app.domain.student_twin.evidence_type import EvidenceType
from app.domain.student_twin.recommendation_state import RecommendationKind
from tests.domain.student_twin.helpers import make_event, make_twin


def test_evidence_policy_rejects_forbidden_metadata():
    from datetime import UTC, datetime

    from app.domain.student_twin.evidence_event import EvidenceEvent

    bad = EvidenceEvent.create(
        "bad",
        EvidenceType.PRACTICE_RESULT,
        datetime(2026, 7, 1, tzinfo=UTC),
        topic_id="t1",
        metadata=[("pdf", "x.pdf")],
    )
    with pytest.raises(EvidenceRejected):
        EvidencePolicy.validate_event(bad)


def test_evidence_policy_duplicate():
    twin = make_twin()
    event = make_event("e1")
    twin = twin.with_evidence(event)
    with pytest.raises(PolicyViolation):
        EvidencePolicy.assert_admissible(twin, event)


@pytest.mark.parametrize("etype", list(EvidenceType))
def test_mastery_weight_for_each_type(etype):
    assert MasteryPolicy.weight_for(etype) > 0


@pytest.mark.parametrize(
    "outcome,expected_sign",
    [
        ("pass", 1),
        ("fail", -1),
        ("success", 1),
        ("incorrect", -1),
        ("partial", 0),
        (None, 0),  # assessment without outcome is neutral
    ],
)
def test_mastery_polarity(outcome, expected_sign):
    event = make_event("e1", EvidenceType.ASSESSMENT_OUTCOME, outcome=outcome)
    pol = MasteryPolicy.polarity(event)
    if expected_sign == 0:
        assert pol == 0.0
    elif expected_sign > 0:
        assert pol > 0
    else:
        assert pol < 0


def test_completion_without_outcome_is_weakly_positive():
    event = make_event(
        "e1",
        EvidenceType.ACTIVITY_COMPLETED,
        outcome=None,
        score=None,
    )
    assert MasteryPolicy.polarity(event) > 0


def test_mastery_apply_delta_clamps():
    assert MasteryPolicy.apply_delta(0.95, 0.2) == 1.0
    assert MasteryPolicy.apply_delta(0.05, -0.2) == 0.0


@pytest.mark.parametrize("n", [0, 1, 5, 10, 20, 50])
def test_confidence_volume_score(n):
    score = ConfidencePolicy.volume_score(n)
    assert 0.0 <= score <= 1.0


def test_confidence_consistency_conflict():
    events = [
        make_event("a", outcome="pass"),
        make_event("b", outcome="fail"),
        make_event("c", outcome="pass"),
        make_event("d", outcome="fail"),
    ]
    score = ConfidencePolicy.consistency_score(events)
    assert score < 1.0


@pytest.mark.parametrize(
    "epd,expected",
    [(0.0, False), (7.9, False), (8.0, True), (12.0, True)],
)
def test_should_take_break(epd, expected):
    assert RecommendationPolicy.should_take_break(epd) is expected


@pytest.mark.parametrize("kind", list(RecommendationKind))
def test_expected_benefit_for_all_kinds(kind):
    assert RecommendationPolicy.expected_benefit_for(kind)
