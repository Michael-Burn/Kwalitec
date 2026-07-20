"""Specification: EducationalOrchestrator plan and references are valid.

Architecture Source
    EDUCATIONAL_ORCHESTRATION_MODEL.md
    ORCHESTRATION_INVARIANTS.md
Concept
    OrchestrationIsValidSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.orchestrator.enums import OrchestrationStatus

if TYPE_CHECKING:
    from domain.education.orchestrator.aggregates.educational_orchestrator import (
        EducationalOrchestrator,
    )


class OrchestrationIsValidSpecification:
    """True when orchestration lawfully references an approved decision and plan.

    Validity is structural coordination fitness. It does not diagnose,
    interpret evidence, choose strategies, or change priorities.
    """

    def is_satisfied_by(self, orchestrator: EducationalOrchestrator) -> bool:
        if not orchestrator.decision_reference.approved:
            return False
        if orchestrator.plan.stage_count() < 1:
            return False
        if not orchestrator.strategy_references:
            return False
        if orchestrator.state.status not in {
            OrchestrationStatus.PLANNED,
            OrchestrationStatus.ACTIVE,
            OrchestrationStatus.PAUSED,
            OrchestrationStatus.COMPLETED,
        }:
            return False
        # Unique stage identities already enforced by plan; re-check indexes.
        indexes = [s.sequence_index for s in orchestrator.stages]
        if len(indexes) != len(set(indexes)):
            return False
        return True

    def assert_satisfied_by(self, orchestrator: EducationalOrchestrator) -> None:
        if not self.is_satisfied_by(orchestrator):
            raise EducationalInvariantViolation(
                "orchestration is not valid",
                invariant="OrchestrationIsValidSpecification.unsatisfied",
            )
