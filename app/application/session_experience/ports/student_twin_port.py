"""Student Twin port — readiness / insight facts for session summary.

Session Experience never imports Student Twin packages.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class StudentTwinPort(Protocol):
    """Structural contract for Twin collaboration on summary projections.

    Experience may display readiness change labels from Twin facts.
    It must never compute readiness.
    """

    @property
    def component_id(self) -> str:
        """Stable component identity."""

    @property
    def component_version(self) -> str:
        """Version string for health / diagnostics."""

    def is_available(self) -> bool:
        """True when the Twin port can accept work."""

    def get_readiness_summary(self, student_id: str) -> dict[str, Any] | None:
        """Return opaque readiness summary."""

    def get_learning_insights(self, student_id: str) -> dict[str, Any] | None:
        """Return opaque learning insights."""
