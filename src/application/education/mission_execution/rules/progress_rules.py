"""Progress derivation rules — completed steps only."""

from __future__ import annotations

from application.education.mission_execution.enums import StepOutcome
from application.education.mission_execution.models.execution_progress import (
    ExecutionProgress,
)
from application.education.mission_generation.ids import MissionStepId
from application.education.mission_generation.models.mission import Mission


class ProgressRules:
    """Build ExecutionProgress from completed / skipped step identities."""

    @staticmethod
    def build_progress(
        *,
        mission: Mission,
        completed_step_ids: tuple[MissionStepId, ...],
        skipped_step_ids: tuple[MissionStepId, ...],
        current_step_id: MissionStepId | None,
    ) -> ExecutionProgress:
        completed_set = set(completed_step_ids)
        skipped_set = set(skipped_step_ids)
        outcomes: list[tuple[MissionStepId, StepOutcome]] = []
        for step in mission.steps:
            if step.step_id in completed_set:
                outcomes.append((step.step_id, StepOutcome.COMPLETED))
            elif step.step_id in skipped_set:
                outcomes.append((step.step_id, StepOutcome.SKIPPED))
            else:
                outcomes.append((step.step_id, StepOutcome.PENDING))
        return ExecutionProgress(
            total_steps=len(mission.steps),
            completed_step_ids=completed_step_ids,
            skipped_step_ids=skipped_step_ids,
            current_step_id=current_step_id,
            step_outcomes=tuple(outcomes),
        )

    @staticmethod
    def next_current_step(
        *,
        mission: Mission,
        completed_step_ids: tuple[MissionStepId, ...],
        skipped_step_ids: tuple[MissionStepId, ...],
    ) -> MissionStepId | None:
        """First unresolved step in mission order, or None when fully resolved."""
        resolved = set(completed_step_ids) | set(skipped_step_ids)
        for step in mission.steps:
            if step.step_id not in resolved:
                return step.step_id
        return None
