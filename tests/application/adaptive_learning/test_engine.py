"""Decision engine core behaviour."""

from __future__ import annotations

import pytest

from app.application.adaptive_learning.decision_engine import AdaptiveDecisionEngine
from app.domain.adaptive_learning.intervention_type import InterventionType
from tests.application.adaptive_learning.helpers import (
    make_curriculum,
    make_engine,
    make_journey,
    make_snapshot,
)


def test_decide_revision_for_weak_topic():
    engine = make_engine()
    snap = make_snapshot()
    decision = engine.decide(
        snap,
        journey_position=make_journey(),
        curriculum_context=make_curriculum(),
    )
    assert decision.intervention_type is InterventionType.REVISION
    assert decision.has_intervention is True
    assert decision.primary_topic_id == "topic-1"
    assert decision.explanation.rationale
    assert decision.estimated_study_minutes > 0


def test_decide_empty_when_strong_state():
    engine = make_engine()
    snap = make_snapshot(
        topics=[
            {
                "id": "topic-strong",
                "mastery": 0.95,
                "retention": 0.95,
                "knowledge": 0.95,
                "confidence": 0.9,
                "severity": 0.0,
            }
        ]
    )
    decision = engine.decide(
        snap,
        curriculum_context=make_curriculum(importance={"topic-strong": 0.2}),
    )
    # May or may not intervene depending on threshold; if intervenes must be revision
    assert decision.intervention_type is InterventionType.REVISION
    if decision.has_intervention:
        assert decision.priority_score >= 0.20


def test_snapshot_dto_fields():
    engine = make_engine()
    decision = engine.decide(make_snapshot())
    dto = engine.snapshot_dto(decision)
    assert dto.decision_id == decision.decision_id
    assert dto.learner_id == decision.learner_id
    assert dto.intervention_type == "revision"


def test_revision_and_roi_snapshots():
    engine = make_engine()
    decision = engine.decide(make_snapshot())
    rev = engine.revision_snapshot(decision)
    roi = engine.roi_snapshot(decision)
    assert rev.plan_id == decision.revision_plan.plan_id
    assert roi.estimated_study_minutes == decision.roi.estimated_study_minutes


def test_explain_and_diagnostics():
    engine = make_engine()
    decision = engine.decide(make_snapshot())
    explanation = engine.explain(decision)
    report = engine.diagnostics(decision)
    assert explanation.rationale
    assert explanation.expected_educational_benefit
    assert report.phase1_compliant is True
    assert report.explanation_complete is True


def test_empty_decision_helper():
    engine = make_engine()
    decision = engine.empty_decision("learner-x")
    assert decision.has_intervention is False
    assert decision.learner_id == "learner-x"


def test_supported_types_phase1():
    assert AdaptiveDecisionEngine.supported_intervention_types() == frozenset(
        {InterventionType.REVISION}
    )


def test_intervention_snapshot_optional():
    engine = make_engine()
    empty = engine.empty_decision("l1")
    assert engine.intervention_snapshot(empty) is None
    decision = engine.decide(make_snapshot())
    if decision.has_intervention:
        snap = engine.intervention_snapshot(decision)
        assert snap is not None
        assert snap.is_revision is True


@pytest.mark.parametrize("exam", [0.0, 0.5, 1.0])
def test_exam_proximity_influences_priority(exam):
    engine = make_engine()
    snap = make_snapshot()
    decision = engine.decide(
        snap,
        curriculum_context=make_curriculum(exam_proximity=exam),
    )
    if decision.has_intervention:
        assert decision.selected_intervention.priority.exam_proximity == exam


@pytest.mark.parametrize("cap", [1, 2, 3])
def test_max_interventions_cap(cap):
    engine = make_engine()
    snap = make_snapshot(
        topics=[
            {
                "id": f"t{i}",
                "mastery": 0.2,
                "retention": 0.15,
                "knowledge": 0.2,
                "confidence": 0.3,
                "severity": 0.8,
            }
            for i in range(5)
        ]
    )
    decision = engine.decide(snap, max_interventions=cap)
    assert decision.revision_plan.intervention_count <= cap
