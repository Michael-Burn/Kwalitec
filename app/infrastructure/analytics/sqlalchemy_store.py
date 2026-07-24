"""SQLAlchemy durable adapters for analytics events + outbox (EP-002).

Composed explicitly for worker / CLI / tests. Never imported on educational
hot paths when ``ANALYTICS_EVENTS_V1`` is off (default).
"""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from sqlalchemy import and_, or_
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.infrastructure.analytics.contracts import AnalyticsEvent
from app.infrastructure.analytics.outbox import OutboxRecord
from app.infrastructure.analytics.serialization import AnalyticsEventSerializer
from app.infrastructure.analytics.status import (
    DEFAULT_MAX_ATTEMPTS,
    DEFAULT_PROCESSED_RETENTION_DAYS,
    OUTBOX_DEAD_LETTER,
    OUTBOX_FAILED,
    OUTBOX_PENDING,
    OUTBOX_PROCESSED,
    OUTBOX_PROCESSING,
)
from app.models.analytics_events import (
    AnalyticsAuditLogRecord,
    AnalyticsEventRecord,
    AnalyticsOutboxRecord,
)

logger = logging.getLogger(__name__)


def _naive_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value
    return value.astimezone(UTC).replace(tzinfo=None)


def _aware_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def _row_to_outbox(row: AnalyticsOutboxRecord) -> OutboxRecord:
    return OutboxRecord(
        outbox_id=row.outbox_id,
        event_id=row.event_id,
        event_type=row.event_type,
        user_id=row.user_id,
        idempotency_key=row.idempotency_key,
        payload_json=row.payload_json,
        created_at=_aware_utc(row.created_at),
        attempts=row.attempts,
        status=row.status,
        last_error=row.last_error,
        updated_at=_aware_utc(row.updated_at) if row.updated_at else None,
    )


class SqlAnalyticsEventStore:
    """Append-only SQL event store with purge + user cascade helpers."""

    name: str = "sql_event_store"

    def __init__(
        self,
        *,
        serializer: AnalyticsEventSerializer | None = None,
    ) -> None:
        self._serializer = serializer or AnalyticsEventSerializer()

    def append(self, event: AnalyticsEvent, *, payload_json: str) -> bool:
        """Append event. Returns False when idempotent duplicate."""
        now = _naive_utc(datetime.now(tz=UTC))
        row = AnalyticsEventRecord(
            event_id=event.event_id,
            event_type=event.event_type,
            user_id=event.user_id,
            schema_version=int(event.schema_version),
            idempotency_key=event.idempotency_key,
            correlation_id=event.correlation_id or None,
            payload_json=payload_json,
            occurred_at=_naive_utc(event.occurred_at),
            created_at=now,
        )
        db.session.add(row)
        try:
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            logger.info(
                "analytics.duplicate_suppressed event_id=%s type=%s",
                event.event_id,
                event.event_type,
            )
            return False

    def get_by_event_id(self, event_id: str) -> AnalyticsEvent | None:
        row = AnalyticsEventRecord.query.filter_by(event_id=event_id).one_or_none()
        if row is None:
            return None
        return self._serializer.from_json(row.payload_json)

    def count_expired(self, *, cutoff: datetime) -> int:
        return (
            AnalyticsEventRecord.query.filter(
                AnalyticsEventRecord.occurred_at < _naive_utc(cutoff)
            ).count()
        )

    def delete_expired(self, *, cutoff: datetime, limit: int) -> int:
        rows = (
            AnalyticsEventRecord.query.filter(
                AnalyticsEventRecord.occurred_at < _naive_utc(cutoff)
            )
            .order_by(AnalyticsEventRecord.occurred_at.asc())
            .limit(limit)
            .all()
        )
        for row in rows:
            db.session.delete(row)
        db.session.commit()
        return len(rows)

    def delete_for_user(self, user_id: int) -> int:
        """Delete all raw event rows for ``user_id``. Returns deleted count."""
        rows = AnalyticsEventRecord.query.filter_by(user_id=user_id).all()
        for row in rows:
            db.session.delete(row)
        db.session.commit()
        return len(rows)

    def list_for_user(self, user_id: int, *, limit: int = 10_000) -> list[dict]:
        """Return raw event JSON payloads for student export."""
        rows = (
            AnalyticsEventRecord.query.filter_by(user_id=user_id)
            .order_by(AnalyticsEventRecord.occurred_at.asc())
            .limit(limit)
            .all()
        )
        out: list[dict] = []
        for row in rows:
            try:
                out.append(json.loads(row.payload_json))
            except json.JSONDecodeError:
                out.append(
                    {
                        "event_id": row.event_id,
                        "event_type": row.event_type,
                        "user_id": row.user_id,
                        "payload_json": row.payload_json,
                    }
                )
        return out


