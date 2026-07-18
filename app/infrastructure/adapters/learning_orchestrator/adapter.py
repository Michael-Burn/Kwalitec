"""Learning Orchestrator production wiring and supporting stage adapters."""

from __future__ import annotations

from typing import Any

from app.application.learning_orchestrator.dto.orchestration_request import (
    OrchestrationRequest,
)
from app.application.learning_orchestrator.learning_orchestrator import (
    LearningOrchestrator,
)
from app.infrastructure.adapters.adaptive_learning.adapter import (
    AdaptiveLearningAdapter,
)
from app.infrastructure.adapters.mission.adapter import MissionPortAdapter
from app.infrastructure.adapters.student_twin.adapter import StudentTwinAdapter
from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics
from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.diagnostics.pipeline_metrics import PipelineMetrics
from app.infrastructure.diagnostics.tracing import ExecutionTracer
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    evidence_recorded,
    learning_session_completed,
)
from app.infrastructure.persistence.evidence_store import EvidenceStore
from app.infrastructure.persistence.unit_of_work import UnitOfWork


class EvidencePortAdapter:
    """Production adapter for EvidencePort — structural evidence intake."""

    ADAPTER_ID = "evidence"
    ADAPTER_VERSION = "1.0.0"

    def __init__(
        self,
        store: EvidenceStore | None = None,
        *,
        events: EventRegistry | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        available: bool = True,
    ) -> None:
        self._store = store or EvidenceStore()
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

    def process_evidence(self, request: OrchestrationRequest) -> dict[str, Any]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        ids = CorrelationContext.current()
        subject = (request.subject_id or "UNKNOWN").strip() or "UNKNOWN"
        record = self._store.append(
            learner_id=request.learner_id,
            subject_id=subject,
            evidence_type=request.event_type,
            payload={
                "event_id": request.event_id,
                "topic_id": request.topic_id,
                "session_id": request.session_id,
            },
            record_id=request.evidence_id or request.event_id,
            correlation_id=ids.correlation_id or (request.correlation_id or ""),
            causation_id=ids.causation_id or "",
            source=self.ADAPTER_ID,
        )
        payload = {
            "component": self.ADAPTER_ID,
            "ok": True,
            "evidence_id": record.record_id,
            "record_id": record.record_id,
            "learner_id": record.learner_id,
            "subject_id": record.subject_id,
            "evidence_type": record.evidence_type,
        }
        self._events.publish(
            evidence_recorded(
                payload,
                correlation_id=payload["learner_id"] and (
                    ids.correlation_id or (request.correlation_id or "")
                ),
                causation_id=request.event_id,
                source=self.ADAPTER_ID,
            )
        )
        if request.event_type.lower().endswith("session_completed") or (
            request.session_id and "complete" in request.event_type.lower()
        ):
            self._events.publish(
                learning_session_completed(
                    {
                        "session_id": request.session_id,
                        "learner_id": request.learner_id,
                        "subject_id": subject,
                    },
                    correlation_id=ids.correlation_id or (request.correlation_id or ""),
                    causation_id=request.event_id,
                    source=self.ADAPTER_ID,
                )
            )
        return payload


class AnalyticsPortAdapter:
    """Production adapter for AnalyticsPort — operational observation only."""

    ADAPTER_ID = "analytics"
    ADAPTER_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        metrics: PipelineMetrics | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        available: bool = True,
    ) -> None:
        self._metrics = metrics or PipelineMetrics()
        self._diagnostics = diagnostics or AdapterDiagnostics()
        self._available = available
        self._observations: list[dict[str, Any]] = []
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

    def record_execution(
        self,
        request: OrchestrationRequest,
        *,
        stage_payloads: dict[str, Any],
        execution_summary: dict[str, Any],
    ) -> dict[str, Any]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        success = bool(execution_summary.get("success", True))
        self._metrics.incr(
            "pipeline_completed" if success else "pipeline_failed",
            event_type=request.event_type,
        )
        observation = {
            "component": self.ADAPTER_ID,
            "ok": True,
            "learner_id": request.learner_id,
            "stages": sorted(stage_payloads),
            "success": success,
        }
        self._observations.append(observation)
        return observation


class LearningOrchestratorAdapter:
    """Production composition root for the Learning Orchestrator.

    Wires infrastructure port adapters into the framework-independent
    LearningOrchestrator. Application services never import this class.
    """

    ADAPTER_ID = "learning_orchestrator"
    ADAPTER_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        events: EventRegistry | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        metrics: PipelineMetrics | None = None,
        tracer: ExecutionTracer | None = None,
        uow: UnitOfWork | None = None,
        evidence: EvidencePortAdapter | None = None,
        twin: StudentTwinAdapter | None = None,
        adaptive: AdaptiveLearningAdapter | None = None,
        mission: MissionPortAdapter | None = None,
        analytics: AnalyticsPortAdapter | None = None,
    ) -> None:
        self._events = events or EventRegistry()
        self._diagnostics = diagnostics or AdapterDiagnostics()
        self._metrics = metrics or PipelineMetrics()
        self._tracer = tracer or ExecutionTracer()
        self._uow = uow or UnitOfWork()
        self.evidence = evidence or EvidencePortAdapter(
            events=self._events, diagnostics=self._diagnostics
        )
        self.twin = twin or StudentTwinAdapter(
            events=self._events, diagnostics=self._diagnostics
        )
        self.adaptive = adaptive or AdaptiveLearningAdapter(
            events=self._events, diagnostics=self._diagnostics
        )
        self.mission = mission or MissionPortAdapter(
            events=self._events, diagnostics=self._diagnostics
        )
        self.analytics = analytics or AnalyticsPortAdapter(
            metrics=self._metrics, diagnostics=self._diagnostics
        )
        self._orchestrator = LearningOrchestrator.create(
            evidence=self.evidence,
            twin=self.twin,
            adaptive_learning=self.adaptive,
            mission=self.mission,
            analytics=self.analytics,
        )
        self._diagnostics.record_health(
            self.ADAPTER_ID,
            available=True,
            version=self.ADAPTER_VERSION,
        )

    @property
    def component_id(self) -> str:
        return self.ADAPTER_ID

    @property
    def component_version(self) -> str:
        return self.ADAPTER_VERSION

    @property
    def orchestrator(self) -> LearningOrchestrator:
        """Underlying framework-independent orchestrator."""
        return self._orchestrator

    def is_available(self) -> bool:
        return True

    def orchestrate(self, request: OrchestrationRequest) -> Any:
        """Run orchestration inside correlation + optional UoW boundaries."""
        tokens = CorrelationContext.set(
            correlation_id=request.correlation_id or None,
            causation_id=request.event_id,
        )
        span = self._tracer.start(
            "learning_orchestrator.orchestrate",
            event_type=request.event_type,
            learner_id=request.learner_id,
        )
        self._metrics.incr("pipeline_started", event_type=request.event_type)
        try:
            with self._uow.transaction():
                self._uow.set_metadata(
                    "correlation_id",
                    CorrelationContext.get_correlation_id(),
                )
                response = self._orchestrator.orchestrate(request)
            self._metrics.incr(
                "transaction_committed", event_type=request.event_type
            )
            self._tracer.end(span, status="ok")
            self._diagnostics.record_call(self.ADAPTER_ID)
            return response
        except Exception:
            self._metrics.incr(
                "transaction_rolled_back", event_type=request.event_type
            )
            self._metrics.incr("pipeline_failed", event_type=request.event_type)
            self._tracer.end(span, status="error")
            self._diagnostics.record_call(self.ADAPTER_ID, error=True)
            raise
        finally:
            CorrelationContext.reset(tokens)
