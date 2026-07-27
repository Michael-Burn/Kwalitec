"""AssessmentPipelineService — observe activity → Twin update → feedback.

Pipeline (deterministic):
  Learner Activity
    → Validation
    → Assessment Event
    → Observation Creation
    → StudentReasoningService
    → Student Digital Twin Update
    → Learning Feedback
    → Mission Refresh Trigger

Never performs educational reasoning. Never duplicates Twin state.
"""

from __future__ import annotations

import uuid
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from app.application.assessment_pipeline.persistence import (
    AssessmentPipelinePersistenceService,
)
from app.application.student_digital_twin.observation_service import ObservationService
from app.application.student_digital_twin.student_digital_twin_service import (
    StudentDigitalTwinService,
)
from app.application.student_digital_twin.student_reasoning_service import (
    StudentReasoningService,
)
from app.domain.assessment_pipeline.assessment_event import (
    AssessmentEvent,
    AssessmentEventType,
)
from app.domain.assessment_pipeline.assessment_pipeline import (
    prepare_pipeline_artifacts,
)
from app.domain.assessment_pipeline.assessment_result import AssessmentResult
from app.domain.assessment_pipeline.attempt import ActivityAttempt
from app.domain.assessment_pipeline.feedback_validator import (
    FeedbackValidationResult,
    validate_learning_feedback,
)
from app.domain.assessment_pipeline.learning_feedback import LearningFeedback
from app.domain.assessment_pipeline.performance_summary import PerformanceSummary
from app.domain.student_digital_twin.observation import Observation
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin
from app.extensions import db


@dataclass(frozen=True)
class PipelineRunResult:
    """Outcome of one assessment pipeline execution."""

    event: AssessmentEvent
    validation: FeedbackValidationResult
    observation: Observation | None
    result: AssessmentResult | None
    feedback: LearningFeedback | None
    twin: StudentDigitalTwin | None
    mission_refresh_triggered: bool = False
    refreshed_mission_id: str | None = None

    @property
    def ok(self) -> bool:
        return (
            self.validation.passed
            and self.observation is not None
            and self.result is not None
            and self.feedback is not None
        )