class SqlOutboxSink:
    """Durable SQL outbox implementing :class:`DurableOutboxPort`."""

    name: str = "sql_outbox"

    def enqueue(self, event: AnalyticsEvent, *, payload_json: str) -> OutboxRecord:
        key = (event.user_id, event.event_type, event.idempotency_key)
        existing = AnalyticsOutboxRecord.query.filter_by(
            user_id=key[0],
            event_type=key[1],
            idempotency_key=key[2],
        ).one_or_none()
        if existing is not None:
            return _row_to_outbox(existing)

        now = _naive_utc(datetime.now(tz=UTC))
        row = AnalyticsOutboxRecord(
            outbox_id=uuid4().hex,
            event_id=event.event_id,
            event_type=event.event_type,
            user_id=event.user_id,
            idempotency_key=event.idempotency_key,
            payload_json=payload_json,
            status=OUTBOX_PENDING,
            attempts=0,
            created_at=now,
            updated_at=now,
        )
        db.session.add(row)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            existing = AnalyticsOutboxRecord.query.filter_by(
                user_id=key[0],
                event_type=key[1],
                idempotency_key=key[2],
            ).one()
            return _row_to_outbox(existing)
        return _row_to_outbox(row)

    def pending(self) -> tuple[OutboxRecord, ...]:
        rows = (
            AnalyticsOutboxRecord.query.filter_by(status=OUTBOX_PENDING)
            .order_by(AnalyticsOutboxRecord.created_at.asc())
            .all()
        )
        return tuple(_row_to_outbox(r) for r in rows)

    def claim_batch(
        self,
        *,
        limit: int = 100,
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
    ) -> tuple[OutboxRecord, ...]:
        filt = or_(
            AnalyticsOutboxRecord.status == OUTBOX_PENDING,
            and_(
                AnalyticsOutboxRecord.status == OUTBOX_FAILED,
                AnalyticsOutboxRecord.attempts < max_attempts,
            ),
        )
        query = (
            AnalyticsOutboxRecord.query.filter(filt)
            .order_by(AnalyticsOutboxRecord.created_at.asc())
            .limit(limit)
        )
        # PostgreSQL: SKIP LOCKED for concurrent workers. SQLite ignores / errors.
        try:
            if db.engine.dialect.name != "sqlite":
                query = query.with_for_update(skip_locked=True)
            candidates = query.all()
        except Exception:  # noqa: BLE001 — dialect / lock capability fallback
            db.session.rollback()
            candidates = (
                AnalyticsOutboxRecord.query.filter(filt)
                .order_by(AnalyticsOutboxRecord.created_at.asc())
                .limit(limit)
                .all()
            )

        now = _naive_utc(datetime.now(tz=UTC))
        claimed: list[OutboxRecord] = []
        for row in candidates:
            row.status = OUTBOX_PROCESSING
            row.updated_at = now
            claimed.append(_row_to_outbox(row))
        db.session.commit()
        return tuple(claimed)

    def mark_processed(self, outbox_id: str) -> None:
        row = AnalyticsOutboxRecord.query.filter_by(outbox_id=outbox_id).one_or_none()
        if row is None:
            return
        row.status = OUTBOX_PROCESSED
        row.updated_at = _naive_utc(datetime.now(tz=UTC))
        db.session.commit()

    def mark_failed(self, outbox_id: str, *, error: str) -> None:
        row = AnalyticsOutboxRecord.query.filter_by(outbox_id=outbox_id).one_or_none()
        if row is None:
            return
        row.status = OUTBOX_FAILED
        row.attempts = int(row.attempts or 0) + 1
        row.last_error = (error or "")[:512]
        row.updated_at = _naive_utc(datetime.now(tz=UTC))
        db.session.commit()

    def mark_dead_letter(self, outbox_id: str, *, error: str) -> None:
        row = AnalyticsOutboxRecord.query.filter_by(outbox_id=outbox_id).one_or_none()
        if row is None:
            return
        row.status = OUTBOX_DEAD_LETTER
        row.attempts = int(row.attempts or 0) + 1
        row.last_error = (error or "")[:512]
        row.updated_at = _naive_utc(datetime.now(tz=UTC))
        db.session.commit()

    def requeue(self, outbox_id: str, *, reset_attempts: bool = False) -> bool:
        row = AnalyticsOutboxRecord.query.filter_by(outbox_id=outbox_id).one_or_none()
        if row is None:
            return False
        if row.status not in {
            OUTBOX_FAILED,
            OUTBOX_DEAD_LETTER,
            OUTBOX_PROCESSING,
        }:
            return False
        row.status = OUTBOX_PENDING
        if reset_attempts:
            row.attempts = 0
        row.last_error = None
        row.updated_at = _naive_utc(datetime.now(tz=UTC))
        db.session.commit()
        return True

    def count_by_status(self) -> dict[str, int]:
        rows = (
            db.session.query(
                AnalyticsOutboxRecord.status,
                db.func.count(AnalyticsOutboxRecord.id),
            )
            .group_by(AnalyticsOutboxRecord.status)
            .all()
        )
        return {str(status): int(count) for status, count in rows}

    def delete_processed(
        self,
        *,
        older_than: datetime | None = None,
        limit: int = 1000,
    ) -> int:
        cutoff = older_than
        if cutoff is None:
            cutoff = datetime.now(tz=UTC) - timedelta(
                days=DEFAULT_PROCESSED_RETENTION_DAYS
            )
        rows = (
            AnalyticsOutboxRecord.query.filter(
                AnalyticsOutboxRecord.status == OUTBOX_PROCESSED,
                AnalyticsOutboxRecord.updated_at < _naive_utc(cutoff),
            )
            .order_by(AnalyticsOutboxRecord.updated_at.asc())
            .limit(limit)
            .all()
        )
        for row in rows:
            db.session.delete(row)
        db.session.commit()
        return len(rows)

    def get(self, outbox_id: str) -> OutboxRecord | None:
        row = AnalyticsOutboxRecord.query.filter_by(outbox_id=outbox_id).one_or_none()
        if row is None:
            return None
        return _row_to_outbox(row)

    def list_dead_letters(self, *, limit: int = 100) -> tuple[OutboxRecord, ...]:
        rows = (
            AnalyticsOutboxRecord.query.filter_by(status=OUTBOX_DEAD_LETTER)
            .order_by(AnalyticsOutboxRecord.updated_at.asc())
            .limit(limit)
            .all()
        )
        return tuple(_row_to_outbox(r) for r in rows)

    def delete_for_user(self, user_id: int) -> int:
        rows = AnalyticsOutboxRecord.query.filter_by(user_id=user_id).all()
        for row in rows:
            db.session.delete(row)
        db.session.commit()
        return len(rows)


