"""Domain event: teaching strategy was selected.

Architecture Source
    TEACHING_STRATEGY_ARCHITECTURE.md
Concept
    TeachingStrategySelected
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)
from domain.education.foundation.enums import TeachingStrategyType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import TeachingStrategyId
from domain.education.teaching_strategy.enums import EffectivenessLevel


@dataclass(frozen=True, slots=True)
class TeachingStrategySelected(EducationalValueObject):
    """Immutable record that a TeachingStrategy was selected."""

    strategy_id: TeachingStrategyId
    student_id: str
    primary_strategy: TeachingStrategyType
    effectiveness_level: EffectivenessLevel
    intention_count: int
    diagnosis_count: int
    hypothesis_count: int
    secondary_count: int

    def _validate(self) -> None:
        if not isinstance(self.strategy_id, TeachingStrategyId):
            raise EducationalInvariantViolation(
                "strategy_id must be a TeachingStrategyId",
                invariant="TeachingStrategySelected.strategy_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_identity_value(self.student_id, "student_id"),
        )
        if not isinstance(self.primary_strategy, TeachingStrategyType):
            raise EducationalInvariantViolation(
                "primary_strategy must be a TeachingStrategyType",
                invariant="TeachingStrategySelected.primary_strategy.type",
            )
        if not isinstance(self.effectiveness_level, EffectivenessLevel):
            raise EducationalInvariantViolation(
                "effectiveness_level must be an EffectivenessLevel",
                invariant="TeachingStrategySelected.effectiveness_level.type",
            )
        if not isinstance(self.intention_count, int) or self.intention_count < 1:
            raise EducationalInvariantViolation(
                "intention_count must be a positive integer",
                invariant="TeachingStrategySelected.intention_count.positive",
            )
        if not isinstance(self.diagnosis_count, int) or self.diagnosis_count < 1:
            raise EducationalInvariantViolation(
                "diagnosis_count must be a positive integer",
                invariant="TeachingStrategySelected.diagnosis_count.positive",
            )
        if not isinstance(self.hypothesis_count, int) or self.hypothesis_count < 0:
            raise EducationalInvariantViolation(
                "hypothesis_count must be a non-negative integer",
                invariant="TeachingStrategySelected.hypothesis_count.non_negative",
            )
        if not isinstance(self.secondary_count, int) or self.secondary_count < 0:
            raise EducationalInvariantViolation(
                "secondary_count must be a non-negative integer",
                invariant="TeachingStrategySelected.secondary_count.non_negative",
            )
