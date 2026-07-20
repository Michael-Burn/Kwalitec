"""Value object tests for Teaching Intention."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.teaching_intention import (
    ExpectedOutcome,
    IntentionStrength,
    IntentionStrengthLevel,
)


@pytest.mark.parametrize("level", list(IntentionStrengthLevel))
def test_strength_of_each_level(level: IntentionStrengthLevel) -> None:
    strength = IntentionStrength.of(level, rationale=f"rationale {level.value}")
    assert strength.level is level
    assert level.value in str(strength)


def test_strengthen_and_weaken_ladder() -> None:
    strength = IntentionStrength.tentative()
    strength = strength.strengthened()
    assert strength.level is IntentionStrengthLevel.MODERATE
    strength = strength.strengthened()
    assert strength.level is IntentionStrengthLevel.FIRM
    strength = strength.strengthened()
    assert strength.level is IntentionStrengthLevel.COMMITTED
    with pytest.raises(EducationalInvariantViolation, match="maximum"):
        strength.strengthened()
    strength = strength.weakened()
    assert strength.level is IntentionStrengthLevel.FIRM
    while strength.level is not IntentionStrengthLevel.TENTATIVE:
        strength = strength.weakened()
    with pytest.raises(EducationalInvariantViolation, match="minimum"):
        strength.weakened()


def test_strength_is_at_least() -> None:
    firm = IntentionStrength.firm()
    assert firm.is_at_least(IntentionStrengthLevel.MODERATE)
    assert not IntentionStrength.tentative().is_at_least(
        IntentionStrengthLevel.COMMITTED
    )


def test_strength_blank_rationale_rejected() -> None:
    with pytest.raises(EducationalInvariantViolation, match="rationale"):
        IntentionStrength.of(IntentionStrengthLevel.MODERATE, rationale="  ")


def test_strength_factories() -> None:
    assert IntentionStrength.moderate().level is IntentionStrengthLevel.MODERATE
    assert IntentionStrength.committed().level is IntentionStrengthLevel.COMMITTED


def test_expected_outcome_requires_evaluable() -> None:
    with pytest.raises(EducationalInvariantViolation, match="evaluable"):
        ExpectedOutcome.of(
            "Improved retention",
            "Spaced probe success",
            evaluable=False,
        )


def test_expected_outcome_with_helpers() -> None:
    outcome = ExpectedOutcome.of(
        "Displace wrong mental model",
        "Correct discrimination on contrastive cases",
    )
    amended = outcome.with_statement("Corrected structure usable in explanation")
    assert "Corrected" in amended.statement
    evidence = outcome.with_success_evidence("Own-words corrected explanation")
    assert "Own-words" in evidence.success_evidence
    assert str(outcome) == outcome.statement


def test_expected_outcome_rejects_strategy_language() -> None:
    with pytest.raises(EducationalInvariantViolation, match="strategy"):
        ExpectedOutcome.of(
            "Select teaching strategy for repair",
            "Student improves",
        )


def test_expected_outcome_rejects_mastery() -> None:
    with pytest.raises(EducationalInvariantViolation, match="mastery"):
        ExpectedOutcome.of(
            "Declare mastery after one probe",
            "Single correct answer",
        )


def test_expected_outcome_blank_rejected() -> None:
    with pytest.raises(EducationalInvariantViolation):
        ExpectedOutcome.of("  ", "evidence")
    with pytest.raises(EducationalInvariantViolation):
        ExpectedOutcome.of("statement", "  ")
