"""TwinPort — Digital Twin update contract for live orchestration."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from app.application.learning_orchestrator.dto.orchestration_request import (
    OrchestrationRequest,
)


@runtime_checkable
class TwinPort(Protocol):
    """Structural contract for Twin coordination during orchestration.

    The orchestrator never mutates Twin beliefs itself — it only invokes
    the Twin port with prior stage payloads.
    """

    @property
    def component_id(self) -> str:
        """Stable component identity (e.g. ``twin``)."""

    @property
    def component_version(self) -> str:
        """Version string for health / diagnostics."""

    def update_from_evidence(
        self,
        request: OrchestrationRequest,
        *,
        evidence_payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Apply evidence structurally; return opaque Twin payload."""

    def is_available(self) -> bool:
        """True when the Twin port can accept work."""
