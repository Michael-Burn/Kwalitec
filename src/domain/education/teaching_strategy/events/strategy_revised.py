"""Domain event: teaching strategy was revised.

Architecture Source
    TEACHING_STRATEGY_ARCHITECTURE.md
Concept
    TeachingStrategyRevised
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
from domain.education.teaching_strategy.enums import (
    EffectivenessLevel,
    StrategyRevisionKind,
)


@dataclass(frozen=True, slots=True)
class TeachingStrategyRevised(EducationalValueObject):
    """Immutable record that a TeachingStrategy was revised."""

    strategy_id: TeachingStrategyId
    student_id: str
    primary_strategy: TeachingStrategyType
    effectiveness_level: EffectivenessLevel
    revision_kind: StrategyRevisionKind
    secondary_count: int = 0

    def _validate(self) -> None:
        if not isinstance(self.strategy_id, TeachingStrategyId):
            raise EducationalInvariantViolation(
                "strategy_id must be a TeachingStrategyId",
                invariant="TeachingStrategyRevised.strategy_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_identity_value(self.student_id, "student_id"),
        )
        if not isinstance(self.primary_strategy, TeachingStrategyType):
            raise EducationalInvariantViolation(
                "primary_strategy must be a TeachingStrategyType",
                invariant="TeachingStrategyRevised.primary_strategy.type",
            )
        if not isinstance(self.effectiveness_level, EffectivenessLevel):
            raise EducationalInvariantViolation(
                "effectiveness_level must be an EffectivenessLevel",
                invariant="TeachingStrategyRevised.effectiveness_level.type",
            )
        if not isinstance(self.revision_kind, StrategyRevisionKind):
            raise EducationalInvariantViolation(
                "revision_kind must be a StrategyRevisionKind",
                invariant="TeachingStrategyRevised.revision_kind.type",
            )
        if not isinstance(self.secondary_count, int) or self.secondary_count < 0:
            raise EducationalInvariantViolation(
                "secondary_count must be a non-negative integer",
                invariant="TeachingStrategyRevised.secondary_count.non_negative",
            )
