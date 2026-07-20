"""Entity tests for Teaching Intention."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import (
    DiagnosisType,
    LearningDimension,
    TeachingIntentionType,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, MisconceptionId, PriorityId
from domain.education.foundation.references import (
    ConceptReference,
    MisconceptionReference,
)
from domain.education.teaching_intention import (
    DiagnosisReference,
    HypothesisReference,
    IntentionConstraintKind,
    IntentionGoal,
    IntentionGoalId,
    IntentionScopeKind,
    IntentionStrengthLevel,
    PriorityReference,
)
from tests.domain.education.teaching_intention.conftest import (
    make_constraint,
    make_goal,
    make_hypothesis_ref,
    make_scope,
)


def test_goal_identity_equality() -> None:
    a = make_goal(goal_id="g1", statement="Repair wrong model of select ages")
    b = make_goal(goal_id="g1", statement="Different statement same id")
    c = make_goal(goal_id="g2")
    assert a == b
    assert a != c


def test_goal_with_statement() -> None:
    goal = make_goal()
    amended = goal.with_statement("Establish minimal correct explanation")
    assert amended.statement == "Establish minimal correct explanation"
    assert amended.goal_id == goal.goal_id


def test_scope_rejects_duplicate_concepts() -> None:
    ref = ConceptReference(concept_id=ConceptId("c1"), label="A")
    with pytest.raises(EducationalInvariantViolation, match="duplicate concept"):
        make_scope(concepts=(ref, ref))


def test_scope_rejects_duplicate_misconceptions() -> None:
    ref = MisconceptionReference(
        misconception_id=MisconceptionId("m1"),
        label="Wrong model",
    )
    with pytest.raises(
        EducationalInvariantViolation, match="duplicate misconception"
    ):
        make_scope(
            scope_kind=IntentionScopeKind.MISCONCEPTION,
            misconceptions=(ref, ref),
        )


def test_scope_with_statement() -> None:
    scope = make_scope()
    amended = scope.with_statement("Narrowed instructional locus")
    assert amended.statement == "Narrowed instructional locus"
    assert amended.concept_ids() == scope.concept_ids()


def test_scope_dimension_and_kinds() -> None:
    for kind in IntentionScopeKind:
        scope = make_scope(
            scope_id=f"s-{kind.value}",
            statement=f"Scope {kind.value}",
            scope_kind=kind,
            dimension=LearningDimension.TRANSFER,
        )
        assert scope.scope_kind is kind
        assert scope.learning_dimension is LearningDimension.TRANSFER


def test_constraint_cap_strength_requires_payload() -> None:
    with pytest.raises(EducationalInvariantViolation, match="max_strength"):
        make_constraint(kind=IntentionConstraintKind.CAP_STRENGTH)


def test_constraint_forbid_type_requires_payload() -> None:
    with pytest.raises(
        EducationalInvariantViolation, match="forbidden_intention_type"
    ):
        make_constraint(kind=IntentionConstraintKind.FORBID_INTENTION_TYPE)


def test_constraint_signature_stable() -> None:
    c = make_constraint(
        kind=IntentionConstraintKind.CAP_STRENGTH,
        max_strength=IntentionStrengthLevel.FIRM,
    )
    assert c.constraint_signature() == (
        "cap_strength",
        None,
        "firm",
    )


def test_priority_reference_validation() -> None:
    ref = PriorityReference(priority_id=PriorityId("p1"))
    assert str(ref) == "p1"
    with pytest.raises(EducationalInvariantViolation):
        PriorityReference(priority_id="not-an-id")  # type: ignore[arg-type]


def test_diagnosis_reference_str() -> None:
    from domain.education.foundation.ids import DiagnosisId

    ref = DiagnosisReference(
        diagnosis_id=DiagnosisId("diag-x"),
        diagnosis_type=DiagnosisType.MISCONCEPTION,
    )
    assert "misconception" in str(ref)


def test_hypothesis_reference() -> None:
    ref = make_hypothesis_ref(hypothesis_id="hyp-z")
    assert str(ref) == "hyp-z"
    assert isinstance(ref, HypothesisReference)


def test_goal_rejects_blank_statement() -> None:
    with pytest.raises(EducationalInvariantViolation):
        IntentionGoal(
            goal_id=IntentionGoalId("g-blank"),
            statement="   ",
            intention_type=TeachingIntentionType.BUILD_INTUITION,
        )


def test_goal_success_hint_optional() -> None:
    goal = make_goal(success_evidence_hint=None)
    assert goal.success_evidence_hint is None
    amended = goal.with_success_evidence_hint("Correct paraphrase")
    assert amended.success_evidence_hint == "Correct paraphrase"
