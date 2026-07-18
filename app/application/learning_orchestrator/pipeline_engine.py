"""Pipeline engine — runs live-learner stages in deterministic order.

Evidence → Twin → Adaptive Decision → Mission → Analytics

Failures are isolated per PipelinePolicy. Never recovers educational state.
Never mutates curriculum. Never uses AI.
"""

from __future__ import annotations

import time
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any

from app.application.learning_orchestrator.analytics_pipeline import (
    AnalyticsPipeline,
)
from app.application.learning_orchestrator.decision_pipeline import (
    DecisionPipeline,
)
from app.application.learning_orchestrator.dto.execution_summary import (
    ExecutionSummary,
)
from app.application.learning_orchestrator.dto.orchestration_request import (
    OrchestrationRequest,
)
from app.application.learning_orchestrator.dto.orchestration_response import (
    OrchestrationResponse,
)
from app.application.learning_orchestrator.dto.pipeline_snapshot import (
    PipelineSnapshot,
)
from app.application.learning_orchestrator.evidence_pipeline import (
    EvidencePipeline,
)
from app.application.learning_orchestrator.exceptions import OrchestrationError
from app.application.learning_orchestrator.mission_pipeline import (
    MissionPipeline,
)
from app.application.learning_orchestrator.policies.orchestration_policy import (
    OrchestrationPolicy,
)
from app.application.learning_orchestrator.policies.pipeline_policy import (
    PipelinePolicy,
)
from app.application.learning_orchestrator.policies.retry_policy import (
    RetryPolicy,
)
from app.application.learning_orchestrator.twin_pipeline import TwinPipeline
from app.domain.learning_orchestrator.orchestration_context import (
    OrchestrationContext,
)
from app.domain.learning_orchestrator.orchestration_event import (
    OrchestrationEvent,
)
from app.domain.learning_orchestrator.orchestration_result import (
    OrchestrationResult,
)
from app.domain.learning_orchestrator.orchestration_state import (
    OrchestrationState,
)
from app.domain.learning_orchestrator.pipeline_result import PipelineResult
from app.domain.learning_orchestrator.pipeline_stage import PipelineStageName


