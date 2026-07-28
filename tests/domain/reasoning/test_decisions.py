"""Domain tests for educational decisions (AP-002D3)."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.domain.reasoning.decisions.category import DecisionCategory
from app.domain.reasoning.decisions.context import DecisionContext
from app.domain.reasoning.decisions.decision import EducationalDecision
from app.domain.reasoning.decisions.decision_set import EducationalDecisionSet
from app.domain.reasoning.decisions.errors import (
    DuplicateDecision,
    UnknownDecisionCategory,
)
from app.domain.reasoning.decisions.reason import DecisionReason
from app.domain.reasoning.decisions.reference import DecisionReference
from app.domain.reasoning.decisions.version import DECISION_VERSION

FIXED = datetime(2026, 7, 28, 12, 0, 0, tzinfo=UTC).replace(tzinfo=None)


def _context(**overrides) -> DecisionContext:
    base = dict(
        twin_id="twin-1",
        reasoning_request_id="rrq-1",
        evidence_bundle_id="bundle-1",
        session_id="sess-1",
        correlation_id="corr-1",
        decision_version=DECISION_VERSION,
        prior_twin_version=1,
        observation_set_id="eos-1",
    )
    base.update(overrides)
    return DecisionContext(**base)


def _decision(*, decision_id: str = "ed-1", **overrides) -> EducationalDecision:
    base = dict(
        decision_id=decision_id,
        category=DecisionCategory.PROVENANCE_RECORDED,
        twin_id="twin-1",
        subject_ref="twin-1",
        value={"ok": True},
        reason=DecisionReason(code="prov", summary="provenance"),
        reference=DecisionReference(
            evidence_bundle_id="bundle-1",
            educational_observation_ids=("eo-1",),
            reasoning_request_id="rrq-1",
            assessment_session_id="sess-1",
            correlation_id="corr-1",
            learning_objective_reference="lo-1",
            concept_reference="concept-bayes",
            decision_id=decision_id,
        ),
        decision_version=DECISION_VERSION,
        created_at=FIXED,
        provenance={
            "evidence_bundle_id": "bundle-1",
            "educational_observation_ids": ["eo-1"],
            "reasoning_request_id": "rrq-1",
            "decision_id": decision_id,
            "decision_version": DECISION_VERSION,
            "assessment_session_id": "sess-1",
            "correlation_id": "corr-1",
        },
        traceability={
            "evidence_bundle_id": "bundle-1",
            "educational_observation_ids": ["eo-1"],
            "reasoning_request_id": "rrq-1",
            "decision_id": decision_id,
            "decision_version": DECISION_VERSION,
            "assessment_session_id": "sess-1",
            "correlation_id": "corr-1",
            "twin_id": "twin-1",
        },
    )
    base.update(overrides)
    return EducationalDecision(**base)


def test_decision_is_immutable() -> None:
    decision = _decision()
    with pytest.raises(AttributeError):
        decision.decision_id = "x"  # type: ignore[misc]


def test_unknown_category_rejected() -> None:
    with pytest.raises(UnknownDecisionCategory):
        _decision(category="not_a_category")


def test_decision_set_rejects_duplicates() -> None:
    ctx = _context()
    with pytest.raises(DuplicateDecision):
        EducationalDecisionSet(
            set_id="eds-1",
            decisions=(_decision(decision_id="same"), _decision(decision_id="same")),
            context=ctx,
            decision_version=DECISION_VERSION,
        )


def test_decision_set_observation_ids_deduped() -> None:
    ctx = _context()
    d1 = _decision(decision_id="a")
    d2 = _decision(
        decision_id="b",
        reference=DecisionReference(
            evidence_bundle_id="bundle-1",
            educational_observation_ids=("eo-1", "eo-2"),
            reasoning_request_id="rrq-1",
            assessment_session_id="sess-1",
            correlation_id="corr-1",
            learning_objective_reference="lo-1",
            decision_id="b",
        ),
    )
    decision_set = EducationalDecisionSet(
        set_id="eds-1",
        decisions=(d1, d2),
        context=ctx,
        decision_version=DECISION_VERSION,
    )
    assert decision_set.observation_ids == ("eo-1", "eo-2")
