"""Domain event: educational orchestration paused.

Architecture Source
    EDUCATIONAL_ORCHESTRATION_MODEL.md
Concept
    OrchestrationPaused
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import OrchestratorId
from domain.education.orchestrator.entities.orchestration_stage import (
    OrchestrationStageId,
)


@dataclass(frozen=True, slots=True)
class OrchestrationPaused(EducationalValueObject):
    """Immutable record that orchestration coordination was suspended."""

    orchestrator_id: OrchestratorId
    student_id: str
    reason: str
    current_stage_id: OrchestrationStageId | None
    completed_stages: int

    def _validate(self) -> None:
        if not isinstance(self.orchestrator_id, OrchestratorId):
            raise EducationalInvariantViolation(
                "orchestrator_id must be an OrchestratorId",
                invariant="OrchestrationPaused.orchestrator_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_identity_value(self.student_id, "student_id"),
        )
        object.__setattr__(
            self,
            "reason",
            require_non_empty_text(self.reason, "reason"),
        )
        if self.current_stage_id is not None and not isinstance(
            self.current_stage_id, OrchestrationStageId
        ):
            raise EducationalInvariantViolation(
                "current_stage_id must be an OrchestrationStageId when provided",
                invariant="OrchestrationPaused.current_stage_id.type",
            )
        if not isinstance(self.completed_stages, int) or self.completed_stages < 0:
            raise EducationalInvariantViolation(
                "completed_stages must be a non-negative integer",
                invariant="OrchestrationPaused.completed_stages.non_negative",
            )
