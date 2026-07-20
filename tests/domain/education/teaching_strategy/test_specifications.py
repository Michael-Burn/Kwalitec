"""Specification tests for Teaching Strategy."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import TeachingStrategyType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.teaching_strategy import (
    StrategyIsApplicableSpecification,
    StrategyIsComposableSpecification,
)
from tests.domain.education.teaching_strategy.conftest import make_strategy


def test_applicable_requires_selection() -> None:
    strategy = make_strategy()
    spec = StrategyIsApplicableSpecification()
    assert not spec.is_satisfied_by(strategy)
    strategy.select()
    assert spec.is_satisfied_by(strategy)
    spec.assert_satisfied_by(strategy)


def test_applicable_assert_raises_when_draft() -> None:
    strategy = make_strategy()
    with pytest.raises(EducationalInvariantViolation, match="applicable"):
        StrategyIsApplicableSpecification().assert_satisfied_by(strategy)


def test_composable_vacuous_without_secondaries() -> None:
    strategy = make_strategy(select=True)
    assert StrategyIsComposableSpecification().is_satisfied_by(strategy)


def test_composable_with_lawful_secondaries() -> None:
    strategy = make_strategy(
        primary_strategy=TeachingStrategyType.WORKED_EXAMPLE,
        select=True,
    )
    strategy.compose(
        (
            TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
            TeachingStrategyType.FADED_GUIDANCE,
        )
    )
    assert StrategyIsComposableSpecification().is_satisfied_by(strategy)


def test_composable_rejects_incompatible_proposal() -> None:
    from domain.education.teaching_strategy import SecondaryStrategyReference

    strategy = make_strategy(
        primary_strategy=TeachingStrategyType.MISCONCEPTION_CONFRONTATION,
        intention_type=__import__(
            "domain.education.foundation.enums", fromlist=["TeachingIntentionType"]
        ).TeachingIntentionType.REPAIR_MISCONCEPTION,
        select=True,
    )
    proposed = [
        SecondaryStrategyReference(
            strategy_type=TeachingStrategyType.EXAM_SIMULATION,
            sequence_order=1,
        )
    ]
    spec = StrategyIsComposableSpecification()
    assert not spec.is_satisfied_by(strategy, proposed_secondaries=proposed)
    with pytest.raises(EducationalInvariantViolation, match="composition"):
        spec.assert_satisfied_by(strategy, proposed_secondaries=proposed)
