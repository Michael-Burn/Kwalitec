"""Learning Orchestrator port — activity status for Learning Activity UX.

Student Experience never imports the Learning Orchestrator package.
Student-facing language uses "Learning Activity", never Orchestrator.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class LearningOrchestratorPort(Protocol):
    """Structural contract for Learning Orchestrator collaboration.

    Experience may observe activity coordination status for display.
    It must never own pipeline order or educational decisions.
    """

    @property
    def component_id(self) -> str:
        """Stable component identity."""

    @property
    def component_version(self) -> str:
        """Version string for health / diagnostics."""

    def is_available(self) -> bool:
        """True when the Orchestrator port can accept work."""

    def get_activity_status(self, student_id: str) -> dict[str, Any] | None:
        """Return opaque learning activity status for presentation."""

    def acknowledge_activity(
        self, student_id: str, *, activity_id: str
    ) -> dict[str, Any]:
        """Acknowledge an activity presentation event; return opaque status."""
