"""AdaptiveLearningAdapter — implements AdaptiveLearningPort."""

from __future__ import annotations

from typing import Any

from app.application.learning_orchestrator.dto.orchestration_request import (
    OrchestrationRequest,
)
from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics
from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import adaptive_decision_generated


class AdaptiveLearningAdapter:
    """Production adapter for AdaptiveLearningPort.

    Requests decisions from the Adaptive Decision Engine when injected.
    Does not invent Twin state. Does not schedule missions.
    ADR-005: this is the next-action authority bridge for learner-facing
    revision decisions; Journey/Mission may deliver but not independently
    invent alternative next-action rankings.
    """

    ADAPTER_ID = "adaptive_learning"
    ADAPTER_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        decision_engine: Any | None = None,
        events: EventRegistry | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        available: bool = True,
    ) -> None:
        self._engine = decision_engine
        self._events = events or EventRegistry()
        self._diagnostics = diagnostics or AdapterDiagnostics()
        self._available = available
        self._last: dict[str, Any] | None = None
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

    def decide(
        self,
        request: OrchestrationRequest,
        *,
        twin_payload: dict[str, Any],
        evidence_payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Request an adaptive decision; return opaque decision payload."""
        self._diagnostics.record_call(self.ADAPTER_ID)
        ids = CorrelationContext.current()
        payload: dict[str, Any] = {
            "component": self.ADAPTER_ID,
            "ok": True,
            "learner_id": request.learner_id,
            "subject_id": request.subject_id,
            "authority": "adaptive_decision_engine",
            "next_action_authority": True,
            "twin_evidence_count": twin_payload.get("evidence_count"),
            "evidence_id": evidence_payload.get("evidence_id")
            or evidence_payload.get("record_id"),
        }
        if self._engine is not None and hasattr(self._engine, "decide_opaque"):
            decided = self._engine.decide_opaque(
                request, twin_payload=twin_payload, evidence_payload=evidence_payload
            )
            if isinstance(decided, dict):
                payload.update(decided)
        elif self._engine is not None and hasattr(self._engine, "decide"):
            # Engine present but requires domain TwinSnapshot — surface
            # structural deferral rather than inventing educational math.
            payload["engine_bound"] = True
            payload["decision"] = "deferred_to_engine_contract"
        else:
            payload["decision"] = "no_intervention"
            payload["engine_bound"] = False

        self._last = payload
        self._events.publish(
            adaptive_decision_generated(
                payload,
                correlation_id=ids.correlation_id or (request.correlation_id or ""),
                causation_id=ids.causation_id or request.event_id,
                source=self.ADAPTER_ID,
            )
        )
        return dict(payload)

    @property
    def last_decision(self) -> dict[str, Any] | None:
        """Last opaque decision (diagnostics)."""
        return None if self._last is None else dict(self._last)
