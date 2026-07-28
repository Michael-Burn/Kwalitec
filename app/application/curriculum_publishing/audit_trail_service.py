"""Append-only audit trail writers for curriculum publishing (EI-003)."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from app.domain.curriculum_publishing.editorial_action import EditorialAction
from app.extensions import db
from app.models.curriculum_knowledge_graph import (
    CkgEditorialAuditEvent,
    CkgPublicationRecord,
)


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class AuditTrailService:
    """Record editorial and publication events. Never deletes audit rows."""

    def record_editorial(
        self,
        *,
        edition_id: str,
        action: EditorialAction | str,
        actor: str,
        stable_id: str | None = None,
        detail: dict[str, Any] | None = None,
    ) -> str:
        """Append an editorial audit event. Returns event_id."""
        action_value = (
            action.value if isinstance(action, EditorialAction) else action
        )
        event_id = f"edaudit-{uuid4().hex[:12]}"
        db.session.add(
            CkgEditorialAuditEvent(
                event_id=event_id,
                edition_id=edition_id,
                action=action_value,
                actor=(actor or "").strip(),
                stable_id=stable_id,
                detail_json=json.dumps(detail or {}, sort_keys=True),
                created_at=_utc_now(),
            )
        )
        return event_id

    def record_publication(
        self,
        *,
        edition_id: str,
        subject_code: str,
        publisher: str,
        published_at: datetime,
        previous_edition_id: str | None,
        publication_rationale: str,
        validation_status: str,
        review_status: str,
        review_completed_at: datetime | None,
        snapshot_id: str | None,
        detail: dict[str, Any] | None = None,
    ) -> str:
        """Append an immutable publication record. Returns record_id."""
        record_id = f"pubrec-{uuid4().hex[:12]}"
        db.session.add(
            CkgPublicationRecord(
                record_id=record_id,
                edition_id=edition_id,
                subject_code=subject_code,
                publisher=publisher,
                published_at=published_at,
                previous_edition_id=previous_edition_id,
                publication_rationale=publication_rationale,
                validation_status=validation_status,
                review_status=review_status,
                review_completed_at=review_completed_at,
                snapshot_id=snapshot_id,
                detail_json=json.dumps(detail or {}, sort_keys=True),
                created_at=_utc_now(),
            )
        )
        return record_id

    def list_editorial_events(self, edition_id: str) -> list[dict[str, Any]]:
        rows = (
            CkgEditorialAuditEvent.query.filter_by(edition_id=edition_id)
            .order_by(CkgEditorialAuditEvent.created_at.asc())
            .all()
        )
        return [
            {
                "event_id": r.event_id,
                "edition_id": r.edition_id,
                "action": r.action,
                "actor": r.actor,
                "stable_id": r.stable_id,
                "detail": json.loads(r.detail_json or "{}"),
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]

    def list_publication_records(
        self, *, subject_code: str | None = None, edition_id: str | None = None
    ) -> list[dict[str, Any]]:
        query = CkgPublicationRecord.query
        if subject_code:
            query = query.filter_by(subject_code=subject_code)
        if edition_id:
            query = query.filter_by(edition_id=edition_id)
        rows = query.order_by(CkgPublicationRecord.published_at.asc()).all()
        return [
            {
                "record_id": r.record_id,
                "edition_id": r.edition_id,
                "subject_code": r.subject_code,
                "publisher": r.publisher,
                "published_at": (
                    r.published_at.isoformat() if r.published_at else None
                ),
                "previous_edition_id": r.previous_edition_id,
                "publication_rationale": r.publication_rationale,
                "validation_status": r.validation_status,
                "review_status": r.review_status,
                "review_completed_at": (
                    r.review_completed_at.isoformat()
                    if r.review_completed_at
                    else None
                ),
                "snapshot_id": r.snapshot_id,
                "detail": json.loads(r.detail_json or "{}"),
            }
            for r in rows
        ]
