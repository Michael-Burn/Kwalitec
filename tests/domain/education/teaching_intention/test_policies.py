"""Policy tests for Teaching Intention."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import DiagnosisType, TeachingIntentionType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.teaching_intention import (
    IntentionAlignmentPolicy,
    IntentionConstraintKind,
    IntentionStatus,
    IntentionStrengthLevel,
    IntentionValidationPolicy,
)
from tests.domain.education.teaching_intention.conftest import (
    INTENTION_DIAGNOSIS,
    make_constraint,
    make_diagnosis_ref,
    make_goal,
    make_intention,
    make_outcome,
    make_priority_ref,
    make_strength,
)


@pytest.mark.parametrize("intention_type", list(TeachingIntentionType))
def test_alignment_lawful_for_catalogue_defaults(
    intention_type: TeachingIntentionType,
) -> None:
    diagnosis_type = INTENTION_DIAGNOSIS[intention_type]
    assert IntentionAlignmentPolicy.is_type_aligned_with_diagnosis(
        intention_type, diagnosis_type
    )
    lawful = IntentionAlignmentPolicy.lawful_intention_types_for(diagnosis_type)
    assert intention_type in lawful


@pytest.mark.parametrize(
    ("diagnosis_type", "intention_type"),
    [
        (DiagnosisType.MISCONCEPTION, TeachingIntentionType.IMPROVE_TRANSFER),
        (
            DiagnosisType.PREREQUISITE_GAP,
            TeachingIntentionType.PREPARE_FOR_EXAMINATION,
        ),
        (
            DiagnosisType.LOW_CONFIDENCE,
            TeachingIntentionType.INCREASE_PROCEDURAL_FLUENCY,
        ),
        (DiagnosisType.WEAK_RETENTION, TeachingIntentionType.REPAIR_MISCONCEPTION),
    ],
)
def test_alignment_rejects_unlawful_pairs(
    diagnosis_type: DiagnosisType,
    intention_type: TeachingIntentionType,
) -> None:
    assert not IntentionAlignmentPolicy.is_type_aligned_with_diagnosis(
        intention_type, diagnosis_type
    )
    with pytest.raises(EducationalInvariantViolation, match="not aligned"):
        IntentionAlignmentPolicy.assert_aligned_with_diagnoses(
            intention_type,
            [make_diagnosis_ref(diagnosis_type=diagnosis_type)],
        )


def test_alignment_requires_priority() -> None:
    with pytest.raises(EducationalInvariantViolation, match="Priority"):
        IntentionAlignmentPolicy.assert_priority_not_contradicted(
            [],
            [make_diagnosis_ref()],
            TeachingIntentionType.STRENGTHEN_PREREQUISITE,
        )


def test_validation_status_guards() -> None:
    IntentionValidationPolicy.assert_can_activate(IntentionStatus.DRAFT)
    with pytest.raises(EducationalInvariantViolation):
        IntentionValidationPolicy.assert_can_activate(IntentionStatus.ACTIVE)
    with pytest.raises(EducationalInvariantViolation):
        IntentionValidationPolicy.assert_can_strengthen(IntentionStatus.DRAFT)
    with pytest.raises(EducationalInvariantViolation):
        IntentionValidationPolicy.assert_can_strengthen(IntentionStatus.RETIRED)
    IntentionValidationPolicy.assert_can_strengthen(IntentionStatus.ACTIVE)
    IntentionValidationPolicy.assert_can_weaken(IntentionStatus.REVISED)


def test_constraints_satisfied_protect_conceptual_honesty() -> None:
    with pytest.raises(EducationalInvariantViolation, match="misconception"):
        IntentionValidationPolicy.assert_constraints_satisfied(
            [
                make_constraint(
                    kind=IntentionConstraintKind.PROTECT_CONCEPTUAL_HONESTY_OVER_EXAM,
                )
            ],
            intention_type=TeachingIntentionType.PREPARE_FOR_EXAMINATION,
            strength=make_strength(),
            priority_references=[make_priority_ref()],
            diagnosis_references=[
                make_diagnosis_ref(diagnosis_type=DiagnosisType.MISCONCEPTION)
            ],
            hypothesis_references=[],
            expected_outcome=make_outcome(),
        )


def test_require_priority_constraint() -> None:
    with pytest.raises(EducationalInvariantViolation, match="priority"):
        IntentionValidationPolicy.assert_constraints_satisfied(
            [
                make_constraint(
                    kind=IntentionConstraintKind.REQUIRE_PRIORITY_REFERENCE,
                )
            ],
            intention_type=TeachingIntentionType.STRENGTHEN_PREREQUISITE,
            strength=make_strength(),
            priority_references=[],
            diagnosis_references=[make_diagnosis_ref()],
            hypothesis_references=[],
            expected_outcome=make_outcome(),
        )


def test_goal_matches_type_policy() -> None:
    goal = make_goal(intention_type=TeachingIntentionType.BUILD_INTUITION)
    IntentionValidationPolicy.assert_goal_matches_type(
        goal, TeachingIntentionType.BUILD_INTUITION
    )
    with pytest.raises(EducationalInvariantViolation, match="match"):
        IntentionValidationPolicy.assert_goal_matches_type(
            goal, TeachingIntentionType.IMPROVE_RETENTION
        )


def test_type_change_allowed_only_in_draft() -> None:
    IntentionValidationPolicy.assert_type_change_allowed(
        IntentionStatus.DRAFT,
        TeachingIntentionType.BUILD_INTUITION,
        TeachingIntentionType.CONSOLIDATE_UNDERSTANDING,
    )
    with pytest.raises(EducationalInvariantViolation, match="after activation"):
        IntentionValidationPolicy.assert_type_change_allowed(
            IntentionStatus.ACTIVE,
            TeachingIntentionType.BUILD_INTUITION,
            TeachingIntentionType.CONSOLIDATE_UNDERSTANDING,
        )


def test_cap_strength_policy() -> None:
    IntentionValidationPolicy.assert_constraints_satisfied(
        [
            make_constraint(
                kind=IntentionConstraintKind.CAP_STRENGTH,
                max_strength=IntentionStrengthLevel.FIRM,
            )
        ],
        intention_type=TeachingIntentionType.STRENGTHEN_PREREQUISITE,
        strength=make_strength(IntentionStrengthLevel.MODERATE),
        priority_references=[make_priority_ref()],
        diagnosis_references=[make_diagnosis_ref()],
        hypothesis_references=[],
        expected_outcome=make_outcome(),
    )
    with pytest.raises(EducationalInvariantViolation, match="cap"):
        IntentionValidationPolicy.assert_constraints_satisfied(
            [
                make_constraint(
                    kind=IntentionConstraintKind.CAP_STRENGTH,
                    max_strength=IntentionStrengthLevel.MODERATE,
                )
            ],
            intention_type=TeachingIntentionType.STRENGTHEN_PREREQUISITE,
            strength=make_strength(IntentionStrengthLevel.COMMITTED),
            priority_references=[make_priority_ref()],
            diagnosis_references=[make_diagnosis_ref()],
            hypothesis_references=[],
            expected_outcome=make_outcome(),
        )


def test_is_aligned_helper() -> None:
    intention = make_intention()
    assert IntentionAlignmentPolicy.is_aligned(
        intention.intention_type,
        intention.priority_references,
        intention.diagnosis_references,
    )
    assert not IntentionAlignmentPolicy.is_aligned(
        TeachingIntentionType.REPAIR_MISCONCEPTION,
        intention.priority_references,
        intention.diagnosis_references,
    )
