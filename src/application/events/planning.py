"""Application events for teaching-plan coordination."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.events.base import ApplicationEvent, utc_now


@dataclass(frozen=True, slots=True)
class TeachingPlanGeneratedApplicationEvent(ApplicationEvent):
    """Emitted after a teaching plan has been generated and persisted."""

    plan_id: str
    episode_id: str
    student_id: str

    @classmethod
    def create(
        cls,
        *,
        plan_id: str,
        episode_id: str,
        student_id: str,
        occurred_at: datetime | None = None,
    ) -> TeachingPlanGeneratedApplicationEvent:
        return cls(
            occurred_at=occurred_at or utc_now(),
            plan_id=plan_id,
            episode_id=episode_id,
            student_id=student_id,
        )
