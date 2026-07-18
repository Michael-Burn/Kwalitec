"""ROI estimation matrix — educational benefit vs study time."""

from __future__ import annotations

import pytest

from app.application.adaptive_learning.policies.roi_policy import ROIPolicy
from app.application.adaptive_learning.priority_calculator import PriorityCalculator
from app.application.adaptive_learning.roi_estimator import ROIEstimator
from app.domain.adaptive_learning.educational_roi import EducationalROI

PRIORITIES = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
RISKS = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
GAPS = [0.0, 0.5, 1.0]
IMPORTANCE = [0.0, 0.5, 1.0]


@pytest.mark.parametrize("priority", PRIORITIES)
@pytest.mark.parametrize("risk", [0.0, 0.5, 1.0])
def test_study_minutes_bounded(priority, risk):
    minutes = ROIPolicy.estimate_study_minutes(
        priority_score=priority,
        retention_risk=risk,
        mastery_gap=0.4,
    )
    assert ROIPolicy.MIN_STUDY_MINUTES <= minutes <= ROIPolicy.MAX_STUDY_MINUTES


@pytest.mark.parametrize("risk", RISKS)
@pytest.mark.parametrize("gap", [0.0, 0.5, 1.0])
def test_readiness_improvement_bounded(risk, gap):
    improvement = ROIPolicy.estimate_readiness_improvement(
        retention_risk=risk,
        mastery_gap=gap,
        curriculum_importance=0.5,
    )
    assert 0.0 <= improvement <= ROIPolicy.MAX_READINESS_IMPROVEMENT


@pytest.mark.parametrize("priority", PRIORITIES)
@pytest.mark.parametrize("importance", IMPORTANCE)
def test_roi_estimator_determinism(priority, importance):
    a = ROIEstimator.estimate(
        priority=priority,
        retention_risk=0.6,
        mastery_gap=0.5,
        curriculum_importance=importance,
    )
    b = ROIEstimator.estimate(
        priority=priority,
        retention_risk=0.6,
        mastery_gap=0.5,
        curriculum_importance=importance,
    )
    assert a == b
    assert a.estimated_study_minutes > 0.0
    assert a.return_on_study_time == a.cost_benefit_ratio


@pytest.mark.parametrize("gap", GAPS)
@pytest.mark.parametrize("risk", GAPS)
@pytest.mark.parametrize("importance", IMPORTANCE)
def test_roi_from_priority_object(gap, risk, importance):
    priority = PriorityCalculator.calculate(
        retention_score=1.0 - risk,
        mastery_score=1.0 - gap,
        confidence=0.5,
        curriculum_importance=importance,
    )
    roi = ROIEstimator.estimate(
        priority=priority,
        retention_risk=risk,
        mastery_gap=gap,
        curriculum_importance=importance,
    )
    assert isinstance(roi, EducationalROI)
    assert 0.0 <= roi.educational_benefit <= 1.0
    assert roi.expected_readiness_improvement >= 0.0


@pytest.mark.parametrize(
    "ratio,expected",
    [
        (0.0, False),
        (0.14, False),
        (0.15, True),
        (1.0, True),
        (10.0, True),
    ],
)
def test_worthwhile_threshold(ratio, expected):
    assert ROIPolicy.is_worthwhile(ratio) is expected


@pytest.mark.parametrize("priority", [0.2, 0.4, 0.6, 0.8, 1.0])
def test_higher_priority_not_shorter_than_lower(priority):
    low = ROIPolicy.estimate_study_minutes(
        priority_score=0.2,
        retention_risk=0.5,
        mastery_gap=0.5,
    )
    high = ROIPolicy.estimate_study_minutes(
        priority_score=priority,
        retention_risk=0.5,
        mastery_gap=0.5,
    )
    if priority >= 0.2:
        assert high >= low


@pytest.mark.parametrize("risk", RISKS)
def test_benefit_phrase_inputs_stable(risk):
    benefit = ROIPolicy.educational_benefit(
        readiness_improvement=0.2,
        curriculum_importance=0.5,
        priority_score=0.6,
    )
    assert 0.0 <= benefit <= 1.0
    # risk unused — ensure call remains deterministic across loop
    _ = risk
    assert benefit == ROIPolicy.educational_benefit(
        readiness_improvement=0.2,
        curriculum_importance=0.5,
        priority_score=0.6,
    )
