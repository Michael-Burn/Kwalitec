"""Specification tests for Teaching Intention."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.teaching_intention import (
    IntentionIsActionableSpecification,
    IntentionIsAlignedSpecification,
)
from tests.domain.education.teaching_intention.conftest import make_intention


def test_actionable_false_for_draft() -> None:
    intention = make_intention()
    spec = IntentionIsActionableSpecification()
    assert not spec.is_satisfied_by(intention)
    with pytest.raises(EducationalInvariantViolation, match="actionable"):
        spec.assert_satisfied_by(intention)


def test_actionable_true_after_activation() -> None:
    intention = make_intention(activate=True)
    IntentionIsActionableSpecification().assert_satisfied_by(intention)


def test_actionable_true_after_revision() -> None:
    intention = make_intention(activate=True)
    intention.strengthen()
    assert IntentionIsActionableSpecification().is_satisfied_by(intention)


def test_actionable_false_when_retired() -> None:
    intention = make_intention(activate=True)
    intention.retire(reason="replaced")
    assert not IntentionIsActionableSpecification().is_satisfied_by(intention)


def test_aligned_specification() -> None:
    intention = make_intention()
    IntentionIsAlignedSpecification().assert_satisfied_by(intention)


def test_aligned_fails_for_contradiction() -> None:
    from domain.education.foundation.enums import (
        DiagnosisType,
        TeachingIntentionType,
    )
    from tests.domain.education.teaching_intention.conftest import (
        make_diagnosis_ref,
        make_goal,
    )

    # Build via direct constructor bypassing create alignment? Can't —
    # exercise specification against a mutated-like unlawful pair by using
    # draft revise to an unlawful type (should fail at revise).
    intention = make_intention()
    with pytest.raises(EducationalInvariantViolation):
        intention.revise(
            intention_type=TeachingIntentionType.REPAIR_MISCONCEPTION,
            goal=make_goal(
                intention_type=TeachingIntentionType.REPAIR_MISCONCEPTION
            ),
            # keep prerequisite diagnosis — misaligned
            diagnosis_references=[
                make_diagnosis_ref(diagnosis_type=DiagnosisType.PREREQUISITE_GAP)
            ],
        )
