"""Mission port — today's session delivery for Start Session actions.

Student Experience never imports Mission Engine packages.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class MissionPort(Protocol):
    """Structural contract for Mission Engine collaboration.

    Experience may present Today's Session and request start delivery.
    It must never generate missions independently or recommend next actions.
    """

    @property
    def component_id(self) -> str:
        """Stable component identity."""

    @property
    def component_version(self) -> str:
        """Version string for health / diagnostics."""

    def is_available(self) -> bool:
        """True when the Mission port can accept work."""

    def get_todays_session(self, student_id: str) -> dict[str, Any] | None:
        """Return opaque today's session / mission summary."""

    def start_session(
        self,
        student_id: str,
        *,
        mission_id: str | None = None,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        """Request session start via Mission delivery; return opaque status."""

    def get_session_status(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        """Return opaque session status."""
