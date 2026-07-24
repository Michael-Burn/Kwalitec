"""Unit / integration tests — dispatcher lifecycle and feature flag."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from app.infrastructure.analytics.contracts import AnalyticsEvent
from app.infrastructure.analytics.dispatcher import (
    AnalyticsEventDispatcher,
    DispatchStatus,
)
from app.infrastructure.analytics.feature_flag import (
    AnalyticsFeatureFlag,
    resolve_analytics_feature_flag,
)
from app.infrastructure.analytics.idempotency import build_idempotency_key
from app.infrastructure.analytics.outbox import MemoryOutboxSink
from app.infrastructure.analytics.purge import AnalyticsPurgeJob
from app.infrastructure.analytics.registry import (
    INFRASTRUCTURE_PROBE,
    AnalyticsEventRegistry,
)
from app.infrastructure.analytics.repository import MemoryAnalyticsEventStore


def _probe(**kwargs) -> AnalyticsEvent:
    defaults = {
        "event_type": INFRASTRUCTURE_PROBE,
        "user_id": 42,
        "payload": {"ok": True},
        "idempotency_key": build_idempotency_key(
            user_id=42,
            event_type=INFRASTRUCTURE_PROBE,
            entity_key="entity-1",
        ),
    }
    defaults.update(kwargs)
    return AnalyticsEvent.create(**defaults)


def test_feature_flag_defaults_off() -> None:
    flag = resolve_analytics_feature_flag(environ={})
    assert flag.enabled is False
    assert flag.events_v1 is False


def test_feature_flag_truthy_env() -> None:
    for value in ("1", "true", "YES", "on"):
        flag = resolve_analytics_feature_flag(
            environ={"ANALYTICS_EVENTS_V1": value}
        )
        assert flag.enabled is True, value


def test_feature_flag_alias_env() -> None:
    flag = resolve_analytics_feature_flag(
        environ={"KWALITEC_ANALYTICS_EVENTS_V1": "true"}
    )
    assert flag.enabled is True


def test_dispatcher_disabled_is_noop() -> None:
    outbox = MemoryOutboxSink()
    dispatcher = AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=False),
        outbox=outbox,
    )
    result = dispatcher.dispatch(_probe())
    assert result.status is DispatchStatus.DISABLED
    assert outbox.pending() == ()


def test_dispatcher_enqueues_when_enabled() -> None:
    outbox = MemoryOutboxSink()
    dispatcher = AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        outbox=outbox,
        registry=AnalyticsEventRegistry.phase_a_default(),
    )
    result = dispatcher.dispatch(_probe())
    assert result.status is DispatchStatus.ENQUEUED
    assert result.outbox_id
    assert len(outbox.pending()) == 1
    assert result.elapsed_ms >= 0.0


def test_dispatcher_idempotent_duplicate() -> None:
    outbox = MemoryOutboxSink()
    dispatcher = AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        outbox=outbox,
    )
    first = dispatcher.dispatch(_probe())
    second = dispatcher.dispatch(_probe(event_id="different-id"))
    assert first.status is DispatchStatus.ENQUEUED
    assert second.status is DispatchStatus.DUPLICATE
    assert len(outbox.pending()) == 1


def test_dispatcher_rejects_unknown_type_when_enabled() -> None:
    dispatcher = AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        outbox=MemoryOutboxSink(),
    )
    event = AnalyticsEvent.create(
        "analytics.unknown_future_type",
        user_id=1,
        payload={},
        idempotency_key="1:analytics.unknown_future_type:s1",
    )
    result = dispatcher.dispatch(event)
    assert result.status is DispatchStatus.REJECTED
    assert result.errors


def test_dispatcher_assigns_correlation_id() -> None:
    dispatcher = AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        outbox=MemoryOutboxSink(),
    )
    result = dispatcher.dispatch(_probe(correlation_id=""))
    assert result.status is DispatchStatus.ENQUEUED
    pending = dispatcher.outbox.pending()
    assert pending
    # Serialized payload includes a correlation id.
    assert "correlation_id" in pending[0].payload_json


def test_purge_skeleton_no_store() -> None:
    job = AnalyticsPurgeJob(store=None)
    result = job.run(dry_run=True)
    assert result.dry_run is True
    assert result.notes == "no_store"
    assert result.deleted == 0


def test_purge_skeleton_memory_store() -> None:
    store = MemoryAnalyticsEventStore()
    old = _probe(
        event_id="old",
        occurred_at=datetime.now(tz=UTC) - timedelta(days=600),
        idempotency_key=build_idempotency_key(
            user_id=42,
            event_type=INFRASTRUCTURE_PROBE,
            entity_key="old",
        ),
    )
    new = _probe(
        event_id="new",
        occurred_at=datetime.now(tz=UTC),
        idempotency_key=build_idempotency_key(
            user_id=42,
            event_type=INFRASTRUCTURE_PROBE,
            entity_key="new",
        ),
    )
    store.append(old, payload_json="{}")
    store.append(new, payload_json="{}")
    job = AnalyticsPurgeJob(store=store)
    dry = job.run(dry_run=True)
    assert dry.scanned == 1
    assert dry.deleted == 0
    wet = job.run(dry_run=False)
    assert wet.deleted == 1
    assert store.get_by_event_id("new") is not None
    assert store.get_by_event_id("old") is None


def test_memory_store_idempotent_append() -> None:
    store = MemoryAnalyticsEventStore()
    event = _probe()
    assert store.append(event, payload_json="{}") is True
    assert store.append(event, payload_json="{}") is False