class SqlAnalyticsAuditLog:
    """Append-only analytics operational audit log."""

    def append(
        self,
        *,
        action: str,
        user_id: int | None = None,
        detail: dict | None = None,
    ) -> str:
        audit_id = uuid4().hex
        row = AnalyticsAuditLogRecord(
            audit_id=audit_id,
            action=action,
            user_id=user_id,
            detail_json=json.dumps(detail or {}, separators=(",", ":"), sort_keys=True),
            created_at=_naive_utc(datetime.now(tz=UTC)),
        )
        db.session.add(row)
        db.session.commit()
        return audit_id

    def list_actions(
        self,
        *,
        action: str | None = None,
        user_id: int | None = None,
        limit: int = 500,
    ) -> list[dict]:
        q = AnalyticsAuditLogRecord.query
        if action:
            q = q.filter_by(action=action)
        if user_id is not None:
            q = q.filter_by(user_id=user_id)
        rows = q.order_by(AnalyticsAuditLogRecord.created_at.desc()).limit(limit).all()
        result: list[dict] = []
        for row in rows:
            detail: dict = {}
            if row.detail_json:
                try:
                    detail = json.loads(row.detail_json)
                except json.JSONDecodeError:
                    detail = {"raw": row.detail_json}
            result.append(
                {
                    "audit_id": row.audit_id,
                    "action": row.action,
                    "user_id": row.user_id,
                    "detail": detail,
                    "created_at": _aware_utc(row.created_at).isoformat(),
                }
            )
        return result

    def export_jsonl(
        self,
        *,
        action: str | None = None,
        user_id: int | None = None,
        limit: int = 10_000,
    ) -> str:
        entries = self.list_actions(action=action, user_id=user_id, limit=limit)
        return "\n".join(
            json.dumps(e, separators=(",", ":"), sort_keys=True) for e in entries
        )
