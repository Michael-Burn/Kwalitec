"""Expected educational outcome — evaluable success profile for an intention.

Architecture Source
    TEACHING_INTENTION_MODEL.md
Concept
    Expected Educational Outcome / Success Evidence
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class ExpectedOutcome(EducationalValueObject):
    """Immutable expected educational outcome for a teaching intention.

    Outcomes must be evidentially evaluable in principle. They never claim
    mastery as an episode result and never prescribe teaching strategy.
    """

    statement: str
    success_evidence: str
    evaluable: bool = True

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "statement",
            require_non_empty_text(self.statement, "statement"),
        )
        object.__setattr__(
            self,
            "success_evidence",
            require_non_empty_text(self.success_evidence, "success_evidence"),
        )
        if not isinstance(self.evaluable, bool):
            raise EducationalInvariantViolation(
                "evaluable must be a boolean",
                invariant="ExpectedOutcome.evaluable.type",
            )
        if not self.evaluable:
            raise EducationalInvariantViolation(
                "expected outcome must be evidentially evaluable",
                invariant="ExpectedOutcome.evaluable.required",
            )
        self._assert_no_mastery_claim(self.statement)
        self._assert_no_mastery_claim(self.success_evidence)
        self._assert_no_strategy_language(self.statement)

    @staticmethod
    def _assert_no_mastery_claim(text: str) -> None:
        lowered = text.casefold()
        forbidden = ("mastered", "achieve mastery", "declare mastery", "full mastery")
        for token in forbidden:
            if token in lowered:
                raise EducationalInvariantViolation(
                    "expected outcome must never claim mastery as episode outcome",
                    invariant="ExpectedOutcome.no_mastery_claim",
                )

    @staticmethod
    def _assert_no_strategy_language(text: str) -> None:
        lowered = text.casefold()
        forbidden = (
            "use interleaved practice",
            "apply spaced retrieval",
            "select teaching strategy",
            "choose strategy",
        )
        for token in forbidden:
            if token in lowered:
                raise EducationalInvariantViolation(
                    "expected outcome must not select teaching strategy",
                    invariant="ExpectedOutcome.no_strategy",
                )

    @classmethod
    def of(
        cls,
        statement: str,
        success_evidence: str,
        *,
        evaluable: bool = True,
    ) -> ExpectedOutcome:
        return cls(
            statement=statement,
            success_evidence=success_evidence,
            evaluable=evaluable,
        )

    def with_statement(self, statement: str) -> ExpectedOutcome:
        return ExpectedOutcome(
            statement=statement,
            success_evidence=self.success_evidence,
            evaluable=self.evaluable,
        )

    def with_success_evidence(self, success_evidence: str) -> ExpectedOutcome:
        return ExpectedOutcome(
            statement=self.statement,
            success_evidence=success_evidence,
            evaluable=self.evaluable,
        )

    def __str__(self) -> str:
        return self.statement
