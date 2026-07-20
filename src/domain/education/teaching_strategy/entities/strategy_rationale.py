"""Strategy rationale — educational justification for strategy selection.

Architecture Source
    STRATEGY_SELECTION_MODEL.md (R-S14)
    STRATEGY_INVARIANTS.md (S4)
Concept
    Educational Rationale
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class StrategyRationaleId(EducationalValueObject):
    """Identity of a strategy rationale within a TeachingStrategy."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "StrategyRationaleId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class StrategyRationale(EducationalEntity):
    """Narratable educational justification linking diagnosis → intention → strategy.

    Every material strategy selection requires educational language that
    explains *why this approach*. Rationale is not a prompt template or UI
    copy.
    """

    rationale_id: StrategyRationaleId
    statement: str
    diagnosis_link: str | None = None
    hypothesis_link: str | None = None
    intention_link: str | None = None

    @property
    def entity_id(self) -> StrategyRationaleId:
        return self.rationale_id

    def _validate(self) -> None:
        if not isinstance(self.rationale_id, StrategyRationaleId):
            raise EducationalInvariantViolation(
                "rationale_id must be a StrategyRationaleId",
                invariant="StrategyRationale.rationale_id.type",
            )
        object.__setattr__(
            self,
            "statement",
            require_non_empty_text(self.statement, "statement"),
        )
        if len(self.statement) < 12:
            raise EducationalInvariantViolation(
                "strategy rationale must be educationally substantive",
                invariant="StrategyRationale.statement.substantive",
            )
        for field_name, value in (
            ("diagnosis_link", self.diagnosis_link),
            ("hypothesis_link", self.hypothesis_link),
            ("intention_link", self.intention_link),
        ):
            if value is not None:
                object.__setattr__(
                    self,
                    field_name,
                    require_non_empty_text(value, field_name),
                )
        self._assert_no_mastery_claim(self.statement)

    @staticmethod
    def _assert_no_mastery_claim(text: str) -> None:
        lowered = text.casefold()
        forbidden = ("mastered", "achieve mastery", "declare mastery", "full mastery")
        for token in forbidden:
            if token in lowered:
                raise EducationalInvariantViolation(
                    "strategy rationale must never claim mastery",
                    invariant="StrategyRationale.no_mastery_claim",
                )

    def with_statement(self, statement: str) -> StrategyRationale:
        return StrategyRationale(
            rationale_id=self.rationale_id,
            statement=statement,
            diagnosis_link=self.diagnosis_link,
            hypothesis_link=self.hypothesis_link,
            intention_link=self.intention_link,
        )
