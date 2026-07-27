"""Learner goals — educational targets owned by the Twin."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime
from enum import StrEnum


class GoalStatus(StrEnum):
    ACTIVE = "active"
    COMPLETED = "completed"
    DEFERRED = "deferred"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class Goal:
    """An educational goal attached to a Twin (exam sitting, topic coverage)."""

    goal_id: str
    twin_id: str
    title: str
    status: GoalStatus = GoalStatus.ACTIVE
    target_date: date | None = None
    curriculum_entity_id: str = ""
    priority: int = 0
    created_at: datetime | None = None

    def __post_init__(self) -> None:
        if not (self.goal_id or "").strip():
            raise ValueError("goal_id is required")
        status = (
            self.status
            if isinstance(self.status, GoalStatus)
            else GoalStatus(str(self.status))
        )
        object.__setattr__(self, "status", status)
        when = self.created_at
        if when is not None and when.tzinfo is not None:
            object.__setattr__(
                self, "created_at", when.astimezone(UTC).replace(tzinfo=None)
            )
