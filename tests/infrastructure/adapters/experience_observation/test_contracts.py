"""Contract tests — Experience Observation Bridge (P2-MS006)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.infrastructure.adapters.experience_observation import (
    AUTHORITY_EXPERIENCE_OBSERVATION,
    CONTRACT_VERSION,
    OBSERVABLE_EXPERIENCE_EVENTS,
    ExperienceObservation,
    ObservationPublishResult,
    deterministic_observation_id,
)


def test_experience_observation_is_frozen():
    obs = ExperienceObservation(
        observation_id="expobs-1",
        timestamp="2026-07-25T10:00:00+00:00",
        journey_stage="study_session",
        experience_event="session_started",
        student_id="42",
    )
    with pytest.raises(FrozenInstanceError):
        obs.experience_event = "mutated"  # type: ignore[misc]


def test_experience_observation_freezes_nested_mappings():
    state = {"phase": "studying", "nested": {"a": 1}}
    obs = ExperienceObservation(
        observation_id="expobs-2",
        timestamp="2026-07-25T10:00:00+00:00",
        journey_stage="study_session",
        experience_event="session_started",
        presentation_state=state,
        student_id="7",
    )
    state["phase"] = "mutated"
    state["nested"]["a"] = 99
    assert obs.presentation_state["phase"] == "studying"
    assert obs.presentation_state["nested"]["a"] == 1


def test_experience_observation_rejects_missing_required_fields():
    with pytest.raises(ValueError, match="observation_id"):
        ExperienceObservation(
            observation_id="",
            timestamp="2026-07-25T10:00:00+00:00",
            journey_stage="study_session",
            experience_event="session_started",
        )
    with pytest.raises(ValueError, match="timestamp"):
        ExperienceObservation(
            observation_id="expobs-3",
            timestamp="",
            journey_stage="study_session",
            experience_event="session_started",
        )
    with pytest.raises(ValueError, match="experience_event"):
        ExperienceObservation(
            observation_id="expobs-4",
            timestamp="2026-07-25T10:00:00+00:00",
            journey_stage="study_session",
            experience_event="",
        )


def test_experience_observation_serialize_is_deterministic():
    obs = ExperienceObservation(
        observation_id="expobs-5",
        timestamp="2026-07-25T10:00:00+00:00",
        journey_stage="daily_mission",
        experience_event="mission_started",
        presentation_state={"message": "Mission started"},
        metadata=(("via", "test"),),
        correlation_id="corr-1",
        student_id="9",
    )
    assert obs.serialize() == obs.serialize()
    assert obs.authority == AUTHORITY_EXPERIENCE_OBSERVATION
    assert obs.contract_version == CONTRACT_VERSION
    assert "mission_started" in obs.serialize()


def test_deterministic_observation_id_stable():
    kwargs = dict(
        student_id="42",
        timestamp="2026-07-25T10:00:00+00:00",
        journey_stage="study_session",
        experience_event="session_completed",
        presentation_state={"completion_status": "complete"},
        metadata=(("via", "observation_assembler"),),
        correlation_id="abc",
    )
    assert deterministic_observation_id(**kwargs) == deterministic_observation_id(
        **kwargs
    )
    assert deterministic_observation_id(**kwargs).startswith("expobs-")


def test_observable_experience_events_cover_directive_set():
    expected = {
        "mission_started",
        "session_started",
        "session_completed",
        "reflection_started",
        "reflection_completed",
        "reflection_skipped",
    }
    assert expected <= set(OBSERVABLE_EXPERIENCE_EVENTS)


def test_publish_result_validates_status():
    with pytest.raises(ValueError, match="unknown publish status"):
        ObservationPublishResult(ok=False, status="mystery")
