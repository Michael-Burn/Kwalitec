"""Opaque references to priority, intention, and strategy aggregates.

Architecture Source
    EDUCATIONAL_DECISION_POINTS.md
Concept
    Priority Reference / Intention Reference / Strategy Reference
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.enums import (
    TeachingIntentionType,
    TeachingStrategyType,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import (
    PriorityId,
    TeachingIntentionId,
    TeachingStrategyId,
)


@dataclass(frozen=True, slots=True)
class PriorityReference(EducationalValueObject):
    """Opaque citation of an upstream EducationalPriority.

    Decision must reference Priority. It does not import or load the Priority
    package aggregate, recalculate ordering, or invent need.
    """

    priority_id: PriorityId

    def _validate(self) -> None:
        if not isinstance(self.priority_id, PriorityId):
            raise EducationalInvariantViolation(
                "priority_id must be a PriorityId",
                invariant="PriorityReference.priority_id.type",
            )

    def __str__(self) -> str:
        return self.priority_id.value


@dataclass(frozen=True, slots=True)
class IntentionReference(EducationalValueObject):
    """Opaque citation of an upstream TeachingIntention.

    Decision must reference Teaching Intention. It does not redefine the
    educational change sought or select intention types.
    """

    intention_id: TeachingIntentionId
    intention_type: TeachingIntentionType

    def _validate(self) -> None:
        if not isinstance(self.intention_id, TeachingIntentionId):
            raise EducationalInvariantViolation(
                "intention_id must be a TeachingIntentionId",
                invariant="IntentionReference.intention_id.type",
            )
        if not isinstance(self.intention_type, TeachingIntentionType):
            raise EducationalInvariantViolation(
                "intention_type must be a TeachingIntentionType",
                invariant="IntentionReference.intention_type.type",
            )

    def __str__(self) -> str:
        return f"{self.intention_id.value}:{self.intention_type.value}"


@dataclass(frozen=True, slots=True)
class StrategyReference(EducationalValueObject):
    """Opaque citation of an upstream TeachingStrategy.

    Decision must reference Strategy. It does not create, revise, or select
    teaching strategies — only evaluates readiness to execute one.
    """

    strategy_id: TeachingStrategyId
    strategy_type: TeachingStrategyType

    def _validate(self) -> None:
        if not isinstance(self.strategy_id, TeachingStrategyId):
            raise EducationalInvariantViolation(
                "strategy_id must be a TeachingStrategyId",
                invariant="StrategyReference.strategy_id.type",
            )
        if not isinstance(self.strategy_type, TeachingStrategyType):
            raise EducationalInvariantViolation(
                "strategy_type must be a TeachingStrategyType",
                invariant="StrategyReference.strategy_type.type",
            )

    def __str__(self) -> str:
        return f"{self.strategy_id.value}:{self.strategy_type.value}"
