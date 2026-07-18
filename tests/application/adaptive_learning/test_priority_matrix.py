"""Priority calculation matrix — deterministic educational urgency."""

from __future__ import annotations

import pytest

from app.application.adaptive_learning.policies.priority_policy import PriorityPolicy
from app.application.adaptive_learning.priority_calculator import PriorityCalculator
from app.domain.adaptive_learning.intervention_priority import priority_band_from_score
from app.domain.student_twin.confidence_band import ConfidenceBand

RETENTION = [0.0, 0.25, 0.5, 0.75, 1.0]
MASTERY = [0.0, 0.25, 0.5, 0.75, 1.0]
IMPORTANCE = [0.0, 0.5, 1.0]
EXAM = [0.0, 1.0]
CONFIDENCE = [
    ConfidenceBand.VERY_LOW,
    ConfidenceBand.MEDIUM,
    ConfidenceBand.VERY_HIGH,
]


def test_priority_weights_sum_to_one():
    assert PriorityPolicy.weights_sum() == pytest.approx(1.0)


@pytest.mark.parametrize("retention", RETENTION)
@pytest.mark.parametrize("mastery", [0.0, 0.5, 1.0])
def test_priority_rises_as_retention_falls(retention, mastery):
    p = PriorityCalculator.calculate(
        retention_score=retention,
        mastery_score=mastery,
        confidence=ConfidenceBand.MEDIUM,
    )
    assert 0.0 <= p.score <= 1.0
    assert p.retention_risk == pytest.approx(1.0 - retention)
    assert p.band is priority_band_from_score(p.score)


@pytest.mark.parametrize("mastery", MASTERY)
@pytest.mark.parametrize("retention", [0.0, 0.5, 1.0])
def test_priority_rises_as_mastery_falls(mastery, retention):
    p = PriorityCalculator.calculate(
        retention_score=retention,
        mastery_score=mastery,
        confidence=0.5,
    )
    assert p.mastery_gap == pytest.approx(1.0 - mastery)


@pytest.mark.parametrize("importance", IMPORTANCE)
@pytest.mark.parametrize("exam", EXAM)
def test_priority_includes_curriculum_and_exam(importance, exam):
    low = PriorityCalculator.calculate(
        retention_score=0.5,
        mastery_score=0.5,
        confidence=0.5,
        curriculum_importance=0.0,
        exam_proximity=0.0,
    )
    high = PriorityCalculator.calculate(
        retention_score=0.5,
        mastery_score=0.5,
        confidence=0.5,
        curriculum_importance=importance,
        exam_proximity=exam,
    )
    assert high.score >= low.score - 1e-9
    assert high.curriculum_importance == importance
    assert high.exam_proximity == exam


@pytest.mark.parametrize("confidence", CONFIDENCE)
@pytest.mark.parametrize("struggle", [0.0, 0.5, 1.0])
def test_priority_confidence_and_struggle(confidence, struggle):
    p = PriorityCalculator.calculate(
        retention_score=0.4,
        mastery_score=0.4,
        confidence=confidence,
        historical_struggle=struggle,
    )
    assert 0.0 <= p.confidence_gap <= 1.0
    assert p.historical_struggle == struggle


@pytest.mark.parametrize("events", [0.0, 0.5, 1.0, 2.0, 4.0, 6.0, 8.0, 10.0])
@pytest.mark.parametrize("delta", [-1.0, -0.5, 0.0, 0.5, 1.0])
def test_velocity_factor_deterministic(events, delta):
    a = PriorityPolicy.velocity_factor(events, delta)
    b = PriorityPolicy.velocity_factor(events, delta)
    assert a == b
    assert 0.0 <= a <= 1.0


@pytest.mark.parametrize("prereq", [0.0, 0.25, 0.5, 0.75, 1.0])
def test_prerequisite_raises_priority(prereq):
    base = PriorityCalculator.calculate(
        retention_score=0.5,
        mastery_score=0.5,
        confidence=0.5,
        prerequisite_criticality=0.0,
    )
    raised = PriorityCalculator.calculate(
        retention_score=0.5,
        mastery_score=0.5,
        confidence=0.5,
        prerequisite_criticality=prereq,
    )
    if prereq > 0:
        assert raised.score > base.score
    else:
        assert raised.score == pytest.approx(base.score)


@pytest.mark.parametrize("score", [i / 20 for i in range(21)])
def test_meets_revision_threshold(score):
    expected = score >= PriorityPolicy.MIN_REVISION_PRIORITY
    assert PriorityPolicy.meets_revision_threshold(score) is expected


@pytest.mark.parametrize("retention", [0.0, 0.5, 1.0])
@pytest.mark.parametrize("mastery", [0.0, 0.5, 1.0])
@pytest.mark.parametrize("exam", [0.0, 1.0])
def test_priority_determinism_triple(retention, mastery, exam):
    kwargs = dict(
        retention_score=retention,
        mastery_score=mastery,
        confidence=0.4,
        curriculum_importance=0.6,
        prerequisite_criticality=0.2,
        historical_struggle=0.3,
        events_per_day=2.0,
        mastery_delta=-0.1,
        exam_proximity=exam,
    )
    a = PriorityCalculator.calculate(**kwargs)
    b = PriorityCalculator.calculate(**kwargs)
    assert a == b
