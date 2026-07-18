"""Orchestration lifecycle posture (coordination only — not Twin state)."""

from __future__ import annotations

from enum import StrEnum


class OrchestrationState(StrEnum):
    """Lifecycle of a single orchestration execution.

    The orchestrator never owns educational state. These values describe
    coordination progress only.
    """

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    PARTIAL = "partial"
    FAILED = "failed"
    CANCELLED = "cancelled"

    @classmethod
    def terminal_states(cls) -> frozenset[OrchestrationState]:
        """States that end an orchestration execution."""
        return frozenset(
            {cls.COMPLETED, cls.PARTIAL, cls.FAILED, cls.CANCELLED}
        )

    def is_terminal(self) -> bool:
        """True when this state ends an orchestration execution."""
        return self in OrchestrationState.terminal_states()
