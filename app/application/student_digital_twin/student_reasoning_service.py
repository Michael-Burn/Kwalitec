"""StudentReasoningService — Twin orchestration via Educational Reasoning Engine.

Educational logic lives in ``app.domain.educational_reasoning`` (RuleRegistry).
This service:
  1. Delegates inference to EducationalReasoningService / engine
  2. Applies results onto the Student Digital Twin aggregate
  3. Adds prediction scaffolds (framework only)
  4. Persists Twin inferences + Twin reasoning_history (SDT-001)
  5. Relies on EducationalReasoningService for engine audit tables (SDT-002)

No LLM. No educational decisions outside the engine.
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
