"""Domain event: educational execution decision was made.

Architecture Source
    EDUCATIONAL_DECISION_POINTS.md
Concept
    DecisionMade
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.decision.enums import DecisionOutcome, DecisionStatus
from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DecisionId


@dataclass(frozen=True, slots=True)
class DecisionMade(EducationalValueObject):
    """Immutable record that an EducationalDecision commitment was made."""

    decision_id: DecisionId
    student_id: str
    outcome: DecisionOutcome
    status: DecisionStatus
    readiness_band: str
    confidence_level: ConfidenceLevel
    indicator_count: int
    constraint_count: int
    reason_count: int

    def _validate(self) -> None:
        if not isinstance(self.decision_id, DecisionId):
            raise EducationalInvariantViolation(
                "decision_id must be a DecisionId",
                invariant="DecisionMade.decision_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_identity_value(self.student_id, "student_id"),
        )
        if not isinstance(self.outcome, DecisionOutcome):
            raise EducationalInvariantViolation(
                "outcome must be a DecisionOutcome",
                invariant="DecisionMade.outcome.type",
            )
        if not isinstance(self.status, DecisionStatus):
            raise EducationalInvariantViolation(
                "status must be a DecisionStatus",
                invariant="DecisionMade.status.type",
            )
        object.__setattr__(
            self,
            "readiness_band",
            require_identity_value(self.readiness_band, "readiness_band"),
        )
        if not isinstance(self.confidence_level, ConfidenceLevel):
            raise EducationalInvariantViolation(
                "confidence_level must be a ConfidenceLevel",
                invariant="DecisionMade.confidence_level.type",
            )
        if self.confidence_level is ConfidenceLevel.UNKNOWN:
            raise EducationalInvariantViolation(
                "confidence_level must not be UNKNOWN",
                invariant="DecisionMade.confidence_level.known",
            )
        if not isinstance(self.indicator_count, int) or self.indicator_count < 1:
            raise EducationalInvariantViolation(
                "indicator_count must be a positive integer",
                invariant="DecisionMade.indicator_count.positive",
            )
        if not isinstance(self.constraint_count, int) or self.constraint_count < 0:
            raise EducationalInvariantViolation(
                "constraint_count must be a non-negative integer",
                invariant="DecisionMade.constraint_count.non_negative",
            )
        if not isinstance(self.reason_count, int) or self.reason_count < 0:
            raise EducationalInvariantViolation(
                "reason_count must be a non-negative integer",
                invariant="DecisionMade.reason_count.non_negative",
            )
