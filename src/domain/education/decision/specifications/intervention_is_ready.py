"""Specification: planned intervention is ready for execution approval.

Architecture Source
    EDUCATIONAL_DECISION_POINTS.md
Concept
    InterventionIsReadySpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.decision.enums import DecisionStatus, ReadinessBand
from domain.education.decision.policies.decision_policy import DecisionPolicy
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation

if TYPE_CHECKING:
    from domain.education.decision.aggregates.educational_decision import (
        EducationalDecision,
    )


class InterventionIsReadySpecification:
    """True when readiness posture lawfully supports teaching now.

    Readiness means READY band, non-VERY_LOW confidence, required references
    present, and no constraint contradiction for approval. It does **not**
    mean a session has been assembled or a diagnosis created.
    """

    def is_satisfied_by(self, decision: EducationalDecision) -> bool:
        if decision.status not in {
            DecisionStatus.PENDING,
            DecisionStatus.RECONSIDERED,
            DecisionStatus.APPROVED,
        }:
            return False
        if decision.readiness.band is not ReadinessBand.READY:
            return False
        if decision.confidence.level is ConfidenceLevel.VERY_LOW:
            return False
        if not decision.priority_references:
            return False
        if not decision.intention_references:
            return False
        if not decision.strategy_references:
            return False
        if not decision.indicators:
            return False
        try:
            DecisionPolicy.assert_approval_lawful(
                readiness=decision.readiness,
                confidence=decision.confidence,
                indicators=decision.indicators,
                constraints=decision.constraints,
            )
        except EducationalInvariantViolation:
            return False
        return True

    def assert_satisfied_by(self, decision: EducationalDecision) -> None:
        if not self.is_satisfied_by(decision):
            raise EducationalInvariantViolation(
                "intervention is not ready for execution approval",
                invariant="InterventionIsReadySpecification.unsatisfied",
            )
