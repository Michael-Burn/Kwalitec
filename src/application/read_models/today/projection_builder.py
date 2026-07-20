"""TodaysMissionProjectionBuilder — assemble today's mission read model.

Places already-authored mission / session presentation data. Does not select
actions, invent filler tasks, or modify aggregates.
"""

from __future__ import annotations

from application.dto.learning import LearningSessionDTO
from application.dto.teaching_plan import TeachingPlanDTO
from application.read_models.missions.mission_task_read_model import (
    MissionTaskReadModel,
)
from application.read_models.missions.projection_builder import MissionProjectionBuilder
from application.read_models.today.todays_mission_read_model import (
    TodaysMissionReadModel,
)


class TodaysMissionProjectionBuilder:
    """Build ``TodaysMissionReadModel`` from application DTOs and display fields."""

    @staticmethod
    def build(
        *,
        title: str,
        tasks: tuple[MissionTaskReadModel, ...] = (),
        summary: str | None = None,
        estimated_minutes: int | None = None,
        can_open: bool | None = None,
        mission_id: str | None = None,
        episode_id: str | None = None,
        status: str | None = None,
    ) -> TodaysMissionReadModel:
        """Project today's mission presentation fields into an immutable read model."""
        task_count = len(tasks)
        if summary is None:
            resolved_summary = _default_summary(task_count)
        else:
            resolved_summary = summary
        openable = can_open if can_open is not None else task_count > 0
        return TodaysMissionReadModel(
            title=title.strip(),
            summary=_optional_text(resolved_summary),
            task_count=task_count,
            tasks=tasks,
            estimated_minutes=estimated_minutes,
            can_open=openable,
            mission_id=_optional_text(mission_id),
            episode_id=_optional_text(episode_id),
            status=_optional_text(status),
        )

    @staticmethod
    def from_teaching_plan(
        plan: TeachingPlanDTO,
        *,
        title: str = "Today's Session",
        estimated_minutes: int | None = None,
        mission_id: str | None = None,
    ) -> TodaysMissionReadModel:
        """Project a teaching-plan DTO into today's mission read model."""
        tasks = MissionProjectionBuilder.build_tasks(plan)
        return TodaysMissionProjectionBuilder.build(
            title=title,
            tasks=tasks,
            estimated_minutes=estimated_minutes,
            mission_id=mission_id,
            episode_id=plan.episode_id,
            status=plan.status,
        )

    @staticmethod
    def from_learning_session(
        session: LearningSessionDTO,
        *,
        title: str = "Today's Session",
        tasks: tuple[MissionTaskReadModel, ...] = (),
        estimated_minutes: int | None = None,
        mission_id: str | None = None,
    ) -> TodaysMissionReadModel:
        """Project a learning-session DTO into today's mission read model."""
        return TodaysMissionProjectionBuilder.build(
            title=title,
            tasks=tasks,
            estimated_minutes=estimated_minutes,
            can_open=True,
            mission_id=mission_id,
            episode_id=session.episode_id,
            status=session.status,
        )


def _default_summary(task_count: int) -> str:
    if task_count == 0:
        return "No tasks in this session"
    if task_count == 1:
        return "1 task"
    return f"{task_count} tasks"


def _optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None
