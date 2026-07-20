"""Mission task line-item for today's mission presentation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MissionTaskReadModel:
    """One executable task headline for the mission card. Display only."""

    task_id: str
    headline: str
    sequence_index: int
    status: str
