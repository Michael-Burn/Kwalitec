"""Activity Engine port — in-session activity execution collaboration.

Session Experience never imports Learning Activity Engine packages.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ActivityEnginePort(Protocol):
    """Structural contract for Learning Activity Engine collaboration.

    Experience may present the current activity and advance the sequence.
    It must never score answers or invent mastery.
    """

    @property
    def component_id(self) -> str:
        """Stable component identity."""

    @property
    def component_version(self) -> str:
        """Version string for health / diagnostics."""

    def is_available(self) -> bool:
        """True when the Activity Engine port can accept work."""

    def get_current_activity(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        """Return opaque current activity facts."""

    def submit_response(
        self,
        student_id: str,
        *,
        session_id: str,
        activity_id: str,
        response: str,
    ) -> dict[str, Any]:
        """Submit a learner response; return opaque activity result."""

    def advance_activity(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        """Advance to the next activity; return opaque next activity or None."""

    def get_activity_progress(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        """Return opaque activity sequence progress facts."""
