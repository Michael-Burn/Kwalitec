"""Immutable progress DTO for Learning Session Experience."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ProgressSnapshot:
    """Session progress projection DTO."""

    session_id: str
    activities_completed: int = 0
    activities_remaining: int = 0
    activities_total: int = 0
    estimated_remaining_minutes: int | None = None
    current_topic: str = ""
    overall_progress: float = 0.0
    progress_percent: int = 0
    is_complete: bool = False
    has_started: bool = False
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)
