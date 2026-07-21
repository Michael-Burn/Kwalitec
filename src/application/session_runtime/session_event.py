"""Immutable lifecycle events for the Study Session Runtime.

Events are append-only facts. Replaying the event log rebuilds ``SessionState``
deterministically. Events never carry educational judgements.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class SessionEventKind(StrEnum):
    """Named lifecycle event kinds."""

    STARTED = "started"
    ADVANCED = "advanced"
    PAUSED = "paused"
    RESUMED = "resumed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class SessionEvent:
    """One immutable lifecycle fact in the session event log.

    Attributes:
        kind: Event kind.
        sequence: 1-based position in the session event log.
        from_stage: Stage before the event was applied.
        to_stage: Stage after the event was applied.
        paused_after: Pause flag after the event was applied.
        cancelled_after: Cancelled flag after the event was applied.
    """

    kind: SessionEventKind
    sequence: int
    from_stage: str
    to_stage: str
    paused_after: bool = False
    cancelled_after: bool = False

    def __post_init__(self) -> None:
        if self.sequence < 1:
            raise ValueError("sequence must be >= 1")
        if not self.kind:
            raise ValueError("kind is required")
        if not self.from_stage:
            raise ValueError("from_stage is required")
        if not self.to_stage:
            raise ValueError("to_stage is required")
