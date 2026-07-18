"""StudentTwinAdapter — implements TwinPort for Learning Orchestrator."""

from __future__ import annotations

from typing import Any

from app.application.learning_orchestrator.dto.orchestration_request import (
    OrchestrationRequest,
)
from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics
from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import twin_updated
from app.infrastructure.persistence.evidence_store import EvidenceStore
from app.infrastructure.repositories.in_memory import (
    InMemoryAggregateRepository,
)


class StudentTwinAdapter:
    """Production adapter for TwinPort.

    Persists opaque Twin projections and evidence refs via infrastructure
    stores. Educational recalculation remains inside Student Digital Twin
    application services when a twin_engine is injected; otherwise this
    adapter records structural updates only (no mastery math here).
    """

    ADAPTER_ID = "twin"
    ADAPTER_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        twin_store: InMemoryAggregateRepository | None = None,
        evidence_store: EvidenceStore | None = None,
        events: EventRegistry | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        twin_engine: Any | None = None,
        available: bool = True,
    ) -> None:
        self._twins = twin_store or InMemoryAggregateRepository(
            repository_id="twin_repository",
            aggregate_name="DigitalTwin",
        )
        self._evidence = evidence_store or EvidenceStore()
        self._events = events or EventRegistry()
        self._diagnostics = diagnostics or AdapterDiagnostics()
        self._twin_engine = twin_engine
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

    def update_from_evidence(
        self,
        request: OrchestrationRequest,
        *,
        evidence_payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Apply structural Twin update from prior evidence payload."""
        self._diagnostics.record_call(self.ADAPTER_ID)
        ids = CorrelationContext.current()
        learner_id = request.learner_id
        subject_id = (request.subject_id or "UNKNOWN").strip() or "UNKNOWN"
        twin_id = f"twin:{learner_id}:{subject_id}"
        existing = self._twins.get(twin_id) or {
            "twin_id": twin_id,
            "learner_id": learner_id,
            "subject_id": subject_id,
            "evidence_count": 0,
            "history": [],
        }
        evidence_id = str(
            evidence_payload.get("evidence_id")
            or evidence_payload.get("record_id")
            or request.event_id
        )
        history = list(existing.get("history") or [])
        history.append(evidence_id)
        updated = {
            **existing,
            "evidence_count": int(existing.get("evidence_count") or 0) + 1,
            "history": history[-50:],
            "last_evidence": dict(evidence_payload),
            "correlation_id": ids.correlation_id or request.correlation_id,
        }
        # Optional: delegate educational recalculation to Twin application
        # engine without embedding Twin math in this adapter.
        if self._twin_engine is not None and hasattr(
            self._twin_engine, "project_opaque"
        ):
            projected = self._twin_engine.project_opaque(updated, evidence_payload)
            if isinstance(projected, dict):
                updated.update(projected)

        ack = self._twins.save(twin_id, updated)
        payload = {
            "component": self.ADAPTER_ID,
            "ok": True,
            "twin_id": twin_id,
            "learner_id": learner_id,
            "subject_id": subject_id,
            "evidence_count": updated["evidence_count"],
            "version": ack.get("version"),
            "authority": "student_twin",
        }
        self._events.publish(
            twin_updated(
                payload,
                correlation_id=ids.correlation_id or request.correlation_id,
                causation_id=ids.causation_id or evidence_id,
                source=self.ADAPTER_ID,
            )
        )
        return payload
