"""Event envelope, serialization, and versioning tests."""

from __future__ import annotations

import pytest

from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.serialization import EventSerializer
from app.infrastructure.events.types import EVENT_TYPES
from app.infrastructure.events.versioning import (
    EventVersionPolicy,
    default_version_policy,
    identity_payload_rename,
)
from tests.infrastructure.helpers import EVENT_TYPE_LIST, LEARNERS, SUBJECTS


@pytest.mark.parametrize("event_type", EVENT_TYPE_LIST)
def test_create_event_requires_type_fields(event_type):
    event = IntegrationEvent.create(
        event_type,
        {"ok": True},
        source="test",
        correlation_id="c1",
        causation_id="cause1",
    )
    assert event.event_type == event_type
    assert event.event_id
    assert event.occurred_at is not None
    assert event.event_version == 1
    assert event.source == "test"
    assert event.correlation_id == "c1"
    assert event.causation_id == "cause1"
    assert event.payload["ok"] is True


@pytest.mark.parametrize("event_type", EVENT_TYPE_LIST)
@pytest.mark.parametrize("learner_id", LEARNERS)
def test_serialization_roundtrip(event_type, learner_id):
    ser = EventSerializer()
    original = IntegrationEvent.create(
        event_type,
        {"learner_id": learner_id},
        correlation_id=f"corr-{learner_id}",
        causation_id="cause",
        source="adapter",
    )
    raw = ser.to_json(original)
    restored = ser.from_json(raw)
    assert restored.event_id == original.event_id
    assert restored.event_type == original.event_type
    assert restored.payload == original.payload
    assert restored.correlation_id == original.correlation_id
    assert restored.causation_id == original.causation_id
    assert restored.event_version == original.event_version


@pytest.mark.parametrize("event_type", EVENT_TYPE_LIST)
@pytest.mark.parametrize("subject_id", SUBJECTS)
def test_to_dict_contains_required_keys(event_type, subject_id):
    ser = EventSerializer()
    event = IntegrationEvent.create(event_type, {"subject_id": subject_id})
    data = ser.to_dict(event)
    for key in (
        "event_id",
        "event_type",
        "occurred_at",
        "event_version",
        "source",
        "payload",
        "correlation_id",
        "causation_id",
    ):
        assert key in data


def test_empty_event_type_rejected():
    with pytest.raises(ValueError):
        IntegrationEvent.create("", {})


def test_invalid_version_rejected():
    with pytest.raises(ValueError):
        IntegrationEvent.create("EvidenceRecorded", {}, event_version=0)


@pytest.mark.parametrize("event_type", EVENT_TYPE_LIST)
def test_registry_knows_catalogue(event_type):
    reg = EventRegistry()
    assert reg.is_known(event_type)
    assert event_type in reg.known_types


@pytest.mark.parametrize("event_type", EVENT_TYPE_LIST)
def test_registry_publish_and_subscribe(event_type):
    reg = EventRegistry()
    seen: list[str] = []
    reg.subscribe(event_type, lambda e: seen.append(e.event_id))
    event = IntegrationEvent.create(event_type, {"x": 1})
    reg.publish(event)
    assert seen == [event.event_id]
    assert reg.published()[-1].event_id == event.event_id


@pytest.mark.parametrize("event_type", EVENT_TYPE_LIST)
def test_upcast_identity_when_already_current(event_type):
    policy = default_version_policy()
    event = IntegrationEvent.create(event_type, {"a": 1})
    assert policy.upcast(event).event_version == 1


@pytest.mark.parametrize("event_type", EVENT_TYPE_LIST)
def test_upcast_rename_key(event_type):
    policy = EventVersionPolicy()
    policy.register_current(event_type, 2)
    policy.register_upcaster(event_type, 1, identity_payload_rename("old", "new"))
    ser = EventSerializer(policy)
    stored = {
        "event_id": "e1",
        "event_type": event_type,
        "occurred_at": "2026-07-18T20:00:00+00:00",
        "event_version": 1,
        "source": "t",
        "payload": {"old": 42},
        "correlation_id": "",
        "causation_id": "",
    }
    event = ser.from_dict(stored, upcast=True)
    assert event.event_version == 2
    assert event.payload["new"] == 42
    assert "old" not in event.payload


@pytest.mark.parametrize("event_type", EVENT_TYPE_LIST)
def test_missing_upcaster_refuses_replay(event_type):
    policy = EventVersionPolicy()
    policy.register_current(event_type, 3)
    event = IntegrationEvent.create(event_type, {}, event_version=1)
    with pytest.raises(ValueError, match="missing upcaster"):
        policy.upcast(event)


@pytest.mark.parametrize("event_type", EVENT_TYPE_LIST)
def test_future_version_rejected(event_type):
    policy = default_version_policy()
    event = IntegrationEvent.create(event_type, {}, event_version=9)
    with pytest.raises(ValueError, match="newer"):
        policy.assert_compatible(event)


def test_event_types_tuple_stable():
    assert len(EVENT_TYPES) == 7
    assert EVENT_TYPES[0] == "EvidenceRecorded"


@pytest.mark.parametrize("event_type", EVENT_TYPE_LIST)
@pytest.mark.parametrize("correlation_id", ["", "c-a", "c-b"])
def test_with_correlation(event_type, correlation_id):
    event = IntegrationEvent.create(event_type, {})
    nxt = event.with_correlation(correlation_id=correlation_id, causation_id="x")
    assert nxt.correlation_id == correlation_id
    assert nxt.causation_id == "x"
    assert nxt.event_id == event.event_id


@pytest.mark.parametrize("missing", ["event_id", "payload", "event_type"])
def test_serializer_missing_keys(missing):
    ser = EventSerializer()
    data = {
        "event_id": "e",
        "event_type": "EvidenceRecorded",
        "occurred_at": "2026-07-18T20:00:00+00:00",
        "event_version": 1,
        "source": "t",
        "payload": {},
        "correlation_id": "",
        "causation_id": "",
    }
    del data[missing]
    with pytest.raises(ValueError, match="missing"):
        ser.from_dict(data)
