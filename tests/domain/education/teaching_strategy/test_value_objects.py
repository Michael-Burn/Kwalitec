"""Value object tests for Teaching Strategy."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.teaching_strategy import (
    ComplexityLevel,
    EffectivenessLevel,
    InstructionalComplexity,
    StrategyEffectiveness,
)


@pytest.mark.parametrize("level", list(EffectivenessLevel))
def test_effectiveness_levels(level: EffectivenessLevel) -> None:
    value = StrategyEffectiveness.of(level, rationale="estimate")
    assert value.level is level
    assert "estimate" in str(value)


def test_effectiveness_rejects_blank_rationale() -> None:
    with pytest.raises(EducationalInvariantViolation, match="non-empty"):
        StrategyEffectiveness.of(EffectivenessLevel.HIGH, rationale="   ")


def test_effectiveness_rejects_mastery_claim() -> None:
    with pytest.raises(EducationalInvariantViolation, match="mastery"):
        StrategyEffectiveness.of(
            EffectivenessLevel.HIGH,
            rationale="student will be fully mastered",
        )


def test_effectiveness_factories() -> None:
    assert StrategyEffectiveness.low().level is EffectivenessLevel.LOW
    assert StrategyEffectiveness.moderate().level is EffectivenessLevel.MODERATE
    assert StrategyEffectiveness.high().level is EffectivenessLevel.HIGH
    assert StrategyEffectiveness.uncertain().level is EffectivenessLevel.UNCERTAIN


def test_effectiveness_ordering() -> None:
    high = StrategyEffectiveness.high()
    assert high.is_at_least(EffectivenessLevel.MODERATE)
    assert not StrategyEffectiveness.low().is_at_least(EffectivenessLevel.HIGH)


@pytest.mark.parametrize("level", list(ComplexityLevel))
def test_complexity_levels(level: ComplexityLevel) -> None:
    value = InstructionalComplexity.of(level, rationale="load")
    assert value.level is level


def test_complexity_rejects_blank_rationale() -> None:
    with pytest.raises(EducationalInvariantViolation, match="non-empty"):
        InstructionalComplexity.of(ComplexityLevel.HIGH, rationale="")


def test_complexity_factories_and_caps() -> None:
    low = InstructionalComplexity.low()
    assert low.is_at_most(ComplexityLevel.MODERATE)
    assert InstructionalComplexity.very_high().exceeds(ComplexityLevel.HIGH)


def test_effectiveness_equality() -> None:
    a = StrategyEffectiveness.moderate(rationale="same")
    b = StrategyEffectiveness.moderate(rationale="same")
    assert a == b
    assert hash(a) == hash(b)