class AssessmentPipelineService:
    """Public facade for the Assessment & Learning Feedback Pipeline.

    Educational state updates only through StudentReasoningService.
    """

    ENGINE_VERSION = "ap001.assessment_pipeline_v1"

    def __init__(
        self,
        *,
        twins: StudentDigitalTwinService | None = None,
        observations: ObservationService | None = None,
        reasoning: StudentReasoningService | None = None,
        persistence: AssessmentPipelinePersistenceService | None = None,
    ) -> None:
        self._twins = twins or StudentDigitalTwinService()
        self._observations = observations or ObservationService()
        self._reasoning = reasoning or StudentReasoningService()
        self._persistence = persistence or AssessmentPipelinePersistenceService()

    def process(
        self,
        event: AssessmentEvent,
        *,
        persist: bool = True,
        reason: bool = True,
        refresh_mission: bool = False,
        available_minutes: int = 45,
    ) -> PipelineRunResult:
        """Run the full assessment → observation → reasoning → feedback pipeline."""
        twin = self._twins.get(event.twin_id)
        if twin is None:
            raise ValueError(f"Student Digital Twin {event.twin_id!r} not found")

        validation, observation, result, feedback = prepare_pipeline_artifacts(event)
        if not validation.passed or (
            observation is None or result is None or feedback is None
        ):
            return PipelineRunResult(
                event=event,
                validation=validation,
                observation=None,
                result=None,
                feedback=None,
                twin=twin,
            )

        feedback_validation = validate_learning_feedback(feedback)
        if not feedback_validation.passed:
            return PipelineRunResult(
                event=event,
                validation=feedback_validation,
                observation=observation,
                result=result,
                feedback=None,
                twin=twin,
            )

        updated, recorded = self._observations.record(
            twin,
            kind=observation.kind,
            curriculum_entity_id=observation.curriculum_entity_id,
            curriculum_entity_kind=observation.curriculum_entity_kind,
            evidence_reference=observation.evidence_reference,
            provenance=observation.provenance,
            metadata=dict(observation.metadata),
            recorded_at=observation.recorded_at,
            observation_id=observation.observation_id,
            persist=persist,
        )

        if reason:
            updated = self._reasoning.reason(
                updated,
                triggered_by=f"assessment_pipeline:{event.event_type.value}",
                observation_ids=(recorded.observation_id,),
                persist=persist,
            )

        if persist:
            self._persistence.save_event(event)
            self._persistence.save_result(result)
            self._persistence.save_feedback(feedback)
            attempt = self._attempt_from_event(event)
            if attempt is not None:
                self._persistence.save_attempt(attempt)
            if event.mission_id:
                self._persistence.save_mission_link(
                    twin_id=event.twin_id,
                    mission_id=event.mission_id,
                    event_id=event.event_id,
                    observation_id=recorded.observation_id,
                    step_id=event.step_id,
                    link_kind=(
                        "step"
                        if event.event_type
                        == AssessmentEventType.MISSION_STEP_COMPLETION
                        else "completion"
                    ),
                    created_at=event.occurred_at,
                )
            db.session.commit()

        mission_refresh_triggered = False
        refreshed_mission_id: str | None = None
        if refresh_mission and reason:
            refreshed_mission_id = self._trigger_mission_refresh(
                twin_id=updated.twin_id,
                available_minutes=available_minutes,
                persist=persist,
            )
            mission_refresh_triggered = refreshed_mission_id is not None

        return PipelineRunResult(
            event=event,
            validation=validation,
            observation=recorded,
            result=result,
            feedback=feedback,
            twin=updated,
            mission_refresh_triggered=mission_refresh_triggered,
            refreshed_mission_id=refreshed_mission_id,
        )

    def ingest(
        self,
        *,
        twin_id: str,
        event_type: AssessmentEventType | str,
        activity_id: str = "",
        curriculum_entity_id: str = "",
        curriculum_entity_kind: str = "",
        concept_ids: tuple[str, ...] | list[str] | None = None,
        mission_id: str = "",
        step_id: str = "",
        source: str = "assessment_pipeline",
        score: float | None = None,
        correct: bool | None = None,
        duration_seconds: int | None = None,
        metadata: Mapping[str, Any] | None = None,
        occurred_at: datetime | None = None,
        persist: bool = True,
        reason: bool = True,
        refresh_mission: bool = False,
        available_minutes: int = 45,
        event_id: str | None = None,
    ) -> PipelineRunResult:
        """Create an assessment event from activity inputs and process it."""
        twin = self._twins.get(twin_id)
        if twin is None:
            raise ValueError(f"Student Digital Twin {twin_id!r} not found")
        event = AssessmentEvent.create(
            event_id=event_id or f"aev-{uuid.uuid4().hex[:16]}",
            event_type=event_type,
            twin_id=twin.twin_id,
            student_id=twin.student.student_id,
            occurred_at=occurred_at,
            activity_id=activity_id,
            curriculum_entity_id=curriculum_entity_id,
            curriculum_entity_kind=curriculum_entity_kind,
            concept_ids=concept_ids,
            mission_id=mission_id,
            step_id=step_id,
            source=source,
            score=score,
            correct=correct,
            duration_seconds=duration_seconds,
            metadata=metadata,
        )
        return self.process(
            event,
            persist=persist,
            reason=reason,
            refresh_mission=refresh_mission,
            available_minutes=available_minutes,
        )

    def record_mission_step_completion(
        self,
        *,
        twin_id: str,
        mission_id: str,
        step_id: str,
        concept_ids: tuple[str, ...] | list[str] | None = None,
        curriculum_entity_id: str = "",
        score: float | None = None,
        outcome_achieved: bool = True,
        metadata: Mapping[str, Any] | None = None,
        occurred_at: datetime | None = None,
        persist: bool = True,
        reason: bool = True,
        refresh_mission: bool = False,
    ) -> PipelineRunResult:
        """Mission step completion → assessment event → Twin update."""
        meta = dict(metadata or {})
        meta.setdefault("outcome_achieved", outcome_achieved)
        return self.ingest(
            twin_id=twin_id,
            event_type=AssessmentEventType.MISSION_STEP_COMPLETION,
            activity_id=step_id,
            curriculum_entity_id=curriculum_entity_id
            or (concept_ids[0] if concept_ids else ""),
            curriculum_entity_kind=(
                "concept" if concept_ids or curriculum_entity_id else ""
            ),
            concept_ids=concept_ids,
            mission_id=mission_id,
            step_id=step_id,
            source="adaptive_mission",
            score=score,
            correct=outcome_achieved if score is None else None,
            metadata=meta,
            occurred_at=occurred_at,
            persist=persist,
            reason=reason,
            refresh_mission=refresh_mission,
        )

    def record_mission_completion(
        self,
        *,
        twin_id: str,
        mission_id: str,
        concept_ids: tuple[str, ...] | list[str] | None = None,
        curriculum_entity_id: str = "",
        outcome_achieved: bool = True,
        reflection_response: str = "",
        feedback_summary: str = "",
        metadata: Mapping[str, Any] | None = None,
        occurred_at: datetime | None = None,
        persist: bool = True,
        reason: bool = True,
        refresh_mission: bool = True,
        available_minutes: int = 45,
    ) -> PipelineRunResult:
        """Mission completion → assessment event → Twin update → mission refresh."""
        meta = dict(metadata or {})
        meta.setdefault("outcome_achieved", outcome_achieved)
        if reflection_response:
            meta["reflection_response"] = reflection_response
        if feedback_summary:
            meta["feedback_summary"] = feedback_summary
        return self.ingest(
            twin_id=twin_id,
            event_type=AssessmentEventType.MISSION_COMPLETION,
            activity_id=mission_id,
            curriculum_entity_id=curriculum_entity_id
            or (concept_ids[0] if concept_ids else ""),
            curriculum_entity_kind=(
                "concept" if concept_ids or curriculum_entity_id else ""
            ),
            concept_ids=concept_ids,
            mission_id=mission_id,
            source="adaptive_mission",
            correct=outcome_achieved,
            metadata=meta,
            occurred_at=occurred_at,
            persist=persist,
            reason=reason,
            refresh_mission=refresh_mission,
            available_minutes=available_minutes,
        )

    def summarise_performance(
        self,
        twin_id: str,
        *,
        persist: bool = True,
        generated_at: datetime | None = None,
    ) -> PerformanceSummary:
        """Build a deterministic performance summary from assessment evidence."""
        twin = self._twins.get(twin_id)
        if twin is None:
            raise ValueError(f"Student Digital Twin {twin_id!r} not found")
        events = self._persistence.list_events_for_twin(twin_id, limit=500)
        when = generated_at or datetime.now(UTC).replace(tzinfo=None)
        correct = sum(1 for e in events if e.correct is True)
        incorrect = sum(1 for e in events if e.correct is False)
        scores = [float(e.score) for e in events if e.score is not None]
        concepts: list[str] = []
        for event in events:
            concepts.extend(event.concept_ids)
            if event.curriculum_entity_id:
                concepts.append(event.curriculum_entity_id)
        summary = PerformanceSummary(
            summary_id=f"aps-{uuid.uuid4().hex[:16]}",
            twin_id=twin_id,
            student_id=twin.student.student_id,
            event_count=len(events),
            attempt_count=sum(
                1
                for e in events
                if e.event_type
                in {
                    AssessmentEventType.QUESTION_ATTEMPT,
                    AssessmentEventType.QUIZ_SUBMISSION,
                    AssessmentEventType.FORMULA_RECALL,
                }
            ),
            correct_count=correct,
            incorrect_count=incorrect,
            mean_score=(sum(scores) / len(scores)) if scores else None,
            concepts_touched=tuple(dict.fromkeys(concepts)),
            generated_at=when,
            window_end=when,
            window_start=min((e.occurred_at for e in events), default=None),
        )
        if persist:
            self._persistence.save_performance_summary(summary)
            db.session.commit()
        return summary

    def list_events(self, twin_id: str, *, limit: int = 100) -> list[AssessmentEvent]:
        return self._persistence.list_events_for_twin(twin_id, limit=limit)

    def list_results(self, twin_id: str, *, limit: int = 100) -> list[AssessmentResult]:
        return self._persistence.list_results_for_twin(twin_id, limit=limit)

    def list_feedback(
        self, twin_id: str, *, limit: int = 100
    ) -> list[LearningFeedback]:
        return self._persistence.list_feedback_for_twin(twin_id, limit=limit)

    def diagnostics_for_twin(self, twin_id: str) -> dict[str, Any]:
        twin = self._twins.get(twin_id)
        if twin is None:
            return {"ok": False, "error": f"twin {twin_id!r} not found"}
        events = self.list_events(twin_id, limit=50)
        results = self.list_results(twin_id, limit=50)
        feedback = self.list_feedback(twin_id, limit=50)
        links = self._persistence.list_mission_links(twin_id=twin_id)
        summary = self.summarise_performance(twin_id, persist=False)
        return {
            "ok": True,
            "engine_version": self.ENGINE_VERSION,
            "twin_id": twin_id,
            "observation_count": len(twin.observations),
            "event_count": len(events),
            "result_count": len(results),
            "feedback_count": len(feedback),
            "mission_link_count": len(links),
            "performance": {
                "event_count": summary.event_count,
                "attempt_count": summary.attempt_count,
                "correct_count": summary.correct_count,
                "incorrect_count": summary.incorrect_count,
                "mean_score": summary.mean_score,
                "accuracy": summary.accuracy,
                "concepts_touched": list(summary.concepts_touched),
            },
            "recent_event_types": [e.event_type.value for e in events[:10]],
            "delegates_reasoning_to": "StudentReasoningService",
            "duplicates_twin_state": False,
        }

    def event_as_dict(self, event: AssessmentEvent) -> dict[str, Any]:
        return self._persistence.event_as_dict(event)

    def result_as_dict(self, result: AssessmentResult) -> dict[str, Any]:
        return self._persistence.result_as_dict(result)

    def feedback_as_dict(self, feedback: LearningFeedback) -> dict[str, Any]:
        return self._persistence.feedback_as_dict(feedback)

    def _attempt_from_event(self, event: AssessmentEvent) -> ActivityAttempt | None:
        if event.event_type not in {
            AssessmentEventType.QUESTION_ATTEMPT,
            AssessmentEventType.QUIZ_SUBMISSION,
            AssessmentEventType.FORMULA_RECALL,
        }:
            return None
        return ActivityAttempt(
            attempt_id=f"att-{uuid.uuid4().hex[:16]}",
            twin_id=event.twin_id,
            student_id=event.student_id,
            activity_id=event.activity_id or event.event_id,
            activity_kind=event.event_type.value,
            attempted_at=event.occurred_at,
            event_id=event.event_id,
            curriculum_entity_id=event.curriculum_entity_id,
            concept_ids=event.concept_ids,
            score=event.score,
            correct=event.correct,
            duration_seconds=event.duration_seconds,
            metadata=dict(event.metadata),
        )

    def _trigger_mission_refresh(
        self,
        *,
        twin_id: str,
        available_minutes: int,
        persist: bool,
    ) -> str | None:
        """Best-effort Adaptive Mission refresh from updated Twin state.

        Lazy-imported to avoid circular imports with AdaptiveMissionService.
        """
        try:
            from app.application.adaptive_mission.adaptive_mission_service import (
                AdaptiveMissionService,
            )

            mission = AdaptiveMissionService().generate_for_twin(
                twin_id,
                available_minutes=available_minutes,
                activate=True,
                persist=persist,
            )
            return mission.mission_id
        except Exception:  # noqa: BLE001 — refresh is best-effort after feedback
            return None
