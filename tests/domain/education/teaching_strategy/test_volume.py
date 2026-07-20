"""High-volume matrices exercising Teaching Strategy domain surface area."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import (
    DiagnosisType,
    TeachingIntentionType,
    TeachingStrategyType,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.teaching_strategy import (
    ComplexityLevel,
    CompositionPattern,
    EffectivenessLevel,
    StrategyCompositionPolicy,
    StrategyConstraintKind,
    StrategyIsApplicableSpecification,
    StrategyIsComposableSpecification,
    StrategyRevisionKind,
    StrategySelectionPolicy,
    StrategyStatus,
    StrategyValidationPolicy,
)
from tests.domain.education.teaching_strategy.conftest import (
    CANONICAL_PRIMARY,
    CANONICAL_SECONDARIES,
    INTENTION_DIAGNOSIS,
    INTENTION_STRATEGY,
    make_complexity,
    make_constraint,
    make_diagnosis_ref,
    make_effectiveness,
    make_goal,
    make_intention_ref,
    make_rationale,
    make_strategy,
)

STRATEGY_TYPES = list(TeachingStrategyType)
INTENTION_TYPES = list(TeachingIntentionType)
DIAGNOSIS_TYPES = list(DiagnosisType)
EFFECTIVENESS_LEVELS = list(EffectivenessLevel)
COMPLEXITY_LEVELS = list(ComplexityLevel)
STUDENTS = tuple(f"student-{i}" for i in range(1, 9))
ACTIONS = ("select", "revise_rationale", "compose", "decompose", "retire")
CONSTRAINT_KINDS = [
    StrategyConstraintKind.REQUIRE_INTENTION_REFERENCE,
    StrategyConstraintKind.REQUIRE_DIAGNOSIS_REFERENCE,
    StrategyConstraintKind.REQUIRE_RATIONALE,
    StrategyConstraintKind.REQUIRE_EFFECTIVENESS,
    StrategyConstraintKind.FORBID_MASTERY_CLAIM,
    StrategyConstraintKind.PROTECT_ATOMICITY,
    StrategyConstraintKind.FORBID_COEQUAL_PRIMARIES,
]
COMPOSITION_PATTERNS = [
    p for p in CompositionPattern if p is not CompositionPattern.CUSTOM
]


@pytest.mark.parametrize("strategy_type", STRATEGY_TYPES)
@pytest.mark.parametrize("student", STUDENTS)
def test_create_per_catalogue_strategy_and_student(
    strategy_type: TeachingStrategyType, student: str
) -> None:
    # Pick a lawful intention for this strategy from affinity tables.
    intention_type = next(
        (
            intention
            for intention in INTENTION_TYPES
            if StrategySelectionPolicy.is_preferred_for_intention(
                strategy_type, intention
            )
        ),
        TeachingIntentionType.CONSOLIDATE_UNDERSTANDING,
    )
    if not StrategySelectionPolicy.is_lawful_for_intention(
        strategy_type, intention_type
    ):
        intention_type = next(
            intention
            for intention in INTENTION_TYPES
            if StrategySelectionPolicy.is_lawful_for_intention(
                strategy_type, intention
            )
        )
    strategy = make_strategy(
        strategy_id=f"ts-{strategy_type.value}-{student}",
        student_id=student,
        primary_strategy=strategy_type,
        intention_type=intention_type,
    )
    assert strategy.student_id == student
    assert strategy.primary_strategy is strategy_type
    assert strategy.is_draft()


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
@pytest.mark.parametrize("student", STUDENTS)
def test_select_preferred_per_intention(
    intention_type: TeachingIntentionType, student: str
) -> None:
    strategy = make_strategy(
        strategy_id=f"ts-pref-{intention_type.value}-{student}",
        student_id=student,
        intention_type=intention_type,
        select=True,
    )
    assert strategy.primary_strategy is INTENTION_STRATEGY[intention_type]
    assert StrategyIsApplicableSpecification().is_satisfied_by(strategy)


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
@pytest.mark.parametrize("strategy_type", STRATEGY_TYPES)
def test_affinity_and_lawfulness_matrix(
    intention_type: TeachingIntentionType, strategy_type: TeachingStrategyType
) -> None:
    preferred = StrategySelectionPolicy.is_preferred_for_intention(
        strategy_type, intention_type
    )
    lawful = StrategySelectionPolicy.is_lawful_for_intention(
        strategy_type, intention_type
    )
    expected_preferred = (
        strategy_type
        in StrategySelectionPolicy.preferred_for_intention(intention_type)
    )
    assert preferred is expected_preferred
    if preferred:
        assert lawful
    if StrategySelectionPolicy.is_forbidden_primary(strategy_type, intention_type):
        assert not lawful


@pytest.mark.parametrize("diagnosis_type", DIAGNOSIS_TYPES)
@pytest.mark.parametrize("strategy_type", STRATEGY_TYPES)
def test_diagnosis_family_membership_matrix(
    diagnosis_type: DiagnosisType, strategy_type: TeachingStrategyType
) -> None:
    family = StrategySelectionPolicy.preferred_for_diagnosis(diagnosis_type)
    assert (strategy_type in family) is (
        strategy_type
        in StrategySelectionPolicy.preferred_for_diagnosis(diagnosis_type)
    )


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
@pytest.mark.parametrize("level", EFFECTIVENESS_LEVELS)
def test_effectiveness_matrix_per_intention(
    intention_type: TeachingIntentionType, level: EffectivenessLevel
) -> None:
    strategy = make_strategy(
        strategy_id=f"ts-eff-{intention_type.value}-{level.value}",
        intention_type=intention_type,
        effectiveness=make_effectiveness(level),
        select=True,
    )
    assert strategy.effectiveness.level is level
    StrategyIsApplicableSpecification().assert_satisfied_by(strategy)


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
@pytest.mark.parametrize("level", COMPLEXITY_LEVELS)
def test_complexity_matrix_per_intention(
    intention_type: TeachingIntentionType, level: ComplexityLevel
) -> None:
    strategy = make_strategy(
        strategy_id=f"ts-cpx-{intention_type.value}-{level.value}",
        intention_type=intention_type,
        complexity=make_complexity(level),
        select=True,
    )
    assert strategy.complexity.level is level


@pytest.mark.parametrize("pattern", COMPOSITION_PATTERNS)
@pytest.mark.parametrize("student", STUDENTS[:5])
def test_canonical_composition_matrix(
    pattern: CompositionPattern, student: str
) -> None:
    primary = CANONICAL_PRIMARY[pattern]
    secondaries = CANONICAL_SECONDARIES[pattern]
    intention_type = next(
        intention
        for intention in INTENTION_TYPES
        if StrategySelectionPolicy.is_lawful_for_intention(primary, intention)
        and not (
            primary
            in {
                TeachingStrategyType.MISCONCEPTION_CONFRONTATION,
                TeachingStrategyType.COUNTEREXAMPLE,
                TeachingStrategyType.ERROR_LED_TEACHING,
            }
            and intention is not TeachingIntentionType.REPAIR_MISCONCEPTION
            and INTENTION_DIAGNOSIS[intention] is DiagnosisType.MISCONCEPTION
        )
    )
    # Prefer matching diagnosis for misconception confrontation primaries.
    if primary is TeachingStrategyType.MISCONCEPTION_CONFRONTATION:
        intention_type = TeachingIntentionType.REPAIR_MISCONCEPTION
    elif primary is TeachingStrategyType.RETRIEVAL_FIRST:
        intention_type = TeachingIntentionType.IMPROVE_RETENTION
    elif primary is TeachingStrategyType.ANALOGY:
        intention_type = TeachingIntentionType.BUILD_INTUITION
    elif primary is TeachingStrategyType.WORKED_EXAMPLE:
        intention_type = TeachingIntentionType.INCREASE_PROCEDURAL_FLUENCY
    elif primary is TeachingStrategyType.CONCEPT_COMPARISON:
        intention_type = TeachingIntentionType.CONNECT_FRAGMENTED_KNOWLEDGE
    elif primary is TeachingStrategyType.GUIDED_DISCOVERY:
        intention_type = TeachingIntentionType.COMPLETE_MISSING_FACETS

    strategy = make_strategy(
        strategy_id=f"ts-comp-{pattern.value}-{student}",
        student_id=student,
        primary_strategy=primary,
        intention_type=intention_type,
        select=True,
    )
    strategy.compose(secondaries, composition_pattern=pattern)
    assert strategy.secondary_count() == len(secondaries)
    assert StrategyIsComposableSpecification().is_satisfied_by(strategy)
    assert strategy.composition_sequence() == (primary, *secondaries)


@pytest.mark.parametrize("action", ACTIONS)
@pytest.mark.parametrize("student", STUDENTS[:5])
def test_lifecycle_action_matrix(action: str, student: str) -> None:
    strategy = make_strategy(
        strategy_id=f"ts-life-{action}-{student}",
        student_id=student,
        primary_strategy=TeachingStrategyType.WORKED_EXAMPLE,
        intention_type=TeachingIntentionType.INCREASE_PROCEDURAL_FLUENCY,
    )
    strategy.pull_events()
    if action == "select":
        strategy.select()
        assert strategy.is_selected()
    elif action == "revise_rationale":
        strategy.select()
        strategy.pull_events()
        strategy.revise(
            rationale=make_rationale(
                statement=f"Revised rationale for {student} after evidence"
            )
        )
        assert strategy.is_revised()
        events = strategy.pull_events()
        assert events[0].revision_kind is StrategyRevisionKind.RATIONALE_AMENDED
    elif action == "compose":
        strategy.select()
        strategy.compose(
            (
                TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
                TeachingStrategyType.FADED_GUIDANCE,
            )
        )
        assert strategy.secondary_count() == 2
    elif action == "decompose":
        strategy.select()
        strategy.compose((TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,))
        strategy.decompose()
        assert strategy.secondary_count() == 0
    elif action == "retire":
        strategy.select()
        strategy.retire(reason=f"retire-{student}")
        assert strategy.is_retired()
        assert strategy.status is StrategyStatus.RETIRED


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
@pytest.mark.parametrize("kind", CONSTRAINT_KINDS)
def test_protective_constraints_attach(
    intention_type: TeachingIntentionType, kind: StrategyConstraintKind
) -> None:
    strategy = make_strategy(
        strategy_id=f"ts-{intention_type.value}-{kind.value}",
        intention_type=intention_type,
        constraints=[
            make_constraint(
                constraint_id=f"c-{intention_type.value}-{kind.value}",
                kind=kind,
            )
        ],
        select=True,
    )
    assert strategy.constraint_count() == 1
    assert StrategyIsApplicableSpecification().is_satisfied_by(strategy)


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
def test_select_then_cannot_change_primary(
    intention_type: TeachingIntentionType,
) -> None:
    strategy = make_strategy(
        strategy_id=f"ts-lock-{intention_type.value}",
        intention_type=intention_type,
        select=True,
    )
    other = next(
        s
        for s in StrategySelectionPolicy.preferred_for_intention(intention_type)
        if s is not strategy.primary_strategy
    )
    with pytest.raises(EducationalInvariantViolation, match="after selection"):
        strategy.revise(
            primary_strategy=other,
            goal=make_goal(strategy_type=other),
        )


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
def test_draft_primary_switch_within_lawful_set(
    intention_type: TeachingIntentionType,
) -> None:
    preferred = list(StrategySelectionPolicy.preferred_for_intention(intention_type))
    if len(preferred) < 2:
        return
    first, second = preferred[0], preferred[1]
    strategy = make_strategy(
        strategy_id=f"ts-switch-{intention_type.value}",
        intention_type=intention_type,
        primary_strategy=first,
    )
    strategy.revise(
        primary_strategy=second,
        goal=make_goal(
            goal_id=f"goal-{second.value}",
            strategy_type=second,
        ),
    )
    assert strategy.primary_strategy is second
    assert strategy.is_draft()


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
@pytest.mark.parametrize("student", STUDENTS[:4])
def test_retired_cannot_revise_matrix(
    intention_type: TeachingIntentionType, student: str
) -> None:
    strategy = make_strategy(
        strategy_id=f"ts-ret-{intention_type.value}-{student}",
        student_id=student,
        intention_type=intention_type,
        select=True,
    )
    strategy.retire(reason="done")
    with pytest.raises(EducationalInvariantViolation, match="retired"):
        strategy.revise(
            rationale=make_rationale(
                statement="Illegal post-retirement rationale amendment"
            )
        )


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
def test_must_reference_intention_matrix(
    intention_type: TeachingIntentionType,
) -> None:
    with pytest.raises(EducationalInvariantViolation, match="Intention"):
        make_strategy(
            strategy_id=f"ts-noint-{intention_type.value}",
            intention_type=intention_type,
            intention_references=[],
        )


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
def test_forbidden_primary_rejected_matrix(
    intention_type: TeachingIntentionType,
) -> None:
    forbidden = [
        s
        for s in STRATEGY_TYPES
        if StrategySelectionPolicy.is_forbidden_primary(s, intention_type)
    ]
    if not forbidden:
        return
    with pytest.raises(EducationalInvariantViolation, match="contradicts"):
        make_strategy(
            strategy_id=f"ts-forbid-{intention_type.value}",
            intention_type=intention_type,
            primary_strategy=forbidden[0],
            intention_references=[
                make_intention_ref(intention_type=intention_type)
            ],
            diagnosis_references=[
                make_diagnosis_ref(
                    diagnosis_type=INTENTION_DIAGNOSIS[intention_type]
                )
            ],
        )


@pytest.mark.parametrize("pattern", COMPOSITION_PATTERNS)
def test_canonical_arc_prefix_detection(pattern: CompositionPattern) -> None:
    arc = StrategyCompositionPolicy.canonical_arc(pattern)
    primary, *rest = arc
    matched = StrategyCompositionPolicy.matches_canonical_prefix(primary, rest)
    assert matched is pattern


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
@pytest.mark.parametrize("eff", EFFECTIVENESS_LEVELS[:2])
@pytest.mark.parametrize("cpx", COMPLEXITY_LEVELS[:2])
def test_combined_create_select_matrix(
    intention_type: TeachingIntentionType,
    eff: EffectivenessLevel,
    cpx: ComplexityLevel,
) -> None:
    strategy = make_strategy(
        strategy_id=f"ts-c-{intention_type.value}-{eff.value}-{cpx.value}",
        intention_type=intention_type,
        effectiveness=make_effectiveness(eff),
        complexity=make_complexity(cpx),
        select=True,
    )
    assert strategy.is_committed()
    StrategyIsApplicableSpecification().assert_satisfied_by(strategy)
    StrategyValidationPolicy.assert_status(strategy.status)


@pytest.mark.parametrize("strategy_type", STRATEGY_TYPES)
def test_follow_ons_are_catalogue_members(
    strategy_type: TeachingStrategyType,
) -> None:
    follow_ons = StrategyCompositionPolicy.compatible_follow_ons(strategy_type)
    for follow in follow_ons:
        assert follow in StrategySelectionPolicy.catalogue()
        assert follow is not strategy_type
