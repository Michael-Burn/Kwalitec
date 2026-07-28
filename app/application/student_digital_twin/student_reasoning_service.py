"""StudentReasoningService — Twin orchestration via Educational Reasoning Engine.

Educational logic lives in ``app.domain.educational_reasoning`` (RuleRegistry).
This service:
  1. Interprets Assessment Evidence into EducationalObservationSet (AP-002D2)
  2. Derives EducationalDecisionSet and applies Twin belief (AP-002D3)
  3. Delegates inference to EducationalReasoningService / engine
  4. Applies results onto the Student Digital Twin aggregate
  5. Adds prediction scaffolds (framework only)
  6. Persists Twin inferences + Twin reasoning_history (SDT-001)
  7. Relies on EducationalReasoningService for engine audit tables (SDT-002)

Interpretation (AP-002D2) does not update Twin belief. AP-002D3 consumes
EducationalObservationSet into validated EducationalDecisionSet and applies
belief updates without storing observations on the Twin. Mission, Tutor, and
Learning Graph remain untouched on the D3 path.

No LLM. No educational decisions outside StudentReasoningService authority.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.application.curriculum_retrieval.curriculum_retrieval_service import (
    CurriculumRetrievalService,
)
from app.application.educational_reasoning.educational_reasoning_service import (
    EducationalReasoningService,
)
from app.application.learning_graph.learning_graph_service import LearningGraphService
from app.application.student_digital_twin.knowledge_gap_service import (
    KnowledgeGapService,
)
from app.application.student_digital_twin.learning_state_service import (
    LearningStateService,
)
from app.application.student_digital_twin.mastery_service import MasteryService
from app.application.student_digital_twin.persistence import TwinPersistenceService
from app.application.student_digital_twin.prediction_service import PredictionService
from app.application.student_digital_twin.recommendation_service import (
    RecommendationService,
)
from app.domain.educational_reasoning.reasoning_engine import ENGINE_VERSION
from app.domain.educational_reasoning.reasoning_result import ReasoningResult
from app.domain.student_digital_twin.reasoning import ReasoningRecord, ReasoningStep
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin
from app.domain.student_digital_twin.timeline import TimelineEvent, TimelineEventKind
from app.extensions import db


class StudentReasoningService:
    """Twin update orchestrator — delegates educational logic to the engine."""

    def __init__(
        self,
        *,
        mastery: MasteryService | None = None,
        learning_state: LearningStateService | None = None,
        knowledge_gaps: KnowledgeGapService | None = None,
        recommendations: RecommendationService | None = None,
        predictions: PredictionService | None = None,
        persistence: TwinPersistenceService | None = None,
        retrieval: CurriculumRetrievalService | None = None,
        educational_reasoning: EducationalReasoningService | None = None,
        learning_graph: LearningGraphService | None = None,
    ) -> None:
        retrieval_svc = retrieval or CurriculumRetrievalService()
        graph_svc = learning_graph or LearningGraphService()
        # Compatibility facades (tests may still call _mastery.recompute etc.).
        self._mastery = mastery or MasteryService()
        self._learning_state = learning_state or LearningStateService()
        self._gaps = knowledge_gaps or KnowledgeGapService(retrieval=retrieval_svc)
        self._recommendations = recommendations or RecommendationService()
        self._predictions = predictions or PredictionService()
        self._persistence = persistence or TwinPersistenceService()
        self._learning_graph = graph_svc
        self._educational = educational_reasoning or EducationalReasoningService(
            retrieval=retrieval_svc,
            learning_graph=graph_svc,
        )

    @property
    def educational_reasoning(self) -> EducationalReasoningService:
        return self._educational

    def reason(
        self,
        twin: StudentDigitalTwin,
        *,
        triggered_by: str = "manual",
        observation_ids: tuple[str, ...] | None = None,
        persist: bool = True,
    ) -> StudentDigitalTwin:
        """Recompute Twin inferences via the Educational Reasoning Engine."""
        now = datetime.now(UTC).replace(tzinfo=None)
        obs_ids = observation_ids or tuple(o.observation_id for o in twin.observations)

        engine_result = self._educational.reason_for_twin(
            twin,
            triggered_by=triggered_by,
            observation_ids=obs_ids,
            persist=persist,
            computed_at=now,
        )

        updated = self._apply_engine_result(
            twin,
            engine_result,
            observation_ids=obs_ids,
            triggered_by=triggered_by,
            persist=persist,
            computed_at=now,
        )

        # Refresh Learning Graph mastery projections after Twin inferences settle.
        if persist:
            self._learning_graph.refresh_projections(
                updated, computed_at=now, persist=True
            )
            db.session.commit()

        return updated

    def accept_assessment_evidence(
        self,
        twin: StudentDigitalTwin,
        *,
        bundle,
        correlation_id: str,
        reasoning_request_id: str | None = None,
        persist: bool = True,
        submissions=None,
    ):
        """AP-002D1 ingress: accept Assessment EvidenceBundle via AP-001 boundary.

        Validates the evidence contract, maps facts onto Twin observations through
        existing ObservationService pathways, then delegates to ``reason()``.
        No new educational algorithms.
        """
        from app.application.assessment_pipeline.evidence_ingress import (
            EvidenceIngressRequest,
            EvidenceIngressService,
        )

        return EvidenceIngressService(
            reasoning=self,
            submissions=submissions,
        ).accept(
            EvidenceIngressRequest(
                twin_id=twin.twin_id,
                bundle=bundle,
                correlation_id=correlation_id,
                reasoning_request_id=reasoning_request_id,
            ),
            twin=twin,
            persist=persist,
            reason=True,
        )

    def interpret_assessment_evidence(
        self,
        *,
        bundle,
        correlation_id: str,
        reasoning_request_id: str | None = None,
        interpreted_at=None,
        as_dto: bool = False,
    ):
        """AP-002D2: interpret Assessment Evidence into EducationalObservationSet.

        Deterministic interpretation only. Does **not** update the Student Digital
        Twin, Mission Engine, Learning Graph, or Tutor. Does not estimate mastery
        or produce recommendations. Output is ready for later Twin consumption.
        """
        from app.application.reasoning.dto.interpretation_dto import (
            InterpretationRequestDTO,
        )
        from app.application.reasoning.interpretation.evidence_interpreter import (
            EvidenceInterpreter,
        )
        from app.application.reasoning.mappers.evidence_mapper import (
            map_interpretation_result,
        )

        result = EvidenceInterpreter().interpret(
            InterpretationRequestDTO(
                bundle=bundle,
                correlation_id=correlation_id,
                reasoning_request_id=reasoning_request_id,
            ),
            interpreted_at=interpreted_at,
        )
        if as_dto:
            return map_interpretation_result(result)
        return result

    def consume_educational_observations(
        self,
        twin: StudentDigitalTwin,
        observation_set,
        *,
        correlation_id: str,
        session_id: str | None = None,
        decided_at=None,
        persist: bool = True,
        as_dto: bool = False,
    ):
        """AP-002D3: EducationalObservationSet → EducationalDecisionSet → Twin.

        Generates validated educational decisions from immutable observations
        and applies them to Twin belief. Does **not** append observations to
        the Twin, refresh Learning Graph, trigger Mission, or Tutor.
        Does not generate recommendations or estimate exam readiness.
        """
        from app.application.reasoning.decisions.decision_generator import (
            DecisionGenerator,
        )
        from app.application.reasoning.decisions.twin_updater import TwinUpdater
        from app.application.reasoning.mappers.decision_mapper import (
            map_decision_result,
        )

        decision_result = DecisionGenerator().generate(
            observation_set,
            twin=twin,
            correlation_id=correlation_id,
            session_id=session_id,
            decided_at=decided_at,
        )
        updated = TwinUpdater().apply(
            twin,
            decision_result.decision_set,
            updated_at=decided_at,
        )
        if persist:
            self._persistence.replace_inferences(updated)
            db.session.commit()
        if as_dto:
            return updated, map_decision_result(decision_result)
        return updated, decision_result

    def integrate_assessment_evidence(
        self,
        twin: StudentDigitalTwin,
        *,
        bundle,
        correlation_id: str,
        reasoning_request_id: str | None = None,
        interpreted_at=None,
        persist: bool = True,
        as_dto: bool = False,
    ):
        """AP-002D3 end-to-end: Evidence Bundle → observations → decisions → Twin.

        Sole authority path for Assessment evidence to influence Twin belief
        without Mission / Tutor / Learning Graph side effects.
        """
        interpretation = self.interpret_assessment_evidence(
            bundle=bundle,
            correlation_id=correlation_id,
            reasoning_request_id=reasoning_request_id,
            interpreted_at=interpreted_at,
            as_dto=False,
        )
        return self.consume_educational_observations(
            twin,
            interpretation.observation_set,
            correlation_id=correlation_id,
            session_id=interpretation.context.session_id,
            decided_at=interpreted_at,
            persist=persist,
            as_dto=as_dto,
        )

    def _apply_engine_result(
        self,
        twin: StudentDigitalTwin,
        engine_result: ReasoningResult,
        *,
        observation_ids: tuple[str, ...],
        triggered_by: str,
        persist: bool,
        computed_at: datetime,
    ) -> StudentDigitalTwin:
        mastery = engine_result.mastery
        learning_state = engine_result.learning_state
        confidence = engine_result.confidence
        gaps = engine_result.gaps
        recommendations = engine_result.recommendations

        predictions = self._predictions.scaffold(
            twin_id=twin.twin_id,
            learning_state=learning_state,
            mastery=mastery,
            observation_ids=observation_ids,
        )

        steps = _steps_from_engine(engine_result)
        steps = (
            *steps,
            ReasoningStep(
                code="predictions",
                detail="Prediction scaffolds (framework only)",
                outputs={"prediction_count": len(predictions)},
            ),
        )

        reasoning = ReasoningRecord(
            reasoning_id=engine_result.run_id,
            twin_id=twin.twin_id,
            triggered_by=triggered_by,
            observation_ids=observation_ids,
            steps=steps,
            summary=engine_result.summary,
            created_at=computed_at,
            reasoning_version=ENGINE_VERSION,
        )

        timeline_events = (
            TimelineEvent(
                event_id=f"tl-rsn-{reasoning.reasoning_id}",
                twin_id=twin.twin_id,
                kind=TimelineEventKind.REASONING,
                occurred_at=computed_at,
                summary=reasoning.summary,
                reference_id=reasoning.reasoning_id,
            ),
            TimelineEvent(
                event_id=f"tl-state-{learning_state.snapshot_id}",
                twin_id=twin.twin_id,
                kind=TimelineEventKind.STATE_SNAPSHOT,
                occurred_at=computed_at,
                summary="Learning state snapshot",
                reference_id=learning_state.snapshot_id,
            ),
        )

        updated = twin.with_inferences(
            learning_state=learning_state,
            mastery=mastery,
            knowledge_gaps=gaps,
            confidence=confidence,
            recommendations=recommendations,
            predictions=predictions,
            reasoning=reasoning,
            timeline_events=timeline_events,
            updated_at=computed_at,
        )

        if persist:
            self._persistence.replace_inferences(updated)
            db.session.commit()
        return updated


def _steps_from_engine(result: ReasoningResult) -> tuple[ReasoningStep, ...]:
    steps: list[ReasoningStep] = []
    for execution in result.executions:
        steps.append(
            ReasoningStep(
                code=execution.rule_code,
                detail=execution.explanation.summary,
                inputs=dict(execution.inputs),
                outputs=dict(execution.outputs),
            )
        )
    return tuple(steps)
