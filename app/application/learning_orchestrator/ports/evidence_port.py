"""EvidencePort — evidence processing contract for live orchestration."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from app.application.learning_orchestrator.dto.orchestration_request import (
    OrchestrationRequest,
)


@runtime_checkable
class EvidencePort(Protocol):
    """Structural contract for evidence intake during orchestration.

    The orchestrator requests structural evidence processing only.
    Evidence scoring and Twin belief updates remain in their engines.
    """

    @property
    def component_id(self) -> str:
        """Stable component identity (e.g. ``evidence``)."""

    @property
    def component_version(self) -> str:
        """Version string for health / diagnostics."""

    def process_evidence(self, request: OrchestrationRequest) -> dict[str, Any]:
        """Process evidence for the learner event; return opaque payload."""

    def is_available(self) -> bool:
        """True when the evidence port can accept work."""
