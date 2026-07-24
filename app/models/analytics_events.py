"""ORM models for PRD-001 analytics event store (append-only).

Operational observation only. Never stores Twin / Educational State payloads,
free-text reflections, or exam PII. Independent of educational authorities.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.extensions import db


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class AnalyticsEventRecord(db.Model):
    """Durable append-only analytics event row."""

    __tablename__ = "analytics_events"
    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "event_type",
            "idempotency_key",
            name="uq_analytics_events_idempotency",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    event_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    event_type: str = db.Column(db.String(128), nullable=False, index=True)
    user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    schema_version: int = db.Column(db.Integer, nullable=False, default=1)
    idempotency_key: str = db.Column(db.String(255), nullable=False)
    correlation_id: str | None = db.Column(db.String(64), nullable=True, index=True)
    payload_json: str = db.Column(db.Text, nullable=False)
    occurred_at: datetime = db.Column(db.DateTime, nullable=False, index=True)
    created_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, index=True
    )
    # Optional integrity HMAC (PRD §9) — populated when secret configured.
    row_hmac: str | None = db.Column(db.String(128), nullable=True)

    def __repr__(self) -> str:
        return (
            f"<AnalyticsEventRecord id={self.id} type={self.event_type} "
            f"user={self.user_id}>"
        )


class AnalyticsOutboxRecord(db.Model):
    """Outbox / retry queue for fail-open analytics emits."""

    __tablename__ = "analytics_outbox"
    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "event_type",
            "idempotency_key",
            name="uq_analytics_outbox_idempotency",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    outbox_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    event_id: str = db.Column(db.String(64), nullable=False, index=True)
    event_type: str = db.Column(db.String(128), nullable=False, index=True)
    user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    idempotency_key: str = db.Column(db.String(255), nullable=False)
    payload_json: str = db.Column(db.Text, nullable=False)
    status: str = db.Column(
        db.String(32), nullable=False, default="pending", index=True
    )
    attempts: int = db.Column(db.Integer, nullable=False, default=0)
    last_error: str | None = db.Column(db.String(512), nullable=True)
    created_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, index=True
    )
    updated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, onupdate=_utc_now
    )

    def __repr__(self) -> str:
        return (
            f"<AnalyticsOutboxRecord id={self.id} status={self.status} "
            f"type={self.event_type}>"
        )


class AnalyticsAuditLogRecord(db.Model):
    """Append-only analytics operational audit log (PRD §7.3 / §9)."""

    __tablename__ = "analytics_audit_log"

    id: int = db.Column(db.Integer, primary_key=True)
    audit_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    action: str = db.Column(db.String(64), nullable=False, index=True)
    user_id: int | None = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=True, index=True
    )
    detail_json: str | None = db.Column(db.Text, nullable=True)
    created_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, index=True
    )

    def __repr__(self) -> str:
        return f"<AnalyticsAuditLogRecord id={self.id} action={self.action}>"
