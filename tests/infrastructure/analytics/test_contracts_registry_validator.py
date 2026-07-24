"""Unit tests — analytics event contracts, registry, validator, serialization."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.infrastructure.analytics.contracts import AnalyticsEvent
from app.infrastructure.analytics.correlation import new_correlation_id
from app.infrastructure.analytics.idempotency import build_idempotency_key
from app.infrastructure.analytics.registry import (
    INFRASTRUCTURE_PROBE,
    AnalyticsEventRegistry,
    EventTypeRegistration,
)
from app.infrastructure.analytics.serialization import AnalyticsEventSerializer
from app.infrastructure.analytics.validator import (
    MAX_PAYLOAD_BYTES,
    AnalyticsEventValidator,
)
from app.infrastructure.analytics.versioning import AnalyticsEventVersion


def _probe_event(**kwargs) -> AnalyticsEvent:
    defaults = {
        "event_type": INFRASTRUCTURE_PROBE,
        "user_id": 1,
        "payload": {"probe": True},
        "idempotency_key": build_idempotency_key(
            user_id=1,
            event_type=INFRASTRUCTURE_PROBE,
            entity_key="probe-1",
        ),
        "correlation_id": new_correlation_id(),
    }
    defaults.update(kwargs)
    return AnalyticsEvent.create(**defaults)


def test_analytics_event_create_requires_type_and_user() -> None:
    event = _probe_event()
    assert event.event_type == INFRASTRUCTURE_PROBE
    assert event.user_id == 1
    assert event.schema_version == AnalyticsEventVersion.V1
    assert event.event_id
    assert event.occurred_at.tzinfo is not None


def test_empty_event_type_rejected() -> None:
    with pytest.raises(ValueError):
        AnalyticsEvent.create("", user_id=1, payload={})


def test_invalid_user_id_rejected() -> None:
    with pytest.raises(ValueError):
        AnalyticsEvent.create(INFRASTRUCTURE_PROBE, user_id=0, payload={})


def test_schema_version_coerce() -> None:
    assert AnalyticsEventVersion.coerce(1) is AnalyticsEventVersion.V1
    with pytest.raises(ValueError):
        AnalyticsEventVersion.coerce(99)


def test_idempotency_key_stable() -> None:
    a = build_idempotency_key(
        user_id=7, event_type="analytics.infrastructure_probe", entity_key="x"
    )
    b = build_idempotency_key(
        user_id=7, event_type="analytics.infrastructure_probe", entity_key="x"
    )
    assert a == b == "7:analytics.infrastructure_probe:x"


def test_idempotency_key_requires_entity() -> None:
    with pytest.raises(ValueError):
        build_idempotency_key(
            user_id=1, event_type=INFRASTRUCTURE_PROBE, entity_key=""
        )


def test_correlation_id_unique() -> None:
    assert new_correlation_id() != new_correlation_id()
    assert len(new_correlation_id()) == 32


def test_registry_phase_a_knows_probe_only() -> None:
    registry = AnalyticsEventRegistry.phase_a_default()
    assert registry.is_known(INFRASTRUCTURE_PROBE)
    assert registry.known_types == (INFRASTRUCTURE_PROBE,)
    assert not registry.is_known("session.started")


def test_registry_phase_b_knows_session_events() -> None:
    registry = AnalyticsEventRegistry.phase_b_default()
    assert registry.is_known(INFRASTRUCTURE_PROBE)
    assert registry.is_known("session.started")
    assert registry.is_known("session.completed")
    assert not registry.is_known("reflection.completed")
    assert not registry.is_known("reflection.submitted")
    assert registry.get("session.started").required_payload_keys == (
        "session_id",
        "mission_id",
    )
    assert registry.get("session.completed").required_payload_keys == (
        "session_id",
        "mission_id",
        "completion_status",
    )


def test_registry_phase_c_knows_reflection_events() -> None:
    registry = AnalyticsEventRegistry.phase_c_default()
    assert registry.is_known(INFRASTRUCTURE_PROBE)
    assert registry.is_known("session.started")
    assert registry.is_known("session.completed")
    assert registry.is_known("reflection.submitted")
    assert registry.is_known("reflection.completed")
    assert not registry.is_known("journey.progressed")
    assert not registry.is_known("educational_state.snapshot")
    assert registry.get("reflection.submitted").required_payload_keys == (
        "reflection_id",
        "session_id",
        "student_id",
        "reflection_type",
    )
    assert registry.get("reflection.completed").required_payload_keys == (
        "reflection_id",
        "processing_status",
    )


def test_registry_phase_d_knows_educational_state_snapshot() -> None:
    registry = AnalyticsEventRegistry.phase_d_default()
    assert registry.is_known(INFRASTRUCTURE_PROBE)
    assert registry.is_known("session.started")
    assert registry.is_known("reflection.completed")
    assert registry.is_known("educational_state.snapshot")
    assert not registry.is_known("journey.progressed")
    assert not registry.is_known("twin.evolved")
    assert registry.get("educational_state.snapshot").required_payload_keys == (
        "snapshot_id",
        "content_hash",
    )


def test_registry_phase_e_knows_journey_and_twin_events() -> None:
    registry = AnalyticsEventRegistry.phase_e_default()
    assert registry.is_known(INFRASTRUCTURE_PROBE)
    assert registry.is_known("educational_state.snapshot")
    assert registry.is_known("journey.progressed")
    assert registry.is_known("twin.evolved")
    assert not registry.is_known("journey.milestone_reached")
    assert registry.get("journey.progressed").required_payload_keys == (
        "journey_id",
        "curriculum_node_id",
        "transition_id",
    )
    assert registry.get("twin.evolved").required_payload_keys == (
        "twin_snapshot_id",
        "twin_version",
        "evolution_reason",
        "snapshot_hash",
    )


def test_registry_register_custom_type() -> None:
    registry = AnalyticsEventRegistry()
    registry.register(
        EventTypeRegistration(
            event_type="custom.test",
            required_payload_keys=("a",),
        )
    )
    assert registry.is_known("custom.test")
    assert registry.get("custom.test").required_payload_keys == ("a",)


def test_validator_accepts_valid_probe() -> None:
    registry = AnalyticsEventRegistry.phase_a_default()
    validator = AnalyticsEventValidator(registry)
    result = validator.validate(_probe_event())
    assert result.ok
    assert result.errors == ()


def test_validator_rejects_unknown_type() -> None:
    registry = AnalyticsEventRegistry.phase_a_default()
    validator = AnalyticsEventValidator(registry)
    # Unknown type is allowed at envelope construction; registry rejects at validate.
    event = AnalyticsEvent.create(
        "analytics.unknown_future_type",
        user_id=1,
        payload={},
        idempotency_key="1:analytics.unknown_future_type:s1",
    )
    result = validator.validate(event)
    assert not result.ok
    assert any("unknown event_type" in e for e in result.errors)


def test_validator_rejects_missing_idempotency_key() -> None:
    registry = AnalyticsEventRegistry.phase_a_default()
    validator = AnalyticsEventValidator(registry)
    event = _probe_event(idempotency_key="")
    result = validator.validate(event)
    assert not result.ok
    assert any("idempotency_key" in e for e in result.errors)


def test_validator_rejects_oversized_payload() -> None:
    registry = AnalyticsEventRegistry.phase_a_default()
    validator = AnalyticsEventValidator(registry)
    huge = {"blob": "x" * (MAX_PAYLOAD_BYTES + 100)}
    event = _probe_event(payload=huge)
    result = validator.validate(event)
    assert not result.ok


def test_serialization_roundtrip() -> None:
    ser = AnalyticsEventSerializer()
    original = _probe_event(
        occurred_at=datetime(2026, 7, 24, 12, 0, tzinfo=UTC),
        correlation_id="corr-abc",
    )
    raw = ser.to_json(original)
    restored = ser.from_json(raw)
    assert restored.event_id == original.event_id
    assert restored.event_type == original.event_type
    assert restored.user_id == original.user_id
    assert restored.payload == original.payload
    assert restored.idempotency_key == original.idempotency_key
    assert restored.correlation_id == original.correlation_id
    assert int(restored.schema_version) == int(original.schema_version)


def test_serialization_missing_keys() -> None:
    ser = AnalyticsEventSerializer()
    with pytest.raises(ValueError, match="missing keys"):
        ser.from_dict({"event_id": "x"})
