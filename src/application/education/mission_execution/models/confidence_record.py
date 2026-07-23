"""ConfidenceRecord — one self-reported confidence observation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.education.mission_execution.errors import (
    MissionExecutionInvariantViolation,
)
from domain.education.foundation.enums import ConfidenceLevel


@dataclass(frozen=True, slots=True)
class ConfidenceRecord:
    """Immutable confidence observation recorded during mission execution.

    Preserved in append-only history. Never estimates mastery.
    """

    level: ConfidenceLevel
    recorded_at: datetime
    step_id: str | None = None
    note: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.level, ConfidenceLevel):
            raise MissionExecutionInvariantViolation(
                "level must be a ConfidenceLevel",
                invariant="ConfidenceRecord.level.type",
            )
        if self.level is ConfidenceLevel.UNKNOWN:
            raise MissionExecutionInvariantViolation(
                "confidence level must not be UNKNOWN",
                invariant="ConfidenceRecord.level.known",
            )
        if not isinstance(self.recorded_at, datetime):
            raise MissionExecutionInvariantViolation(
                "recorded_at must be a datetime",
                invariant="ConfidenceRecord.recorded_at.type",
            )
        step_id = (self.step_id or "").strip() or None
        object.__setattr__(self, "step_id", step_id)
        note = (self.note or "").strip() or None
        object.__setattr__(self, "note", note)
