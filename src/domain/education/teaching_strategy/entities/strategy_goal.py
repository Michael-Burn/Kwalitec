"""Strategy goal — instructional aim realised by a teaching strategy.

Architecture Source
    TEACHING_STRATEGY_ARCHITECTURE.md
Concept
    Strategy Goal
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.enums import TeachingStrategyType
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class StrategyGoalId(EducationalValueObject):
    """Identity of a strategy goal within a TeachingStrategy."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "StrategyGoalId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class StrategyGoal(EducationalEntity):
    """Instructional aim the strategy pursues for a Teaching Intention.

    States *how* instruction will advance the intention for the next
    episode grain. Must not claim mastery as an outcome.
    """

    goal_id: StrategyGoalId
    statement: str
    strategy_type: TeachingStrategyType
    expected_evidence_hint: str | None = None

    @property
    def entity_id(self) -> StrategyGoalId:
        return self.goal_id

    def _validate(self) -> None:
        if not isinstance(self.goal_id, StrategyGoalId):
            raise EducationalInvariantViolation(
                "goal_id must be a StrategyGoalId",
                invariant="StrategyGoal.goal_id.type",
            )
        object.__setattr__(
            self,
            "statement",
            require_non_empty_text(self.statement, "statement"),
        )
        if not isinstance(self.strategy_type, TeachingStrategyType):
            raise EducationalInvariantViolation(
                "strategy_type must be a TeachingStrategyType",
                invariant="StrategyGoal.strategy_type.type",
            )
        if self.expected_evidence_hint is not None:
            object.__setattr__(
                self,
                "expected_evidence_hint",
                require_non_empty_text(
                    self.expected_evidence_hint, "expected_evidence_hint"
                ),
            )
        self._assert_no_mastery_claim(self.statement)
        if self.expected_evidence_hint is not None:
            self._assert_no_mastery_claim(self.expected_evidence_hint)

    @staticmethod
    def _assert_no_mastery_claim(text: str) -> None:
        lowered = text.casefold()
        forbidden = ("mastered", "achieve mastery", "declare mastery", "full mastery")
        for token in forbidden:
            if token in lowered:
                raise EducationalInvariantViolation(
                    "strategy goal must never claim mastery as episode outcome",
                    invariant="StrategyGoal.no_mastery_claim",
                )

    def with_statement(self, statement: str) -> StrategyGoal:
        return StrategyGoal(
            goal_id=self.goal_id,
            statement=statement,
            strategy_type=self.strategy_type,
            expected_evidence_hint=self.expected_evidence_hint,
        )
