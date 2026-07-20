"""Adaptive Decision port — next recommendation after session completion.

Session Experience never imports Adaptive Decision packages.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class AdaptiveDecisionPort(Protocol):
    """Structural contract for Adaptive Decision collaboration.

    Experience may display the next recommendation after completion.
    It must never invent recommendations (ADR-005).
    """

    @property
    def component_id(self) -> str:
        """Stable component identity."""

    @property
    def component_version(self) -> str:
        """Version string for health / diagnostics."""

    def is_available(self) -> bool:
        """True when the Adaptive Decision port can accept work."""

    def get_todays_recommendation(self, student_id: str) -> dict[str, Any] | None:
        """Return opaque today's / next recommendation."""
