"""Founder-facing CIP DTOs."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class StageEventView:
    """One processing stage event for Founder inspection."""

    event_id: str
    stage: str
    stage_label: str
    status: str
    message: str
    started_at: str | None
    finished_at: str | None
    duration_ms: int | None
    error_message: str | None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ProcessingJobView:
    """Founder-safe CIP job projection."""

    job_id: str
    document_id: int
    workspace_id: str
    status: str
    status_label: str
    checkpoint_stage: str | None
    attempt_count: int
    last_error: str | None
    started_at: str | None
    finished_at: str | None
    can_retry: bool
    can_cancel: bool
    events: tuple[StageEventView, ...]

    def to_dict(self) -> dict:
        return {
            "job_id": self.job_id,
            "document_id": self.document_id,
            "workspace_id": self.workspace_id,
            "status": self.status,
            "status_label": self.status_label,
            "checkpoint_stage": self.checkpoint_stage,
            "attempt_count": self.attempt_count,
            "last_error": self.last_error,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "can_retry": self.can_retry,
            "can_cancel": self.can_cancel,
            "events": [e.to_dict() for e in self.events],
        }
