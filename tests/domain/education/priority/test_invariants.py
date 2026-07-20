"""Invariant enforcement tests for Educational Priority."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.priority import (
    PriorityConstraintKind,
    PriorityFactorKind,
    PriorityScoreBand,
    UrgencyLevel,
)
from tests.domain.education.priority.conftest import (
    make_constraint,
    make_diagnosis_ref,
    make_factor,
    make_hypothesis_ref,
    make_priority,
    make_scope,
    make_score,
    make_urgency,
)


def test_must_reference_diagnosis() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc_info:
        make_priority(diagnosis_references=[])
    assert "diagnosis" in (exc_info.value.invariant or "")


def test_must_reference_hypothesis() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc_info:
        make_priority(hypothesis_references=[])
    assert "hypothesis" in (exc_info.value.invariant or "")


def test_must_possess_score() -> None:
    # assign() always calculates or accepts score; empty factors block score.
    with pytest.raises(EducationalInvariantViolation):
        make_priority(factors=[])


def test_must_possess_urgency_and_impact_via_calculation() -> None:
    priority = make_priority()
    assert priority.urgency is not None
    assert priority.instructional_impact is not None
    assert priority.score is not None


def test_cannot_contain_duplicate_factor_ids() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_priority(
            factors=[
                make_factor(factor_id="dup"),
                make_factor(
                    factor_id="dup",
                    kind=PriorityFactorKind.EXAM_RELEVANCE,
                ),
            ]
        )


def test_cannot_contain_duplicate_factor_kinds() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_priority(
            factors=[
                make_factor(
                    factor_id="a",
                    kind=PriorityFactorKind.TRANSFER_BLOCKING,
                ),
                make_factor(
                    factor_id="b",
                    kind=PriorityFactorKind.TRANSFER_BLOCKING,
                ),
            ]
        )


def test_cannot_contradict_educational_constraints() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_priority(
            factors=[
                make_factor(
                    kind=PriorityFactorKind.CONCEPT_CENTRALITY,
                    contribution=0.2,
                ),
                make_factor(
                    factor_id="exam",
                    kind=PriorityFactorKind.EXAM_RELEVANCE,
                    contribution=0.95,
                ),
            ],
            constraints=[
                make_constraint(
                    kind=PriorityConstraintKind.PROTECT_UNDERSTANDING_OVER_SPEED
                )
            ],
        )


def test_must_remain_recalculable() -> None:
    priority = make_priority()
    priority.stabilise()
    # Recalculation always available.
    priority.recalculate()
    assert priority.is_revised()


def test_severity_not_used_as_priority_ordering() -> None:
    # Priority score bands are instructional; they are not diagnosis severity.
    priority = make_priority(
        calculate=False,
        score=make_score(PriorityScoreBand.LOW, ratio=0.2),
        urgency=make_urgency(UrgencyLevel.DEFERRED),
    )
    assert priority.score.band is PriorityScoreBand.LOW
    assert not hasattr(priority, "severity")


def test_duplicate_diagnosis_reference_rejected() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_priority(
            diagnosis_references=[
                make_diagnosis_ref(),
                make_diagnosis_ref(),
            ]
        )


def test_duplicate_hypothesis_reference_rejected() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_priority(
            hypothesis_references=[
                make_hypothesis_ref(),
                make_hypothesis_ref(),
            ]
        )


def test_scope_required() -> None:
    priority = make_priority(scope=make_scope(statement="Clear educational locus"))
    assert priority.scope.statement


def test_cap_urgency_blocks_promote() -> None:
    priority = make_priority(
        calculate=False,
        score=make_score(PriorityScoreBand.MEDIUM, ratio=0.5),
        urgency=make_urgency(UrgencyLevel.ROUTINE),
        constraints=[
            make_constraint(
                kind=PriorityConstraintKind.CAP_URGENCY,
                max_urgency=UrgencyLevel.ROUTINE,
            )
        ],
    )
    with pytest.raises(EducationalInvariantViolation):
        priority.promote()


def test_stabilised_blocks_promote_and_demote_and_stabilise() -> None:
    priority = make_priority()
    priority.stabilise()
    with pytest.raises(EducationalInvariantViolation):
        priority.promote()
    with pytest.raises(EducationalInvariantViolation):
        priority.demote()
    with pytest.raises(EducationalInvariantViolation):
        priority.stabilise()


def test_multiple_diagnoses_and_hypotheses_allowed_when_distinct() -> None:
    priority = make_priority(
        diagnosis_references=[
            make_diagnosis_ref(diagnosis_id="diag-a"),
            make_diagnosis_ref(diagnosis_id="diag-b"),
        ],
        hypothesis_references=[
            make_hypothesis_ref(hypothesis_id="hyp-a"),
            make_hypothesis_ref(hypothesis_id="hyp-b"),
        ],
    )
    assert priority.diagnosis_count() == 2
    assert priority.hypothesis_count() == 2
