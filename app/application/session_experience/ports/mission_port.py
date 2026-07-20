"""Mission port — session identity for Learning Session Experience.

Session Experience never imports Mission Engine packages.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class MissionPort(Protocol):
    """Structural contract for Mission delivery collaboration.

    Experience may resolve today's session identity. It must never
    generate missions or recommend next actions.
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

    def get_session_status(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        """Return opaque session status."""
