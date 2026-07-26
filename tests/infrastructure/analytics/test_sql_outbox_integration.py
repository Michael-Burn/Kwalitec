"""EP-002 SQL outbox + worker integration (durable path; flag composition optional)."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from app.infrastructure.analytics.contracts import AnalyticsEvent
from app.infrastructure.analytics.dispatcher import (
    AnalyticsEventDispatcher,
    DispatchStatus,
)
from app.infrastructure.analytics.feature_flag import AnalyticsFeatureFlag
from app.infrastructure.analytics.idempotency import build_idempotency_key
from app.infrastructure.analytics.metrics import AnalyticsOperationalMetrics
from app.infrastructure.analytics.outbox import serialize_for_outbox
from app.infrastructure.analytics.privacy import AnalyticsPrivacyService
from app.infrastructure.analytics.sqlalchemy_store import (
    SqlAnalyticsAuditLog,
    SqlAnalyticsEventStore,
    SqlOutboxSink,
)
from app.infrastructure.analytics.status import OUTBOX_PROCESSED
from app.infrastructure.analytics.worker import AnalyticsOutboxWorker
from app.models.user import User


def _user(email: str) -> User:
    u = User(email=email, is_active_user=True)
    u.set_password("password123")
    u.alpha_onboarding_completed = True
    return u


def test_sql_outbox_enqueue_worker_drain(app, db, ctx) -> None:
    user = _user(f"ep002-sql-{uuid4().hex[:8]}@example.com")
    db.session.add(user)
    db.session.commit()

    outbox = SqlOutboxSink()
    store = SqlAnalyticsEventStore()
    metrics = AnalyticsOperationalMetrics()
    dispatcher = AnalyticsEventDispatcher(
        outbox=outbox,
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        metrics=metrics,
    )
    event = AnalyticsEvent.create(
        "session.started",
        user_id=user.id,
        payload={"session_id": "sql-s1", "mission_id": "m1"},
        idempotency_key=build_idempotency_key(
            user_id=user.id, event_type="session.started", entity_key="sql-s1"
        ),
    )
    result = dispatcher.dispatch(event)
    assert result.status == DispatchStatus.ENQUEUED
    assert len(outbox.pending()) == 1

    # Duplicate enqueue suppressed.
    dup = dispatcher.dispatch(event)
    assert dup.status == DispatchStatus.DUPLICATE

    worker = AnalyticsOutboxWorker(
        outbox=outbox, store=store, metrics=metrics, max_attempts=3
    )
    batch = worker.run_once()
    assert batch.processed == 1
    assert store.get_by_event_id(event.event_id) is not None
    assert outbox.get(result.outbox_id).status == OUTBOX_PROCESSED
    assert outbox.pending() == ()


def test_sql_privacy_delete_and_export(app, db, ctx) -> None:
    user = _user(f"ep002-priv-{uuid4().hex[:8]}@example.com")
    db.session.add(user)
    db.session.commit()

    store = SqlAnalyticsEventStore()
    outbox = SqlOutboxSink()
    audit = SqlAnalyticsAuditLog()
    privacy = AnalyticsPrivacyService(
        event_store=store, outbox=outbox, audit=audit
    )
    event = AnalyticsEvent.create(
        "session.completed",
        user_id=user.id,
        payload={
            "session_id": "sql-s2",
            "mission_id": "m1",
            "completion_status": "completed",
            "started_at": datetime.now(tz=UTC).isoformat(),
        },
        idempotency_key=build_idempotency_key(
            user_id=user.id,
            event_type="session.completed",
            entity_key="sql-s2",
        ),
    )
    payload = serialize_for_outbox(event)
    assert store.append(event, payload_json=payload) is True
    outbox.enqueue(event, payload_json=payload)

    export = privacy.export_student(user.id)
    assert export.event_count == 1
    deleted = privacy.delete_user_analytics(user.id, requested_by="test")
    assert deleted.events_deleted == 1
    assert deleted.outbox_deleted == 1
    assert store.list_for_user(user.id) == []
    assert audit.list_actions(action="analytics.user_deleted")
