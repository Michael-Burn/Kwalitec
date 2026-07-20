"""Specification tests for Educational Priority."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.priority import (
    PriorityIsActionableSpecification,
    PriorityIsStableSpecification,
    PriorityScoreBand,
    UrgencyLevel,
)
from tests.domain.education.priority.conftest import (
    make_factor,
    make_impact,
    make_priority,
    make_score,
    make_urgency,
)


def test_actionable_for_assigned_priority() -> None:
    priority = make_priority()
    PriorityIsActionableSpecification().assert_satisfied_by(priority)


def test_actionable_false_for_negligible_score() -> None:
    priority = make_priority(
        calculate=False,
        score=make_score(PriorityScoreBand.NEGLIGIBLE, ratio=0.05),
        urgency=make_urgency(UrgencyLevel.DEFERRED),
        instructional_impact=make_impact(statement="Marginal optional enrichment"),
    )
    assert not PriorityIsActionableSpecification().is_satisfied_by(priority)


def test_actionable_assert_raises() -> None:
    priority = make_priority(
        calculate=False,
        score=make_score(PriorityScoreBand.NEGLIGIBLE, ratio=0.05),
        urgency=make_urgency(UrgencyLevel.DEFERRED),
    )
    with pytest.raises(EducationalInvariantViolation):
        PriorityIsActionableSpecification().assert_satisfied_by(priority)


def test_stable_requires_stabilised_status() -> None:
    priority = make_priority()
    assert not PriorityIsStableSpecification().is_satisfied_by(priority)
    priority.stabilise()
    PriorityIsStableSpecification().assert_satisfied_by(priority)


def test_stable_false_when_manual_score_diverges_from_calculation() -> None:
    priority = make_priority(
        calculate=False,
        factors=[make_factor(contribution=0.95)],
        score=make_score(PriorityScoreBand.LOW, ratio=0.2),
        urgency=make_urgency(UrgencyLevel.DEFERRED),
    )
    priority.stabilise()
    assert not PriorityIsStableSpecification().is_satisfied_by(priority)


def test_stable_assert_raises_when_unsatisfied() -> None:
    priority = make_priority()
    with pytest.raises(EducationalInvariantViolation):
        PriorityIsStableSpecification().assert_satisfied_by(priority)


def test_actionable_after_recalculate() -> None:
    priority = make_priority()
    priority.recalculate()
    assert PriorityIsActionableSpecification().is_satisfied_by(priority)


def test_actionable_when_stabilised() -> None:
    priority = make_priority()
    priority.stabilise()
    assert PriorityIsActionableSpecification().is_satisfied_by(priority)
