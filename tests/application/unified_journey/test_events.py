"""JourneyEvent contract tests (P2-MS003)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.application.unified_journey import (
    CONTRACT_VERSION,
    JourneyEvent,
    JourneyEventType,
    JourneyStage,
    event_for_completion_status,
    event_for_reflection_state,
    event_for_session_phase,
    mission_completed,
    mission_started,
    reflection_available,
    reflection_completed,
    reflection_skipped,
    reflection_started,
    session_completed,
    session_resumed,
    session_started,
    weekly_review_available,
    wrap_up_started,
)


def test_journey_events_are_immutable():
    event = mission_started()
    assert event.event_type is JourneyEventType.MISSION_STARTED
    assert event.stage is JourneyStage.DAILY_MISSION
    assert event.contract_version == CONTRACT_VERSION
    with pytest.raises(FrozenInstanceError):
        event.message = "changed"  # type: ignore[misc]


def test_factory_helpers():
    assert mission_completed().event_type is JourneyEventType.MISSION_COMPLETED
    assert (
        reflection_available().event_type
        is JourneyEventType.REFLECTION_AVAILABLE
    )
    assert reflection_available().stage is JourneyStage.SESSION_REFLECTION
    assert (
        weekly_review_available().event_type
        is JourneyEventType.WEEKLY_REVIEW_AVAILABLE
    )
    assert weekly_review_available().stage is JourneyStage.WEEKLY_REVIEW
    assert session_started().event_type is JourneyEventType.SESSION_STARTED
    assert session_started().stage is JourneyStage.STUDY_SESSION
    assert session_resumed().event_type is JourneyEventType.SESSION_RESUMED
    assert session_completed().event_type is JourneyEventType.SESSION_COMPLETED
    assert wrap_up_started().event_type is JourneyEventType.WRAP_UP_STARTED
    assert reflection_started().event_type is JourneyEventType.REFLECTION_STARTED
    assert (
        reflection_completed().event_type
        is JourneyEventType.REFLECTION_COMPLETED
    )
    assert reflection_skipped().event_type is JourneyEventType.REFLECTION_SKIPPED
    assert reflection_started().stage is JourneyStage.SESSION_REFLECTION


def test_event_for_completion_status():
    started = event_for_completion_status("in_progress")
    assert started is not None
    assert started.event_type is JourneyEventType.MISSION_STARTED

    done = event_for_completion_status("complete")
    assert done is not None
    assert done.event_type is JourneyEventType.MISSION_COMPLETED

    assert event_for_completion_status("not_started") is None
    assert event_for_completion_status("") is None


def test_event_for_session_phase():
    assert (
        event_for_session_phase("studying", previous_phase="ready").event_type
        is JourneyEventType.SESSION_STARTED
    )
    assert (
        event_for_session_phase(
            "studying", previous_phase="wrapping_up"
        ).event_type
        is JourneyEventType.SESSION_RESUMED
    )
    assert (
        event_for_session_phase("wrapping_up").event_type
        is JourneyEventType.WRAP_UP_STARTED
    )
    assert (
        event_for_session_phase("complete").event_type
        is JourneyEventType.SESSION_COMPLETED
    )
    assert event_for_session_phase("ready") is None


def test_event_for_reflection_state():
    assert (
        event_for_reflection_state(
            "in_progress", previous_state="available"
        ).event_type
        is JourneyEventType.REFLECTION_STARTED
    )
    assert (
        event_for_reflection_state("completed").event_type
        is JourneyEventType.REFLECTION_COMPLETED
    )
    assert (
        event_for_reflection_state("skipped").event_type
        is JourneyEventType.REFLECTION_SKIPPED
    )
    assert (
        event_for_reflection_state("available", previous_state="complete").event_type
        is JourneyEventType.REFLECTION_AVAILABLE
    )


def test_rejects_unknown_event_type():
    with pytest.raises(ValueError):
        JourneyEvent(event_type="invented_transition")  # type: ignore[arg-type]


def test_events_do_not_encode_educational_authority():
    """Events are Experience transitions — no engine / persistence fields."""
    event = mission_started(message="UI transition only")
    assert not hasattr(event, "recommendation_id")
    assert not hasattr(event, "mastery_delta")
    assert event.metadata == ()
    session = session_started()
    assert not hasattr(session, "evidence_id")
    assert session.contract_version.startswith("p2.ms005")
    reflection = reflection_started()
    assert not hasattr(reflection, "evidence_id")
    assert reflection.contract_version == CONTRACT_VERSION
