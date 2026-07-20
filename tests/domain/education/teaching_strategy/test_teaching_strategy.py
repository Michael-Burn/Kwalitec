"""Aggregate behaviour tests for TeachingStrategy."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import (
    TeachingIntentionType,
    TeachingStrategyType,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import TeachingStrategyId
from domain.education.teaching_strategy import (
    CompositionPattern,
    EffectivenessLevel,
    StrategyRevisionKind,
    StrategyStatus,
)
from tests.domain.education.teaching_strategy.conftest import (
    make_effectiveness,
    make_goal,
    make_rationale,
    make_strategy,
)


def test_create_starts_draft() -> None:
    strategy = make_strategy()
    assert strategy.is_draft()
    assert strategy.status is StrategyStatus.DRAFT
    assert strategy.pull_events() == []


def test_select_commits_strategy() -> None:
    strategy = make_strategy()
    strategy.select()
    assert strategy.is_selected()
    assert strategy.is_committed()


def test_select_twice_rejected() -> None:
    strategy = make_strategy(select=True)
    with pytest.raises(EducationalInvariantViolation, match="already selected"):
        strategy.select()


def test_revise_rationale_on_selected() -> None:
    strategy = make_strategy(select=True)
    strategy.pull_events()
    strategy.revise(
        rationale=make_rationale(
            statement="Evidence warrants continuing this instructional approach"
        )
    )
    assert strategy.is_revised()
    events = strategy.pull_events()
    assert events[0].revision_kind is StrategyRevisionKind.RATIONALE_AMENDED


def test_revise_effectiveness() -> None:
    strategy = make_strategy(select=True)
    strategy.revise(
        effectiveness=make_effectiveness(
            EffectivenessLevel.HIGH, rationale="strong early evidence"
        )
    )
    assert strategy.effectiveness.level is EffectivenessLevel.HIGH


def test_compose_and_decompose() -> None:
    strategy = make_strategy(
        primary_strategy=TeachingStrategyType.WORKED_EXAMPLE,
        intention_type=TeachingIntentionType.INCREASE_PROCEDURAL_FLUENCY,
        select=True,
    )
    strategy.compose(
        (
            TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
            TeachingStrategyType.FADED_GUIDANCE,
        )
    )
    assert strategy.secondary_count() == 2
    assert strategy.composition_pattern is CompositionPattern.MODELLING_TO_INDEPENDENCE
    assert strategy.has_secondary(TeachingStrategyType.FADED_GUIDANCE)
    strategy.decompose(remove_strategy=TeachingStrategyType.FADED_GUIDANCE)
    assert strategy.secondary_count() == 1
    strategy.decompose()
    assert strategy.secondary_count() == 0
    assert strategy.composition_pattern is None


def test_decompose_empty_rejected() -> None:
    strategy = make_strategy(select=True)
    with pytest.raises(EducationalInvariantViolation, match="no secondary"):
        strategy.decompose()


def test_identity_equality() -> None:
    a = make_strategy(strategy_id="ts-same")
    b = make_strategy(strategy_id="ts-same", student_id="student-other")
    assert a == b
    assert hash(a) == hash(b)
    assert a != make_strategy(strategy_id="ts-other")


def test_query_helpers() -> None:
    strategy = make_strategy(select=True)
    assert strategy.intention_count() == 1
    assert strategy.diagnosis_count() == 1
    assert strategy.hypothesis_count() == 1
    assert strategy.constraint_count() == 0
    assert strategy.has_intention(strategy.intention_references[0].intention_id)
    assert strategy.has_diagnosis(strategy.diagnosis_references[0].diagnosis_id)
    assert strategy.has_hypothesis(strategy.hypothesis_references[0].hypothesis_id)


def test_draft_primary_may_change() -> None:
    strategy = make_strategy(intention_type=TeachingIntentionType.BUILD_INTUITION)
    next_type = TeachingStrategyType.DIRECT_EXPLANATION
    strategy.revise(
        primary_strategy=next_type,
        goal=make_goal(goal_id="goal-2", strategy_type=next_type),
    )
    assert strategy.primary_strategy is next_type
    assert strategy.is_draft()


def test_repr_contains_identity() -> None:
    strategy = make_strategy(strategy_id=TeachingStrategyId("ts-repr"))
    text = repr(strategy)
    assert "ts-repr" in text
    assert "TeachingStrategy" in text
