"""Unit tests — Phase E Journey progression events."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.infrastructure.analytics.dispatcher import (
    AnalyticsEventDispatcher,
    DispatchStatus,
)
from app.infrastructure.analytics.feature_flag import AnalyticsFeatureFlag
from app.infrastructure.analytics.journey_events import (
    JOURNEY_PROGRESSED,
    build_journey_progressed_event,
    emit_journey_progressed,
)
from app.infrastructure.analytics.outbox import MemoryOutboxSink
from app.infrastructure.analytics.registry import AnalyticsEventRegistry
from app.infrastructure.analytics.serialization import AnalyticsEventSerializer
from app.infrastructure.analytics.validator import AnalyticsEventValidator


def test_build_journey_progressed_metadata_only() -> None:
    event = build_journey_progressed_event(
        user_id=42,
        journey_id="journey-1",
        curriculum_node_id="topic-a",
        transition_id="start_journey",
        correlation_id="corr-j",
        occurred_at=datetime(2026, 7, 24, 11, 0, tzinfo=UTC),
    )
    assert event.event_type == JOURNEY_PROGRESSED
    assert event.user_id == 42
    assert event.payload == {
        "journey_id": "journey-1",
        "curriculum_node_id": "topic-a",
        "transition_id": "start_journey",
    }
    assert event.correlation_id == "corr-j"
    assert int(event.schema_version) == 1
    assert "progress" not in event.payload
    assert "recommendation" not in event.payload
    assert "objectives" not in event.payload
    assert "EducationalState" not in event.payload


def test_invalid_transition_id_rejected() -> None:
    with pytest.raises(ValueError, match="transition_id"):
        build_journey_progressed_event(
            user_id=1,
            journey_id="journey-1",
            curriculum_node_id="topic-a",
            transition_id="invented_transition",
        )


def test_serialize_journey_progressed_roundtrip() -> None:
    event = build_journey_progressed_event(
        user_id=7,
        journey_id="j-7",
        curriculum_node_id="node-7",
        transition_id="confirm_topic_complete",
    )
    serializer = AnalyticsEventSerializer()
    restored = serializer.from_json(serializer.to_json(event))
    assert restored.event_type == JOURNEY_PROGRESSED
    assert restored.payload["transition_id"] == "confirm_topic_complete"


def test_validator_accepts_registered_journey_progressed() -> None:
    registry = AnalyticsEventRegistry.phase_e_default()
    validator = AnalyticsEventValidator(registry)
    event = build_journey_progressed_event(
        user_id=1,
        journey_id="j-1",
        curriculum_node_id="t-1",
        transition_id="pause_journey",
    )
    assert validator.validate(event).ok


def test_emit_flag_off_is_disabled() -> None:
    result = emit_journey_progressed(
        user_id=1,
        journey_id="j-1",
        curriculum_node_id="t-1",
        transition_id="start_journey",
        dispatcher=AnalyticsEventDispatcher(
            feature_flag=AnalyticsFeatureFlag(events_v1=False),
            outbox=MemoryOutboxSink(),
            registry=AnalyticsEventRegistry.phase_e_default(),
        ),
    )
    assert result.status is DispatchStatus.DISABLED


def test_emit_flag_on_enqueues() -> None:
    outbox = MemoryOutboxSink()
    result = emit_journey_progressed(
        user_id=1,
        journey_id="j-1",
        curriculum_node_id="t-1",
        transition_id="start_journey",
        dispatcher=AnalyticsEventDispatcher(
            feature_flag=AnalyticsFeatureFlag(events_v1=True),
            outbox=outbox,
            registry=AnalyticsEventRegistry.phase_e_default(),
        ),
    )
    assert result.status is DispatchStatus.ENQUEUED
    assert len(outbox.pending()) == 1
    assert outbox.pending()[0].event_type == JOURNEY_PROGRESSED
