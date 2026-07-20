"""Application events for learning session / episode coordination."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.events.base import ApplicationEvent, utc_now


@dataclass(frozen=True, slots=True)
class LearningSessionStartedApplicationEvent(ApplicationEvent):
    """Emitted after a learning episode session has been started."""

    episode_id: str
    student_id: str

    @classmethod
    def create(
        cls,
        *,
        episode_id: str,
        student_id: str,
        occurred_at: datetime | None = None,
    ) -> LearningSessionStartedApplicationEvent:
        return cls(
            occurred_at=occurred_at or utc_now(),
            episode_id=episode_id,
            student_id=student_id,
        )


@dataclass(frozen=True, slots=True)
class LearningEpisodeCompletedApplicationEvent(ApplicationEvent):
    """Emitted after a learning episode has been completed."""

    episode_id: str
    student_id: str
    outcome_kind: str

    @classmethod
    def create(
        cls,
        *,
        episode_id: str,
        student_id: str,
        outcome_kind: str,
        occurred_at: datetime | None = None,
    ) -> LearningEpisodeCompletedApplicationEvent:
        return cls(
            occurred_at=occurred_at or utc_now(),
            episode_id=episode_id,
            student_id=student_id,
            outcome_kind=outcome_kind,
        )
