"""Specification: TeachingStrategy composition is lawful.

Architecture Source
    STRATEGY_COMPOSITION_MODEL.md
Concept
    StrategyIsComposableSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.teaching_strategy.policies.strategy_composition_policy import (
    StrategyCompositionPolicy,
)

if TYPE_CHECKING:
    from domain.education.teaching_strategy.aggregates.teaching_strategy import (
        TeachingStrategy,
    )
    from domain.education.teaching_strategy.entities.strategy_reference import (
        SecondaryStrategyReference,
    )


class StrategyIsComposableSpecification:
    """True when secondary strategies form a lawful composition with primary.

    Composability requires no duplicates, contiguous ordering, and either a
    canonical arc prefix or pairwise follow-on compatibility. A strategy with
    no secondaries is vacuously composable.
    """

    def is_satisfied_by(
        self,
        strategy: TeachingStrategy,
        *,
        proposed_secondaries: tuple[SecondaryStrategyReference, ...]
        | list[SecondaryStrategyReference]
        | None = None,
    ) -> bool:
        secondaries = (
            tuple(proposed_secondaries)
            if proposed_secondaries is not None
            else strategy.secondary_strategies
        )
        try:
            StrategyCompositionPolicy.assert_secondaries(
                strategy.primary_strategy, secondaries
            )
            StrategyCompositionPolicy.assert_no_coequal_primaries(
                strategy.primary_strategy, secondaries
            )
        except EducationalInvariantViolation:
            return False
        return True

    def assert_satisfied_by(
        self,
        strategy: TeachingStrategy,
        *,
        proposed_secondaries: tuple[SecondaryStrategyReference, ...]
        | list[SecondaryStrategyReference]
        | None = None,
    ) -> None:
        if not self.is_satisfied_by(
            strategy, proposed_secondaries=proposed_secondaries
        ):
            raise EducationalInvariantViolation(
                "teaching strategy composition is not lawful",
                invariant="StrategyIsComposableSpecification.unsatisfied",
            )
