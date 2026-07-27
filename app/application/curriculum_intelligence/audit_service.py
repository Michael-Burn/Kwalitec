"""AuditService — append-only CIP audit trail (CIP-002)."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from uuid import uuid4

from app.domain.curriculum_intelligence.audit import AuditAction, AuditEvent
from app.extensions import db
from app.models.curriculum_intelligence import CipAuditEvent


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def _iso(dt: datetime) -> str:
    return dt.replace(microsecond=0).isoformat() + "Z"


class AuditService:
    """Record immutable CIP audit events. Never updates prior rows."""

    def record(
        self,
        *,
        action: AuditAction,
        actor_id: str,
        subject_kind: str,
        subject_id: str,
        message: str,
        document_id: int | None = None,
        pipeline_job_id: str = "",
        document_version: str = "",
        workspace_id: str = "",
        attributes: dict[str, str] | None = None,
    ) -> AuditEvent:
        """Append one audit event and return the domain contract."""
        now = _utc_now()
        event_id = f"aud-{uuid4().hex[:12]}"
        attrs = attributes or {}
        row = CipAuditEvent(
            event_id=event_id,
            action=action.value,
            actor_id=actor_id or "system",
            subject_kind=subject_kind,
            subject_id=subject_id,
            document_id=document_id,
            pipeline_job_id=pipeline_job_id or "",
            document_version=document_version or "",
            workspace_id=workspace_id or "",
            message=(message or "")[:512],
            attributes_json=json.dumps(
                attrs, ensure_ascii=False, separators=(",", ":")
            ),
            created_at=now,
        )
        db.session.add(row)
        db.session.flush()
        return AuditEvent(
            event_id=event_id,
            action=action,
            actor_id=row.actor_id,
            subject_kind=subject_kind,
            subject_id=subject_id,
            document_id=document_id,
            pipeline_job_id=row.pipeline_job_id,
            document_version=row.document_version,
            workspace_id=row.workspace_id,
            message=row.message,
            created_at_iso=_iso(now),
            attributes=tuple(sorted(attrs.items())),
        )

    def history_for_subject(
        self, *, subject_kind: str, subject_id: str, limit: int = 50
    ) -> list[AuditEvent]:
        """Return recent audit events for one subject (newest first)."""
        rows = (
            CipAuditEvent.query.filter_by(
                subject_kind=subject_kind, subject_id=subject_id
            )
            .order_by(CipAuditEvent.id.desc())
            .limit(max(1, min(limit, 200)))
            .all()
        )
        return [self._to_domain(r) for r in rows]

    def history_for_workspace(
        self, *, workspace_id: str, limit: int = 100
    ) -> list[AuditEvent]:
        """Return recent audit events for a workspace."""
        rows = (
            CipAuditEvent.query.filter_by(workspace_id=workspace_id)
            .order_by(CipAuditEvent.id.desc())
            .limit(max(1, min(limit, 500)))
            .all()
        )
        return [self._to_domain(r) for r in rows]

    @staticmethod
    def _to_domain(row: CipAuditEvent) -> AuditEvent:
        try:
            attrs = json.loads(row.attributes_json or "{}")
        except json.JSONDecodeError:
            attrs = {}
        if not isinstance(attrs, dict):
            attrs = {}
        return AuditEvent(
            event_id=row.event_id,
            action=AuditAction(row.action),
            actor_id=row.actor_id,
            subject_kind=row.subject_kind,
            subject_id=row.subject_id,
            document_id=row.document_id,
            pipeline_job_id=row.pipeline_job_id,
            document_version=row.document_version,
            workspace_id=row.workspace_id,
            message=row.message,
            created_at_iso=_iso(row.created_at) if row.created_at else "",
            attributes=tuple(sorted((str(k), str(v)) for k, v in attrs.items())),
        )
