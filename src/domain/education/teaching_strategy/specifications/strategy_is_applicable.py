"""Specification: TeachingStrategy is educationally applicable.

Architecture Source
    STRATEGY_SELECTION_MODEL.md
Concept
    StrategyIsApplicableSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.teaching_strategy.enums import StrategyStatus
from domain.education.teaching_strategy.policies.strategy_selection_policy import (
    StrategySelectionPolicy,
)
from domain.education.teaching_strategy.policies.strategy_validation_policy import (
    StrategyValidationPolicy,
)

if TYPE_CHECKING:
    from domain.education.teaching_strategy.aggregates.teaching_strategy import (
        TeachingStrategy,
    )


class StrategyIsApplicableSpecification:
    """True when a strategy lawfully serves its Teaching Intention.

    Applicability means the strategy is SELECTED or REVISED, references
    Intention and Diagnosis, possesses rationale and effectiveness, and does
    not contradict intention affinity / misconception duty. It does **not**
    mean a learning episode has been enacted.
    """

    def is_satisfied_by(self, strategy: TeachingStrategy) -> bool:
        if strategy.status not in {
            StrategyStatus.SELECTED,
            StrategyStatus.REVISED,
        }:
            return False
        if not strategy.intention_references:
            return False
        if not strategy.diagnosis_references:
            return False
        if not strategy.rationale.statement:
            return False
        if not strategy.student_id:
            return False
        try:
            StrategyValidationPolicy.assert_educational_integrity(
                primary=strategy.primary_strategy,
                intention_references=strategy.intention_references,
                diagnosis_references=strategy.diagnosis_references,
            )
            StrategyValidationPolicy.assert_constraints_satisfied(
                strategy.constraints,
                primary=strategy.primary_strategy,
                complexity=strategy.complexity,
                intention_references=strategy.intention_references,
                diagnosis_references=strategy.diagnosis_references,
                hypothesis_references=strategy.hypothesis_references,
                rationale=strategy.rationale,
                effectiveness=strategy.effectiveness,
                secondaries=strategy.secondary_strategies,
            )
            if not StrategySelectionPolicy.is_lawful_for_intention(
                strategy.primary_strategy,
                strategy.intention_references[0].intention_type,
            ):
                return False
        except EducationalInvariantViolation:
            return False
        return True

    def assert_satisfied_by(self, strategy: TeachingStrategy) -> None:
        if not self.is_satisfied_by(strategy):
            raise EducationalInvariantViolation(
                "teaching strategy is not educationally applicable",
                invariant="StrategyIsApplicableSpecification.unsatisfied",
            )
