"""Session progress — projection of how much remains in the study flow.

Assembles presentation facts from upstream runtime / activity ports.
Never calculates educational progress independently of those ports.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SessionProgress:
    """Domain projection for in-session progress indicators.

    Display only. Educational completion law stays in Session Runtime /
    Activity Engine.
    """

    session_id: str
    activities_completed: int = 0
    activities_remaining: int = 0
    activities_total: int = 0
    estimated_remaining_minutes: int | None = None
    current_topic: str = ""
    overall_progress: float = 0.0
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        session_id: str,
        *,
        activities_completed: int = 0,
        activities_remaining: int = 0,
        activities_total: int | None = None,
        estimated_remaining_minutes: int | None = None,
        current_topic: str = "",
        overall_progress: float | None = None,
        metadata: list[tuple[str, str]] | tuple[tuple[str, str], ...] | None = None,
    ) -> SessionProgress:
        """Build a session progress projection from port facts."""
        sid = _require_non_empty(session_id, "session_id")
        completed = _non_negative_int(activities_completed, "activities_completed")
        remaining = _non_negative_int(activities_remaining, "activities_remaining")
        if activities_total is None:
            total = completed + remaining
        else:
            total = _non_negative_int(activities_total, "activities_total")
        if estimated_remaining_minutes is not None and estimated_remaining_minutes < 0:
            raise ValueError("estimated_remaining_minutes must be non-negative")
        if overall_progress is None:
            ratio = (completed / total) if total > 0 else 0.0
        else:
            ratio = float(overall_progress)
        if not 0.0 <= ratio <= 1.0:
            raise ValueError("overall_progress must be between 0 and 1")
        return cls(
            session_id=sid,
            activities_completed=completed,
            activities_remaining=remaining,
            activities_total=total,
            estimated_remaining_minutes=estimated_remaining_minutes,
            current_topic=(current_topic or "").strip(),
            overall_progress=ratio,
            metadata=tuple(metadata or ()),
        )

    @property
    def progress_percent(self) -> int:
        """Rounded progress percentage for display."""
        return int(round(self.overall_progress * 100))

    @property
    def is_complete(self) -> bool:
        """True when no activities remain (presentation signal only)."""
        return self.activities_remaining == 0 and self.activities_total > 0

    @property
    def has_started(self) -> bool:
        """True when at least one activity has been completed."""
        return self.activities_completed > 0


def _non_negative_int(value: int, field_name: str) -> int:
    ivalue = int(value)
    if ivalue < 0:
        raise ValueError(f"{field_name} must be non-negative")
    return ivalue


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
