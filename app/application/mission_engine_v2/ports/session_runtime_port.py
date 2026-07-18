"""Learning Session Runtime port consumed by Mission Engine 2.0."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class SessionRuntimePort(Protocol):
    """Structural contract for Learning Session Runtime reads.

    Mission Engine 2.0 may inspect runtime phase for resume / continue
    dispatch. It must never start, pause, or complete sessions.
    """

    def runtime_phase_for(self, session_id: str) -> str | None:
        """Return the runtime phase value for ``session_id``, if known."""

    def has_outstanding_reflection(self, session_id: str) -> bool:
        """True when the session owes a reflection (structural signal only)."""
