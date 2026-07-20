"""Today'sMissionReadModel — presentation projection of today's session work."""

from __future__ import annotations

from dataclasses import dataclass

from application.read_models.missions.mission_task_read_model import (
    MissionTaskReadModel,
)


@dataclass(frozen=True, slots=True)
class TodaysMissionReadModel:
    """UI-ready today's mission card. Never carries domain aggregates."""

    title: str
    summary: str | None
    task_count: int
    tasks: tuple[MissionTaskReadModel, ...]
    estimated_minutes: int | None
    can_open: bool
    mission_id: str | None = None
    episode_id: str | None = None
    status: str | None = None
