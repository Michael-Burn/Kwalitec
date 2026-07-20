"""Behavioural tests for EducationalPriority aggregate."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import PriorityId
from domain.education.priority import (
    PriorityAssigned,
    PriorityFactorKind,
    PriorityIsActionableSpecification,
    PriorityIsStableSpecification,
    PriorityRevised,
    PriorityRevisionKind,
    PriorityScoreBand,
    PriorityStatus,
    UrgencyLevel,
)
from tests.domain.education.priority.conftest import (
    DIAGNOSIS_001,
    HYPOTHESIS_001,
    make_constraint,
    make_factor,
    make_priority,
    make_score,
    make_urgency,
)


def test_assign_emits_priority_assigned() -> None:
    priority = make_priority()
    events = priority.pull_events()
    assert len(events) == 1
    assert isinstance(events[0], PriorityAssigned)
    assert events[0].priority_id == PriorityId("prio-001")
    assert priority.is_assigned()
    assert priority.pull_events() == []


def test_assign_calculates_score_from_factors() -> None:
    priority = make_priority(
        factors=[
            make_factor(
                kind=PriorityFactorKind.PREREQUISITE_IMPORTANCE,
                contribution=0.9,
            )
        ]
    )
    assert priority.score.band is PriorityScoreBand.CRITICAL
    assert priority.urgency.level in {
        UrgencyLevel.IMMEDIATE,
        UrgencyLevel.CRITICAL,
    }
    assert priority.instructional_impact.statement


def test_promote_raises_ordering_and_emits_revised() -> None:
    priority = make_priority(
        calculate=False,
        score=make_score(PriorityScoreBand.MEDIUM, ratio=0.5),
        urgency=make_urgency(UrgencyLevel.ROUTINE),
    )
    priority.pull_events()
    priority.promote()
    assert priority.score.band is PriorityScoreBand.HIGH
    assert priority.urgency.level is UrgencyLevel.ELEVATED
    assert priority.is_revised()
    events = priority.pull_events()
    assert isinstance(events[0], PriorityRevised)
    assert events[0].revision_kind is PriorityRevisionKind.PROMOTED


def test_demote_lowers_ordering_and_emits_revised() -> None:
    priority = make_priority(
        calculate=False,
        score=make_score(PriorityScoreBand.HIGH, ratio=0.7),
        urgency=make_urgency(UrgencyLevel.ELEVATED),
    )
    priority.pull_events()
    priority.demote()
    assert priority.score.band is PriorityScoreBand.MEDIUM
    assert priority.urgency.level is UrgencyLevel.ROUTINE
    events = priority.pull_events()
    assert events[0].revision_kind is PriorityRevisionKind.DEMOTED


def test_recalculate_recomputes_from_factors() -> None:
    priority = make_priority(
        factors=[
            make_factor(
                kind=PriorityFactorKind.TRANSFER_BLOCKING,
                contribution=0.4,
            )
        ]
    )
    priority.pull_events()
    priority.recalculate(
        factors=[
            make_factor(
                factor_id="factor-strong",
                kind=PriorityFactorKind.MISCONCEPTION_PERSISTENCE,
                contribution=0.95,
            )
        ]
    )
    assert priority.score.band is PriorityScoreBand.CRITICAL
    assert priority.is_revised()
    events = priority.pull_events()
    assert events[0].revision_kind is PriorityRevisionKind.FACTORS_REPLACED


def test_recalculate_without_factor_replacement() -> None:
    priority = make_priority()
    priority.pull_events()
    before = priority.score.band
    priority.recalculate()
    assert priority.score.band is before
    events = priority.pull_events()
    assert events[0].revision_kind is PriorityRevisionKind.RECALCULATED


def test_stabilise_locks_ordering() -> None:
    priority = make_priority()
    priority.pull_events()
    priority.stabilise("ordering commitment for next episode")
    assert priority.is_stabilised()
    assert priority.stabilisation_reason is not None
    events = priority.pull_events()
    assert events[0].revision_kind is PriorityRevisionKind.STABILISED
    with pytest.raises(EducationalInvariantViolation):
        priority.promote()
    with pytest.raises(EducationalInvariantViolation):
        priority.demote()


def test_recalculate_reopens_stabilised_priority() -> None:
    priority = make_priority()
    priority.stabilise()
    priority.pull_events()
    priority.recalculate()
    assert priority.status is PriorityStatus.REVISED
    assert priority.stabilisation_reason is None


def test_duplicate_factor_kind_rejected() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc_info:
        make_priority(
            factors=[
                make_factor(factor_id="a", kind=PriorityFactorKind.EXAM_RELEVANCE),
                make_factor(factor_id="b", kind=PriorityFactorKind.EXAM_RELEVANCE),
            ]
        )
    assert "duplicate" in str(exc_info.value).casefold()


def test_missing_diagnosis_rejected() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_priority(diagnosis_references=[])


def test_missing_hypothesis_rejected() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_priority(hypothesis_references=[])


def test_constraint_enforcement_on_assign() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_priority(
            factors=[
                make_factor(
                    kind=PriorityFactorKind.PREREQUISITE_IMPORTANCE,
                    contribution=0.3,
                ),
                make_factor(
                    factor_id="factor-exam",
                    kind=PriorityFactorKind.EXAM_RELEVANCE,
                    contribution=0.9,
                ),
            ],
            constraints=[make_constraint()],
        )


def test_identity_equality() -> None:
    left = make_priority(priority_id="same")
    right = make_priority(priority_id="same")
    other = make_priority(priority_id="other")
    assert left == right
    assert left != other
    assert hash(left) == hash(right)


def test_queries() -> None:
    priority = make_priority()
    assert priority.has_diagnosis(DIAGNOSIS_001)
    assert priority.has_hypothesis(HYPOTHESIS_001)
    assert priority.has_factor_kind(PriorityFactorKind.PREREQUISITE_IMPORTANCE)
    assert priority.factor_count() == 1
    assert priority.diagnosis_count() == 1
    assert priority.hypothesis_count() == 1
    assert priority.peak_factor().kind is PriorityFactorKind.PREREQUISITE_IMPORTANCE


def test_actionable_specification() -> None:
    priority = make_priority()
    assert PriorityIsActionableSpecification().is_satisfied_by(priority)


def test_stable_specification() -> None:
    priority = make_priority()
    assert not PriorityIsStableSpecification().is_satisfied_by(priority)
    priority.stabilise()
    assert PriorityIsStableSpecification().is_satisfied_by(priority)


def test_promote_at_max_fails() -> None:
    priority = make_priority(
        calculate=False,
        score=make_score(PriorityScoreBand.CRITICAL, ratio=0.9),
        urgency=make_urgency(UrgencyLevel.CRITICAL),
    )
    with pytest.raises(EducationalInvariantViolation):
        priority.promote()


def test_demote_at_min_fails() -> None:
    priority = make_priority(
        calculate=False,
        score=make_score(PriorityScoreBand.NEGLIGIBLE, ratio=0.05),
        urgency=make_urgency(UrgencyLevel.DEFERRED),
    )
    with pytest.raises(EducationalInvariantViolation):
        priority.demote()


def test_repr_contains_identity() -> None:
    priority = make_priority(priority_id="prio-repr")
    assert "prio-repr" in repr(priority)
