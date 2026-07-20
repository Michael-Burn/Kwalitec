"""Specification: an orchestration stage is executable now.

Architecture Source
    EDUCATIONAL_ORCHESTRATION_MODEL.md
Concept
    StageIsExecutableSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.orchestrator.enums import OrchestrationStatus, StageStatus
from domain.education.orchestrator.policies.sequencing_policy import (
    SequencingPolicy,
)

if TYPE_CHECKING:
    from domain.education.orchestrator.aggregates.educational_orchestrator import (
        EducationalOrchestrator,
    )
    from domain.education.orchestrator.entities.orchestration_stage import (
        OrchestrationStage,
    )


class StageIsExecutableSpecification:
    """True when a stage is the lawful next coordination act.

    Executability means the orchestrator is ACTIVE, the stage is ACTIVE or
    the next PENDING stage in sequence, and prior required stages are done.
    It does not interpret evidence or select strategies.
    """

    def is_satisfied_by(
        self,
        orchestrator: EducationalOrchestrator,
        stage: OrchestrationStage | None = None,
    ) -> bool:
        if orchestrator.state.status is not OrchestrationStatus.ACTIVE:
            return False
        try:
            next_stage = SequencingPolicy.assert_can_advance(orchestrator.stages)
        except EducationalInvariantViolation:
            return False
        if stage is None:
            return next_stage.status in {StageStatus.ACTIVE, StageStatus.PENDING}
        if stage.stage_id != next_stage.stage_id:
            return False
        return stage.status in {StageStatus.ACTIVE, StageStatus.PENDING}

    def assert_satisfied_by(
        self,
        orchestrator: EducationalOrchestrator,
        stage: OrchestrationStage | None = None,
    ) -> None:
        if not self.is_satisfied_by(orchestrator, stage):
            raise EducationalInvariantViolation(
                "orchestration stage is not executable",
                invariant="StageIsExecutableSpecification.unsatisfied",
            )
