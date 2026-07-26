"""Unit tests — Phase E Twin evolution events + snapshot hash."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.application.twin_repository.content_hash import compute_twin_snapshot_hash
from app.infrastructure.analytics.dispatcher import (
    AnalyticsEventDispatcher,
    DispatchStatus,
)
from app.infrastructure.analytics.feature_flag import AnalyticsFeatureFlag
from app.infrastructure.analytics.outbox import MemoryOutboxSink
from app.infrastructure.analytics.registry import AnalyticsEventRegistry
from app.infrastructure.analytics.serialization import AnalyticsEventSerializer
from app.infrastructure.analytics.twin_events import (
    EVOLUTION_BIRTH,
    EVOLUTION_SUCCESSOR,
    TWIN_EVOLVED,
    build_twin_evolved_event,
    emit_twin_evolved,
)
from app.infrastructure.analytics.validator import AnalyticsEventValidator

_HASH_A = "a" * 64
_HASH_B = "b" * 64


def test_snapshot_hash_deterministic() -> None:
    payload = '{"format_version":"1.0","twin":{"identity":{"student_id":"42"}}}'
    a = compute_twin_snapshot_hash(payload)
    b = compute_twin_snapshot_hash(payload)
    assert a == b
    assert len(a) == 64
    assert a == a.lower()


def test_snapshot_hash_changes_on_material_difference() -> None:
    first = compute_twin_snapshot_hash('{"twin":{"v":1}}')
    second = compute_twin_snapshot_hash('{"twin":{"v":2}}')
    assert first != second


def test_build_twin_evolved_payload_hash_and_metadata_only() -> None:
    event = build_twin_evolved_event(
        user_id=42,
        twin_snapshot_id="snap-1",
        twin_version="1",
        evolution_reason=EVOLUTION_BIRTH,
        snapshot_hash=_HASH_A,
        correlation_id="corr-twin",
        occurred_at=datetime(2026, 7, 24, 10, 0, tzinfo=UTC),
    )
    assert event.event_type == TWIN_EVOLVED
    assert event.user_id == 42
    assert event.payload == {
        "twin_snapshot_id": "snap-1",
        "twin_version": "1",
        "evolution_reason": EVOLUTION_BIRTH,
        "snapshot_hash": _HASH_A,
    }
    assert event.idempotency_key == "42:twin.evolved:snap-1"
    assert event.correlation_id == "corr-twin"
    assert int(event.schema_version) == 1
    # Forbidden Twin / educational payloads
    assert "knowledge" not in event.payload
    assert "beliefs" not in event.payload
    assert "mastery" not in event.payload
    assert "twin_payload" not in event.payload
    assert "EducationalState" not in event.payload


def test_invalid_snapshot_hash_rejected() -> None:
    with pytest.raises(ValueError, match="snapshot_hash"):
        build_twin_evolved_event(
            user_id=1,
            twin_snapshot_id="snap-1",
            twin_version="1",
            evolution_reason=EVOLUTION_BIRTH,
            snapshot_hash="not-a-hash",
        )


def test_invalid_evolution_reason_rejected() -> None:
    with pytest.raises(ValueError, match="evolution_reason"):
        build_twin_evolved_event(
            user_id=1,
            twin_snapshot_id="snap-1",
            twin_version="1",
            evolution_reason="mastery_recalc",
            snapshot_hash=_HASH_A,
        )


def test_serialize_twin_evolved_roundtrip() -> None:
    event = build_twin_evolved_event(
        user_id=7,
        twin_snapshot_id="snap-7",
        twin_version="3",
        evolution_reason=EVOLUTION_SUCCESSOR,
        snapshot_hash=_HASH_B,
    )
    serializer = AnalyticsEventSerializer()
    restored = serializer.from_json(serializer.to_json(event))
    assert restored.event_type == TWIN_EVOLVED
    assert restored.payload["snapshot_hash"] == _HASH_B
    assert "twin_payload" not in restored.payload


def test_validator_accepts_registered_twin_evolved() -> None:
    registry = AnalyticsEventRegistry.phase_e_default()
    validator = AnalyticsEventValidator(registry)
    event = build_twin_evolved_event(
        user_id=1,
        twin_snapshot_id="snap-1",
        twin_version="1",
        evolution_reason=EVOLUTION_BIRTH,
        snapshot_hash=_HASH_A,
    )
    assert validator.validate(event).ok


def test_emit_flag_off_is_disabled() -> None:
    result = emit_twin_evolved(
        user_id=1,
        twin_snapshot_id="snap-1",
        twin_version="1",
        evolution_reason=EVOLUTION_BIRTH,
        snapshot_hash=_HASH_A,
        dispatcher=AnalyticsEventDispatcher(
            feature_flag=AnalyticsFeatureFlag(events_v1=False),
            outbox=MemoryOutboxSink(),
            registry=AnalyticsEventRegistry.phase_e_default(),
        ),
    )
    assert result.status is DispatchStatus.DISABLED


def test_emit_flag_on_enqueues() -> None:
    outbox = MemoryOutboxSink()
    result = emit_twin_evolved(
        user_id=1,
        twin_snapshot_id="snap-1",
        twin_version="1",
        evolution_reason=EVOLUTION_BIRTH,
        snapshot_hash=_HASH_A,
        dispatcher=AnalyticsEventDispatcher(
            feature_flag=AnalyticsFeatureFlag(events_v1=True),
            outbox=outbox,
            registry=AnalyticsEventRegistry.phase_e_default(),
        ),
    )
    assert result.status is DispatchStatus.ENQUEUED
    assert len(outbox.pending()) == 1
    assert outbox.pending()[0].event_type == TWIN_EVOLVED
