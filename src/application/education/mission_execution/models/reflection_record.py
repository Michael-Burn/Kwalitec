"""ReflectionRecord — one student reflection during execution."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.education.mission_execution.errors import (
    MissionExecutionInvariantViolation,
)


@dataclass(frozen=True, slots=True)
class ReflectionRecord:
    """Immutable reflection observation recorded during mission execution.

    History is append-only. Never estimates mastery.
    """

    text: str
    recorded_at: datetime
    step_id: str | None = None

    def __post_init__(self) -> None:
        text = (self.text or "").strip()
        if not text:
            raise MissionExecutionInvariantViolation(
                "reflection text must be non-empty",
                invariant="ReflectionRecord.text.required",
            )
        object.__setattr__(self, "text", text)
        if not isinstance(self.recorded_at, datetime):
            raise MissionExecutionInvariantViolation(
                "recorded_at must be a datetime",
                invariant="ReflectionRecord.recorded_at.type",
            )
        step_id = (self.step_id or "").strip() or None
        object.__setattr__(self, "step_id", step_id)
