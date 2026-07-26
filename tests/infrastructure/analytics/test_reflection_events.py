"""Unit tests — Phase C reflection event builders, validation, serialization."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.infrastructure.analytics.dispatcher import (
    AnalyticsEventDispatcher,
    DispatchStatus,
)
from app.infrastructure.analytics.feature_flag import AnalyticsFeatureFlag
from app.infrastructure.analytics.outbox import MemoryOutboxSink
from app.infrastructure.analytics.reflection_events import (
    PROCESSING_COMPLETED,
    REFLECTION_COMPLETED,
    REFLECTION_SUBMITTED,
    REFLECTION_TYPE_JOURNEY_SESSION,
    build_reflection_completed_event,
    build_reflection_submitted_event,
    emit_reflection_completed,
    emit_reflection_lifecycle,
    emit_reflection_submitted,
)
from app.infrastructure.analytics.registry import AnalyticsEventRegistry
from app.infrastructure.analytics.serialization import AnalyticsEventSerializer
from app.infrastructure.analytics.validator import AnalyticsEventValidator


def test_build_reflection_submitted_payload() -> None:
    event = build_reflection_submitted_event(
        user_id=7,
        reflection_id="ref-abc",
        session_id="sess-1",
        correlation_id="corr-sub",
        occurred_at=datetime(2026, 7, 24, 10, 0, tzinfo=UTC),
    )
    assert event.event_type == REFLECTION_SUBMITTED
    assert event.user_id == 7
    assert event.payload["reflection_id"] == "ref-abc"
    assert event.payload["session_id"] == "sess-1"
    assert event.payload["student_id"] == 7
    assert event.payload["reflection_type"] == REFLECTION_TYPE_JOURNEY_SESSION
    assert event.idempotency_key == "7:reflection.submitted:ref-abc"
    assert event.correlation_id == "corr-sub"
    assert int(event.schema_version) == 1
    assert "content" not in event.payload
    assert "summary" not in event.payload
    assert "what_was_learned" not in event.payload


def test_build_reflection_completed_payload() -> None:
    event = build_reflection_completed_event(
        user_id=7,
        reflection_id="ref-abc",
        processing_status=PROCESSING_COMPLETED,
        occurred_at=datetime(2026, 7, 24, 11, 0, tzinfo=UTC),
    )
    assert event.event_type == REFLECTION_COMPLETED
    assert event.payload["reflection_id"] == "ref-abc"
    assert event.payload["processing_status"] == "completed"
    assert event.idempotency_key == "7:reflection.completed:ref-abc"
    assert "EducationalState" not in event.payload
    assert "twin" not in event.payload


def test_invalid_processing_status_rejected() -> None:
    with pytest.raises(ValueError, match="processing_status"):
        build_reflection_completed_event(
            user_id=1,
            reflection_id="ref-1",
            processing_status="failed",
        )


def test_invalid_reflection_type_rejected() -> None:
    with pytest.raises(ValueError, match="reflection_type"):
        build_reflection_submitted_event(
            user_id=1,
            reflection_id="ref-1",
            session_id="sess-1",
            reflection_type="free_text_diary",
        )


def test_reflection_events_validate_against_phase_c_registry() -> None:
    registry = AnalyticsEventRegistry.phase_c_default()
    validator = AnalyticsEventValidator(registry)
    submitted = build_reflection_submitted_event(
        user_id=1, reflection_id="ref-1", session_id="s1"
    )
    completed = build_reflection_completed_event(
        user_id=1, reflection_id="ref-1"
    )
    assert validator.validate(submitted).ok
    assert validator.validate(completed).ok


def test_reflection_events_rejected_on_phase_b_registry() -> None:
    registry = AnalyticsEventRegistry.phase_b_default()
    validator = AnalyticsEventValidator(registry)
    submitted = build_reflection_submitted_event(
        user_id=1, reflection_id="ref-1", session_id="s1"
    )
    result = validator.validate(submitted)
    assert not result.ok
    assert any("unknown event_type" in e for e in result.errors)


def test_reflection_event_serialization_roundtrip() -> None:
    ser = AnalyticsEventSerializer()
    original = build_reflection_submitted_event(
        user_id=5,
        reflection_id="ref-x",
        session_id="sess-y",
        occurred_at=datetime(2026, 7, 24, 12, 0, tzinfo=UTC),
    )
    restored = ser.from_json(ser.to_json(original))
    assert restored.event_type == REFLECTION_SUBMITTED
    assert restored.payload == original.payload
    assert restored.idempotency_key == original.idempotency_key


def test_emit_reflection_submitted_flag_off_is_noop() -> None:
    outbox = MemoryOutboxSink()
    dispatcher = AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=False),
        outbox=outbox,
    )
    result = emit_reflection_submitted(
        user_id=1,
        reflection_id="ref-10",
        session_id="sess-10",
        dispatcher=dispatcher,
    )
    assert result.status is DispatchStatus.DISABLED
    assert outbox.pending() == ()


def test_emit_reflection_completed_flag_on_enqueues() -> None:
    outbox = MemoryOutboxSink()
    dispatcher = AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        outbox=outbox,
        registry=AnalyticsEventRegistry.phase_c_default(),
    )
    result = emit_reflection_completed(
        user_id=1,
        reflection_id="ref-10",
        dispatcher=dispatcher,
    )
    assert result.status is DispatchStatus.ENQUEUED
    assert len(outbox.pending()) == 1
    assert REFLECTION_COMPLETED in outbox.pending()[0].payload_json


def test_emit_lifecycle_shares_correlation_id() -> None:
    outbox = MemoryOutboxSink()
    dispatcher = AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        outbox=outbox,
        registry=AnalyticsEventRegistry.phase_c_default(),
    )
    submitted, completed = emit_reflection_lifecycle(
        user_id=2,
        reflection_id="ref-pair",
        session_id="sess-pair",
        dispatcher=dispatcher,
        correlation_id="shared-corr",
    )
    assert submitted.status is DispatchStatus.ENQUEUED
    assert completed.status is DispatchStatus.ENQUEUED
    assert len(outbox.pending()) == 2
    types = {r.event_type for r in outbox.pending()}
    assert types == {REFLECTION_SUBMITTED, REFLECTION_COMPLETED}
    # Correlation lives in the serialized envelope JSON.
    for record in outbox.pending():
        assert "shared-corr" in record.payload_json


class _BoomOutbox(MemoryOutboxSink):
    def enqueue(self, event, *, payload_json: str = ""):  # type: ignore[override]
        raise RuntimeError("outbox unavailable")


def test_emit_fail_open_when_outbox_unavailable() -> None:
    dispatcher = AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        outbox=_BoomOutbox(),
        registry=AnalyticsEventRegistry.phase_c_default(),
    )
    result = emit_reflection_submitted(
        user_id=1,
        reflection_id="ref-99",
        session_id="sess-99",
        dispatcher=dispatcher,
    )
    assert result.status is DispatchStatus.FAILED
    assert "analytics.emit_failed" in result.errors
