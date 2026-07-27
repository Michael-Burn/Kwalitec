"""Mission completion record."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True)
class MissionCompletion:
    """Immutable completion event for an adaptive mission."""

    completion_id: str
    mission_id: str
    twin_id: str
    completed_at: datetime
    steps_completed: int
    steps_total: int
    outcome_achieved: bool
    reflection_response: str = ""
    feedback_summary: str = ""

    def __post_init__(self) -> None:
        if not (self.completion_id or "").strip():
            raise ValueError("completion_id is required")
        if not (self.mission_id or "").strip():
            raise ValueError("mission_id is required")
        when = self.completed_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "completed_at", when.astimezone(UTC).replace(tzinfo=None)
            )
