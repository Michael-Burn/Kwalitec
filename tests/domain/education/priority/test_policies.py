"""Tests for Educational Priority policies."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.priority import (
    PriorityCalculationPolicy,
    PriorityConstraintKind,
    PriorityFactorKind,
    PriorityScoreBand,
    PriorityValidationPolicy,
    UrgencyLevel,
)
from tests.domain.education.priority.conftest import (
    make_constraint,
    make_factor,
    make_score,
    make_urgency,
)


@pytest.mark.parametrize("kind", list(PriorityFactorKind))
def test_gate_affinity_known_for_all_kinds(kind: PriorityFactorKind) -> None:
    gate = PriorityCalculationPolicy.gate_for(kind)
    assert 1 <= gate <= 10


def test_prerequisite_outranks_exam_in_ordering_weight() -> None:
    prereq = make_factor(
        kind=PriorityFactorKind.PREREQUISITE_IMPORTANCE, contribution=0.5
    )
    exam = make_factor(
        factor_id="exam",
        kind=PriorityFactorKind.EXAM_RELEVANCE,
        contribution=0.5,
    )
    assert PriorityCalculationPolicy.factor_ordering_weight(
        prereq
    ) > PriorityCalculationPolicy.factor_ordering_weight(exam)


def test_misconception_outranks_exam_in_ordering_weight() -> None:
    misconception = make_factor(
        kind=PriorityFactorKind.MISCONCEPTION_PERSISTENCE, contribution=0.6
    )
    exam = make_factor(
        factor_id="exam",
        kind=PriorityFactorKind.EXAM_RELEVANCE,
        contribution=0.6,
    )
    assert PriorityCalculationPolicy.factor_ordering_weight(
        misconception
    ) > PriorityCalculationPolicy.factor_ordering_weight(exam)


@pytest.mark.parametrize("contribution", [0.1, 0.3, 0.5, 0.7, 0.9, 1.0])
def test_calculate_produces_coherent_triple(contribution: float) -> None:
    score, urgency, impact = PriorityCalculationPolicy.calculate(
        [
            make_factor(
                kind=PriorityFactorKind.CONCEPT_CENTRALITY,
                contribution=contribution,
            )
        ]
    )
    assert score.band in PriorityCalculationPolicy.score_order()
    assert urgency.level in PriorityCalculationPolicy.urgency_order()
    assert impact.level in PriorityCalculationPolicy.impact_order()
    assert score.ratio is not None


def test_calculate_rejects_empty_factors() -> None:
    with pytest.raises(EducationalInvariantViolation):
        PriorityCalculationPolicy.calculate([])


def test_promote_and_demote_policy() -> None:
    score = make_score(PriorityScoreBand.MEDIUM)
    urgency = make_urgency(UrgencyLevel.ROUTINE)
    promoted_score, promoted_urgency = PriorityCalculationPolicy.promote(
        score, urgency
    )
    assert promoted_score.band is PriorityScoreBand.HIGH
    assert promoted_urgency.level is UrgencyLevel.ELEVATED
    demoted_score, demoted_urgency = PriorityCalculationPolicy.demote(
        promoted_score, promoted_urgency
    )
    assert demoted_score.band is PriorityScoreBand.MEDIUM
    assert demoted_urgency.level is UrgencyLevel.ROUTINE


def test_validation_rejects_duplicate_factor_kinds() -> None:
    with pytest.raises(EducationalInvariantViolation):
        PriorityValidationPolicy.assert_factors(
            [
                make_factor(factor_id="a"),
                make_factor(factor_id="b"),
            ]
        )


def test_validation_require_factor_constraint() -> None:
    factors = [
        make_factor(kind=PriorityFactorKind.EXAM_RELEVANCE, contribution=0.4)
    ]
    constraints = [
        make_constraint(
            kind=PriorityConstraintKind.REQUIRE_FACTOR,
            related_factor_kind=PriorityFactorKind.MISCONCEPTION_PERSISTENCE,
        )
    ]
    with pytest.raises(EducationalInvariantViolation):
        PriorityValidationPolicy.assert_constraints_satisfied(
            constraints,
            factors,
            make_score(PriorityScoreBand.MEDIUM, ratio=0.4),
            make_urgency(UrgencyLevel.ROUTINE),
        )


def test_validation_forbid_factor_constraint() -> None:
    factors = [
        make_factor(kind=PriorityFactorKind.EXAM_RELEVANCE, contribution=0.4)
    ]
    constraints = [
        make_constraint(
            kind=PriorityConstraintKind.FORBID_FACTOR,
            related_factor_kind=PriorityFactorKind.EXAM_RELEVANCE,
        )
    ]
    with pytest.raises(EducationalInvariantViolation):
        PriorityValidationPolicy.assert_constraints_satisfied(
            constraints,
            factors,
            make_score(PriorityScoreBand.MEDIUM, ratio=0.4),
            make_urgency(UrgencyLevel.ROUTINE),
        )


def test_validation_cap_urgency() -> None:
    with pytest.raises(EducationalInvariantViolation):
        PriorityValidationPolicy.assert_constraints_satisfied(
            [
                make_constraint(
                    kind=PriorityConstraintKind.CAP_URGENCY,
                    max_urgency=UrgencyLevel.ROUTINE,
                )
            ],
            [make_factor()],
            make_score(),
            make_urgency(UrgencyLevel.CRITICAL),
        )


def test_validation_cap_score() -> None:
    with pytest.raises(EducationalInvariantViolation):
        PriorityValidationPolicy.assert_constraints_satisfied(
            [
                make_constraint(
                    kind=PriorityConstraintKind.CAP_SCORE,
                    max_score_band=PriorityScoreBand.MEDIUM,
                )
            ],
            [make_factor()],
            make_score(PriorityScoreBand.CRITICAL, ratio=0.9),
            make_urgency(UrgencyLevel.ROUTINE),
        )


def test_protect_misconception_over_exam() -> None:
    with pytest.raises(EducationalInvariantViolation):
        PriorityValidationPolicy.assert_constraints_satisfied(
            [
                make_constraint(
                    kind=PriorityConstraintKind.PROTECT_MISCONCEPTION_OVER_PRACTICE
                )
            ],
            [
                make_factor(
                    kind=PriorityFactorKind.MISCONCEPTION_PERSISTENCE,
                    contribution=0.2,
                ),
                make_factor(
                    factor_id="exam",
                    kind=PriorityFactorKind.EXAM_RELEVANCE,
                    contribution=0.9,
                ),
            ],
            make_score(PriorityScoreBand.HIGH, ratio=0.6),
            make_urgency(UrgencyLevel.ELEVATED),
        )


def test_exam_must_not_skip_conceptual_repair() -> None:
    with pytest.raises(EducationalInvariantViolation):
        PriorityValidationPolicy.assert_constraints_satisfied(
            [
                make_constraint(
                    kind=PriorityConstraintKind.EXAM_MUST_NOT_SKIP_CONCEPTUAL_REPAIR
                )
            ],
            [
                make_factor(
                    kind=PriorityFactorKind.MISCONCEPTION_PERSISTENCE,
                    contribution=0.4,
                ),
                make_factor(
                    factor_id="exam",
                    kind=PriorityFactorKind.EXAM_RELEVANCE,
                    contribution=0.4,
                ),
            ],
            make_score(PriorityScoreBand.HIGH, ratio=0.6),
            make_urgency(UrgencyLevel.ELEVATED),
        )


def test_lawful_constraint_combination_passes() -> None:
    PriorityValidationPolicy.assert_constraints_satisfied(
        [
            make_constraint(),
            make_constraint(
                constraint_id="c2",
                kind=PriorityConstraintKind.FORBID_ENGAGEMENT_ORDERING,
            ),
        ],
        [
            make_factor(
                kind=PriorityFactorKind.PREREQUISITE_IMPORTANCE,
                contribution=0.9,
            ),
            make_factor(
                factor_id="exam",
                kind=PriorityFactorKind.EXAM_RELEVANCE,
                contribution=0.2,
            ),
        ],
        make_score(PriorityScoreBand.HIGH, ratio=0.7),
        make_urgency(UrgencyLevel.ELEVATED),
    )


def test_band_for_ratio_thresholds() -> None:
    assert (
        PriorityCalculationPolicy.band_for_ratio(0.0) is PriorityScoreBand.NEGLIGIBLE
    )
    assert PriorityCalculationPolicy.band_for_ratio(0.2) is PriorityScoreBand.LOW
    assert PriorityCalculationPolicy.band_for_ratio(0.4) is PriorityScoreBand.MEDIUM
    assert PriorityCalculationPolicy.band_for_ratio(0.6) is PriorityScoreBand.HIGH
    assert (
        PriorityCalculationPolicy.band_for_ratio(0.9) is PriorityScoreBand.CRITICAL
    )
