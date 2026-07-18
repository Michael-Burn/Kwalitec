"""EducationPlatformPort — contract toward Education Platform.

Studio never imports Education Platform packages.
Adapters (future) implement this port for health probes and optional
student-surface preview (display only — never publishes).
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class EducationPlatformPort(Protocol):
    """Structural contract for Education Platform collaboration.

    Studio does not orchestrate student learning via this port.
    It may probe availability and request a student-surface projection
    for Founder display only.
    """

    @property
    def component_id(self) -> str:
        """Stable component identity (e.g. ``education_platform``)."""

    @property
    def component_version(self) -> str:
        """Version string for health / diagnostics."""

    def is_available(self) -> bool:
        """True when the Education Platform port can accept work."""

    def health(self) -> dict[str, Any]:
        """Return an opaque platform health payload."""

    def student_surface(
        self,
        *,
        subject_code: str,
        version_id: str | None = None,
    ) -> dict[str, Any] | None:
        """Optional student-visible surface projection (display only)."""
