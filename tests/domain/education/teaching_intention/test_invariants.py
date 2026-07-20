"""Invariant enforcement for Teaching Intention."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import DiagnosisType, TeachingIntentionType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.teaching_intention import (
    IntentionConstraintKind,
    IntentionStrengthLevel,
)
from tests.domain.education.teaching_intention.conftest import (
    make_constraint,
    make_diagnosis_ref,
    make_goal,
    make_intention,
    make_outcome,
    make_priority_ref,
    make_strength,
)


def test_cannot_duplicate_constraints() -> None:
    c1 = make_constraint(
        constraint_id="c1",
        kind=IntentionConstraintKind.PROTECT_ATOMICITY,
    )
    c2 = make_constraint(
        constraint_id="c2",
        kind=IntentionConstraintKind.PROTECT_ATOMICITY,
    )
    with pytest.raises(EducationalInvariantViolation, match="duplicate constraints"):
        make_intention(constraints=[c1, c2])


def test_duplicate_constraint_ids_rejected() -> None:
    c1 = make_constraint(
        constraint_id="same",
        kind=IntentionConstraintKind.PROTECT_ATOMICITY,
    )
    c2 = make_constraint(
        constraint_id="same",
        kind=IntentionConstraintKind.FORBID_STRATEGY_SELECTION,
    )
    with pytest.raises(EducationalInvariantViolation, match="duplicate"):
        make_intention(constraints=[c1, c2])


def test_cannot_contradict_priority_via_misaligned_type() -> None:
    with pytest.raises(EducationalInvariantViolation, match="not aligned"):
        make_intention(
            intention_type=TeachingIntentionType.PREPARE_FOR_EXAMINATION,
            goal=make_goal(
                intention_type=TeachingIntentionType.PREPARE_FOR_EXAMINATION
            ),
            diagnosis_references=[
                make_diagnosis_ref(diagnosis_type=DiagnosisType.MISCONCEPTION)
            ],
        )


def test_goal_must_match_intention_type() -> None:
    with pytest.raises(EducationalInvariantViolation, match="match"):
        make_intention(
            intention_type=TeachingIntentionType.STRENGTHEN_PREREQUISITE,
            goal=make_goal(intention_type=TeachingIntentionType.IMPROVE_TRANSFER),
        )


def test_mastery_claim_forbidden_in_goal() -> None:
    with pytest.raises(EducationalInvariantViolation, match="mastery"):
        make_goal(statement="Make the student fully mastered on this objective")


def test_mastery_claim_forbidden_in_outcome() -> None:
    with pytest.raises(EducationalInvariantViolation, match="mastery"):
        make_outcome(statement="Achieve mastery this episode")


def test_strategy_language_forbidden_in_goal() -> None:
    with pytest.raises(EducationalInvariantViolation, match="strategy"):
        make_goal(statement="Use interleaved practice to fix the gap")


def test_cap_strength_constraint_enforced() -> None:
    constraint = make_constraint(
        kind=IntentionConstraintKind.CAP_STRENGTH,
        max_strength=IntentionStrengthLevel.MODERATE,
    )
    intention = make_intention(
        constraints=[constraint],
        strength=make_strength(IntentionStrengthLevel.MODERATE),
        activate=True,
    )
    with pytest.raises(EducationalInvariantViolation, match="cap"):
        intention.strengthen()


def test_forbid_intention_type_constraint() -> None:
    constraint = make_constraint(
        kind=IntentionConstraintKind.FORBID_INTENTION_TYPE,
        forbidden_intention_type=TeachingIntentionType.PREPARE_FOR_EXAMINATION,
    )
    with pytest.raises(EducationalInvariantViolation, match="forbids"):
        make_intention(
            intention_type=TeachingIntentionType.PREPARE_FOR_EXAMINATION,
            goal=make_goal(
                intention_type=TeachingIntentionType.PREPARE_FOR_EXAMINATION
            ),
            diagnosis_references=[
                make_diagnosis_ref(
                    diagnosis_type=DiagnosisType.EXAM_TECHNIQUE_WEAKNESS
                )
            ],
            constraints=[constraint],
        )


def test_require_hypothesis_constraint() -> None:
    constraint = make_constraint(
        kind=IntentionConstraintKind.REQUIRE_HYPOTHESIS_REFERENCE,
    )
    with pytest.raises(EducationalInvariantViolation, match="hypothesis"):
        make_intention(constraints=[constraint], hypothesis_references=[])


def test_duplicate_priority_references_rejected() -> None:
    with pytest.raises(EducationalInvariantViolation, match="duplicate priority"):
        make_intention(
            priority_references=[make_priority_ref(), make_priority_ref()]
        )


def test_duplicate_diagnosis_references_rejected() -> None:
    with pytest.raises(EducationalInvariantViolation, match="duplicate diagnosis"):
        make_intention(
            diagnosis_references=[
                make_diagnosis_ref(),
                make_diagnosis_ref(),
            ]
        )


def test_exam_vs_misconception_alignment_guard() -> None:
    with pytest.raises(EducationalInvariantViolation, match="misconception"):
        make_intention(
            intention_type=TeachingIntentionType.PREPARE_FOR_EXAMINATION,
            goal=make_goal(
                intention_type=TeachingIntentionType.PREPARE_FOR_EXAMINATION
            ),
            diagnosis_references=[
                make_diagnosis_ref(
                    diagnosis_id="d1",
                    diagnosis_type=DiagnosisType.MISCONCEPTION,
                ),
                make_diagnosis_ref(
                    diagnosis_id="d2",
                    diagnosis_type=DiagnosisType.EXAM_TECHNIQUE_WEAKNESS,
                ),
            ],
            # Still fails: misconception present without pure exam path when
            # protect conceptual honesty constraint is present.
            constraints=[
                make_constraint(
                    kind=IntentionConstraintKind.PROTECT_CONCEPTUAL_HONESTY_OVER_EXAM,
                )
            ],
        )


def test_cannot_activate_twice() -> None:
    intention = make_intention(activate=True)
    with pytest.raises(EducationalInvariantViolation, match="already activated"):
        intention.activate()


def test_cannot_retire_twice() -> None:
    intention = make_intention(activate=True)
    intention.retire()
    with pytest.raises(EducationalInvariantViolation, match="already retired"):
        intention.retire()
