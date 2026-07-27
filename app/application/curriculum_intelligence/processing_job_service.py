"""ProcessingJobService — CIP job lifecycle, events, retry/resume/cancel."""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from app.application.curriculum_intelligence.dto.processing_job_view import (
    ProcessingJobView,
    StageEventView,
)
from app.application.curriculum_intelligence.exceptions import (
    JobNotFoundError,
    PipelineTransitionError,
)
from app.domain.curriculum_intelligence.pipeline_stage import (
    PipelineStage,
    founder_label,
    is_failure,
    is_terminal,
    resolve_pipeline_stage,
)
from app.extensions import db
from app.models.curriculum_intelligence import CipProcessingEvent, CipProcessingJob
from app.models.curriculum_studio_foundation import StudioFoundationDocument

logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def _iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat(timespec="seconds")


class ProcessingJobService:
    """Create and advance durable CIP processing jobs."""

    def create_job(
        self,
        *,
        document_id: int,
        workspace_id: str,
        subject_code: str,
        kind: str,
        storage_key: str,
        job_id: str | None = None,
    ) -> CipProcessingJob:
        """Create a QUEUED job (idempotent if an active non-terminal job exists)."""
        active = (
            CipProcessingJob.query.filter_by(document_id=document_id)
            .order_by(CipProcessingJob.id.desc())
            .first()
        )
        if active is not None and not is_terminal(active.status):
            return active

        jid = (job_id or "").strip() or f"cip-{uuid4().hex[:12]}"
        job = CipProcessingJob(
            job_id=jid,
            document_id=document_id,
            workspace_id=workspace_id,
            subject_code=subject_code,
            kind=kind,
            storage_key=storage_key,
            status=PipelineStage.QUEUED.value,
            checkpoint_stage=PipelineStage.QUEUED.value,
            attempt_count=0,
            started_at=_utc_now(),
        )
        db.session.add(job)
        self._sync_document_stage(document_id, PipelineStage.QUEUED)
        self.record_event(
            jid,
            stage=PipelineStage.QUEUED,
            status="completed",
            message="Document queued for curriculum intelligence pipeline",
        )
        db.session.flush()
        return job

    def get_job(self, job_id: str) -> CipProcessingJob:
        job = CipProcessingJob.query.filter_by(job_id=job_id).first()
        if job is None:
            raise JobNotFoundError(f"Processing job not found: {job_id}")
        return job

    def get_latest_for_document(self, document_id: int) -> CipProcessingJob | None:
        return (
            CipProcessingJob.query.filter_by(document_id=document_id)
            .order_by(CipProcessingJob.id.desc())
            .first()
        )

    def record_event(
        self,
        job_id: str,
        *,
        stage: PipelineStage | str,
        status: str,
        message: str = "",
        error_message: str | None = None,
        diagnostics: dict[str, Any] | None = None,
        started_at: datetime | None = None,
        finished_at: datetime | None = None,
        duration_ms: int | None = None,
        event_type: str = "stage",
    ) -> CipProcessingEvent:
        stage_token = resolve_pipeline_stage(stage).value
        start = started_at or _utc_now()
        finish = finished_at
        if finish is None and status in {"completed", "failed", "cancelled"}:
            finish = _utc_now()
        duration = duration_ms
        if duration is None and finish is not None:
            duration = int((finish - start).total_seconds() * 1000)
        event = CipProcessingEvent(
            event_id=f"cipevt-{uuid4().hex[:12]}",
            job_id=job_id,
            stage=stage_token,
            event_type=event_type,
            status=status,
            message=(message or "")[:512],
            diagnostics_json=json.dumps(diagnostics or {}, ensure_ascii=False),
            error_message=error_message,
            started_at=start,
            finished_at=finish,
            duration_ms=duration,
        )
        db.session.add(event)
        return event

    def mark_stage(
        self,
        job: CipProcessingJob,
        stage: PipelineStage,
        *,
        message: str = "",
        diagnostics: dict[str, Any] | None = None,
        duration_ms: int | None = None,
        started_at: datetime | None = None,
    ) -> None:
        """Advance job + foundation document to ``stage`` and record event."""
        if job.cancel_requested and stage not in {
            PipelineStage.CANCELLED,
            PipelineStage.FAILED,
        }:
            raise PipelineTransitionError(
                "Job cancellation was requested.",
                code="cancel_requested",
            )
        job.status = stage.value
        if stage not in {PipelineStage.FAILED, PipelineStage.CANCELLED}:
            job.checkpoint_stage = stage.value
            job.last_error = None
        if stage is PipelineStage.READY_FOR_EMBEDDINGS:
            job.finished_at = _utc_now()
        self._sync_document_stage(job.document_id, stage)
        self.record_event(
            job.job_id,
            stage=stage,
            status="completed",
            message=message or f"Reached {founder_label(stage)}",
            diagnostics=diagnostics,
            started_at=started_at,
            duration_ms=duration_ms,
        )
        db.session.flush()

    def mark_failed(
        self,
        job: CipProcessingJob,
        *,
        stage: PipelineStage | str,
        error: str,
        diagnostics: dict[str, Any] | None = None,
    ) -> None:
        job.status = PipelineStage.FAILED.value
        job.last_error = (error or "")[:2000]
        job.finished_at = _utc_now()
        self._sync_document_stage(job.document_id, PipelineStage.FAILED)
        self.record_event(
            job.job_id,
            stage=stage,
            status="failed",
            message="Pipeline stage failed",
            error_message=error,
            diagnostics=diagnostics,
        )
        db.session.flush()

    def request_cancel(self, job_id: str) -> CipProcessingJob:
        job = self.get_job(job_id)
        if is_terminal(job.status):
            return job
        job.cancel_requested = True
        job.status = PipelineStage.CANCELLED.value
        job.finished_at = _utc_now()
        self._sync_document_stage(job.document_id, PipelineStage.CANCELLED)
        self.record_event(
            job.job_id,
            stage=PipelineStage.CANCELLED,
            status="cancelled",
            message="Processing cancelled by Founder",
            event_type="cancel",
        )
        db.session.commit()
        return job

    def prepare_retry(self, job_id: str, *, resume: bool = True) -> CipProcessingJob:
        """Reset a FAILED/CANCELLED job for another attempt."""
        job = self.get_job(job_id)
        if (
            not is_failure(job.status)
            and resolve_pipeline_stage(job.status) is not PipelineStage.CANCELLED
        ):
            raise PipelineTransitionError(
                "Only failed or cancelled jobs can be retried.",
                code="not_retryable",
            )
        checkpoint = job.checkpoint_stage or PipelineStage.QUEUED.value
        job.status = checkpoint if resume else PipelineStage.QUEUED.value
        # Always re-enter from checkpoint (coordinator runs next stages).
        if not resume:
            job.checkpoint_stage = PipelineStage.QUEUED.value
            job.status = PipelineStage.QUEUED.value
        job.cancel_requested = False
        job.last_error = None
        job.finished_at = None
        job.attempt_count = int(job.attempt_count or 0) + 1
        job.started_at = _utc_now()
        self._sync_document_stage(job.document_id, resolve_pipeline_stage(job.status))
        self.record_event(
            job.job_id,
            stage=job.status,
            status="completed",
            message="Retry requested" if not resume else "Resume requested",
            event_type="retry" if not resume else "resume",
            diagnostics={"checkpoint": checkpoint, "resume": resume},
        )
        db.session.flush()
        return job

    def to_view(self, job: CipProcessingJob) -> ProcessingJobView:
        events = tuple(
            StageEventView(
                event_id=e.event_id,
                stage=e.stage,
                stage_label=founder_label(e.stage),
                status=e.status,
                message=e.message,
                started_at=_iso(e.started_at),
                finished_at=_iso(e.finished_at),
                duration_ms=e.duration_ms,
                error_message=e.error_message,
            )
            for e in sorted(job.events, key=lambda x: x.id)
        )
        status = resolve_pipeline_stage(job.status)
        return ProcessingJobView(
            job_id=job.job_id,
            document_id=job.document_id,
            workspace_id=job.workspace_id,
            status=status.value,
            status_label=founder_label(status),
            checkpoint_stage=job.checkpoint_stage,
            attempt_count=int(job.attempt_count or 0),
            last_error=job.last_error,
            started_at=_iso(job.started_at),
            finished_at=_iso(job.finished_at),
            can_retry=is_terminal(status)
            and status is not PipelineStage.READY_FOR_EMBEDDINGS,
            can_cancel=not is_terminal(status),
            events=events,
        )

    @staticmethod
    def _sync_document_stage(document_id: int, stage: PipelineStage) -> None:
        doc = db.session.get(StudioFoundationDocument, document_id)
        if doc is not None:
            doc.processing_stage = stage.value
