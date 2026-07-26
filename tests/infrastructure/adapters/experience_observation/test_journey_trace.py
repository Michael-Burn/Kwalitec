"""JourneyTrace lifecycle tests — Experience Observability (P2-MS007)."""

from __future__ import annotations

import pytest

from app.infrastructure.adapters.experience_observation import (
    OBSERVATION_STATUS_PENDING,
    OBSERVATION_STATUS_PUBLISHED,
    PIPELINE_STAGE_EVIDENCE_ACK,
    PIPELINE_STAGE_JOURNEY_EVENT,
    JourneyTrace,
    build_journey_trace,
    build_journey_trace_store,
    deterministic_trace_id,
)


def test_journey_trace_is_frozen():
    trace = build_journey_trace(
        correlation_id="corr-1",
        journey_stage="daily_mission",
        experience_event="mission_started",
        observation_status=OBSERVATION_STATUS_PENDING,
        timestamp="2026-07-25T10:00:00+00:00",
        pipeline_stage=PIPELINE_STAGE_JOURNEY_EVENT,
    )
    with pytest.raises(Exception):
        trace.correlation_id = "mutated"  # type: ignore[misc]


def test_journey_trace_rejects_unknown_status_or_stage():
    with pytest.raises(ValueError, match="observation_status"):
        JourneyTrace(
            trace_id="jtrace-x",
            correlation_id="c",
            journey_stage="daily_mission",
            experience_event="mission_started",
            observation_status="invented",
            timestamp="2026-07-25T10:00:00+00:00",
            pipeline_stage=PIPELINE_STAGE_JOURNEY_EVENT,
        )
    with pytest.raises(ValueError, match="pipeline_stage"):
        JourneyTrace(
            trace_id="jtrace-y",
            correlation_id="c",
            journey_stage="daily_mission",
            experience_event="mission_started",
            observation_status=OBSERVATION_STATUS_PENDING,
            timestamp="2026-07-25T10:00:00+00:00",
            pipeline_stage="invented",
        )


def test_deterministic_trace_id_is_stable():
    a = deterministic_trace_id(
        correlation_id="corr",
        journey_stage="study_session",
        experience_event="session_started",
        pipeline_stage=PIPELINE_STAGE_JOURNEY_EVENT,
        timestamp="2026-07-25T10:00:00+00:00",
        observation_id="expobs-1",
    )
    b = deterministic_trace_id(
        correlation_id="corr",
        journey_stage="study_session",
        experience_event="session_started",
        pipeline_stage=PIPELINE_STAGE_JOURNEY_EVENT,
        timestamp="2026-07-25T10:00:00+00:00",
        observation_id="expobs-1",
    )
    assert a == b
    assert a.startswith("jtrace-")


def test_journey_trace_canonical_dict_excludes_student_fields():
    trace = build_journey_trace(
        correlation_id="corr-2",
        journey_stage="study_session",
        experience_event="session_completed",
        observation_status=OBSERVATION_STATUS_PUBLISHED,
        timestamp="2026-07-25T11:00:00+00:00",
        pipeline_stage=PIPELINE_STAGE_EVIDENCE_ACK,
        observation_id="expobs-abc",
        evidence_id="ev-1",
        latency_ms=12.5,
    )
    payload = trace.to_canonical_dict()
    assert "student_id" not in payload
    assert "email" not in payload
    assert payload["correlation_id"] == "corr-2"
    assert payload["evidence_id"] == "ev-1"
    assert payload["latency_ms"] == 12.5


def test_trace_store_ring_and_correlation_lookup():
    store = build_journey_trace_store(capacity=3)
    for i in range(4):
        store.append(
            build_journey_trace(
                correlation_id="shared" if i % 2 == 0 else f"other-{i}",
                journey_stage="daily_mission",
                experience_event="mission_started",
                observation_status=OBSERVATION_STATUS_PENDING,
                timestamp=f"2026-07-25T10:0{i}:00+00:00",
                pipeline_stage=PIPELINE_STAGE_JOURNEY_EVENT,
                observation_id=f"obs-{i}",
            )
        )
    assert len(store) == 3
    shared = store.by_correlation_id("shared")
    assert len(shared) >= 1
    assert all(t.correlation_id == "shared" for t in shared)
    recent = store.recent(limit=2)
    assert len(recent) == 2
