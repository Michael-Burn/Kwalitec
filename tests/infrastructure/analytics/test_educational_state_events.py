"""Unit tests — Phase D Educational State snapshot events + content hash."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.application.educational_state import EducationalStateSnapshot
from app.application.educational_state.content_hash import (
    compute_educational_state_content_hash,
)
from app.infrastructure.analytics.dispatcher import (
    AnalyticsEventDispatcher,
    DispatchStatus,
)
from app.infrastructure.analytics.educational_state_events import (
    EDUCATIONAL_STATE_SNAPSHOT,
    build_educational_state_snapshot_event,
    emit_educational_state_snapshot,
)
from app.infrastructure.analytics.feature_flag import AnalyticsFeatureFlag
from app.infrastructure.analytics.outbox import MemoryOutboxSink
from app.infrastructure.analytics.registry import AnalyticsEventRegistry
from app.infrastructure.analytics.serialization import AnalyticsEventSerializer
from app.infrastructure.analytics.validator import AnalyticsEventValidator

_HASH_A = "a" * 64
_HASH_B = "b" * 64


def _snapshot(**overrides) -> EducationalStateSnapshot:
    base = dict(
        student_id="42",
        learner_summary={"display_name": "Ada"},
        readiness_summary={"level": "building"},
        recommendation={"topic_id": "t1"},
        todays_session={"mission_id": 9},
        journey_progress={"pct": 10},
        journey_topics=({"id": "t1"},),
        learning_insights={"streak": 3},
        revision_options=({"id": "r1"},),
        twin_available=True,
        adaptive_available=True,
        mission_available=True,
        journey_available=True,
    )
    base.update(overrides)
    return EducationalStateSnapshot(**base)


def test_content_hash_deterministic() -> None:
    a = compute_educational_state_content_hash(_snapshot())
    b = compute_educational_state_content_hash(_snapshot())
    assert a == b
    assert len(a) == 64
    assert a == a.lower()


def test_content_hash_changes_on_material_difference() -> None:
    first = compute_educational_state_content_hash(_snapshot())
    second = compute_educational_state_content_hash(
        _snapshot(readiness_summary={"level": "exam_ready"})
    )
    assert first != second


def test_build_snapshot_event_payload_hash_and_metadata_only() -> None:
    event = build_educational_state_snapshot_event(
        user_id=42,
        snapshot_id="snap-1",
        content_hash=_HASH_A,
        correlation_id="corr-ess",
        occurred_at=datetime(2026, 7, 24, 10, 0, tzinfo=UTC),
    )
    assert event.event_type == EDUCATIONAL_STATE_SNAPSHOT
    assert event.user_id == 42
    assert event.payload == {
        "snapshot_id": "snap-1",
        "content_hash": _HASH_A,
    }
    assert event.idempotency_key == "42:educational_state.snapshot:snap-1"
    assert event.correlation_id == "corr-ess"
    assert int(event.schema_version) == 1
    # Forbidden educational payloads
    assert "learner_summary" not in event.payload
    assert "readiness_summary" not in event.payload
    assert "recommendation" not in event.payload
    assert "journey_topics" not in event.payload
    assert "learning_insights" not in event.payload
    assert "EducationalState" not in event.payload
    assert "twin" not in event.payload


def test_invalid_content_hash_rejected() -> None:
    with pytest.raises(ValueError, match="content_hash"):
        build_educational_state_snapshot_event(
            user_id=1,
            snapshot_id="snap-1",
            content_hash="not-a-hash",
        )


def test_empty_snapshot_id_rejected() -> None:
    with pytest.raises(ValueError, match="snapshot_id"):
        build_educational_state_snapshot_event(
            user_id=1,
            snapshot_id="  ",
            content_hash=_HASH_A,
        )


def test_snapshot_event_validates_against_phase_d_registry() -> None:
    registry = AnalyticsEventRegistry.phase_d_default()
    validator = AnalyticsEventValidator(registry)
    event = build_educational_state_snapshot_event(
        user_id=1,
        snapshot_id="snap-1",
        content_hash=_HASH_A,
    )
    assert validator.validate(event).ok


def test_snapshot_event_rejected_on_phase_c_registry() -> None:
    registry = AnalyticsEventRegistry.phase_c_default()
    validator = AnalyticsEventValidator(registry)
    event = build_educational_state_snapshot_event(
        user_id=1,
        snapshot_id="snap-1",
        content_hash=_HASH_A,
    )
    result = validator.validate(event)
    assert not result.ok
    assert any("unknown event_type" in e for e in result.errors)


def test_snapshot_event_serialization_roundtrip() -> None:
    ser = AnalyticsEventSerializer()
    original = build_educational_state_snapshot_event(
        user_id=5,
        snapshot_id="snap-x",
        content_hash=_HASH_B,
        occurred_at=datetime(2026, 7, 24, 12, 0, tzinfo=UTC),
    )
    restored = ser.from_json(ser.to_json(original))
    assert restored.event_type == EDUCATIONAL_STATE_SNAPSHOT
    assert restored.payload == original.payload
    assert restored.idempotency_key == original.idempotency_key


def test_emit_snapshot_flag_off_is_noop() -> None:
    outbox = MemoryOutboxSink()
    dispatcher = AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=False),
        outbox=outbox,
    )
    result = emit_educational_state_snapshot(
        user_id=1,
        snapshot_id="snap-10",
        content_hash=_HASH_A,
        dispatcher=dispatcher,
    )
    assert result.status is DispatchStatus.DISABLED
    assert outbox.pending() == ()


def test_emit_snapshot_flag_on_enqueues() -> None:
    outbox = MemoryOutboxSink()
    dispatcher = AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        outbox=outbox,
        registry=AnalyticsEventRegistry.phase_d_default(),
    )
    result = emit_educational_state_snapshot(
        user_id=1,
        snapshot_id="snap-10",
        content_hash=_HASH_A,
        dispatcher=dispatcher,
    )
    assert result.status is DispatchStatus.ENQUEUED
    assert len(outbox.pending()) == 1
    assert EDUCATIONAL_STATE_SNAPSHOT in outbox.pending()[0].payload_json
    assert _HASH_A in outbox.pending()[0].payload_json
    assert "learner_summary" not in outbox.pending()[0].payload_json


class _BoomOutbox(MemoryOutboxSink):
    def enqueue(self, event, *, payload_json: str = ""):  # type: ignore[override]
        raise RuntimeError("outbox unavailable")


def test_emit_fail_open_when_outbox_unavailable() -> None:
    dispatcher = AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        outbox=_BoomOutbox(),
        registry=AnalyticsEventRegistry.phase_d_default(),
    )
    result = emit_educational_state_snapshot(
        user_id=1,
        snapshot_id="snap-99",
        content_hash=_HASH_A,
        dispatcher=dispatcher,
    )
    assert result.status is DispatchStatus.FAILED
    assert "analytics.emit_failed" in result.errors
