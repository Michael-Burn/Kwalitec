"""Abstract time allocation for a mission (no calendar scheduling)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MissionSchedule:
    """Time budget for today's mission.

    AME-001 allocates estimated minutes only — it does not schedule clock times.
    """

    total_minutes: int
    focus_block_minutes: int
    reflection_minutes: int = 5
    allocation_note: str = ""

    def __post_init__(self) -> None:
        total = max(1, int(self.total_minutes))
        focus = max(1, min(int(self.focus_block_minutes), total))
        reflection = max(0, min(int(self.reflection_minutes), total))
        object.__setattr__(self, "total_minutes", total)
        object.__setattr__(self, "focus_block_minutes", focus)
        object.__setattr__(self, "reflection_minutes", reflection)
