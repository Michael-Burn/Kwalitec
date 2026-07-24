"""Unit tests — Phase B session event builders, validation, serialization."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.infrastructure.analytics.dispatcher import (
    AnalyticsEventDispatcher,
    DispatchStatus,
)
from app.infrastructure.analytics.feature_flag import AnalyticsFeatureFlag
from app.infrastructure.analytics.outbox import MemoryOutboxSink
from app.infrastructure.analytics.registry import AnalyticsEventRegistry
from app.infrastructure.analytics.serialization import AnalyticsEventSerializer
from app.infrastructure.analytics.session_events import (
    COMPLETION_ABANDONED_AFTER_START,
    COMPLETION_COMPLETED,
    SESSION_COMPLETED,
    SESSION_STARTED,
    build_session_completed_event,
    build_session_started_event,
    emit_session_completed,
    emit_session_started,
    session_entity_key,
)
from app.infrastructure.analytics.validator import AnalyticsEventValidator


def test_session_entity_key() -> None:
    assert session_entity_key(42) == "mission:42"


def test_build_session_started_payload() -> None:
    event = build_session_started_event(
        user_id=7,
        mission_id=42,
        curriculum_node_id=99,
        correlation_id="corr-start",
        occurred_at=datetime(2026, 7, 24, 10, 0, tzinfo=UTC),
    )
    assert event.event_type == SESSION_STARTED
    assert event.user_id == 7
    assert event.payload["session_id"] == "mission:42"
    assert event.payload["mission_id"] == 42
    assert event.payload["curriculum_node_id"] == 99
    assert event.idempotency_key == "7:session.started:mission:42"
    assert event.correlation_id == "corr-start"
    assert int(event.schema_version) == 1


def test_build_session_completed_payload() -> None:
    event = build_session_completed_event(
        user_id=7,
        mission_id=42,
        completion_status=COMPLETION_COMPLETED,
        topic_id=11,
        duration_seconds=1800,
        occurred_at=datetime(2026, 7, 24, 11, 0, tzinfo=UTC),
    )
    assert event.event_type == SESSION_COMPLETED
    assert event.payload["completion_status"] == "completed"
    assert event.payload["topic_id"] == 11
    assert event.payload["duration_seconds"] == 1800
    assert event.payload["started_at"] == "2026-07-24T10:30:00Z"
    assert event.idempotency_key == "7:session.completed:mission:42"


def test_build_session_abandoned_payload() -> None:
    event = build_session_completed_event(
        user_id=3,
        mission_id=9,
        completion_status=COMPLETION_ABANDONED_AFTER_START,
        abandon_reason="completion_no",
    )
    assert event.payload["completion_status"] == "abandoned_after_start"
    assert event.payload["abandon_reason"] == "completion_no"
    assert "EducationalState" not in event.payload
    assert "twin" not in event.payload


def test_invalid_completion_status_rejected() -> None:
    with pytest.raises(ValueError, match="completion_status"):
        build_session_completed_event(
            user_id=1,
            mission_id=1,
            completion_status="cancelled",
        )


def test_session_events_validate_against_phase_b_registry() -> None:
    registry = AnalyticsEventRegistry.phase_b_default()
    validator = AnalyticsEventValidator(registry)
    started = build_session_started_event(user_id=1, mission_id=2)
    completed = build_session_completed_event(
        user_id=1,
        mission_id=2,
        completion_status=COMPLETION_COMPLETED,
    )
    assert validator.validate(started).ok
    assert validator.validate(completed).ok


def test_session_events_rejected_on_phase_a_registry() -> None:
    registry = AnalyticsEventRegistry.phase_a_default()
    validator = AnalyticsEventValidator(registry)
    started = build_session_started_event(user_id=1, mission_id=2)
    result = validator.validate(started)
    assert not result.ok
    assert any("unknown event_type" in e for e in result.errors)


def test_session_event_serialization_roundtrip() -> None:
    ser = AnalyticsEventSerializer()
    original = build_session_completed_event(
        user_id=5,
        mission_id=8,
        completion_status=COMPLETION_ABANDONED_AFTER_START,
        abandon_reason="completion_no",
        occurred_at=datetime(2026, 7, 24, 12, 0, tzinfo=UTC),
    )
    restored = ser.from_json(ser.to_json(original))
    assert restored.event_type == SESSION_COMPLETED
    assert restored.payload == original.payload
    assert restored.idempotency_key == original.idempotency_key


def test_emit_session_started_flag_off_is_noop() -> None:
    outbox = MemoryOutboxSink()
    dispatcher = AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=False),
        outbox=outbox,
    )
    result = emit_session_started(
        user_id=1,
        mission_id=10,
        dispatcher=dispatcher,
    )
    assert result.status is DispatchStatus.DISABLED
    assert outbox.pending() == ()


def test_emit_session_completed_flag_on_enqueues() -> None:
    outbox = MemoryOutboxSink()
    dispatcher = AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        outbox=outbox,
        registry=AnalyticsEventRegistry.phase_b_default(),
    )
    result = emit_session_completed(
        user_id=1,
        mission_id=10,
        completion_status=COMPLETION_COMPLETED,
        topic_id=3,
        dispatcher=dispatcher,
    )
    assert result.status is DispatchStatus.ENQUEUED
    assert len(outbox.pending()) == 1
    assert SESSION_COMPLETED in outbox.pending()[0].payload_json


class _BoomOutbox(MemoryOutboxSink):
    def enqueue(self, event, *, payload_json: str = ""):  # type: ignore[override]
        raise RuntimeError("outbox unavailable")


def test_emit_fail_open_when_outbox_unavailable() -> None:
    dispatcher = AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        outbox=_BoomOutbox(),
        registry=AnalyticsEventRegistry.phase_b_default(),
    )
    result = emit_session_started(
        user_id=1,
        mission_id=99,
        dispatcher=dispatcher,
    )
    assert result.status is DispatchStatus.FAILED
    assert "analytics.emit_failed" in result.errors
