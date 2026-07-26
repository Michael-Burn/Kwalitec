"""EP-002 reliability tests — outbox durability without educational impact."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from app.infrastructure.analytics.audit_log import MemoryAnalyticsAuditLog
from app.infrastructure.analytics.cleanup import (
    AnalyticsCleanupJob,
    AnalyticsRetentionEnforcer,
)
from app.infrastructure.analytics.contracts import AnalyticsEvent
from app.infrastructure.analytics.dispatcher import (
    AnalyticsEventDispatcher,
    DispatchStatus,
)
from app.infrastructure.analytics.feature_flag import AnalyticsFeatureFlag
from app.infrastructure.analytics.idempotency import build_idempotency_key
from app.infrastructure.analytics.metrics import AnalyticsOperationalMetrics
from app.infrastructure.analytics.outbox import (
    MemoryOutboxSink,
    OutboxRecord,
    serialize_for_outbox,
)
from app.infrastructure.analytics.privacy import AnalyticsPrivacyService
from app.infrastructure.analytics.purge import AnalyticsPurgeJob
from app.infrastructure.analytics.replay import AnalyticsReplayService
from app.infrastructure.analytics.repository import MemoryAnalyticsEventStore
from app.infrastructure.analytics.status import (
    OUTBOX_DEAD_LETTER,
    OUTBOX_FAILED,
    OUTBOX_PROCESSED,
)
from app.infrastructure.analytics.worker import AnalyticsOutboxWorker


def _event(
    *,
    user_id: int = 1,
    event_type: str = "session.started",
    entity: str = "s1",
    payload: dict | None = None,
) -> AnalyticsEvent:
    return AnalyticsEvent.create(
        event_type,
        user_id=user_id,
        payload=payload
        or {
            "session_id": entity,
            "mission_id": "m1",
        },
        idempotency_key=build_idempotency_key(
            user_id=user_id, event_type=event_type, entity_key=entity
        ),
    )


def _enabled_dispatcher(
    outbox: MemoryOutboxSink,
    metrics: AnalyticsOperationalMetrics | None = None,
) -> AnalyticsEventDispatcher:
    return AnalyticsEventDispatcher(
        outbox=outbox,
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        metrics=metrics or AnalyticsOperationalMetrics(),
    )


def test_restart_recovery_pending_survives_new_worker() -> None:
    """Pending outbox rows drain after a simulated process restart."""
    outbox = MemoryOutboxSink()
    store = MemoryAnalyticsEventStore()
    metrics = AnalyticsOperationalMetrics()
    dispatcher = _enabled_dispatcher(outbox, metrics)
    event = _event(entity="restart-1")
    result = dispatcher.dispatch(event)
    assert result.status == DispatchStatus.ENQUEUED
    assert len(outbox.pending()) == 1

    # Simulated restart: new worker, same durable outbox + empty store.
    worker = AnalyticsOutboxWorker(
        outbox=outbox, store=store, metrics=metrics, max_attempts=3
    )
    batch = worker.run_once()
    assert batch.processed == 1
    assert store.get_by_event_id(event.event_id) is not None
    assert outbox.pending() == ()
    assert outbox.get(result.outbox_id).status == OUTBOX_PROCESSED


def test_worker_interruption_leaves_processing_reclaimable() -> None:
    """Interrupted claim can be requeued and drained."""
    outbox = MemoryOutboxSink()
    store = MemoryAnalyticsEventStore()
    event = _event(entity="interrupt-1")
    payload = serialize_for_outbox(event)
    record = outbox.enqueue(event, payload_json=payload)
    claimed = outbox.claim_batch(limit=1)
    assert len(claimed) == 1
    assert claimed[0].status == "processing"

    # Operator recovery: requeue processing row after crash.
    assert outbox.requeue(record.outbox_id, reset_attempts=False) is True
    worker = AnalyticsOutboxWorker(outbox=outbox, store=store, max_attempts=3)
    batch = worker.drain()
    assert batch.processed == 1
    assert store.get_by_event_id(event.event_id) is not None


def test_retry_correctness_then_dead_letter() -> None:
    class BoomStore:
        def append(self, event, *, payload_json: str) -> bool:
            raise RuntimeError("transient store failure")

        def get_by_event_id(self, event_id: str):
            return None

    outbox = MemoryOutboxSink()
    metrics = AnalyticsOperationalMetrics()
    event = _event(entity="retry-1")
    record = outbox.enqueue(event, payload_json=serialize_for_outbox(event))
    worker = AnalyticsOutboxWorker(
        outbox=outbox,
        store=BoomStore(),
        metrics=metrics,
        max_attempts=3,
        batch_size=10,
    )
    # Attempt 1 + 2 → failed; attempt 3 → dead letter.
    worker.run_once()
    row = outbox.get(record.outbox_id)
    assert row is not None
    assert row.status == OUTBOX_FAILED
    assert row.attempts == 1
    worker.run_once()
    row = outbox.get(record.outbox_id)
    assert row is not None
    assert row.status == OUTBOX_FAILED
    assert row.attempts == 2
    worker.run_once()
    row = outbox.get(record.outbox_id)
    assert row is not None
    assert row.status == OUTBOX_DEAD_LETTER
    assert row.attempts == 3
    assert metrics.dead_letter_count == 1


def test_duplicate_prevention_on_enqueue_and_drain() -> None:
    outbox = MemoryOutboxSink()
    store = MemoryAnalyticsEventStore()
    metrics = AnalyticsOperationalMetrics()
    dispatcher = _enabled_dispatcher(outbox, metrics)
    event = _event(entity="dup-1")
    first = dispatcher.dispatch(event)
    second = dispatcher.dispatch(event)
    assert first.status == DispatchStatus.ENQUEUED
    assert second.status == DispatchStatus.DUPLICATE
    assert len(outbox.pending()) == 1

    worker = AnalyticsOutboxWorker(outbox=outbox, store=store, metrics=metrics)
    assert worker.run_once().processed == 1

    # Re-enqueue same key after processed (simulates race) then drain again.
    # Memory outbox still holds the key → enqueue returns existing processed.
    again = outbox.enqueue(event, payload_json=serialize_for_outbox(event))
    assert again.status == OUTBOX_PROCESSED


def test_outbox_corruption_dead_letters() -> None:
    outbox = MemoryOutboxSink()
    store = MemoryAnalyticsEventStore()
    metrics = AnalyticsOperationalMetrics()
    event = _event(entity="corrupt-1")
    record = outbox.enqueue(event, payload_json="{not-json")
    worker = AnalyticsOutboxWorker(
        outbox=outbox, store=store, metrics=metrics, max_attempts=1
    )
    batch = worker.run_once()
    assert batch.dead_lettered == 1
    assert outbox.get(record.outbox_id).status == OUTBOX_DEAD_LETTER
    assert store.get_by_event_id(event.event_id) is None


def test_feature_flag_transitions_no_educational_side_effects() -> None:
    outbox = MemoryOutboxSink()
    metrics = AnalyticsOperationalMetrics()
    event = _event(entity="flag-1")

    off = AnalyticsEventDispatcher(
        outbox=outbox,
        feature_flag=AnalyticsFeatureFlag(events_v1=False),
        metrics=metrics,
    )
    assert off.dispatch(event).status == DispatchStatus.DISABLED
    assert outbox.pending() == ()

    on = AnalyticsEventDispatcher(
        outbox=outbox,
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        metrics=metrics,
    )
    assert on.dispatch(event).status == DispatchStatus.ENQUEUED
    assert len(outbox.pending()) == 1

    # Kill switch: new dispatcher with flag off writes nothing further.
    off2 = AnalyticsEventDispatcher(
        outbox=outbox,
        feature_flag=AnalyticsFeatureFlag(events_v1=False),
        metrics=metrics,
    )
    assert off2.dispatch(_event(entity="flag-2")).status == DispatchStatus.DISABLED
    assert len(outbox.pending()) == 1  # prior row retained; no new writes


def test_database_unavailable_fail_open_dispatch() -> None:
    class BoomOutbox:
        name = "boom"

        def enqueue(self, event, *, payload_json: str):
            raise RuntimeError("database unavailable")

        def pending(self):
            return ()

    metrics = AnalyticsOperationalMetrics()
    dispatcher = AnalyticsEventDispatcher(
        outbox=BoomOutbox(),
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        metrics=metrics,
    )
    result = dispatcher.dispatch(_event(entity="db-down"))
    assert result.status == DispatchStatus.FAILED
    assert metrics.events_failed == 1


def test_replay_dead_letter_then_process() -> None:
    outbox = MemoryOutboxSink()
    store = MemoryAnalyticsEventStore()
    metrics = AnalyticsOperationalMetrics()
    event = _event(entity="replay-1")
    record = outbox.enqueue(event, payload_json="{bad")
    worker = AnalyticsOutboxWorker(
        outbox=outbox, store=store, metrics=metrics, max_attempts=1
    )
    worker.run_once()
    assert outbox.get(record.outbox_id).status == OUTBOX_DEAD_LETTER

    # Fix payload then replay.
    for i, row in enumerate(outbox._records):
        if row.outbox_id == record.outbox_id:
            outbox._records[i] = OutboxRecord(
                outbox_id=row.outbox_id,
                event_id=row.event_id,
                event_type=row.event_type,
                user_id=row.user_id,
                idempotency_key=row.idempotency_key,
                payload_json=serialize_for_outbox(event),
                created_at=row.created_at,
                attempts=row.attempts,
                status=row.status,
                last_error=row.last_error,
                updated_at=row.updated_at,
            )
    replay = AnalyticsReplayService(
        outbox=outbox, worker=worker, metrics=metrics
    )
    result = replay.replay_and_drain(outbox_ids=(record.outbox_id,))
    assert result.requeued == 1
    assert result.processed == 1
    assert store.get_by_event_id(event.event_id) is not None
    assert metrics.replay_count == 1


def test_cleanup_processed_outbox_rows() -> None:
    outbox = MemoryOutboxSink()
    event = _event(entity="clean-1")
    record = outbox.enqueue(event, payload_json=serialize_for_outbox(event))
    outbox.mark_processed(record.outbox_id)
    # Age the row.
    aged = outbox.get(record.outbox_id)
    assert aged is not None
    outbox._records[0] = OutboxRecord(
        outbox_id=aged.outbox_id,
        event_id=aged.event_id,
        event_type=aged.event_type,
        user_id=aged.user_id,
        idempotency_key=aged.idempotency_key,
        payload_json=aged.payload_json,
        created_at=aged.created_at - timedelta(days=30),
        attempts=aged.attempts,
        status=OUTBOX_PROCESSED,
        last_error=None,
        updated_at=datetime.now(tz=UTC) - timedelta(days=30),
    )
    job = AnalyticsCleanupJob(outbox=outbox, retention_days=7)
    result = job.run(dry_run=False)
    assert result.deleted == 1
    assert outbox.get(record.outbox_id) is None


def test_retention_enforcement_audited() -> None:
    store = MemoryAnalyticsEventStore()
    outbox = MemoryOutboxSink()
    audit = MemoryAnalyticsAuditLog()
    old = _event(entity="old-1")
    # Force old occurred_at
    old = AnalyticsEvent.create(
        old.event_type,
        user_id=old.user_id,
        payload=dict(old.payload),
        event_id=old.event_id,
        occurred_at=datetime.now(tz=UTC) - timedelta(days=600),
        idempotency_key=old.idempotency_key,
    )
    store.append(old, payload_json=serialize_for_outbox(old))
    purge = AnalyticsPurgeJob(store=store)
    cleanup = AnalyticsCleanupJob(outbox=outbox, audit=audit)
    enforcer = AnalyticsRetentionEnforcer(
        purge_job=purge, cleanup_job=cleanup, audit=audit
    )
    result = enforcer.run(dry_run=False)
    assert result.purge.deleted == 1
    assert result.audit_id
    assert audit.list_actions(action="analytics.purge_run")


def test_privacy_delete_export_consent() -> None:
    store = MemoryAnalyticsEventStore()
    outbox = MemoryOutboxSink()
    audit = MemoryAnalyticsAuditLog()
    metrics = AnalyticsOperationalMetrics()
    privacy = AnalyticsPrivacyService(
        event_store=store,
        outbox=outbox,
        audit=audit,
        metrics=metrics,
    )
    event = _event(user_id=42, entity="priv-1")
    store.append(event, payload_json=serialize_for_outbox(event))
    outbox.enqueue(event, payload_json=serialize_for_outbox(event))

    consent = privacy.verify_consent(user_id=42)
    assert consent.allowed is True
    assert privacy.verify_consent(user_id=42, marketing_use=True).allowed is False

    export = privacy.export_student(42)
    assert export.event_count == 1
    assert '"user_id": 42' in export.payload

    deleted = privacy.delete_user_analytics(42)
    assert deleted.events_deleted == 1
    assert deleted.outbox_deleted == 1
    assert store.list_for_user(42) == []
    assert audit.list_actions(action="analytics.user_deleted")
    assert metrics.user_deletions == 1


def test_metrics_snapshot_infrastructure_only() -> None:
    metrics = AnalyticsOperationalMetrics()
    metrics.record_dispatch(status="enqueued", elapsed_ms=1.5)
    metrics.record_dead_letter()
    metrics.set_queue_depth(3)
    snap = metrics.snapshot()
    assert snap["events_received"] == 1
    assert snap["events_dispatched"] == 1
    assert snap["dead_letter_count"] == 1
    assert snap["queue_depth"] == 3
    # No educational metric keys.
    forbidden = ("mastery", "readiness", "recommendation", "confidence")
    joined = " ".join(snap.keys()).lower()
    for needle in forbidden:
        assert needle not in joined


def test_flag_off_default_environment_disabled(monkeypatch) -> None:
    monkeypatch.delenv("ANALYTICS_EVENTS_V1", raising=False)
    monkeypatch.delenv("KWALITEC_ANALYTICS_EVENTS_V1", raising=False)
    from app.infrastructure.analytics.feature_flag import resolve_analytics_feature_flag

    flag = resolve_analytics_feature_flag(environ={})
    assert flag.enabled is False
    assert DispatchStatus.DISABLED.value == "disabled"
    assert DispatchStatus.ENQUEUED.value == "enqueued"
