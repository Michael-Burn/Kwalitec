"""Intervention selection and explanation tests."""

from __future__ import annotations

import pytest

from app.application.adaptive_learning.explanation_service import ExplanationService
from app.application.adaptive_learning.intervention_selector import InterventionSelector
from app.application.adaptive_learning.policies.intervention_policy import (
    InterventionPolicy,
)
from app.domain.adaptive_learning.intervention_type import InterventionType
from tests.application.adaptive_learning.helpers import make_engine, make_snapshot
from tests.domain.adaptive_learning.helpers import make_candidate, make_explanation


@pytest.mark.parametrize(
    "itype",
    [
        InterventionType.CONTINUE,
        InterventionType.REPEAT,
        InterventionType.ASSESS,
        InterventionType.BREAK,
        InterventionType.SKIP,
    ],
)
def test_non_revision_types_unsupported_in_phase1(itype):
    assert InterventionPolicy.is_supported(itype) is False
    with pytest.raises(ValueError):
        InterventionPolicy.assert_supported(itype)


def test_revision_supported():
    assert InterventionPolicy.is_supported(InterventionType.REVISION) is True
    InterventionPolicy.assert_supported(InterventionType.REVISION)


@pytest.mark.parametrize("n", range(0, 8))
def test_selector_caps_interventions(n):
    candidates = [
        make_candidate(f"t{i}", priority=0.9 - i * 0.05, retention=0.2)
        for i in range(n)
    ]
    selected, plan = InterventionSelector.select_revision(candidates, plan_id="p")
    if n == 0:
        assert selected is None
        assert plan.is_empty
    else:
        assert selected is not None
        assert plan.intervention_count <= InterventionPolicy.max_interventions()
        assert all(i.is_revision for i in plan.interventions)


@pytest.mark.parametrize("priority", [0.05, 0.1, 0.19])
def test_selector_rejects_below_threshold(priority):
    candidates = [make_candidate("t1", priority=priority, retention=0.9)]
    selected, plan = InterventionSelector.select_revision(candidates)
    assert selected is None
    assert plan.is_empty


@pytest.mark.parametrize("priority", [0.2, 0.5, 0.9])
def test_selector_accepts_at_or_above_threshold(priority):
    candidates = [make_candidate("t1", priority=priority, retention=0.2)]
    selected, plan = InterventionSelector.select_revision(candidates)
    assert selected is not None
    assert plan.intervention_count == 1
    ExplanationService.require_complete(selected.explanation)


def test_explain_decision_dto():
    engine = make_engine()
    decision = engine.decide(make_snapshot())
    dto = ExplanationService.explain_decision(decision)
    assert dto.rationale
    assert dto.expected_educational_benefit
    assert dto.priority_score == decision.explanation.priority_score


def test_require_complete_rejects_empty_rationale():
    from app.application.adaptive_learning.exceptions import ExplanationError
    from app.domain.adaptive_learning.decision_explanation import DecisionExplanation
    from app.domain.adaptive_learning.intervention_priority import PriorityBand
    from app.domain.student_twin.confidence_band import ConfidenceBand

    broken = DecisionExplanation(
        evidence_considered=(),
        rationale="",
        priority_score=0.5,
        priority_band=PriorityBand.MEDIUM,
        expected_educational_benefit="x",
        confidence=ConfidenceBand.MEDIUM,
    )
    with pytest.raises(ExplanationError):
        ExplanationService.require_complete(broken)


@pytest.mark.parametrize("kind", list(InterventionType))
def test_select_preferred_type_phase1(kind):
    candidates = [make_candidate("t1", priority=0.8, retention=0.2)]
    if kind is InterventionType.REVISION:
        selected, plan = InterventionSelector.select(candidates, preferred_type=kind)
        assert selected is not None
        assert not plan.is_empty
    else:
        with pytest.raises(ValueError):
            InterventionSelector.select(candidates, preferred_type=kind)


def test_make_explanation_helper_usable():
    explanation = make_explanation()
    assert explanation.has_evidence is True
