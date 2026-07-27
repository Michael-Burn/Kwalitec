"""Mission identity and lifecycle status."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import StrEnum


class MissionStatus(StrEnum):
    """Lifecycle status for an adaptive mission."""

    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    SUPERSEDED = "superseded"
    REJECTED = "rejected"


@dataclass(frozen=True)
class Mission:
    """Identity envelope for one adaptive daily mission."""

    mission_id: str
    twin_id: str
    student_id: str
    mission_date: date
    status: MissionStatus = MissionStatus.DRAFT
    goal: str = ""

    def __post_init__(self) -> None:
        if not (self.mission_id or "").strip():
            raise ValueError("mission_id is required")
        if not (self.twin_id or "").strip():
            raise ValueError("twin_id is required")
        if not (self.student_id or "").strip():
            raise ValueError("student_id is required")
        status = (
            self.status
            if isinstance(self.status, MissionStatus)
            else MissionStatus(str(self.status))
        )
        object.__setattr__(self, "status", status)
