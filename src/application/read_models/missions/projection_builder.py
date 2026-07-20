"""MissionProjectionBuilder — project plan/session steps into task read models.

Structural mapping only. Does not compose missions, invent filler tasks, or
modify aggregates.
"""

from __future__ import annotations

from application.dto.teaching_plan import TeachingPlanDTO, TeachingPlanStepDTO
from application.read_models.missions.mission_task_read_model import (
    MissionTaskReadModel,
)


class MissionProjectionBuilder:
    """Build mission task read models from application teaching-plan DTOs."""

    @staticmethod
    def build_tasks(plan: TeachingPlanDTO) -> tuple[MissionTaskReadModel, ...]:
        """Project teaching-plan steps into ordered mission task read models."""
        return tuple(
            MissionProjectionBuilder.build_task(step) for step in plan.steps
        )

    @staticmethod
    def build_task(step: TeachingPlanStepDTO) -> MissionTaskReadModel:
        """Project one teaching-plan step into a mission task read model."""
        return MissionTaskReadModel(
            task_id=step.step_id,
            headline=step.label.strip() or step.kind,
            sequence_index=step.sequence_index,
            status=step.status,
        )
