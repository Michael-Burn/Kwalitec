"""Invariant enforcement tests for Teaching Strategy."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import (
    TeachingIntentionType,
    TeachingStrategyType,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.teaching_strategy import (
    StrategyConstraintKind,
    StrategyStatus,
)
from tests.domain.education.teaching_strategy.conftest import (
    INTENTION_STRATEGY,
    make_constraint,
    make_goal,
    make_rationale,
    make_strategy,
)


def test_must_reference_teaching_intention() -> None:
    with pytest.raises(EducationalInvariantViolation, match="Intention"):
        make_strategy(intention_references=[])


def test_must_identify_one_primary_strategy() -> None:
    strategy = make_strategy()
    assert isinstance(strategy.primary_strategy, TeachingStrategyType)


def test_must_include_rationale() -> None:
    from domain.education.foundation.ids import TeachingStrategyId
    from domain.education.teaching_strategy import TeachingStrategy
    from tests.domain.education.teaching_strategy.conftest import (
        make_complexity,
        make_diagnosis_ref,
        make_effectiveness,
        make_goal,
        make_intention_ref,
    )

    with pytest.raises(EducationalInvariantViolation, match="rationale"):
        TeachingStrategy.create(
            strategy_id=TeachingStrategyId("ts-no-rationale"),
            student_id="student-ada",
            primary_strategy=TeachingStrategyType.WORKED_EXAMPLE,
            goal=make_goal(),
            rationale="not-a-rationale",  # type: ignore[arg-type]
            effectiveness=make_effectiveness(),
            complexity=make_complexity(),
            intention_references=[make_intention_ref()],
            diagnosis_references=[make_diagnosis_ref()],
        )


def test_must_possess_effectiveness() -> None:
    strategy = make_strategy()
    assert strategy.effectiveness is not None


def test_cannot_contradict_teaching_intention() -> None:
    with pytest.raises(EducationalInvariantViolation, match="contradicts"):
        make_strategy(
            intention_type=TeachingIntentionType.REPAIR_MISCONCEPTION,
            primary_strategy=TeachingStrategyType.SPACED_REINFORCEMENT,
        )


def test_cannot_duplicate_composed_strategies() -> None:
    strategy = make_strategy(
        primary_strategy=TeachingStrategyType.WORKED_EXAMPLE,
        select=True,
    )
    with pytest.raises(EducationalInvariantViolation, match="duplicate"):
        strategy.compose(
            (
                TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
                TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
            )
        )


def test_cannot_revise_after_retirement() -> None:
    strategy = make_strategy(select=True)
    strategy.retire(reason="done")
    with pytest.raises(EducationalInvariantViolation, match="retired"):
        strategy.revise(rationale=make_rationale(statement="New rationale text here"))


def test_cannot_compose_after_retirement() -> None:
    strategy = make_strategy(
        primary_strategy=TeachingStrategyType.WORKED_EXAMPLE,
        select=True,
    )
    strategy.retire(reason="done")
    with pytest.raises(EducationalInvariantViolation, match="retired"):
        strategy.compose((TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,))


def test_cannot_change_primary_after_selection() -> None:
    strategy = make_strategy(
        intention_type=TeachingIntentionType.BUILD_INTUITION,
        select=True,
    )
    other = TeachingStrategyType.DIRECT_EXPLANATION
    with pytest.raises(EducationalInvariantViolation, match="after selection"):
        strategy.revise(
            primary_strategy=other,
            goal=make_goal(strategy_type=other),
        )


def test_one_primary_enforced() -> None:
    strategy = make_strategy(select=True)
    assert strategy.secondary_count() == 0
    assert len(strategy.composition_sequence()) == 1


def test_duplicate_constraints_rejected() -> None:
    kind = StrategyConstraintKind.PROTECT_ATOMICITY
    with pytest.raises(EducationalInvariantViolation, match="duplicate"):
        make_strategy(
            constraints=[
                make_constraint(constraint_id="a", kind=kind),
                make_constraint(constraint_id="b", kind=kind),
            ]
        )


def test_goal_must_match_primary() -> None:
    with pytest.raises(EducationalInvariantViolation, match="match"):
        make_strategy(
            primary_strategy=TeachingStrategyType.ANALOGY,
            intention_type=TeachingIntentionType.BUILD_INTUITION,
            goal=make_goal(strategy_type=TeachingStrategyType.WORKED_EXAMPLE),
        )


@pytest.mark.parametrize("intention_type", list(TeachingIntentionType))
def test_default_mapping_is_lawful(
    intention_type: TeachingIntentionType,
) -> None:
    strategy = make_strategy(intention_type=intention_type, select=True)
    assert strategy.primary_strategy is INTENTION_STRATEGY[intention_type]
    assert strategy.status is StrategyStatus.SELECTED


def test_retire_is_terminal() -> None:
    strategy = make_strategy(select=True)
    strategy.retire(reason="superseded")
    assert strategy.is_retired()
    assert strategy.retire_reason == "superseded"
    with pytest.raises(EducationalInvariantViolation, match="already retired"):
        strategy.retire(reason="again")
