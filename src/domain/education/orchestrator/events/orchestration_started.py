"""Domain event: educational orchestration started.

Architecture Source
    EDUCATIONAL_ORCHESTRATION_MODEL.md
Concept
    OrchestrationStarted
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DecisionId, OrchestratorId
from domain.education.orchestrator.entities.orchestration_stage import (
    OrchestrationStageId,
)


@dataclass(frozen=True, slots=True)
class OrchestrationStarted(EducationalValueObject):
    """Immutable record that orchestration coordination began."""

    orchestrator_id: OrchestratorId
    student_id: str
    decision_id: DecisionId
    first_stage_id: OrchestrationStageId
    stage_count: int

    def _validate(self) -> None:
        if not isinstance(self.orchestrator_id, OrchestratorId):
            raise EducationalInvariantViolation(
                "orchestrator_id must be an OrchestratorId",
                invariant="OrchestrationStarted.orchestrator_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_identity_value(self.student_id, "student_id"),
        )
        if not isinstance(self.decision_id, DecisionId):
            raise EducationalInvariantViolation(
                "decision_id must be a DecisionId",
                invariant="OrchestrationStarted.decision_id.type",
            )
        if not isinstance(self.first_stage_id, OrchestrationStageId):
            raise EducationalInvariantViolation(
                "first_stage_id must be an OrchestrationStageId",
                invariant="OrchestrationStarted.first_stage_id.type",
            )
        if not isinstance(self.stage_count, int) or self.stage_count < 1:
            raise EducationalInvariantViolation(
                "stage_count must be a positive integer",
                invariant="OrchestrationStarted.stage_count.positive",
            )
