"""MissionAdapter — implements MissionPort for Learning Orchestrator."""

from __future__ import annotations

from typing import Any

from app.application.learning_orchestrator.dto.orchestration_request import (
    OrchestrationRequest,
)
from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics
from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import mission_updated
from app.infrastructure.repositories.in_memory import InMemoryAggregateRepository


class MissionPortAdapter:
    """Production adapter for orchestrator MissionPort.

    Delivers / updates mission work from adaptive decisions.
    Does NOT independently recommend learner-facing next actions (ADR-005).
    """

    ADAPTER_ID = "mission"
    ADAPTER_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        mission_store: InMemoryAggregateRepository | None = None,
        mission_engine: Any | None = None,
        events: EventRegistry | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        available: bool = True,
    ) -> None:
        self._missions = mission_store or InMemoryAggregateRepository(
            repository_id="mission_repository",
            aggregate_name="DailyMission",
        )
        self._engine = mission_engine
        self._events = events or EventRegistry()
        self._diagnostics = diagnostics or AdapterDiagnostics()
        self._available = available
        self._diagnostics.record_health(
            self.ADAPTER_ID,
            available=available,
            version=self.ADAPTER_VERSION,
        )

    @property
    def component_id(self) -> str:
        return self.ADAPTER_ID

    @property
    def component_version(self) -> str:
        return self.ADAPTER_VERSION

    def is_available(self) -> bool:
        return self._available

    def set_available(self, available: bool) -> None:
        self._available = available
        self._diagnostics.record_health(
            self.ADAPTER_ID,
            available=available,
            version=self.ADAPTER_VERSION,
        )

    def apply_decision(
        self,
        request: OrchestrationRequest,
        *,
        decision_payload: dict[str, Any],
        twin_payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Apply an adaptive decision to missions; return opaque payload."""
        self._diagnostics.record_call(self.ADAPTER_ID)
        ids = CorrelationContext.current()
        mission_id = (
            request.mission_id
            or f"mission:{request.learner_id}:{request.event_id}"
        )
        document = {
            "mission_id": mission_id,
            "learner_id": request.learner_id,
            "subject_id": request.subject_id,
            "decision": dict(decision_payload),
            "twin_ref": twin_payload.get("twin_id"),
            "role": "delivery",
            "next_action_authority": False,
        }
        if self._engine is not None and hasattr(self._engine, "apply_opaque"):
            applied = self._engine.apply_opaque(
                request,
                decision_payload=decision_payload,
                twin_payload=twin_payload,
            )
            if isinstance(applied, dict):
                document.update(applied)

        ack = self._missions.save(mission_id, document)
        payload = {
            "component": self.ADAPTER_ID,
            "ok": True,
            "mission_id": mission_id,
            "learner_id": request.learner_id,
            "version": ack.get("version"),
            "authority": "mission_engine",
            "next_action_authority": False,
        }
        self._events.publish(
            mission_updated(
                payload,
                correlation_id=ids.correlation_id or (request.correlation_id or ""),
                causation_id=ids.causation_id or request.event_id,
                source=self.ADAPTER_ID,
            )
        )
        return payload
