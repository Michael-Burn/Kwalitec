"""Educational Intelligence Platform certification pipeline harness.

Runs the complete certified pipeline using existing stage authorities only:

  Evidence Bundle
    → Interpretation (AP-002D2)
    → Decision + Twin (AP-002D3)
    → Projection (AP-002D4)
    → Mission Planning (AP-002D5)
    → Tutor Explanation (AP-002D6)

Does not introduce a production orchestrator and does not change stage authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from time import perf_counter

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
from app.domain.intelligent_tutor.explainability.result import ExplanationResult
from app.domain.learning_graph.learning_graph import LearningGraph
from app.domain.learning_graph.projections.result import ProjectionResult
from app.domain.mission.planning.result import PlanningResult
from app.domain.reasoning.decisions.decision_set import EducationalDecisionSet
from app.domain.reasoning.decisions.result import DecisionResult
from app.domain.reasoning.interpretation.result import InterpretationResult
from app.domain.reasoning.observations.observation_set import EducationalObservationSet
from app.domain.student_digital_twin.student import Student
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin
from application.assessment.evidence.dto import EvidenceBundleDTO
from tests.certification.educational_intelligence.fingerprints import (
    PipelineFingerprints,
    build_fingerprints,
)
from tests.certification.educational_intelligence.fixtures import (
    CERT_FIXED_AT,
    ReplayFixture,
)
from tests.certification.educational_intelligence.provenance import (
    ProvenanceChain,
    audit_provenance,
)


@dataclass(frozen=True, slots=True)
class StageTimings:
    """Per-stage wall-clock timings in milliseconds (baseline only)."""

    interpretation_ms: float
    decision_ms: float
    twin_ms: float
    projection_ms: float
    mission_ms: float
    explanation_ms: float
    total_ms: float


@dataclass(frozen=True, slots=True)
class PipelineCertificationResult:
    """Full certified pipeline outcome for one evidence cycle."""

    twin: StudentDigitalTwin
    observation_set: EducationalObservationSet
    interpretation: InterpretationResult
    decision_set: EducationalDecisionSet
    decision_result: DecisionResult
    projection: ProjectionResult
    mission: PlanningResult
    explanation: ExplanationResult
    fingerprints: PipelineFingerprints
    provenance: ProvenanceChain
    timings: StageTimings
    learning_graph: LearningGraph | None = None
    errors: tuple[str, ...] = field(default_factory=tuple)

    @property
    def certified(self) -> bool:
        return self.provenance.is_complete and not self.errors


class EducationalIntelligencePipelineHarness:
    """Certification harness — sequential stage invocation, no new authority."""

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

    def make_cold_start_twin(
        self,
        *,
        twin_id: str,
        student_id: str,
        created_at: datetime = CERT_FIXED_AT,
    ) -> StudentDigitalTwin:
        return StudentDigitalTwin.create(
            twin_id=twin_id,
            student=Student(
                student_id=student_id,
                display_name="Certification Learner",
            ),
            created_at=created_at,
        )

    def run(
        self,
        twin: StudentDigitalTwin,
        bundle: EvidenceBundleDTO,
        *,
        correlation_id: str,
        reasoning_request_id: str,
        at: datetime = CERT_FIXED_AT,
        graph_id: str | None = None,
        persist: bool = False,
        learning_graph: LearningGraph | None = None,
    ) -> PipelineCertificationResult:
        """Execute Evidence → Explanation and audit provenance + fingerprints."""
        t0 = perf_counter()

        t = perf_counter()
        interpretation = self._interpreter.interpret_bundle(
            bundle,
            correlation_id=correlation_id,
            reasoning_request_id=reasoning_request_id,
            interpreted_at=at,
        )
        interpretation_ms = (perf_counter() - t) * 1000.0

        t = perf_counter()
        decision_result = self._decisions.generate(
            interpretation.observation_set,
            twin=twin,
            correlation_id=correlation_id,
            session_id=interpretation.context.session_id,
            decided_at=at,
        )
        decision_ms = (perf_counter() - t) * 1000.0

        t = perf_counter()
        updated = self._twin_updater.apply(
            twin,
            decision_result.decision_set,
            updated_at=at,
        )
        twin_ms = (perf_counter() - t) * 1000.0

        resolved_graph_id = graph_id or f"lg-cert-{updated.twin_id}"
        t = perf_counter()
        projection = self._projection.project(
            updated,
            decision_result.decision_set,
            graph=learning_graph,
            graph_id=resolved_graph_id,
            projected_at=at,
            persist=persist,
            allow_idempotent_skip=True,
        )
        projection_ms = (perf_counter() - t) * 1000.0

        graph = learning_graph
        if graph is None:
            graph = LearningGraph.create(
                graph_id=resolved_graph_id,
                twin_id=updated.twin_id,
                student_id=updated.student.student_id,
                created_at=at,
            )

        t = perf_counter()
        mission = self._planning.plan(
            updated,
            decision_result.decision_set,
            learning_graph=graph,
            planned_at=at,
            persist=persist,
            allow_idempotent_skip=True,
        )
        mission_ms = (perf_counter() - t) * 1000.0

        t = perf_counter()
        explanation = self._explanations.explain(
            updated,
            decision_result.decision_set,
            study_mission_plan=mission.study_mission_plan,
            learning_graph=graph,
            explained_at=at,
            persist=persist,
            allow_idempotent_skip=True,
        )
        explanation_ms = (perf_counter() - t) * 1000.0
        total_ms = (perf_counter() - t0) * 1000.0

        fingerprints = build_fingerprints(
            observation_set=interpretation.observation_set,
            decision_set=decision_result.decision_set,
            twin=updated,
            projection=projection,
            mission=mission,
            explanation=explanation,
        )
        provenance = audit_provenance(
            observation_set=interpretation.observation_set,
            decision_set=decision_result.decision_set,
            twin=updated,
            projection=projection,
            mission=mission,
            explanation=explanation,
        )
        errors: list[str] = []
        if not explanation.available:
            errors.append("explanation unavailable")
        if not provenance.is_complete:
            errors.extend(provenance.broken_links)

        return PipelineCertificationResult(
            twin=updated,
            observation_set=interpretation.observation_set,
            interpretation=interpretation,
            decision_set=decision_result.decision_set,
            decision_result=decision_result,
            projection=projection,
            mission=mission,
            explanation=explanation,
            fingerprints=fingerprints,
            provenance=provenance,
            timings=StageTimings(
                interpretation_ms=interpretation_ms,
                decision_ms=decision_ms,
                twin_ms=twin_ms,
                projection_ms=projection_ms,
                mission_ms=mission_ms,
                explanation_ms=explanation_ms,
                total_ms=total_ms,
            ),
            learning_graph=graph,
            errors=tuple(errors),
        )

    def run_fixture(
        self,
        fixture: ReplayFixture,
        *,
        twin: StudentDigitalTwin | None = None,
        at: datetime = CERT_FIXED_AT,
        persist: bool = False,
    ) -> PipelineCertificationResult:
        """Run a named replay fixture through the full certified pipeline."""
        twin = twin or self.make_cold_start_twin(
            twin_id=fixture.twin_id,
            student_id=fixture.student_id,
            created_at=at,
        )
        return self.run(
            twin,
            fixture.bundle,
            correlation_id=fixture.correlation_id,
            reasoning_request_id=fixture.reasoning_request_id,
            at=at,
            graph_id=f"lg-{fixture.scenario.value}",
            persist=persist,
        )

    def replay(
        self,
        twin: StudentDigitalTwin,
        bundle: EvidenceBundleDTO,
        *,
        correlation_id: str,
        reasoning_request_id: str,
        at: datetime = CERT_FIXED_AT,
        graph_id: str | None = None,
    ) -> PipelineCertificationResult:
        """Second pass with fresh stage services — must match fingerprints."""
        return EducationalIntelligencePipelineHarness().run(
            twin,
            bundle,
            correlation_id=correlation_id,
            reasoning_request_id=reasoning_request_id,
            at=at,
            graph_id=graph_id,
            persist=False,
        )
