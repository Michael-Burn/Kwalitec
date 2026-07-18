"""AdaptiveLearningPort — Adaptive Decision Engine contract."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from app.application.learning_orchestrator.dto.orchestration_request import (
    OrchestrationRequest,
)


@runtime_checkable
class AdaptiveLearningPort(Protocol):
    """Structural contract for adaptive decision coordination.

    The orchestrator never selects interventions — it only requests a
    decision from the Adaptive Decision Engine via this port.
    """

    @property
    def component_id(self) -> str:
        """Stable component identity (e.g. ``adaptive_learning``)."""

    @property
    def component_version(self) -> str:
        """Version string for health / diagnostics."""

    def decide(
        self,
        request: OrchestrationRequest,
        *,
        twin_payload: dict[str, Any],
        evidence_payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Request an adaptive decision; return opaque decision payload."""

    def is_available(self) -> bool:
        """True when the adaptive learning port can accept work."""
