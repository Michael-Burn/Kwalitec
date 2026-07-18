"""Learning Journey port — journey progress for Journey surfaces.

Student Experience never imports the Learning Journey packages.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class LearningJourneyPort(Protocol):
    """Structural contract for Learning Journey collaboration.

    Experience projects topic progress and completion estimates.
    It must never own journey progression or invent Topic Complete.
    """

    @property
    def component_id(self) -> str:
        """Stable component identity."""

    @property
    def component_version(self) -> str:
        """Version string for health / diagnostics."""

    def is_available(self) -> bool:
        """True when the Learning Journey port can accept work."""

    def get_journey_progress(self, student_id: str) -> dict[str, Any] | None:
        """Return opaque journey progress summary."""

    def get_topic_list(self, student_id: str) -> tuple[dict[str, Any], ...]:
        """Return opaque topic cards (current / completed / upcoming)."""
