"""Specification tests for Educational Hypothesis."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.hypothesis import (
    HypothesisIsRevisableSpecification,
    HypothesisIsSupportedSpecification,
    HypothesisKind,
    Plausibility,
)
from tests.domain.education.hypothesis.conftest import make_hypothesis


def test_supported_when_active_with_warrant() -> None:
    hypothesis = make_hypothesis()
    assert HypothesisIsSupportedSpecification().is_satisfied_by(hypothesis)


def test_supported_false_when_discarded() -> None:
    hypothesis = make_hypothesis()
    hypothesis.discard("contradicted")
    assert not HypothesisIsSupportedSpecification().is_satisfied_by(hypothesis)


def test_supported_assert_raises_when_discarded() -> None:
    hypothesis = make_hypothesis()
    hypothesis.discard("contradicted")
    with pytest.raises(EducationalInvariantViolation):
        HypothesisIsSupportedSpecification().assert_satisfied_by(hypothesis)


def test_revisable_when_active() -> None:
    hypothesis = make_hypothesis()
    assert HypothesisIsRevisableSpecification().is_satisfied_by(hypothesis)


def test_revisable_when_revised() -> None:
    hypothesis = make_hypothesis()
    hypothesis.revise(explanation="Narrowed explanatory reading")
    assert HypothesisIsRevisableSpecification().is_satisfied_by(hypothesis)


def test_revisable_when_suspended() -> None:
    hypothesis = make_hypothesis()
    hypothesis.revise(plausibility=Plausibility.suspended())
    assert HypothesisIsRevisableSpecification().is_satisfied_by(hypothesis)


def test_not_revisable_when_discarded() -> None:
    hypothesis = make_hypothesis()
    hypothesis.discard("replaced")
    assert not HypothesisIsRevisableSpecification().is_satisfied_by(hypothesis)
    with pytest.raises(EducationalInvariantViolation):
        HypothesisIsRevisableSpecification().assert_satisfied_by(hypothesis)


@pytest.mark.parametrize("kind", list(HypothesisKind))
def test_supported_per_kind(kind: HypothesisKind) -> None:
    hypothesis = make_hypothesis(
        hypothesis_id=f"hyp-spec-{kind.value}",
        hypothesis_kind=kind,
    )
    assert HypothesisIsSupportedSpecification().is_satisfied_by(hypothesis)
    assert HypothesisIsRevisableSpecification().is_satisfied_by(hypothesis)