class PipelineEngine:
    """Execute the live-learner pipeline in deterministic stage order."""

    def __init__(
        self,
        *,
        evidence: EvidencePipeline | None = None,
        twin: TwinPipeline | None = None,
        decision: DecisionPipeline | None = None,
        mission: MissionPipeline | None = None,
        analytics: AnalyticsPipeline | None = None,
        pipeline_policy: PipelinePolicy | None = None,
        retry_policy: RetryPolicy | None = None,
        clock=None,
        id_factory=None,
    ) -> None:
        retry = retry_policy or RetryPolicy.none()
        self._evidence = evidence or EvidencePipeline(retry_policy=retry)
        self._twin = twin or TwinPipeline(retry_policy=retry)
        self._decision = decision or DecisionPipeline(retry_policy=retry)
        self._mission = mission or MissionPipeline(retry_policy=retry)
        self._analytics = analytics or AnalyticsPipeline(retry_policy=retry)
        self._pipeline_policy = pipeline_policy or PipelinePolicy.isolated()
        self._clock = clock or (lambda: datetime.now(tz=UTC))
        self._id_factory = id_factory or (
            lambda: f"orch-{int(self._clock().timestamp() * 1000)}"
        )
        self._runners: dict[PipelineStageName, Any] = {
            PipelineStageName.EVIDENCE: self._evidence,
            PipelineStageName.TWIN: self._twin,
            PipelineStageName.DECISION: self._decision,
            PipelineStageName.MISSION: self._mission,
            PipelineStageName.ANALYTICS: self._analytics,
        }

    @property
    def evidence_pipeline(self) -> EvidencePipeline:
        """Evidence stage runner."""
        return self._evidence

    @property
    def twin_pipeline(self) -> TwinPipeline:
        """Twin stage runner."""
        return self._twin

    @property
    def decision_pipeline(self) -> DecisionPipeline:
        """Decision stage runner."""
        return self._decision

    @property
    def mission_pipeline(self) -> MissionPipeline:
        """Mission stage runner."""
        return self._mission

    @property
    def analytics_pipeline(self) -> AnalyticsPipeline:
        """Analytics stage runner."""
        return self._analytics

    def bind_ports(
        self,
        *,
        evidence=None,
        twin=None,
        adaptive_learning=None,
        mission=None,
        analytics=None,
    ) -> None:
        """Bind or replace port implementations on stage runners."""
        if evidence is not None:
            self._evidence.bind(evidence)
        if twin is not None:
            self._twin.bind(twin)
        if adaptive_learning is not None:
            self._decision.bind(adaptive_learning)
        if mission is not None:
            self._mission.bind(mission)
        if analytics is not None:
            self._analytics.bind(analytics)

    def dependency_status(self) -> dict[str, object]:
        """Return bound/available status for each pipeline port."""
        status: dict[str, object] = {}
        mapping = {
            "evidence": self._evidence.port,
            "twin": self._twin.port,
            "adaptive_learning": self._decision.port,
            "mission": self._mission.port,
            "analytics": self._analytics.port,
        }
        for name, port in mapping.items():
            if port is None:
                status[name] = {
                    "bound": False,
                    "available": False,
                    "component_version": None,
                }
            else:
                available = True
                probe = getattr(port, "is_available", None)
                if callable(probe):
                    available = bool(probe())
                status[name] = {
                    "bound": True,
                    "available": available,
                    "component_id": getattr(port, "component_id", name),
                    "component_version": getattr(
                        port, "component_version", "unknown"
                    ),
                }
        return status

    def run(
        self,
        request: OrchestrationRequest,
        *,
        event: OrchestrationEvent | None = None,
    ) -> OrchestrationResponse:
        """Run the pipeline for ``request`` and return an immutable response."""
        started = time.perf_counter()
        orchestration_id = request.orchestration_id or self._id_factory()
        domain_event = event or self._event_from_request(request)
        stages = OrchestrationPolicy.stages_for(request.event_type)

        context = OrchestrationContext(
            event=domain_event,
            orchestration_id=orchestration_id,
            state=OrchestrationState.RUNNING,
            started_at=self._clock(),
        )

        stop = False
        for stage in stages:
            allowed, skip_reason = self._pipeline_policy.may_run_stage(
                stage, prior_results=context.stage_results
            )
            runner = self._runners[stage]
            if not allowed or stop:
                result = runner.skip(
                    skip_reason or "pipeline stopped after prior failure"
                )
            else:
                result = runner.execute(request, context)
            context = context.with_result(result)
            if result.failed and not self._pipeline_policy.should_continue_after(
                result
            ):
                stop = True

        duration_ms = (time.perf_counter() - started) * 1000.0
        terminal_state = self._resolve_state(context.stage_results)
        context = context.with_state(terminal_state)

        domain_result = OrchestrationResult.from_context(
            orchestration_id=orchestration_id,
            event_id=domain_event.event_id,
            learner_id=domain_event.learner_id,
            event_type=domain_event.event_type.value,
            state=terminal_state,
            stage_results=context.stage_results,
            duration_ms=duration_ms,
            warnings=context.warnings,
            error=self._primary_error(context.stage_results),
            diagnostics={
                "dependency_status": self.dependency_status(),
                "stage_count": len(context.stage_results),
            },
            correlation_id=request.correlation_id,
        )

        snapshots = tuple(
            PipelineSnapshot.from_result(r) for r in context.stage_results
        )
        summary = ExecutionSummary.from_result(
            domain_result,
            dependency_status=self.dependency_status(),
            pipeline_snapshots=snapshots,
        )
        return OrchestrationResponse(
            orchestration_id=orchestration_id,
            event_id=domain_event.event_id,
            learner_id=domain_event.learner_id,
            event_type=domain_event.event_type.value,
            success=domain_result.success,
            state=terminal_state.value,
            pipeline_snapshots=snapshots,
            execution_summary=summary,
            warnings=context.warnings,
            error=domain_result.error,
            correlation_id=request.correlation_id,
            metadata=MappingProxyType(
                {
                    "duration_ms": duration_ms,
                    "executed_stages": [
                        s.value for s in domain_result.executed_stages
                    ],
                }
            ),
        )

    def _resolve_state(
        self, results: tuple[PipelineResult, ...]
    ) -> OrchestrationState:
        if not results:
            return OrchestrationState.FAILED
        failures = [r for r in results if r.failed]
        executed = [r for r in results if not r.skipped]
        if failures and len(failures) == len(executed):
            return OrchestrationState.FAILED
        if failures:
            return OrchestrationState.PARTIAL
        if executed and all(r.succeeded for r in executed):
            return OrchestrationState.COMPLETED
        if not executed:
            return OrchestrationState.CANCELLED
        return OrchestrationState.PARTIAL

    def _primary_error(
        self, results: tuple[PipelineResult, ...]
    ) -> str | None:
        for result in results:
            if result.failed and result.error:
                return result.error
        return None

    def _event_from_request(
        self, request: OrchestrationRequest
    ) -> OrchestrationEvent:
        if not OrchestrationPolicy.is_known_event(request.event_type):
            raise OrchestrationError(
                f"Unknown orchestration event type: {request.event_type!r}"
            )
        return OrchestrationEvent.create(
            event_type=request.event_type,
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
            payload=dict(request.payload or {}),
            correlation_id=request.correlation_id,
        )
