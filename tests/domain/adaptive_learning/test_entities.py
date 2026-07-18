"""Domain entity and value-object tests for adaptive learning."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.domain.adaptive_learning.adaptive_decision import AdaptiveDecision
from app.domain.adaptive_learning.decision_snapshot import DecisionSnapshot
from app.domain.adaptive_learning.educational_roi import EducationalROI
from app.domain.adaptive_learning.intervention_priority import (
    InterventionPriority,
    PriorityBand,
    priority_band_from_score,
)
from app.domain.adaptive_learning.intervention_type import (
    PHASE1_IMPLEMENTED_TYPES,
    InterventionType,
    is_phase1_implemented,
    resolve_intervention_type,
)
from app.domain.adaptive_learning.revision_plan import RevisionPlan
from app.domain.adaptive_learning.revision_window import (
    RevisionUrgency,
    urgency_from_priority,
)
from app.domain.student_twin.confidence_band import ConfidenceBand
from tests.domain.adaptive_learning.helpers import (
    make_candidate,
    make_explanation,
    make_intervention,
    make_plan,
    make_priority,
    make_roi,
    make_window,
)


@pytest.mark.parametrize("value", list(InterventionType))
def test_resolve_intervention_type_roundtrip(value):
    assert resolve_intervention_type(value) is value
    assert resolve_intervention_type(value.value) is value


@pytest.mark.parametrize("value", list(InterventionType))
def test_phase1_only_revision_implemented(value):
    assert is_phase1_implemented(value) is (value is InterventionType.REVISION)


def test_phase1_implemented_types_is_revision_only():
    assert PHASE1_IMPLEMENTED_TYPES == frozenset({InterventionType.REVISION})


@pytest.mark.parametrize(
    "score,band",
    [
        (0.0, PriorityBand.NEGLIGIBLE),
        (0.19, PriorityBand.NEGLIGIBLE),
        (0.20, PriorityBand.LOW),
        (0.39, PriorityBand.LOW),
        (0.40, PriorityBand.MEDIUM),
        (0.64, PriorityBand.MEDIUM),
        (0.65, PriorityBand.HIGH),
        (0.84, PriorityBand.HIGH),
        (0.85, PriorityBand.CRITICAL),
        (1.0, PriorityBand.CRITICAL),
    ],
)
def test_priority_band_from_score(score, band):
    assert priority_band_from_score(score) is band


@pytest.mark.parametrize("score", [i / 20 for i in range(21)])
def test_priority_create_clamps_band(score):
    p = InterventionPriority.create(score)
    assert p.score == pytest.approx(score)
    assert p.band is priority_band_from_score(score)


@pytest.mark.parametrize("score", [-0.1, 1.1, 2.0])
def test_priority_rejects_out_of_range(score):
    with pytest.raises(ValueError):
        InterventionPriority.create(score)


def test_priority_negligible():
    p = InterventionPriority.negligible()
    assert p.score == 0.0
    assert p.band is PriorityBand.NEGLIGIBLE


@pytest.mark.parametrize("minutes", [0.0, 10.0, 45.0, 90.0])
def test_roi_create(minutes):
    roi = EducationalROI.create(
        expected_readiness_improvement=0.2,
        estimated_study_minutes=minutes,
        educational_benefit=0.4,
    )
    assert roi.estimated_study_minutes == minutes
    assert roi.cost_benefit_ratio >= 0.0


def test_roi_zero():
    roi = EducationalROI.zero()
    assert roi.educational_benefit == 0.0
    assert roi.is_worthwhile is False


@pytest.mark.parametrize("improvement", [-0.1, 1.1])
def test_roi_rejects_bad_improvement(improvement):
    with pytest.raises(ValueError):
        EducationalROI.create(
            expected_readiness_improvement=improvement,
            estimated_study_minutes=10.0,
        )


def test_explanation_requires_rationale():
    with pytest.raises(ValueError):
        make_explanation(rationale="   ")


def test_explanation_requires_benefit():
    with pytest.raises(ValueError):
        make_explanation(benefit="")


def test_intervention_is_revision():
    intervention = make_intervention()
    assert intervention.is_revision is True
    assert intervention.priority_score == pytest.approx(0.6)


def test_revision_plan_rejects_non_revision():
    from app.domain.adaptive_learning.intervention import Intervention

    bad = Intervention.create(
        "bad",
        InterventionType.CONTINUE,
        topic_id="t1",
        priority=make_priority(0.5),
        roi=make_roi(),
        explanation=make_explanation(),
        confidence=ConfidenceBand.MEDIUM,
    )
    with pytest.raises(ValueError, match="REVISION"):
        RevisionPlan.create("p1", interventions=[bad])


def test_revision_plan_topic_ids():
    plan = make_plan(topics=["a", "b"])
    assert plan.topic_ids == ("a", "b")
    assert plan.intervention_count == 2
    assert plan.is_empty is False


def test_revision_plan_empty():
    plan = RevisionPlan.empty()
    assert plan.is_empty is True
    assert plan.intervention_count == 0


@pytest.mark.parametrize("urgency", list(RevisionUrgency))
def test_window_urgency_roundtrip(urgency):
    window = make_window(urgency=urgency.value)
    assert window.urgency is urgency
    assert window.duration_minutes > 0


@pytest.mark.parametrize(
    "priority,exam,expected",
    [
        (0.95, 0.8, RevisionUrgency.IMMEDIATE),  # 0.95*0.75+0.8*0.25 = 0.9125
        (0.9, 0.0, RevisionUrgency.TODAY),  # 0.675
        (0.7, 0.0, RevisionUrgency.THIS_WEEK),  # 0.525
        (0.5, 0.0, RevisionUrgency.DEFERRED),  # 0.375
        (0.6, 1.0, RevisionUrgency.TODAY),  # 0.70
    ],
)
def test_urgency_from_priority(priority, exam, expected):
    assert urgency_from_priority(priority, exam_proximity=exam) is expected


def test_candidate_ranking_key_orders_by_priority():
    low = make_candidate("a", priority=0.3)
    high = make_candidate("b", priority=0.9)
    assert high.ranking_key < low.ranking_key


def test_candidate_retention_risk_and_mastery_gap():
    c = make_candidate(retention=0.25, mastery=0.4)
    assert c.retention_risk == pytest.approx(0.75)
    assert c.mastery_gap == pytest.approx(0.6)


def test_adaptive_decision_from_intervention():
    intervention = make_intervention(topic_id="topic-x", priority=0.72)
    plan = RevisionPlan.create("plan-x", interventions=[intervention])
    decision = AdaptiveDecision.create(
        "dec-1",
        "learner-1",
        datetime(2026, 7, 18, tzinfo=UTC),
        selected_intervention=intervention,
        revision_plan=plan,
        explanation=intervention.explanation,
    )
    assert decision.has_intervention is True
    assert decision.primary_topic_id == "topic-x"
    assert decision.is_revision_decision is True
    snap = DecisionSnapshot.from_decision(decision)
    assert snap.topic_id == "topic-x"
    assert snap.is_actionable is True


def test_adaptive_decision_empty():
    explanation = make_explanation(rationale="none", priority=0.0)
    decision = AdaptiveDecision.create(
        "dec-empty",
        "learner-1",
        datetime(2026, 7, 18, tzinfo=UTC),
        selected_intervention=None,
        explanation=explanation,
    )
    assert decision.has_intervention is False
    assert decision.priority_score == 0.0
    snap = DecisionSnapshot.from_decision(decision)
    assert snap.is_actionable is False


@pytest.mark.parametrize("field", ["decision_id", "learner_id"])
def test_decision_requires_ids(field):
    kwargs = {
        "decision_id": "d1",
        "learner_id": "l1",
        "decided_at": datetime(2026, 7, 18, tzinfo=UTC),
        "selected_intervention": None,
        "explanation": make_explanation(),
    }
    kwargs[field] = "  "
    with pytest.raises(ValueError):
        AdaptiveDecision.create(**kwargs)
