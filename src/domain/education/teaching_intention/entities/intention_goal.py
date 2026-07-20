"""Intention goal — atomic educational change statement.

Architecture Source
    TEACHING_INTENTION_MODEL.md
Concept
    Intention Goal / Teaching Goal precursor
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.enums import TeachingIntentionType
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class IntentionGoalId(EducationalValueObject):
    """Identity of an intention goal within a TeachingIntention."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "IntentionGoalId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class IntentionGoal(EducationalEntity):
    """Educational change the intention seeks — *what*, never *how*.

    Realises one TeachingIntentionType as an atomic goal statement. Must not
    claim mastery, name a teaching strategy, or bundle unrelated aims.
    """

    goal_id: IntentionGoalId
    statement: str
    intention_type: TeachingIntentionType
    success_evidence_hint: str | None = None

    @property
    def entity_id(self) -> IntentionGoalId:
        return self.goal_id

    def _validate(self) -> None:
        if not isinstance(self.goal_id, IntentionGoalId):
            raise EducationalInvariantViolation(
                "goal_id must be an IntentionGoalId",
                invariant="IntentionGoal.goal_id.type",
            )
        object.__setattr__(
            self,
            "statement",
            require_non_empty_text(self.statement, "statement"),
        )
        if not isinstance(self.intention_type, TeachingIntentionType):
            raise EducationalInvariantViolation(
                "intention_type must be a TeachingIntentionType",
                invariant="IntentionGoal.intention_type.type",
            )
        if self.success_evidence_hint is not None:
            object.__setattr__(
                self,
                "success_evidence_hint",
                require_non_empty_text(
                    self.success_evidence_hint, "success_evidence_hint"
                ),
            )
        self._assert_no_mastery_claim(self.statement)
        if self.success_evidence_hint is not None:
            self._assert_no_mastery_claim(self.success_evidence_hint)
        self._assert_no_strategy_language(self.statement)

    @staticmethod
    def _assert_no_mastery_claim(text: str) -> None:
        lowered = text.casefold()
        forbidden = ("mastered", "achieve mastery", "declare mastery", "full mastery")
        for token in forbidden:
            if token in lowered:
                raise EducationalInvariantViolation(
                    "intention goal must never claim mastery as episode outcome",
                    invariant="IntentionGoal.no_mastery_claim",
                )

    @staticmethod
    def _assert_no_strategy_language(text: str) -> None:
        lowered = text.casefold()
        forbidden = (
            "use interleaved practice",
            "apply spaced retrieval",
            "run socratic questioning",
            "select teaching strategy",
            "choose strategy",
        )
        for token in forbidden:
            if token in lowered:
                raise EducationalInvariantViolation(
                    "intention goal must not select or name teaching strategy",
                    invariant="IntentionGoal.no_strategy",
                )

    def with_statement(self, statement: str) -> IntentionGoal:
        """Return a copy with an amended goal statement."""
        return IntentionGoal(
            goal_id=self.goal_id,
            statement=statement,
            intention_type=self.intention_type,
            success_evidence_hint=self.success_evidence_hint,
        )

    def with_success_evidence_hint(self, hint: str | None) -> IntentionGoal:
        return IntentionGoal(
            goal_id=self.goal_id,
            statement=self.statement,
            intention_type=self.intention_type,
            success_evidence_hint=hint,
        )
