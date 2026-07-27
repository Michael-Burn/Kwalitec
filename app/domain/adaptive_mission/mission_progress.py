"""Progress tracking for an adaptive mission."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True)
class MissionProgress:
    """Progress snapshot for one adaptive mission."""

    progress_id: str
    mission_id: str
    steps_total: int = 0
    steps_completed: int = 0
    percent_complete: float = 0.0
    last_step_id: str = ""
    updated_at: datetime | None = None
    note: str = ""

    def __post_init__(self) -> None:
        if not (self.progress_id or "").strip():
            raise ValueError("progress_id is required")
        if not (self.mission_id or "").strip():
            raise ValueError("mission_id is required")
        total = max(0, int(self.steps_total))
        done = max(
            0,
            min(
                int(self.steps_completed),
                total if total else int(self.steps_completed),
            ),
        )
        percent = (done / total * 100.0) if total else float(self.percent_complete)
        object.__setattr__(self, "steps_total", total)
        object.__setattr__(self, "steps_completed", done)
        object.__setattr__(self, "percent_complete", max(0.0, min(100.0, percent)))
        when = self.updated_at
        if when is not None and when.tzinfo is not None:
            object.__setattr__(
                self, "updated_at", when.astimezone(UTC).replace(tzinfo=None)
            )

    @classmethod
    def empty(cls, *, mission_id: str, progress_id: str) -> MissionProgress:
        return cls(
            progress_id=progress_id,
            mission_id=mission_id,
            steps_total=0,
            steps_completed=0,
            percent_complete=0.0,
        )

    @classmethod
    def from_steps(
        cls,
        *,
        progress_id: str,
        mission_id: str,
        steps_total: int,
        steps_completed: int,
        last_step_id: str = "",
        updated_at: datetime | None = None,
        note: str = "",
    ) -> MissionProgress:
        return cls(
            progress_id=progress_id,
            mission_id=mission_id,
            steps_total=steps_total,
            steps_completed=steps_completed,
            last_step_id=last_step_id,
            updated_at=updated_at,
            note=note,
        )
