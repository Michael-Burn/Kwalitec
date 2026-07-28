"""Operational pipeline events — coordination signals only.

These events are not educational artefacts. They must not carry observation
payloads, decision bodies, mastery scores, mission text, or tutor prose.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum

from app.application.educational_intelligence_pipeline.stages import PipelineStage


class PipelineEventType(StrEnum):
    """Operational event catalogue for pipeline coordination."""

    PIPELINE_STARTED = "PipelineStarted"
    PIPELINE_COMPLETED = "PipelineCompleted"
    PIPELINE_FAILED = "PipelineFailed"
    PIPELINE_STAGE_STARTED = "PipelineStageStarted"
    PIPELINE_STAGE_COMPLETED = "PipelineStageCompleted"
    PIPELINE_STAGE_FAILED = "PipelineStageFailed"


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


@dataclass(frozen=True, slots=True)
class PipelineEvent:
    """Immutable operational event emitted during pipeline execution."""

    event_type: PipelineEventType
    pipeline_id: str
    correlation_id: str
    occurred_at: datetime
    student_id: str | None = None
    assessment_session_id: str | None = None
    reasoning_request_id: str | None = None
    stage: PipelineStage | None = None
    outcome: str | None = None
    failure_cause: str | None = None
    duration_ms: float | None = None

    def to_log_fields(self) -> dict[str, object]:
        """Privacy-safe structured fields for logging (no educational payloads)."""
        fields: dict[str, object] = {
            "event_type": self.event_type.value,
            "pipeline_id": self.pipeline_id,
            "correlation_id": self.correlation_id,
            "occurred_at": self.occurred_at.isoformat(),
        }
        if self.student_id is not None:
            fields["student_id"] = self.student_id
        if self.assessment_session_id is not None:
            fields["assessment_session_id"] = self.assessment_session_id
        if self.reasoning_request_id is not None:
            fields["reasoning_request_id"] = self.reasoning_request_id
        if self.stage is not None:
            fields["stage"] = self.stage.value
        if self.outcome is not None:
            fields["outcome"] = self.outcome
        if self.failure_cause is not None:
            fields["failure_cause"] = self.failure_cause
        if self.duration_ms is not None:
            fields["duration_ms"] = round(self.duration_ms, 3)
        return fields


class PipelineEventCollector:
    """In-memory collector for operational events during one pipeline run."""

    def __init__(self) -> None:
        self._events: list[PipelineEvent] = []

    @property
    def events(self) -> tuple[PipelineEvent, ...]:
        return tuple(self._events)

    def emit(self, event: PipelineEvent) -> PipelineEvent:
        self._events.append(event)
        return event

    def started(
        self,
        *,
        pipeline_id: str,
        correlation_id: str,
        student_id: str | None,
        assessment_session_id: str | None,
        reasoning_request_id: str | None,
        occurred_at: datetime | None = None,
    ) -> PipelineEvent:
        return self.emit(
            PipelineEvent(
                event_type=PipelineEventType.PIPELINE_STARTED,
                pipeline_id=pipeline_id,
                correlation_id=correlation_id,
                occurred_at=occurred_at or _utc_now(),
                student_id=student_id,
                assessment_session_id=assessment_session_id,
                reasoning_request_id=reasoning_request_id,
            )
        )

    def completed(
        self,
        *,
        pipeline_id: str,
        correlation_id: str,
        student_id: str | None,
        assessment_session_id: str | None,
        reasoning_request_id: str | None,
        duration_ms: float,
        occurred_at: datetime | None = None,
    ) -> PipelineEvent:
        return self.emit(
            PipelineEvent(
                event_type=PipelineEventType.PIPELINE_COMPLETED,
                pipeline_id=pipeline_id,
                correlation_id=correlation_id,
                occurred_at=occurred_at or _utc_now(),
                student_id=student_id,
                assessment_session_id=assessment_session_id,
                reasoning_request_id=reasoning_request_id,
                outcome="completed",
                duration_ms=duration_ms,
            )
        )

    def failed(
        self,
        *,
        pipeline_id: str,
        correlation_id: str,
        student_id: str | None,
        assessment_session_id: str | None,
        reasoning_request_id: str | None,
        failure_cause: str,
        stage: PipelineStage | None,
        duration_ms: float,
        occurred_at: datetime | None = None,
    ) -> PipelineEvent:
        return self.emit(
            PipelineEvent(
                event_type=PipelineEventType.PIPELINE_FAILED,
                pipeline_id=pipeline_id,
                correlation_id=correlation_id,
                occurred_at=occurred_at or _utc_now(),
                student_id=student_id,
                assessment_session_id=assessment_session_id,
                reasoning_request_id=reasoning_request_id,
                stage=stage,
                outcome="failed",
                failure_cause=failure_cause,
                duration_ms=duration_ms,
            )
        )

    def stage_started(
        self,
        *,
        pipeline_id: str,
        correlation_id: str,
        stage: PipelineStage,
        student_id: str | None = None,
        assessment_session_id: str | None = None,
        reasoning_request_id: str | None = None,
        occurred_at: datetime | None = None,
    ) -> PipelineEvent:
        return self.emit(
            PipelineEvent(
                event_type=PipelineEventType.PIPELINE_STAGE_STARTED,
                pipeline_id=pipeline_id,
                correlation_id=correlation_id,
                occurred_at=occurred_at or _utc_now(),
                student_id=student_id,
                assessment_session_id=assessment_session_id,
                reasoning_request_id=reasoning_request_id,
                stage=stage,
            )
        )

    def stage_completed(
        self,
        *,
        pipeline_id: str,
        correlation_id: str,
        stage: PipelineStage,
        duration_ms: float,
        student_id: str | None = None,
        assessment_session_id: str | None = None,
        reasoning_request_id: str | None = None,
        occurred_at: datetime | None = None,
    ) -> PipelineEvent:
        return self.emit(
            PipelineEvent(
                event_type=PipelineEventType.PIPELINE_STAGE_COMPLETED,
                pipeline_id=pipeline_id,
                correlation_id=correlation_id,
                occurred_at=occurred_at or _utc_now(),
                student_id=student_id,
                assessment_session_id=assessment_session_id,
                reasoning_request_id=reasoning_request_id,
                stage=stage,
                outcome="completed",
                duration_ms=duration_ms,
            )
        )

    def stage_failed(
        self,
        *,
        pipeline_id: str,
        correlation_id: str,
        stage: PipelineStage,
        failure_cause: str,
        duration_ms: float,
        student_id: str | None = None,
        assessment_session_id: str | None = None,
        reasoning_request_id: str | None = None,
        occurred_at: datetime | None = None,
    ) -> PipelineEvent:
        return self.emit(
            PipelineEvent(
                event_type=PipelineEventType.PIPELINE_STAGE_FAILED,
                pipeline_id=pipeline_id,
                correlation_id=correlation_id,
                occurred_at=occurred_at or _utc_now(),
                student_id=student_id,
                assessment_session_id=assessment_session_id,
                reasoning_request_id=reasoning_request_id,
                stage=stage,
                outcome="failed",
                failure_cause=failure_cause,
                duration_ms=duration_ms,
            )
        )
