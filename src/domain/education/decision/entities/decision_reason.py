"""Decision reason — explanatory warrant for an execution decision.

Architecture Source
    EDUCATIONAL_DECISION_POINTS.md
Concept
    Decision Reason
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
class DecisionReasonId(EducationalValueObject):
    """Identity of a decision reason within an EducationalDecision."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "DecisionReasonId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class DecisionReason(EducationalEntity):
    """Single explanatory reason supporting an educational execution decision.

    Reasons cite *why this readiness outcome fits*. They must not invent
    diagnoses, create strategies, or orchestrate sessions.
    """

    reason_id: DecisionReasonId
    statement: str
    code: str | None = None

    @property
    def entity_id(self) -> DecisionReasonId:
        return self.reason_id

    def _validate(self) -> None:
        if not isinstance(self.reason_id, DecisionReasonId):
            raise EducationalInvariantViolation(
                "reason_id must be a DecisionReasonId",
                invariant="DecisionReason.reason_id.type",
            )
        object.__setattr__(
            self,
            "statement",
            require_non_empty_text(self.statement, "statement"),
        )
        if self.code is not None:
            object.__setattr__(
                self,
                "code",
                require_identity_value(self.code, "code"),
            )
        self._reject_smuggling(self.statement)

    @staticmethod
    def _reject_smuggling(statement: str) -> None:
        """Refuse reasons that encode diagnosis or strategy creation."""
        lowered = statement.casefold()
        forbidden_fragments = (
            "therefore diagnose",
            "diagnosis is",
            "create strategy",
            "select strategy",
            "invent strategy",
            "orchestrate session",
            "assemble session",
            "generate episode sequence",
        )
        for fragment in forbidden_fragments:
            if fragment in lowered:
                raise EducationalInvariantViolation(
                    "decision reason must not encode diagnosis, strategy "
                    "creation, or session orchestration",
                    invariant="DecisionReason.no_smuggling",
                )

    def reason_signature(self) -> tuple[str, str | None]:
        """Structural fingerprint used to prevent duplicate reasons."""
        return (self.statement.casefold(), self.code)

    def with_statement(self, statement: str) -> DecisionReason:
        """Return a copy with an amended reason statement."""
        return DecisionReason(
            reason_id=self.reason_id,
            statement=statement,
            code=self.code,
        )
