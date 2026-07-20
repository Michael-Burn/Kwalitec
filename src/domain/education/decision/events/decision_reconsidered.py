"""Domain event: educational execution decision was reconsidered.

Architecture Source
    EDUCATIONAL_DECISION_POINTS.md
Concept
    DecisionReconsidered
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.decision.enums import DecisionOutcome, DecisionStatus
from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DecisionId


@dataclass(frozen=True, slots=True)
class DecisionReconsidered(EducationalValueObject):
    """Immutable record that a committed EducationalDecision was reopened."""

    decision_id: DecisionId
    student_id: str
    previous_outcome: DecisionOutcome
    previous_status: DecisionStatus
    reason: str

    def _validate(self) -> None:
        if not isinstance(self.decision_id, DecisionId):
            raise EducationalInvariantViolation(
                "decision_id must be a DecisionId",
                invariant="DecisionReconsidered.decision_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_identity_value(self.student_id, "student_id"),
        )
        if not isinstance(self.previous_outcome, DecisionOutcome):
            raise EducationalInvariantViolation(
                "previous_outcome must be a DecisionOutcome",
                invariant="DecisionReconsidered.previous_outcome.type",
            )
        if not isinstance(self.previous_status, DecisionStatus):
            raise EducationalInvariantViolation(
                "previous_status must be a DecisionStatus",
                invariant="DecisionReconsidered.previous_status.type",
            )
        object.__setattr__(
            self,
            "reason",
            require_non_empty_text(self.reason, "reason"),
        )
