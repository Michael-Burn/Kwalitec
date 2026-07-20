"""Domain event: educational orchestration completed.

Architecture Source
    EDUCATIONAL_ORCHESTRATION_MODEL.md
Concept
    OrchestrationCompleted
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DecisionId, OrchestratorId


@dataclass(frozen=True, slots=True)
class OrchestrationCompleted(EducationalValueObject):
    """Immutable record that orchestration terminated correctly."""

    orchestrator_id: OrchestratorId
    student_id: str
    decision_id: DecisionId
    completed_stages: int
    evidence_collection_points_reached: int
    episode_count: int

    def _validate(self) -> None:
        if not isinstance(self.orchestrator_id, OrchestratorId):
            raise EducationalInvariantViolation(
                "orchestrator_id must be an OrchestratorId",
                invariant="OrchestrationCompleted.orchestrator_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_identity_value(self.student_id, "student_id"),
        )
        if not isinstance(self.decision_id, DecisionId):
            raise EducationalInvariantViolation(
                "decision_id must be a DecisionId",
                invariant="OrchestrationCompleted.decision_id.type",
            )
        if not isinstance(self.completed_stages, int) or self.completed_stages < 1:
            raise EducationalInvariantViolation(
                "completed_stages must be a positive integer",
                invariant="OrchestrationCompleted.completed_stages.positive",
            )
        if (
            not isinstance(self.evidence_collection_points_reached, int)
            or self.evidence_collection_points_reached < 0
        ):
            raise EducationalInvariantViolation(
                "evidence_collection_points_reached must be non-negative",
                invariant="OrchestrationCompleted.evidence_points.non_negative",
            )
        if not isinstance(self.episode_count, int) or self.episode_count < 0:
            raise EducationalInvariantViolation(
                "episode_count must be a non-negative integer",
                invariant="OrchestrationCompleted.episode_count.non_negative",
            )
