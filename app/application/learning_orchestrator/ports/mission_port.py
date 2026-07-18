"""MissionPort — Mission Engine contract for live orchestration."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from app.application.learning_orchestrator.dto.orchestration_request import (
    OrchestrationRequest,
)


@runtime_checkable
class MissionPort(Protocol):
    """Structural contract for mission coordination during orchestration.

    Educational mission reasoning remains inside the Mission Engine.
    """

    @property
    def component_id(self) -> str:
        """Stable component identity (e.g. ``mission``)."""

    @property
    def component_version(self) -> str:
        """Version string for health / diagnostics."""

    def apply_decision(
        self,
        request: OrchestrationRequest,
        *,
        decision_payload: dict[str, Any],
        twin_payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Apply an adaptive decision to missions; return opaque payload."""

    def is_available(self) -> bool:
        """True when the mission port can accept work."""
