"""Pipeline execution result — operational envelope around stage artefacts."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.application.educational_intelligence_pipeline.events import PipelineEvent
from app.application.educational_intelligence_pipeline.metrics import PipelineMetrics
from app.application.educational_intelligence_pipeline.stages import PipelineStage
from app.domain.intelligent_tutor.explainability.result import ExplanationResult
from app.domain.learning_graph.learning_graph import LearningGraph
from app.domain.learning_graph.projections.result import ProjectionResult
from app.domain.mission.planning.result import PlanningResult
from app.domain.reasoning.decisions.decision_set import EducationalDecisionSet
from app.domain.reasoning.decisions.result import DecisionResult
from app.domain.reasoning.interpretation.result import InterpretationResult
from app.domain.reasoning.observations.observation_set import EducationalObservationSet
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin


@dataclass(frozen=True, slots=True)
class PipelineExecutionResult:
    """Outcome of one Educational Intelligence pipeline run.

    Educational artefacts are passed through unchanged from certified stages.
    Operational fields (events, metrics, outcome) are orchestration-only.
    """

    pipeline_id: str
    correlation_id: str
    student_id: str
    assessment_session_id: str | None
    reasoning_request_id: str
    outcome: str  # completed | failed
    twin: StudentDigitalTwin | None
    observation_set: EducationalObservationSet | None
    interpretation: InterpretationResult | None
    decision_set: EducationalDecisionSet | None
    decision_result: DecisionResult | None
    projection: ProjectionResult | None
    mission: PlanningResult | None
    explanation: ExplanationResult | None
    learning_graph: LearningGraph | None
    metrics: PipelineMetrics
    events: tuple[PipelineEvent, ...]
    failed_stage: PipelineStage | None = None
    failure_cause: str | None = None
    errors: tuple[str, ...] = field(default_factory=tuple)

    @property
    def succeeded(self) -> bool:
        return self.outcome == "completed" and not self.errors
