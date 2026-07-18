"""Adaptive Decision port — sole next-action recommendation authority.

Student Experience never imports the Adaptive Decision Engine package.
Per ADR-005, Adaptive Decision is the sole learner-facing next-action owner.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class AdaptiveDecisionPort(Protocol):
    """Structural contract for Adaptive Decision collaboration.

    Experience projects Today's Recommendation and Revision options.
    It must never invent next actions or recalculate educational ROI.
    """

    @property
    def component_id(self) -> str:
        """Stable component identity."""

    @property
    def component_version(self) -> str:
        """Version string for health / diagnostics."""

    def is_available(self) -> bool:
        """True when the Adaptive Decision port can accept work."""

    def get_todays_recommendation(
        self, student_id: str
    ) -> dict[str, Any] | None:
        """Return today's next-action recommendation (opaque), or None."""

    def get_revision_options(
        self, student_id: str
    ) -> tuple[dict[str, Any], ...]:
        """Return opaque revision candidates (primary first)."""

    def get_decision_explanation(
        self, student_id: str, *, decision_id: str | None = None
    ) -> dict[str, Any] | None:
        """Return opaque explanation payload for a recommendation."""
