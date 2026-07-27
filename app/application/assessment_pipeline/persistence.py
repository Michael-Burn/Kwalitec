"""Persistence for Assessment & Learning Feedback Pipeline (AP-001).

Stores assessment metadata only — never Twin mastery / gap / recommendation rows.
"""

from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from typing import Any

from app.domain.assessment_pipeline.assessment_event import (
    AssessmentEvent,
    AssessmentEventType,
)
from app.domain.assessment_pipeline.assessment_result import AssessmentResult
from app.domain.assessment_pipeline.attempt import ActivityAttempt
from app.domain.assessment_pipeline.feedback_source import FeedbackSource
from app.domain.assessment_pipeline.learning_feedback import LearningFeedback
from app.domain.assessment_pipeline.performance_summary import PerformanceSummary
from app.extensions import db
from app.models.assessment_pipeline import (
    ApActivityAttempt,
    ApAssessmentEvent,
    ApAssessmentResult,
    ApLearningFeedback,
    ApMissionAssessmentLink,
    ApPerformanceSummary,
)


def _dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)


def _loads(raw: str | None, default: Any) -> Any:
    if not raw:
        return default
    return json.loads(raw)


class AssessmentPipelinePersistenceService:
    """Load and persist assessment pipeline artefacts."""

    def save_event(self, event: AssessmentEvent) -> ApAssessmentEvent:
        existing = ApAssessmentEvent.query.filter_by(event_id=event.event_id).first()
        if existing is not None:
            return existing
        row = ApAssessmentEvent(
            event_id=event.event_id,
            event_type=event.event_type.value,
            twin_id=event.twin_id,
            student_id=event.student_id,
            occurred_at=event.occurred_at,
            activity_id=event.activity_id or "",
            curriculum_entity_id=event.curriculum_entity_id or "",
            curriculum_entity_kind=event.curriculum_entity_kind or "",
            concept_ids_json=_dumps(list(event.concept_ids)),
            mission_id=event.mission_id or "",
            step_id=event.step_id or "",
            source=event.source or "",
            score=event.score,
            correct=event.correct,
            duration_seconds=event.duration_seconds,
            metadata_json=_dumps(dict(event.metadata)),
            created_at=event.occurred_at,
        )
        db.session.add(row)
        return row

    def save_result(self, result: AssessmentResult) -> ApAssessmentResult:
        existing = ApAssessmentResult.query.filter_by(
            result_id=result.result_id
        ).first()
        if existing is not None:
            return existing
        row = ApAssessmentResult(
            result_id=result.result_id,
            event_id=result.event_id,
            twin_id=result.twin_id,
            event_type=result.event_type.value,
            observation_id=result.observation_id,
            performance_label=result.performance_label,
            evidence_json=_dumps(list(result.evidence_generated)),
            concepts_json=_dumps(list(result.concepts_covered)),
            confidence=result.confidence,
            metadata_json=_dumps(dict(result.metadata)),
            created_at=result.created_at,
        )
        db.session.add(row)
        return row

    def save_feedback(self, feedback: LearningFeedback) -> ApLearningFeedback:
        existing = ApLearningFeedback.query.filter_by(
            feedback_id=feedback.feedback_id
        ).first()
        if existing is not None:
            return existing
        row = ApLearningFeedback(
            feedback_id=feedback.feedback_id,
            twin_id=feedback.twin_id,
            event_id=feedback.event_id,
            result_id=feedback.result_id,
            activity=feedback.activity,
            performance=feedback.performance,
            evidence_json=_dumps(list(feedback.evidence_generated)),
            concepts_json=_dumps(list(feedback.concepts_covered)),
            confidence=feedback.confidence,
            suggested_next_action=feedback.suggested_next_action,
            timestamp=feedback.timestamp,
            source=feedback.source.value,
            observation_id=feedback.observation_id or "",
            mission_id=feedback.mission_id or "",
            metadata_json=_dumps(dict(feedback.metadata)),
        )
        db.session.add(row)
        return row

    def save_attempt(self, attempt: ActivityAttempt) -> ApActivityAttempt:
        existing = ApActivityAttempt.query.filter_by(
            attempt_id=attempt.attempt_id
        ).first()
        if existing is not None:
            return existing
        row = ApActivityAttempt(
            attempt_id=attempt.attempt_id,
            twin_id=attempt.twin_id,
            student_id=attempt.student_id,
            activity_id=attempt.activity_id,
            activity_kind=attempt.activity_kind,
            attempted_at=attempt.attempted_at,
            event_id=attempt.event_id or "",
            curriculum_entity_id=attempt.curriculum_entity_id or "",
            concept_ids_json=_dumps(list(attempt.concept_ids)),
            score=attempt.score,
            correct=attempt.correct,
            duration_seconds=attempt.duration_seconds,
            metadata_json=_dumps(dict(attempt.metadata)),
        )
        db.session.add(row)
        return row

    def save_mission_link(
        self,
        *,
        twin_id: str,
        mission_id: str,
        event_id: str,
        observation_id: str = "",
        step_id: str = "",
        link_kind: str = "completion",
        created_at: datetime | None = None,
    ) -> ApMissionAssessmentLink:
        existing = ApMissionAssessmentLink.query.filter_by(
            mission_id=mission_id, event_id=event_id
        ).first()
        if existing is not None:
            return existing
        row = ApMissionAssessmentLink(
            link_id=f"mal-{uuid.uuid4().hex[:16]}",
            twin_id=twin_id,
            mission_id=mission_id,
            event_id=event_id,
            observation_id=observation_id or "",
            step_id=step_id or "",
            link_kind=link_kind,
            created_at=created_at or datetime.now(UTC).replace(tzinfo=None),
        )
        db.session.add(row)
        return row

    def save_performance_summary(
        self, summary: PerformanceSummary
    ) -> ApPerformanceSummary:
        row = ApPerformanceSummary(
            summary_id=summary.summary_id,
            twin_id=summary.twin_id,
            student_id=summary.student_id,
            event_count=summary.event_count,
            attempt_count=summary.attempt_count,
            correct_count=summary.correct_count,
            incorrect_count=summary.incorrect_count,
            mean_score=summary.mean_score,
            concepts_json=_dumps(list(summary.concepts_touched)),
            generated_at=summary.generated_at,
            window_start=summary.window_start,
            window_end=summary.window_end,
        )
        db.session.add(row)
        return row

    def list_events_for_twin(
        self, twin_id: str, *, limit: int = 100
    ) -> list[AssessmentEvent]:
        rows = (
            ApAssessmentEvent.query.filter_by(twin_id=twin_id)
            .order_by(ApAssessmentEvent.occurred_at.desc())
            .limit(limit)
            .all()
        )
        return [self._event_from_row(r) for r in rows]

    def list_results_for_twin(
        self, twin_id: str, *, limit: int = 100
    ) -> list[AssessmentResult]:
        rows = (
            ApAssessmentResult.query.filter_by(twin_id=twin_id)
            .order_by(ApAssessmentResult.created_at.desc())
            .limit(limit)
            .all()
        )
        return [self._result_from_row(r) for r in rows]

    def list_feedback_for_twin(
        self, twin_id: str, *, limit: int = 100
    ) -> list[LearningFeedback]:
        rows = (
            ApLearningFeedback.query.filter_by(twin_id=twin_id)
            .order_by(ApLearningFeedback.timestamp.desc())
            .limit(limit)
            .all()
        )
        return [self._feedback_from_row(r) for r in rows]

    def list_mission_links(
        self, *, twin_id: str | None = None, mission_id: str | None = None
    ) -> list[dict[str, Any]]:
        query = ApMissionAssessmentLink.query
        if twin_id:
            query = query.filter_by(twin_id=twin_id)
        if mission_id:
            query = query.filter_by(mission_id=mission_id)
        rows = query.order_by(ApMissionAssessmentLink.created_at.desc()).all()
        return [
            {
                "link_id": r.link_id,
                "twin_id": r.twin_id,
                "mission_id": r.mission_id,
                "event_id": r.event_id,
                "observation_id": r.observation_id,
                "step_id": r.step_id,
                "link_kind": r.link_kind,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]

    def get_event(self, event_id: str) -> AssessmentEvent | None:
        row = ApAssessmentEvent.query.filter_by(event_id=event_id).first()
        return self._event_from_row(row) if row else None

    def event_as_dict(self, event: AssessmentEvent) -> dict[str, Any]:
        return {
            "event_id": event.event_id,
            "event_type": event.event_type.value,
            "twin_id": event.twin_id,
            "student_id": event.student_id,
            "occurred_at": event.occurred_at.isoformat(),
            "activity_id": event.activity_id,
            "curriculum_entity_id": event.curriculum_entity_id,
            "curriculum_entity_kind": event.curriculum_entity_kind,
            "concept_ids": list(event.concept_ids),
            "mission_id": event.mission_id,
            "step_id": event.step_id,
            "source": event.source,
            "score": event.score,
            "correct": event.correct,
            "duration_seconds": event.duration_seconds,
            "metadata": dict(event.metadata),
        }

    def result_as_dict(self, result: AssessmentResult) -> dict[str, Any]:
        return {
            "result_id": result.result_id,
            "event_id": result.event_id,
            "twin_id": result.twin_id,
            "event_type": result.event_type.value,
            "observation_id": result.observation_id,
            "performance_label": result.performance_label,
            "evidence_generated": list(result.evidence_generated),
            "concepts_covered": list(result.concepts_covered),
            "confidence": result.confidence,
            "created_at": result.created_at.isoformat(),
            "metadata": dict(result.metadata),
        }

    def feedback_as_dict(self, feedback: LearningFeedback) -> dict[str, Any]:
        return {
            "feedback_id": feedback.feedback_id,
            "twin_id": feedback.twin_id,
            "event_id": feedback.event_id,
            "result_id": feedback.result_id,
            "activity": feedback.activity,
            "performance": feedback.performance,
            "evidence_generated": list(feedback.evidence_generated),
            "concepts_covered": list(feedback.concepts_covered),
            "confidence": feedback.confidence,
            "suggested_next_action": feedback.suggested_next_action,
            "timestamp": feedback.timestamp.isoformat(),
            "source": feedback.source.value,
            "observation_id": feedback.observation_id,
            "mission_id": feedback.mission_id,
            "metadata": dict(feedback.metadata),
        }

    def _event_from_row(self, row: ApAssessmentEvent) -> AssessmentEvent:
        return AssessmentEvent(
            event_id=row.event_id,
            event_type=AssessmentEventType(row.event_type),
            twin_id=row.twin_id,
            student_id=row.student_id,
            occurred_at=row.occurred_at,
            activity_id=row.activity_id or "",
            curriculum_entity_id=row.curriculum_entity_id or "",
            curriculum_entity_kind=row.curriculum_entity_kind or "",
            concept_ids=tuple(_loads(row.concept_ids_json, [])),
            mission_id=row.mission_id or "",
            step_id=row.step_id or "",
            source=row.source or "",
            score=row.score,
            correct=row.correct,
            duration_seconds=row.duration_seconds,
            metadata=_loads(row.metadata_json, {}),
        )

    def _result_from_row(self, row: ApAssessmentResult) -> AssessmentResult:
        return AssessmentResult(
            result_id=row.result_id,
            event_id=row.event_id,
            twin_id=row.twin_id,
            event_type=AssessmentEventType(row.event_type),
            observation_id=row.observation_id,
            performance_label=row.performance_label,
            evidence_generated=tuple(_loads(row.evidence_json, [])),
            concepts_covered=tuple(_loads(row.concepts_json, [])),
            confidence=row.confidence,
            created_at=row.created_at,
            metadata=_loads(row.metadata_json, {}),
        )

    def _feedback_from_row(self, row: ApLearningFeedback) -> LearningFeedback:
        return LearningFeedback(
            feedback_id=row.feedback_id,
            twin_id=row.twin_id,
            event_id=row.event_id,
            result_id=row.result_id,
            activity=row.activity,
            performance=row.performance,
            evidence_generated=tuple(_loads(row.evidence_json, [])),
            concepts_covered=tuple(_loads(row.concepts_json, [])),
            confidence=row.confidence,
            suggested_next_action=row.suggested_next_action,
            timestamp=row.timestamp,
            source=FeedbackSource(row.source),
            observation_id=row.observation_id or "",
            mission_id=row.mission_id or "",
            metadata=_loads(row.metadata_json, {}),
        )
