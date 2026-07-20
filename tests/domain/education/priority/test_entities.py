"""Unit tests for Educational Priority entities."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import DiagnosisType, LearningDimension
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DiagnosisId, HypothesisId
from domain.education.foundation.references import ConceptReference
from domain.education.priority import (
    DiagnosisReference,
    HypothesisReference,
    PriorityConstraint,
    PriorityConstraintId,
    PriorityConstraintKind,
    PriorityFactor,
    PriorityFactorId,
    PriorityFactorKind,
    PriorityScope,
    PriorityScopeId,
    PriorityScopeKind,
    PriorityScoreBand,
    UrgencyLevel,
)
from tests.domain.education.priority.conftest import (
    CONCEPT_SELECT,
    make_constraint,
    make_factor,
    make_scope,
)


@pytest.mark.parametrize("kind", list(PriorityFactorKind))
def test_factor_accepts_all_kinds(kind: PriorityFactorKind) -> None:
    factor = make_factor(kind=kind, factor_id=f"f-{kind.value}")
    assert factor.kind is kind
    assert 0.0 <= factor.contribution <= 1.0


def test_factor_rejects_out_of_range_contribution() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_factor(contribution=1.1)
    with pytest.raises(EducationalInvariantViolation):
        make_factor(contribution=-0.01)


def test_factor_rejects_blank_rationale() -> None:
    with pytest.raises(EducationalInvariantViolation):
        PriorityFactor(
            factor_id=PriorityFactorId("f1"),
            kind=PriorityFactorKind.EXAM_RELEVANCE,
            contribution=0.5,
            rationale=" ",
        )


def test_factor_identity_equality() -> None:
    left = make_factor(factor_id="same", contribution=0.2)
    right = make_factor(factor_id="same", contribution=0.9)
    other = make_factor(factor_id="other", contribution=0.2)
    assert left == right
    assert left != other
    assert hash(left) == hash(right)


def test_factor_with_contribution_and_rationale() -> None:
    factor = make_factor(contribution=0.4)
    amended = factor.with_contribution(0.9).with_rationale("Stronger pressure")
    assert amended.contribution == 0.9
    assert amended.rationale == "Stronger pressure"
    assert amended.factor_id == factor.factor_id


def test_scope_requires_statement() -> None:
    with pytest.raises(EducationalInvariantViolation):
        PriorityScope(
            scope_id=PriorityScopeId("s1"),
            statement="",
            scope_kind=PriorityScopeKind.CONCEPT,
        )


@pytest.mark.parametrize("scope_kind", list(PriorityScopeKind))
def test_scope_accepts_all_kinds(scope_kind: PriorityScopeKind) -> None:
    scope = make_scope(scope_kind=scope_kind, scope_id=f"s-{scope_kind.value}")
    assert scope.scope_kind is scope_kind


def test_scope_rejects_duplicate_concepts() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_scope(
            concepts=(
                ConceptReference(concept_id=CONCEPT_SELECT),
                ConceptReference(concept_id=CONCEPT_SELECT),
            )
        )


def test_scope_concept_and_episode_helpers() -> None:
    scope = make_scope()
    assert CONCEPT_SELECT in scope.concept_ids()
    assert scope.with_statement("Amended locus").statement == "Amended locus"


@pytest.mark.parametrize("dimension", list(LearningDimension))
def test_scope_dimensions(dimension: LearningDimension) -> None:
    scope = make_scope(dimension=dimension, scope_id=f"s-{dimension.value}")
    assert scope.learning_dimension is dimension


def test_constraint_cap_urgency_requires_payload() -> None:
    with pytest.raises(EducationalInvariantViolation):
        PriorityConstraint(
            constraint_id=PriorityConstraintId("c1"),
            kind=PriorityConstraintKind.CAP_URGENCY,
            statement="Cap urgency",
        )


def test_constraint_require_factor_requires_payload() -> None:
    with pytest.raises(EducationalInvariantViolation):
        PriorityConstraint(
            constraint_id=PriorityConstraintId("c1"),
            kind=PriorityConstraintKind.REQUIRE_FACTOR,
            statement="Require factor",
        )


def test_constraint_cap_score_ok() -> None:
    constraint = make_constraint(
        kind=PriorityConstraintKind.CAP_SCORE,
        max_score_band=PriorityScoreBand.HIGH,
    )
    assert constraint.max_score_band is PriorityScoreBand.HIGH


def test_constraint_identity_equality() -> None:
    left = make_constraint(constraint_id="same")
    right = make_constraint(
        constraint_id="same",
        kind=PriorityConstraintKind.FORBID_ENGAGEMENT_ORDERING,
    )
    assert left == right


def test_diagnosis_reference_validation() -> None:
    ref = DiagnosisReference(
        diagnosis_id=DiagnosisId("diag-x"),
        diagnosis_type=DiagnosisType.MISCONCEPTION,
    )
    assert "diag-x" in str(ref)
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisReference(
            diagnosis_id="diag-x",  # type: ignore[arg-type]
            diagnosis_type=DiagnosisType.MISCONCEPTION,
        )


def test_hypothesis_reference_validation() -> None:
    ref = HypothesisReference(hypothesis_id=HypothesisId("hyp-x"))
    assert str(ref) == "hyp-x"
    with pytest.raises(EducationalInvariantViolation):
        HypothesisReference(hypothesis_id="hyp-x")  # type: ignore[arg-type]


def test_factor_signature_stable() -> None:
    factor = make_factor(contribution=0.3333334)
    assert factor.factor_signature()[0] == factor.kind.value


def test_constraint_with_max_urgency() -> None:
    constraint = make_constraint(
        kind=PriorityConstraintKind.CAP_URGENCY,
        max_urgency=UrgencyLevel.ELEVATED,
    )
    assert constraint.max_urgency is UrgencyLevel.ELEVATED
