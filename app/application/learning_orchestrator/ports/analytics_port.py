"""AnalyticsPort — analytics observation contract for live orchestration."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from app.application.learning_orchestrator.dto.orchestration_request import (
    OrchestrationRequest,
)


@runtime_checkable
class AnalyticsPort(Protocol):
    """Structural contract for analytics observation during orchestration.

    Analytics never feed educational decisions inside this layer.
    """

    @property
    def component_id(self) -> str:
        """Stable component identity (e.g. ``analytics``)."""

    @property
    def component_version(self) -> str:
        """Version string for health / diagnostics."""

    def record_execution(
        self,
        request: OrchestrationRequest,
        *,
        stage_payloads: dict[str, Any],
        execution_summary: dict[str, Any],
    ) -> dict[str, Any]:
        """Record orchestration observation; return opaque analytics payload."""

    def is_available(self) -> bool:
        """True when the analytics port can accept work."""
