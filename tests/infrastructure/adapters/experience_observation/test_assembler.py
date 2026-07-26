"""Assembler tests — Experience Observation Bridge (P2-MS006)."""

from __future__ import annotations

from app.application.unified_journey import (
    ReflectionExperience,
    SessionOutcome,
    mission_started,
    reflection_completed,
    session_completed,
    session_started,
)
from app.application.unified_journey.reflection_states import ReflectionState
from app.infrastructure.adapters.experience_observation import (
    OBSERVABLE_EXPERIENCE_EVENTS,
    ObservationAssembler,
    build_observation_assembler,
)


def test_build_observation_assembler_respects_enabled_flag():
    assert build_observation_assembler(enabled=False) is None
    assert isinstance(build_observation_assembler(enabled=True), ObservationAssembler)


def test_assemble_from_journey_event_mission_started():
    assembler = ObservationAssembler()
    event = mission_started()
    obs = assembler.assemble_from_journey_event(
        event,
        student_id="42",
        timestamp="2026-07-25T10:00:00+00:00",
        correlation_id="corr-mission",
    )
    assert obs.experience_event == "mission_started"
    assert obs.journey_stage == "daily_mission"
    assert obs.student_id == "42"
    assert obs.correlation_id == "corr-mission"
    assert obs.presentation_state["experience_event"] == "mission_started"
    assert ("via", "observation_assembler") in obs.metadata
    assert ("source", "journey_event") in obs.metadata
    assert obs.observation_id.startswith("expobs-")


def test_assemble_from_journey_event_session_lifecycle():
    assembler = ObservationAssembler()
    started = assembler.assemble_from_journey_event(
        session_started(),
        student_id="7",
        timestamp="2026-07-25T11:00:00+00:00",
    )
    completed = assembler.assemble_from_journey_event(
        session_completed(),
        student_id="7",
        timestamp="2026-07-25T11:30:00+00:00",
    )
    assert started.experience_event == "session_started"
    assert completed.experience_event == "session_completed"
    assert started.journey_stage == "study_session"
    assert completed.observation_id != started.observation_id


def test_assemble_from_session_outcome_is_factual_only():
    assembler = ObservationAssembler()
    outcome = SessionOutcome(
        mission_title="Fractions",
        completion_status="complete",
        reflection_available=True,
        summary_message="Session complete",
        next_transition="reflection",
        upcoming_action="reflect",
        metadata=(("phase", "complete"),),
    )
    obs = assembler.assemble_from_session_outcome(
        outcome,
        student_id="3",
        timestamp="2026-07-25T12:00:00+00:00",
        experience_event="session_completed",
    )
    assert obs.experience_event == "session_completed"
    assert obs.presentation_state["mission_title"] == "Fractions"
    assert obs.presentation_state["completion_status"] == "complete"
    assert obs.presentation_state["reflection_available"] is True
    # No educational conclusion fields introduced by the assembler.
    assert "mastery" not in obs.presentation_state
    assert "score" not in obs.presentation_state
    assert "recommendation" not in obs.presentation_state
    assert ("source", "session_outcome") in obs.metadata


def test_assemble_from_reflection_maps_state_factually():
    assembler = ObservationAssembler()
    reflection = ReflectionExperience(
        session_outcome=SessionOutcome(
            mission_title="Algebra",
            completion_status="complete",
            reflection_available=True,
        ),
        reflection_state=ReflectionState.COMPLETED,
        headline="Brief reflection",
        supporting_message="Nice work",
        next_transition="home",
        skip_available=False,
    )
    for event_name in (
        "reflection_started",
        "reflection_completed",
        "reflection_skipped",
    ):
        obs = assembler.assemble_from_reflection(
            reflection,
            student_id="11",
            timestamp="2026-07-25T13:00:00+00:00",
            experience_event=event_name,
        )
        assert obs.experience_event == event_name
        assert obs.journey_stage == "session_reflection"
        assert obs.presentation_state["reflection_state"] == "completed"
        assert ("source", "reflection_experience") in obs.metadata


def test_assemble_from_reflection_completed_event_factory():
    assembler = ObservationAssembler()
    event = reflection_completed()
    obs = assembler.assemble_from_journey_event(
        event,
        student_id="11",
        timestamp="2026-07-25T13:05:00+00:00",
    )
    assert obs.experience_event == "reflection_completed"
    assert obs.experience_event in OBSERVABLE_EXPERIENCE_EVENTS


def test_is_observable_event_filters_directive_set():
    assembler = ObservationAssembler()
    assert assembler.is_observable_event("mission_started")
    assert assembler.is_observable_event("session_started")
    assert assembler.is_observable_event("reflection_skipped")
    assert not assembler.is_observable_event("weekly_review_available")
    assert not assembler.is_observable_event("wrap_up_started")


def test_identical_inputs_yield_identical_observation_ids():
    assembler = ObservationAssembler()
    event = session_started()
    kwargs = dict(
        student_id="42",
        timestamp="2026-07-25T10:00:00+00:00",
        correlation_id="same",
    )
    a = assembler.assemble_from_journey_event(event, **kwargs)
    b = assembler.assemble_from_journey_event(event, **kwargs)
    assert a.observation_id == b.observation_id
    assert a.serialize() == b.serialize()
