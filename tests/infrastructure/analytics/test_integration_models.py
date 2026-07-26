"""Integration — ORM models register and tables create under test app."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from app.models.analytics_events import (
    AnalyticsAuditLogRecord,
    AnalyticsEventRecord,
    AnalyticsOutboxRecord,
)
from app.models.user import User


def _user(email: str) -> User:
    u = User(email=email, is_active_user=True)
    u.set_password("password123")
    u.alpha_onboarding_completed = True
    return u


def test_analytics_models_persist(app, db, ctx) -> None:
    user = _user("analytics-phase-a@example.com")
    db.session.add(user)
    db.session.commit()

    event_id = uuid4().hex
    outbox_id = uuid4().hex
    audit_id = uuid4().hex
    now = datetime.now(UTC).replace(tzinfo=None)

    row = AnalyticsEventRecord(
        event_id=event_id,
        event_type="analytics.infrastructure_probe",
        user_id=user.id,
        schema_version=1,
        idempotency_key=f"{user.id}:analytics.infrastructure_probe:probe-1",
        correlation_id="corr-test",
        payload_json='{"probe":true}',
        occurred_at=now,
        created_at=now,
    )
    outbox = AnalyticsOutboxRecord(
        outbox_id=outbox_id,
        event_id=event_id,
        event_type="analytics.infrastructure_probe",
        user_id=user.id,
        idempotency_key=f"{user.id}:analytics.infrastructure_probe:probe-1",
        payload_json='{"probe":true}',
        status="pending",
        attempts=0,
        created_at=now,
        updated_at=now,
    )
    audit = AnalyticsAuditLogRecord(
        audit_id=audit_id,
        action="analytics.emit_test",
        user_id=user.id,
        detail_json='{"ok":true}',
        created_at=now,
    )
    db.session.add_all([row, outbox, audit])
    db.session.commit()

    assert AnalyticsEventRecord.query.filter_by(event_id=event_id).one()
    assert AnalyticsOutboxRecord.query.filter_by(outbox_id=outbox_id).one()
    assert AnalyticsAuditLogRecord.query.filter_by(audit_id=audit_id).one()


def test_analytics_event_idempotency_unique(app, db, ctx) -> None:
    user = _user("analytics-idem@example.com")
    db.session.add(user)
    db.session.commit()

    now = datetime.now(UTC).replace(tzinfo=None)
    key = f"{user.id}:analytics.infrastructure_probe:same"
    first = AnalyticsEventRecord(
        event_id=uuid4().hex,
        event_type="analytics.infrastructure_probe",
        user_id=user.id,
        schema_version=1,
        idempotency_key=key,
        payload_json="{}",
        occurred_at=now,
        created_at=now,
    )
    db.session.add(first)
    db.session.commit()

    duplicate = AnalyticsEventRecord(
        event_id=uuid4().hex,
        event_type="analytics.infrastructure_probe",
        user_id=user.id,
        schema_version=1,
        idempotency_key=key,
        payload_json="{}",
        occurred_at=now,
        created_at=now,
    )
    db.session.add(duplicate)
    try:
        db.session.commit()
        raised = False
    except Exception:  # noqa: BLE001
        db.session.rollback()
        raised = True
    assert raised is True
