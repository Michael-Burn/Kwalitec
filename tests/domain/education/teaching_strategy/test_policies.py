"""Policy tests for Teaching Strategy selection, validation, and composition."""

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
    StrategyCompositionPolicy,
    StrategyConstraintKind,
    StrategySelectionPolicy,
    StrategyValidationPolicy,
)
from tests.domain.education.teaching_strategy.conftest import (
    CANONICAL_PRIMARY,
    CANONICAL_SECONDARIES,
    make_constraint,
    make_diagnosis_ref,
    make_intention_ref,
    make_strategy,
)


@pytest.mark.parametrize("strategy_type", list(TeachingStrategyType))
def test_catalogue_contains_only_documented_strategies(
    strategy_type: TeachingStrategyType,
) -> None:
    assert StrategySelectionPolicy.is_catalogue_strategy(strategy_type)


@pytest.mark.parametrize("intention_type", list(TeachingIntentionType))
def test_preferred_affinity_non_empty(
    intention_type: TeachingIntentionType,
) -> None:
    preferred = StrategySelectionPolicy.preferred_for_intention(intention_type)
    assert len(preferred) >= 1
    for strategy_type in preferred:
        assert StrategySelectionPolicy.is_lawful_for_intention(
            strategy_type, intention_type
        )


@pytest.mark.parametrize("diagnosis_type", list(DiagnosisType))
def test_diagnosis_family_non_empty(diagnosis_type: DiagnosisType) -> None:
    family = StrategySelectionPolicy.preferred_for_diagnosis(diagnosis_type)
    assert len(family) >= 1


def test_forbidden_exam_for_repair_misconception() -> None:
    assert StrategySelectionPolicy.is_forbidden_primary(
        TeachingStrategyType.EXAM_SIMULATION,
        TeachingIntentionType.REPAIR_MISCONCEPTION,
    )
    with pytest.raises(EducationalInvariantViolation, match="contradicts"):
        StrategySelectionPolicy.assert_serves_intention(
            TeachingStrategyType.EXAM_SIMULATION,
            [
                make_intention_ref(
                    intention_type=TeachingIntentionType.REPAIR_MISCONCEPTION
                )
            ],
        )


def test_misconception_duty() -> None:
    with pytest.raises(EducationalInvariantViolation, match="misconception"):
        StrategySelectionPolicy.assert_misconception_duty(
            TeachingStrategyType.DELIBERATE_PRACTICE,
            [
                make_intention_ref(
                    intention_type=TeachingIntentionType.REPAIR_MISCONCEPTION
                )
            ],
            [make_diagnosis_ref(diagnosis_type=DiagnosisType.MISCONCEPTION)],
        )


def test_exam_over_misconception_forbidden() -> None:
    with pytest.raises(EducationalInvariantViolation, match="exam simulation"):
        StrategySelectionPolicy.assert_not_exam_over_misconception(
            TeachingStrategyType.EXAM_SIMULATION,
            [make_diagnosis_ref(diagnosis_type=DiagnosisType.MISCONCEPTION)],
        )


@pytest.mark.parametrize(
    "pattern",
    [
        p
        for p in CompositionPattern
        if p is not CompositionPattern.CUSTOM
    ],
)
def test_canonical_arcs(pattern: CompositionPattern) -> None:
    arc = StrategyCompositionPolicy.canonical_arc(pattern)
    assert len(arc) >= 2
    assert arc[0] is CANONICAL_PRIMARY[pattern]
    secondaries = CANONICAL_SECONDARIES[pattern]
    assert arc[1:] == secondaries


def test_canonical_custom_rejected() -> None:
    with pytest.raises(EducationalInvariantViolation, match="CUSTOM"):
        StrategyCompositionPolicy.canonical_arc(CompositionPattern.CUSTOM)


def test_composition_rejects_duplicates() -> None:
    with pytest.raises(EducationalInvariantViolation, match="duplicate"):
        StrategyCompositionPolicy.assert_compose_types(
            TeachingStrategyType.WORKED_EXAMPLE,
            (
                TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
                TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
            ),
        )


def test_composition_rejects_incompatible_pair() -> None:
    with pytest.raises(EducationalInvariantViolation, match="incompatible"):
        StrategyCompositionPolicy.assert_compose_types(
            TeachingStrategyType.MISCONCEPTION_CONFRONTATION,
            (TeachingStrategyType.EXAM_SIMULATION,),
        )


def test_composition_accepts_modelling_arc() -> None:
    refs = StrategyCompositionPolicy.assert_compose_types(
        TeachingStrategyType.WORKED_EXAMPLE,
        (
            TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
            TeachingStrategyType.FADED_GUIDANCE,
        ),
    )
    assert len(refs) == 2
    assert StrategyCompositionPolicy.matches_canonical_prefix(
        TeachingStrategyType.WORKED_EXAMPLE,
        [r.strategy_type for r in refs],
    ) is CompositionPattern.MODELLING_TO_INDEPENDENCE


def test_validation_requires_intention() -> None:
    with pytest.raises(EducationalInvariantViolation, match="Intention"):
        make_strategy(intention_references=[])


def test_validation_requires_diagnosis() -> None:
    with pytest.raises(EducationalInvariantViolation, match="diagnosis"):
        make_strategy(diagnosis_references=[])


def test_constraint_cap_complexity() -> None:
    from tests.domain.education.teaching_strategy.conftest import make_complexity

    with pytest.raises(EducationalInvariantViolation, match="complexity"):
        make_strategy(
            complexity=make_complexity(ComplexityLevel.VERY_HIGH),
            constraints=[
                make_constraint(
                    kind=StrategyConstraintKind.CAP_COMPLEXITY,
                    max_complexity=ComplexityLevel.MODERATE,
                )
            ],
        )


def test_require_affinity_constraint() -> None:
    # Worked example is lawful but not preferred for improve retention.
    with pytest.raises(EducationalInvariantViolation, match="affinity"):
        make_strategy(
            intention_type=TeachingIntentionType.IMPROVE_RETENTION,
            primary_strategy=TeachingStrategyType.WORKED_EXAMPLE,
            diagnosis_references=[
                make_diagnosis_ref(diagnosis_type=DiagnosisType.WEAK_RETENTION)
            ],
            constraints=[
                make_constraint(
                    kind=StrategyConstraintKind.REQUIRE_INTENTION_AFFINITY
                )
            ],
        )


def test_identity_and_status_helpers() -> None:
    from domain.education.foundation.ids import TeachingStrategyId
    from domain.education.teaching_strategy import StrategyStatus

    sid = TeachingStrategyId("ts-x")
    assert StrategyValidationPolicy.assert_identity(sid) is sid
    assert (
        StrategyValidationPolicy.assert_status(StrategyStatus.DRAFT)
        is StrategyStatus.DRAFT
    )
