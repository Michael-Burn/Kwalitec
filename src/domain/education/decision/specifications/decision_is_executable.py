"""Specification: EducationalDecision is executable (approved to teach).

Architecture Source
    EDUCATIONAL_DECISION_POINTS.md
Concept
    DecisionIsExecutableSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.decision.enums import DecisionOutcome, DecisionStatus
from domain.education.decision.specifications.intervention_is_ready import (
    InterventionIsReadySpecification,
)
from domain.education.foundation.errors import EducationalInvariantViolation

if TYPE_CHECKING:
    from domain.education.decision.aggregates.educational_decision import (
        EducationalDecision,
    )


class DecisionIsExecutableSpecification:
    """True when a decision commits TEACH_NOW and remains structurally ready.

    Executability means APPROVED with TEACH_NOW outcome and readiness still
    supporting approval. It does **not** orchestrate sessions or invent
    strategies.
    """

    def __init__(self) -> None:
        self._ready = InterventionIsReadySpecification()

    def is_satisfied_by(self, decision: EducationalDecision) -> bool:
        if decision.status is not DecisionStatus.APPROVED:
            return False
        if decision.outcome is not DecisionOutcome.TEACH_NOW:
            return False
        return self._ready.is_satisfied_by(decision)

    def assert_satisfied_by(self, decision: EducationalDecision) -> None:
        if not self.is_satisfied_by(decision):
            raise EducationalInvariantViolation(
                "decision is not executable",
                invariant="DecisionIsExecutableSpecification.unsatisfied",
            )
