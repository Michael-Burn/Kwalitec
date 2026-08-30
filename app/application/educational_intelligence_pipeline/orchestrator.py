"""Educational Pipeline Orchestrator — production coordination layer.

Executes the certified Educational Intelligence pipeline in lawful order:

  Assessment Evidence
    → Interpretation
    → Decision
    → Twin Update
    → Graph Projection
    → Mission Planning
    → Tutor Explanation

Coordinates existing certified stage services only. Introduces no educational
logic, heuristics, Twin semantics, Mission prioritisation, Tutor wording, or
Assessment behaviour. Emits operational events, privacy-safe logs, and
performance metrics.

ADR-027 Phase 2 Stage 3: this orchestrator + DecisionGenerator chain is a
test/cert harness only — it is not wired to student Home. It remains the
legacy SDT / Epic-2 certification path until a separate programme rewrites it
against Twin B. Sandbox retention matches resolution #3: Phase 2
implementation plus one subsequent review cycle, then remove unless claimed.
Functional behaviour is intentionally unchanged in Stage 3.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from time import perf_counter

from app.application.educational_intelligence_pipeline.events import (
    PipelineEventCollector,
)
from app.application.educational_intelligence_pipeline.metrics import MetricsCollector
from app.application.educational_intelligence_pipeline.observability import (
    log_pipeline_event,
    log_pipeline_summary,
)
from app.application.educational_intelligence_pipeline.result import (
    PipelineExecutionResult,
)
from app.application.educational_intelligence_pipeline.stages import PipelineStage
from app.application.educational_intelligence_pipeline.versions import (
    ORCHESTRATOR_VERSION,
)
from app.application.intelligent_tutor.explainability.tutor_explanation_service import (
    TutorExplanationService,
)
from app.application.learning_graph.projections.twin_projection_service import (
    TwinProjectionService,
)
from app.application.mission_engine.planning.mission_planning_service import (
    MissionPlanningService,
)
from app.application.reasoning.decisions.decision_generator import DecisionGenerator
from app.application.reasoning.decisions.twin_updater import TwinUpdater
from app.application.reasoning.interpretation.evidence_interpreter import (
    EvidenceInterpreter,
)
from app.domain.learning_graph.learning_graph import LearningGraph
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin
from application.assessment.evidence.dto import EvidenceBundleDTO


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class EducationalPipelineOrchestrator:
    """Production orchestrator for the certified Educational Intelligence Platform.

    Invokes stage authorities in certified order. Does not interpret evidence,
    generate decisions, update Twin belief logic, project graphs, plan missions,
    or author tutor explanations — those remain owned by their stage services.
    """

    version = ORCHESTRATOR_VERSION

    def __init__(
        self,
        *,
        interpreter: EvidenceInterpreter | None = None,
        decision_generator: DecisionGenerator | None = None,
        twin_updater: TwinUpdater | None = None,
        projection: TwinProjectionService | None = None,
        planning: MissionPlanningService | None = None,
        explanations: TutorExplanationService | None = None,
    ) -> None:
        self._interpreter = interpreter or EvidenceInterpreter()
        self._decisions = decision_generator or DecisionGenerator()
        self._twin_updater = twin_updater or TwinUpdater()
        self._projection = projection or TwinProjectionService()
        self._planning = planning or MissionPlanningService()
        self._explanations = explanations or TutorExplanationService()

    def execute(
        self,
        twin: StudentDigitalTwin,
        bundle: EvidenceBundleDTO,
        *,
        correlation_id: str,
        reasoning_request_id: str | None = None,
        pipeline_id: str | None = None,
        at: datetime | None = None,
        graph_id: str | None = None,
        persist: bool = False,
        learning_graph: LearningGraph | None = None,
    ) -> PipelineExecutionResult:
        """Run Evidence → Tutor Explanation via certified stage services.

        Args:
            twin: Current Student Digital Twin (pre-update).
            bundle: Assessment evidence bundle (AP-002C.1).
            correlation_id: Cross-system correlation token.
            reasoning_request_id: Optional reasoning request identity.
            pipeline_id: Optional pipeline run identity (generated when omitted).
            at: Fixed clock for deterministic stage invocation.
            graph_id: Optional Learning Graph identity.
            persist: Whether stage services may persist ledgers (default False).
            learning_graph: Optional existing Learning Graph.

        Returns:
            PipelineExecutionResult with stage artefacts and operational metadata.
        """
        when = at or _utc_now()
        run_id = (pipeline_id or "").strip() or f"eip-{uuid.uuid4().hex[:16]}"
        rrq = (reasoning_request_id or "").strip() or f"rrq-{uuid.uuid4().hex[:16]}"
        corr = (correlation_id or "").strip()
        student_id = twin.student.student_id
        session_id = getattr(bundle, "session_id", None)

        events = PipelineEventCollector()
        metrics = MetricsCollector()
        t0 = perf_counter()

        started = events.started(
            pipeline_id=run_id,
            correlation_id=corr,
            student_id=student_id,
            assessment_session_id=session_id,
            reasoning_request_id=rrq,
            occurred_at=when,
        )
        log_pipeline_event(started)

        interpretation = None
        decision_result = None
        updated = twin
        projection = None
        mission = None
        explanation = None
        graph = learning_graph
        current_stage: PipelineStage | None = None

        try:
            current_stage = PipelineStage.INTERPRETATION
            interpretation = self._run_stage(
                current_stage,
                events=events,
                metrics=metrics,
                pipeline_id=run_id,
                correlation_id=corr,
                student_id=student_id,
                assessment_session_id=session_id,
                reasoning_request_id=rrq,
                at=when,
                call=lambda: self._interpreter.interpret_bundle(
                    bundle,
                    correlation_id=corr,
                    reasoning_request_id=rrq,
                    interpreted_at=when,
                ),
            )

            current_stage = PipelineStage.DECISION
            decision_result = self._run_stage(
                current_stage,
                events=events,
                metrics=metrics,
                pipeline_id=run_id,
                correlation_id=corr,
                student_id=student_id,
                assessment_session_id=session_id,
                reasoning_request_id=rrq,
                at=when,
                call=lambda: self._decisions.generate(
                    interpretation.observation_set,
                    twin=twin,
                    correlation_id=corr,
                    session_id=interpretation.context.session_id,
                    decided_at=when,
                ),
            )

            current_stage = PipelineStage.TWIN_UPDATE
            updated = self._run_stage(
                current_stage,
                events=events,
                metrics=metrics,
                pipeline_id=run_id,
                correlation_id=corr,
                student_id=student_id,
                assessment_session_id=session_id,
                reasoning_request_id=rrq,
                at=when,
                call=lambda: self._twin_updater.apply(
                    twin,
                    decision_result.decision_set,
                    updated_at=when,
                ),
            )

            resolved_graph_id = graph_id or f"lg-{updated.twin_id}"
            current_stage = PipelineStage.GRAPH_PROJECTION
            projection = self._run_stage(
                current_stage,
                events=events,
                metrics=metrics,
                pipeline_id=run_id,
                correlation_id=corr,
                student_id=student_id,
                assessment_session_id=session_id,
                reasoning_request_id=rrq,
                at=when,
                call=lambda: self._projection.project(
                    updated,
                    decision_result.decision_set,
                    graph=graph,
                    graph_id=resolved_graph_id,
                    projected_at=when,
                    persist=persist,
                    allow_idempotent_skip=True,
                ),
            )

            if graph is None:
                graph = LearningGraph.create(
                    graph_id=resolved_graph_id,
                    twin_id=updated.twin_id,
                    student_id=updated.student.student_id,
                    created_at=when,
                )

            current_stage = PipelineStage.MISSION_PLANNING
            mission = self._run_stage(
                current_stage,
                events=events,
                metrics=metrics,
                pipeline_id=run_id,
                correlation_id=corr,
                student_id=student_id,
                assessment_session_id=session_id,
                reasoning_request_id=rrq,
                at=when,
                call=lambda: self._planning.plan(
                    updated,
                    decision_result.decision_set,
                    learning_graph=graph,
                    planned_at=when,
                    persist=persist,
                    allow_idempotent_skip=True,
                ),
            )

            current_stage = PipelineStage.TUTOR_EXPLANATION
            explanation = self._run_stage(
                current_stage,
                events=events,
                metrics=metrics,
                pipeline_id=run_id,
                correlation_id=corr,
                student_id=student_id,
                assessment_session_id=session_id,
                reasoning_request_id=rrq,
                at=when,
                call=lambda: self._explanations.explain(
                    updated,
                    decision_result.decision_set,
                    study_mission_plan=mission.study_mission_plan,
                    learning_graph=graph,
                    explained_at=when,
                    persist=persist,
                    allow_idempotent_skip=True,
                ),
            )
        except Exception as exc:  # noqa: BLE001 — classify as operational failure
            failure_cause = f"{exc.__class__.__name__}: {exc}"
            total_ms = (perf_counter() - t0) * 1000.0
            metrics.set_total(total_ms)
            failed = events.failed(
                pipeline_id=run_id,
                correlation_id=corr,
                student_id=student_id,
                assessment_session_id=session_id,
                reasoning_request_id=rrq,
                failure_cause=failure_cause,
                stage=current_stage,
                duration_ms=total_ms,
                occurred_at=when,
            )
            log_pipeline_event(failed)
            log_pipeline_summary(
                pipeline_id=run_id,
                correlation_id=corr,
                student_id=student_id,
                assessment_session_id=session_id,
                reasoning_request_id=rrq,
                outcome="failed",
                metrics=metrics.metrics,
                failure_cause=failure_cause,
            )
            return PipelineExecutionResult(
                pipeline_id=run_id,
                correlation_id=corr,
                student_id=student_id,
                assessment_session_id=session_id,
                reasoning_request_id=rrq,
                outcome="failed",
                twin=updated,
                observation_set=(
                    interpretation.observation_set if interpretation else None
                ),
                interpretation=interpretation,
                decision_set=(
                    decision_result.decision_set if decision_result else None
                ),
                decision_result=decision_result,
                projection=projection,
                mission=mission,
                explanation=explanation,
                learning_graph=graph,
                metrics=metrics.metrics,
                events=events.events,
                failed_stage=current_stage,
                failure_cause=failure_cause,
                errors=(failure_cause,),
            )

        total_ms = (perf_counter() - t0) * 1000.0
        metrics.set_total(total_ms)
        completed = events.completed(
            pipeline_id=run_id,
            correlation_id=corr,
            student_id=student_id,
            assessment_session_id=session_id,
            reasoning_request_id=rrq,
            duration_ms=total_ms,
            occurred_at=when,
        )
        log_pipeline_event(completed)
        log_pipeline_summary(
            pipeline_id=run_id,
            correlation_id=corr,
            student_id=student_id,
            assessment_session_id=session_id,
            reasoning_request_id=rrq,
            outcome="completed",
            metrics=metrics.metrics,
        )

        errors: list[str] = []
        if explanation is not None and not explanation.available:
            errors.append("explanation unavailable")

        return PipelineExecutionResult(
            pipeline_id=run_id,
            correlation_id=corr,
            student_id=student_id,
            assessment_session_id=session_id,
            reasoning_request_id=rrq,
            outcome="completed" if not errors else "failed",
            twin=updated,
            observation_set=interpretation.observation_set,
            interpretation=interpretation,
            decision_set=decision_result.decision_set,
            decision_result=decision_result,
            projection=projection,
            mission=mission,
            explanation=explanation,
            learning_graph=graph,
            metrics=metrics.metrics,
            events=events.events,
            failure_cause=("explanation unavailable" if errors else None),
            errors=tuple(errors),
        )

    def _run_stage(
        self,
        stage: PipelineStage,
        *,
        events: PipelineEventCollector,
        metrics: MetricsCollector,
        pipeline_id: str,
        correlation_id: str,
        student_id: str,
        assessment_session_id: str | None,
        reasoning_request_id: str,
        at: datetime,
        call,
    ):
        """Invoke one certified stage with operational instrumentation."""
        events.stage_started(
            pipeline_id=pipeline_id,
            correlation_id=correlation_id,
            stage=stage,
            student_id=student_id,
            assessment_session_id=assessment_session_id,
            reasoning_request_id=reasoning_request_id,
            occurred_at=at,
        )
        log_pipeline_event(events.events[-1])
        t = perf_counter()
        try:
            result = call()
        except Exception as exc:
            duration_ms = (perf_counter() - t) * 1000.0
            metrics.record(stage, duration_ms, succeeded=False)
            cause = f"{exc.__class__.__name__}: {exc}"
            failed = events.stage_failed(
                pipeline_id=pipeline_id,
                correlation_id=correlation_id,
                stage=stage,
                failure_cause=cause,
                duration_ms=duration_ms,
                student_id=student_id,
                assessment_session_id=assessment_session_id,
                reasoning_request_id=reasoning_request_id,
                occurred_at=at,
            )
            log_pipeline_event(failed)
            raise

        duration_ms = (perf_counter() - t) * 1000.0
        metrics.record(stage, duration_ms, succeeded=True)
        completed = events.stage_completed(
            pipeline_id=pipeline_id,
            correlation_id=correlation_id,
            stage=stage,
            duration_ms=duration_ms,
            student_id=student_id,
            assessment_session_id=assessment_session_id,
            reasoning_request_id=reasoning_request_id,
            occurred_at=at,
        )
        log_pipeline_event(completed)
        return result
