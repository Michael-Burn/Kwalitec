"""Opaque references owned by Educational Orchestrator.

Architecture Source
    EDUCATIONAL_ORCHESTRATION_MODEL.md
Concept
    Approved Decision Reference / Strategy Reference / Episode Reference
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.enums import TeachingStrategyType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import (
    DecisionId,
    LearningEpisodeId,
    TeachingStrategyId,
)


@dataclass(frozen=True, slots=True)
class ApprovedDecisionReference(EducationalValueObject):
    """Opaque citation of an upstream approved EducationalDecision.

    Orchestration must reference an approved decision. It does not evaluate
    readiness, reconsider outcomes, diagnose, or select strategies.
    """

    decision_id: DecisionId
    approved: bool = True

    def _validate(self) -> None:
        if not isinstance(self.decision_id, DecisionId):
            raise EducationalInvariantViolation(
                "decision_id must be a DecisionId",
                invariant="ApprovedDecisionReference.decision_id.type",
            )
        if not isinstance(self.approved, bool):
            raise EducationalInvariantViolation(
                "approved must be a bool",
                invariant="ApprovedDecisionReference.approved.type",
            )
        if not self.approved:
            raise EducationalInvariantViolation(
                "orchestration must reference an approved decision",
                invariant="ApprovedDecisionReference.approved.required",
            )

    def __str__(self) -> str:
        return self.decision_id.value


@dataclass(frozen=True, slots=True)
class StrategyReference(EducationalValueObject):
    """Opaque citation of an upstream TeachingStrategy.

    Orchestration coordinates strategy references supplied by prior reasoning.
    It does not choose, revise, or invent teaching strategies.
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


@dataclass(frozen=True, slots=True)
class EpisodeReference(EducationalValueObject):
    """Opaque citation of a Learning Episode coordinated by orchestration.

    Orchestration coordinates episode creation and sequencing. It does not
    execute episode pedagogy or interpret episode outcomes.
    """

    episode_id: LearningEpisodeId

    def _validate(self) -> None:
        if not isinstance(self.episode_id, LearningEpisodeId):
            raise EducationalInvariantViolation(
                "episode_id must be a LearningEpisodeId",
                invariant="EpisodeReference.episode_id.type",
            )

    def __str__(self) -> str:
        return self.episode_id.value
