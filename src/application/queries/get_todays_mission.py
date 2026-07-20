"""GetTodaysMission query — today's mission presentation section."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetTodaysMission:
    """Request today's mission read model for a student episode."""

    student_id: str
    episode_id: str
