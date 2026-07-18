"""LearningOrchestrator — public facade for live learner event coordination.

Coordinates Evidence → Twin → Adaptive Decision → Mission → Analytics.
Owns NO educational rules. Never mutates curriculum. Never persists.
Framework-independent: no Flask, SQLAlchemy, or AI.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.application.learning_orchestrator.diagnostics import (
    DiagnosticReport,
    Diagnostics,
)
from app.application.learning_orchestrator.dto.orchestration_request import (
    OrchestrationRequest,
)
from app.application.learning_orchestrator.dto.orchestration_response import (
    OrchestrationResponse,
)
from app.application.learning_orchestrator.event_dispatcher import (
    EventDispatcher,
)
from app.application.learning_orchestrator.health_service import HealthService
from app.application.learning_orchestrator.pipeline_engine import PipelineEngine
from app.application.learning_orchestrator.policies.pipeline_policy import (
    PipelinePolicy,
)
from app.application.learning_orchestrator.policies.retry_policy import (
    RetryPolicy,
)
from app.application.learning_orchestrator.ports.adaptive_learning_port import (
    AdaptiveLearningPort,
)
from app.application.learning_orchestrator.ports.analytics_port import (
    AnalyticsPort,
)
from app.application.learning_orchestrator.ports.evidence_port import (
    EvidencePort,
)
from app.application.learning_orchestrator.ports.mission_port import MissionPort
from app.application.learning_orchestrator.ports.twin_port import TwinPort
from app.domain.learning_orchestrator.orchestration_event import (
    OrchestrationEvent,
    OrchestrationEventType,
)


class LearningOrchestrator:
    """Single public API for live-learner event orchestration.

    Deterministic pipeline execution only. No AI. No educational reasoning.
    Framework-independent: no Flask, SQLAlchemy, or persistence.
    """

    ORCHESTRATOR_VERSION = "learning-orchestrator-1"

    def __init__(
        self,
        *,
        engine: PipelineEngine | None = None,
        dispatcher: EventDispatcher | None = None,
        health: HealthService | None = None,
        diagnostics: Diagnostics | None = None,
        pipeline_policy: PipelinePolicy | None = None,
        retry_policy: RetryPolicy | None = None,
        clock=None,
        id_factory=None,
    ) -> None:
        self._clock = clock or (lambda: datetime.now(tz=UTC))
        self._id_factory = id_factory
        self._engine = engine or PipelineEngine(
            pipeline_policy=pipeline_policy,
            retry_policy=retry_policy,
            clock=self._clock,
            id_factory=id_factory,
        )
        self._dispatcher = dispatcher or EventDispatcher(
            self._engine,
            clock=self._clock,
            id_factory=id_factory,
        )
        self._health = health or HealthService(
            engine=self._engine,
            orchestrator_version=self.ORCHESTRATOR_VERSION,
            clock=self._clock,
        )
        self._diagnostics = diagnostics or Diagnostics(
            engine=self._engine,
            orchestrator_version=self.ORCHESTRATOR_VERSION,
            clock=self._clock,
        )

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    @classmethod
    def create(
        cls,
        *,
        evidence: EvidencePort | None = None,
        twin: TwinPort | None = None,
        adaptive_learning: AdaptiveLearningPort | None = None,
        mission: MissionPort | None = None,
        analytics: AnalyticsPort | None = None,
        pipeline_policy: PipelinePolicy | None = None,
        retry_policy: RetryPolicy | None = None,
        clock=None,
        id_factory=None,
    ) -> LearningOrchestrator:
        """Assemble an orchestrator with optional injected ports."""
        orchestrator = cls(
            pipeline_policy=pipeline_policy,
            retry_policy=retry_policy,
            clock=clock,
            id_factory=id_factory,
        )
        orchestrator.bind_ports(
            evidence=evidence,
            twin=twin,
            adaptive_learning=adaptive_learning,
            mission=mission,
            analytics=analytics,
        )
        return orchestrator

    # ------------------------------------------------------------------
    # Port binding / substitution
    # ------------------------------------------------------------------

    @property
    def engine(self) -> PipelineEngine:
        """Underlying pipeline engine."""
        return self._engine

    @property
    def dispatcher(self) -> EventDispatcher:
        """Underlying event dispatcher."""
        return self._dispatcher

    def bind_ports(
        self,
        *,
        evidence: EvidencePort | None = None,
        twin: TwinPort | None = None,
        adaptive_learning: AdaptiveLearningPort | None = None,
        mission: MissionPort | None = None,
        analytics: AnalyticsPort | None = None,
    ) -> None:
        """Bind or replace port implementations."""
        self._engine.bind_ports(
            evidence=evidence,
            twin=twin,
            adaptive_learning=adaptive_learning,
            mission=mission,
            analytics=analytics,
        )

    def replace_port(self, name: str, port: object) -> None:
        """Replace a single named port (``evidence`` / ``twin`` / …)."""
        kwargs = {name: port}
        # Map adaptive_learning alias
        if name == "decision":
            kwargs = {"adaptive_learning": port}
        self._engine.bind_ports(**kwargs)

    # ------------------------------------------------------------------
    # Orchestration entry points
    # ------------------------------------------------------------------

    def orchestrate(
        self, request: OrchestrationRequest
    ) -> OrchestrationResponse:
        """Run the full live-learner pipeline for ``request``."""
        response = self._dispatcher.dispatch(request)
        if response.execution_summary is not None:
            self._diagnostics.record_execution(response.execution_summary)
        return response

    def handle_event(
        self, event: OrchestrationEvent
    ) -> OrchestrationResponse:
        """Dispatch a domain ``OrchestrationEvent`` through the pipeline."""
        response = self._dispatcher.dispatch(event)
        if response.execution_summary is not None:
            self._diagnostics.record_execution(response.execution_summary)
        return response

    def handle_learning_activity_completed(
        self, request: OrchestrationRequest
    ) -> OrchestrationResponse:
        """Coordinate a learning-activity-completed event."""
        return self._run_typed(
            OrchestrationEventType.LEARNING_ACTIVITY_COMPLETED, request
        )

    def handle_knowledge_check_completed(
        self, request: OrchestrationRequest
    ) -> OrchestrationResponse:
        """Coordinate a knowledge-check-completed event."""
        return self._run_typed(
            OrchestrationEventType.KNOWLEDGE_CHECK_COMPLETED, request
        )

    def handle_reflection_submitted(
        self, request: OrchestrationRequest
    ) -> OrchestrationResponse:
        """Coordinate a reflection-submitted event."""
        return self._run_typed(
            OrchestrationEventType.REFLECTION_SUBMITTED, request
        )

    def handle_session_completed(
        self, request: OrchestrationRequest
    ) -> OrchestrationResponse:
        """Coordinate a session-completed event."""
        return self._run_typed(
            OrchestrationEventType.SESSION_COMPLETED, request
        )

    def handle_mission_completed(
        self, request: OrchestrationRequest
    ) -> OrchestrationResponse:
        """Coordinate a mission-completed event."""
        return self._run_typed(
            OrchestrationEventType.MISSION_COMPLETED, request
        )

    def handle_manual_confidence_update(
        self, request: OrchestrationRequest
    ) -> OrchestrationResponse:
        """Coordinate a manual-confidence-update event."""
        return self._run_typed(
            OrchestrationEventType.MANUAL_CONFIDENCE_UPDATE, request
        )

    # ------------------------------------------------------------------
    # Health / diagnostics
    # ------------------------------------------------------------------

    def health_status(self) -> dict[str, object]:
        """Return read-only health (never mutates composition)."""
        return self._health.status()

    def diagnostics(self) -> DiagnosticReport:
        """Return an immutable diagnostic report."""
        return self._diagnostics.report()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _run_typed(
        self,
        event_type: OrchestrationEventType,
        request: OrchestrationRequest,
    ) -> OrchestrationResponse:
        typed = OrchestrationRequest(
            event_type=event_type.value,
            learner_id=request.learner_id,
            event_id=request.event_id,
            occurred_at=request.occurred_at,
            subject_id=request.subject_id,
            topic_id=request.topic_id,
            journey_id=request.journey_id,
            session_id=request.session_id,
            activity_id=request.activity_id,
            mission_id=request.mission_id,
            evidence_id=request.evidence_id,
            correlation_id=request.correlation_id,
            orchestration_id=request.orchestration_id,
            payload=request.payload,
            metadata=request.metadata,
        )
        return self.orchestrate(typed)
