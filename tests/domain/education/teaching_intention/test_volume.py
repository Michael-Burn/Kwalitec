"""High-volume matrices exercising Teaching Intention domain surface area."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import (
    DiagnosisType,
    LearningDimension,
    TeachingIntentionType,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.teaching_intention import (
    IntentionAlignmentPolicy,
    IntentionConstraintKind,
    IntentionIsActionableSpecification,
    IntentionIsAlignedSpecification,
    IntentionRevisionKind,
    IntentionScopeKind,
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
    make_scope,
    make_strength,
)

INTENTION_TYPES = list(TeachingIntentionType)
DIAGNOSIS_TYPES = list(DiagnosisType)
STRENGTH_LEVELS = list(IntentionStrengthLevel)
SCOPE_KINDS = list(IntentionScopeKind)
DIMENSIONS = list(LearningDimension)
CONSTRAINT_KINDS = [
    IntentionConstraintKind.REQUIRE_PRIORITY_REFERENCE,
    IntentionConstraintKind.REQUIRE_DIAGNOSIS_ALIGNMENT,
    IntentionConstraintKind.FORBID_MASTERY_CLAIM,
    IntentionConstraintKind.FORBID_STRATEGY_SELECTION,
    IntentionConstraintKind.REQUIRE_EVALUABLE_OUTCOME,
    IntentionConstraintKind.PROTECT_ATOMICITY,
]
STUDENTS = tuple(f"student-{i}" for i in range(1, 9))
ACTIONS = ("activate", "revise_scope", "strengthen", "weaken", "retire")


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
@pytest.mark.parametrize("student", STUDENTS)
def test_create_per_catalogue_type_and_student(
    intention_type: TeachingIntentionType, student: str
) -> None:
    intention = make_intention(
        intention_id=f"ti-{intention_type.value}-{student}",
        student_id=student,
        intention_type=intention_type,
    )
    assert intention.student_id == student
    assert intention.intention_type is intention_type
    assert intention.is_draft()
    assert IntentionIsAlignedSpecification().is_satisfied_by(intention)


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
@pytest.mark.parametrize("level", STRENGTH_LEVELS)
def test_strength_matrix_per_type(
    intention_type: TeachingIntentionType, level: IntentionStrengthLevel
) -> None:
    intention = make_intention(
        intention_id=f"ti-{intention_type.value}-{level.value}",
        intention_type=intention_type,
        strength=make_strength(level),
        activate=True,
    )
    assert intention.strength.level is level
    assert IntentionIsActionableSpecification().is_satisfied_by(intention)


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
@pytest.mark.parametrize("scope_kind", SCOPE_KINDS)
def test_scope_kind_matrix(
    intention_type: TeachingIntentionType, scope_kind: IntentionScopeKind
) -> None:
    intention = make_intention(
        intention_id=f"ti-{intention_type.value}-{scope_kind.value}",
        intention_type=intention_type,
        scope=make_scope(
            scope_id=f"scope-{intention_type.value}-{scope_kind.value}",
            statement=f"Scope {scope_kind.value} for {intention_type.value}",
            scope_kind=scope_kind,
        ),
    )
    assert intention.scope.scope_kind is scope_kind


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
@pytest.mark.parametrize("dimension", DIMENSIONS)
def test_dimension_matrix(
    intention_type: TeachingIntentionType, dimension: LearningDimension
) -> None:
    intention = make_intention(
        intention_id=f"ti-{intention_type.value}-{dimension.value}",
        intention_type=intention_type,
        scope=make_scope(
            scope_id=f"scope-{intention_type.value}-{dimension.value}",
            statement=f"Dimension {dimension.value}",
            dimension=dimension,
        ),
    )
    assert intention.scope.learning_dimension is dimension


@pytest.mark.parametrize("diagnosis_type", DIAGNOSIS_TYPES)
@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
def test_alignment_matrix(
    diagnosis_type: DiagnosisType, intention_type: TeachingIntentionType
) -> None:
    lawful = IntentionAlignmentPolicy.is_type_aligned_with_diagnosis(
        intention_type, diagnosis_type
    )
    expected = intention_type in IntentionAlignmentPolicy.lawful_intention_types_for(
        diagnosis_type
    )
    assert lawful is expected


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
@pytest.mark.parametrize("kind", CONSTRAINT_KINDS)
def test_protective_constraints_attach(
    intention_type: TeachingIntentionType, kind: IntentionConstraintKind
) -> None:
    intention = make_intention(
        intention_id=f"ti-{intention_type.value}-{kind.value}",
        intention_type=intention_type,
        constraints=[
            make_constraint(
                constraint_id=f"c-{intention_type.value}-{kind.value}",
                kind=kind,
            )
        ],
        activate=True,
    )
    assert intention.constraint_count() == 1
    assert IntentionIsActionableSpecification().is_satisfied_by(intention)


@pytest.mark.parametrize("action", ACTIONS)
@pytest.mark.parametrize("student", STUDENTS[:5])
def test_lifecycle_action_matrix(action: str, student: str) -> None:
    intention = make_intention(
        intention_id=f"ti-life-{action}-{student}",
        student_id=student,
        strength=make_strength(IntentionStrengthLevel.MODERATE),
    )
    intention.pull_events()
    if action == "activate":
        intention.activate()
        assert intention.is_active()
    elif action == "revise_scope":
        intention.activate()
        intention.pull_events()
        intention.revise(
            scope=make_scope(statement=f"Revised scope for {student}")
        )
        assert intention.is_revised()
        events = intention.pull_events()
        assert events[0].revision_kind is IntentionRevisionKind.SCOPE_AMENDED
    elif action == "strengthen":
        intention.activate()
        intention.strengthen()
        assert intention.strength.level is IntentionStrengthLevel.FIRM
    elif action == "weaken":
        intention.activate()
        intention.weaken()
        assert intention.strength.level is IntentionStrengthLevel.TENTATIVE
    elif action == "retire":
        intention.activate()
        intention.retire(reason=f"retire-{student}")
        assert intention.is_retired()
        assert intention.status is IntentionStatus.RETIRED


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
def test_activate_then_cannot_change_type(
    intention_type: TeachingIntentionType,
) -> None:
    intention = make_intention(
        intention_id=f"ti-lock-{intention_type.value}",
        intention_type=intention_type,
        activate=True,
    )
    other = next(t for t in INTENTION_TYPES if t is not intention_type)
    with pytest.raises(EducationalInvariantViolation, match="after activation"):
        intention.revise(
            intention_type=other,
            goal=make_goal(intention_type=other),
            diagnosis_references=[
                make_diagnosis_ref(diagnosis_type=INTENTION_DIAGNOSIS[other])
            ],
        )


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
def test_draft_type_switch_to_aligned_default(
    intention_type: TeachingIntentionType,
) -> None:
    # Start from prerequisite, switch to each catalogue type while draft.
    intention = make_intention(intention_id=f"ti-switch-{intention_type.value}")
    if intention_type is TeachingIntentionType.STRENGTHEN_PREREQUISITE:
        return
    intention.revise(
        intention_type=intention_type,
        goal=make_goal(
            goal_id=f"goal-{intention_type.value}",
            intention_type=intention_type,
        ),
        diagnosis_references=[
            make_diagnosis_ref(
                diagnosis_id=f"diag-{intention_type.value}",
                diagnosis_type=INTENTION_DIAGNOSIS[intention_type],
            )
        ],
        expected_outcome=make_outcome(
            statement=f"Outcome for {intention_type.value}",
            success_evidence=f"Evidence for {intention_type.value}",
        ),
    )
    assert intention.intention_type is intention_type
    assert intention.is_draft()


@pytest.mark.parametrize("from_level", STRENGTH_LEVELS[:-1])
@pytest.mark.parametrize("student", STUDENTS[:4])
def test_strengthen_ladder_matrix(
    from_level: IntentionStrengthLevel, student: str
) -> None:
    intention = make_intention(
        intention_id=f"ti-str-{from_level.value}-{student}",
        student_id=student,
        strength=make_strength(from_level),
        activate=True,
    )
    intention.strengthen()
    expected_index = STRENGTH_LEVELS.index(from_level) + 1
    assert intention.strength.level is STRENGTH_LEVELS[expected_index]


@pytest.mark.parametrize("from_level", STRENGTH_LEVELS[1:])
@pytest.mark.parametrize("student", STUDENTS[:4])
def test_weaken_ladder_matrix(
    from_level: IntentionStrengthLevel, student: str
) -> None:
    intention = make_intention(
        intention_id=f"ti-wk-{from_level.value}-{student}",
        student_id=student,
        strength=make_strength(from_level),
        activate=True,
    )
    intention.weaken()
    expected_index = STRENGTH_LEVELS.index(from_level) - 1
    assert intention.strength.level is STRENGTH_LEVELS[expected_index]


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
@pytest.mark.parametrize("student", STUDENTS[:4])
def test_retired_cannot_strengthen_matrix(
    intention_type: TeachingIntentionType, student: str
) -> None:
    intention = make_intention(
        intention_id=f"ti-ret-{intention_type.value}-{student}",
        student_id=student,
        intention_type=intention_type,
        activate=True,
    )
    intention.retire(reason="done")
    with pytest.raises(EducationalInvariantViolation, match="retired"):
        intention.strengthen()


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
def test_must_reference_priority_matrix(
    intention_type: TeachingIntentionType,
) -> None:
    with pytest.raises(EducationalInvariantViolation, match="Priority"):
        make_intention(
            intention_id=f"ti-noprio-{intention_type.value}",
            intention_type=intention_type,
            priority_references=[],
        )


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
def test_duplicate_constraints_matrix(
    intention_type: TeachingIntentionType,
) -> None:
    kind = IntentionConstraintKind.PROTECT_ATOMICITY
    with pytest.raises(EducationalInvariantViolation, match="duplicate"):
        make_intention(
            intention_id=f"ti-dupc-{intention_type.value}",
            intention_type=intention_type,
            constraints=[
                make_constraint(constraint_id="a", kind=kind),
                make_constraint(constraint_id="b", kind=kind),
            ],
        )


@pytest.mark.parametrize("diagnosis_type", DIAGNOSIS_TYPES)
def test_lawful_types_non_empty(diagnosis_type: DiagnosisType) -> None:
    lawful = IntentionAlignmentPolicy.lawful_intention_types_for(diagnosis_type)
    assert len(lawful) >= 1
    for intention_type in lawful:
        assert isinstance(intention_type, TeachingIntentionType)


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
@pytest.mark.parametrize("scope_kind", SCOPE_KINDS[:4])
@pytest.mark.parametrize("level", STRENGTH_LEVELS[:2])
def test_combined_create_activate_matrix(
    intention_type: TeachingIntentionType,
    scope_kind: IntentionScopeKind,
    level: IntentionStrengthLevel,
) -> None:
    intention = make_intention(
        intention_id=f"ti-c-{intention_type.value}-{scope_kind.value}-{level.value}",
        intention_type=intention_type,
        scope=make_scope(
            scope_id=f"sc-{intention_type.value}-{scope_kind.value}-{level.value}",
            statement=f"Combined {intention_type.value}",
            scope_kind=scope_kind,
        ),
        strength=make_strength(level),
        activate=True,
    )
    assert intention.is_activated()
    IntentionIsActionableSpecification().assert_satisfied_by(intention)
    IntentionValidationPolicy.assert_status(intention.status)
