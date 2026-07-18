"""Student Twin port — opaque learner state reads for projections.

Student Experience never imports the Twin package.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class StudentTwinPort(Protocol):
    """Structural contract for Student Digital Twin collaboration.

    Experience may read learning insights and readiness summaries.
    It must never mutate twin state or invent readiness scores.
    """

    @property
    def component_id(self) -> str:
        """Stable component identity."""

    @property
    def component_version(self) -> str:
        """Version string for health / diagnostics."""

    def is_available(self) -> bool:
        """True when the Twin port can accept work."""

    def get_learner_summary(self, student_id: str) -> dict[str, Any] | None:
        """Return an opaque learner summary, or None when unknown."""

    def get_readiness_summary(self, student_id: str) -> dict[str, Any] | None:
        """Return an opaque readiness summary (exam readiness facts)."""

    def get_learning_insights(self, student_id: str) -> dict[str, Any] | None:
        """Return opaque learning insights for history / profile surfaces."""
