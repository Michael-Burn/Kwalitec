"""MissionValidator integrity tests."""

from __future__ import annotations

import pytest

from app.application.mission_engine_v2.exceptions import (
    ActiveMissionExists,
    DuplicateMission,
    InvalidJourneyReference,
    InvalidSessionReference,
    TopicUnavailable,
)
from app.application.mission_engine_v2.lifecycle import MissionState
from app.application.mission_engine_v2.validator import MissionValidator
from app.domain.learning_journey.value_objects.journey_state import JourneyState
from tests.application.mission_engine_v2.helpers import (
    TODAY,
    FakeNavigation,
    make_mission,
    make_session,
    make_snapshot,
)


def _validator(**kwargs) -> MissionValidator:
    return MissionValidator(**kwargs)


def test_validate_no_duplicate_ok():
    existing = [make_mission(mission_id="m1")]
    candidate = make_mission(mission_id="m2", session_id="sess-2")
    _validator().validate_no_duplicate(existing, candidate)


def test_validate_no_duplicate_raises():
    existing = [make_mission()]
    candidate = make_mission(mission_id="m2")
    with pytest.raises(DuplicateMission):
        _validator().validate_no_duplicate(existing, candidate)


def test_validate_no_duplicate_ignores_completed():
    existing = [
        make_mission(state=MissionState.COMPLETED),
    ]
    candidate = make_mission(mission_id="m2")
    _validator().validate_no_duplicate(existing, candidate)


def test_validate_one_active_ok():
    missions = [make_mission(state=MissionState.READY)]
    _validator().validate_one_active(missions)


def test_validate_one_active_raises():
    missions = [make_mission(state=MissionState.ACTIVE)]
    with pytest.raises(ActiveMissionExists):
        _validator().validate_one_active(missions)


def test_validate_one_active_excluding_self():
    missions = [make_mission(mission_id="m1", state=MissionState.ACTIVE)]
    _validator().validate_one_active(missions, activating_mission_id="m1")


def test_validate_session_reference_empty_raises():
    mission = make_mission(session_id="  ")
    with pytest.raises(InvalidSessionReference, match="session_id"):
        _validator().validate_session_reference(mission)


def test_validate_session_reference_journey_mismatch():
    snap = make_snapshot(journey_id="journey-a")
    mission = make_mission(journey_id="journey-b")
    with pytest.raises(InvalidSessionReference, match="does not match"):
        _validator().validate_session_reference(mission, snap)


def test_validate_session_reference_unknown_session():
    snap = make_snapshot(sessions=(make_session(sid="sess-known"),))
    mission = make_mission(session_id="unknown-id")
    with pytest.raises(InvalidSessionReference, match="not found"):
        _validator().validate_session_reference(mission, snap)


def test_validate_session_reference_planned_session_prefix_ok():
    snap = make_snapshot(sessions=(make_session(sid="sess-1"),))
    mission = make_mission(session_id="sess-new")
    _validator().validate_session_reference(mission, snap)


def test_validate_journey_state_valid():
    snap = make_snapshot(state=JourneyState.ACTIVE)
    _validator().validate_journey_state(snap)


@pytest.mark.parametrize(
    "state",
    [
        JourneyState.COMPLETED,
        JourneyState.ABANDONED,
        JourneyState.ARCHIVED,
    ],
)
def test_validate_journey_state_invalid(state):
    snap = make_snapshot(state=state)
    with pytest.raises(InvalidJourneyReference):
        _validator().validate_journey_state(snap)


def test_validate_journey_state_deferred_not_allowed():
    snap = make_snapshot(state=JourneyState.DEFERRED)
    with pytest.raises(InvalidJourneyReference, match="deferred"):
        _validator().validate_journey_state(snap, allow_deferred=False)


def test_validate_topic_available_ok():
    _validator(navigation=FakeNavigation()).validate_topic_available("topic-a")


def test_validate_topic_unavailable():
    nav = FakeNavigation(topics=("topic-a",))
    with pytest.raises(TopicUnavailable):
        _validator(navigation=nav).validate_topic_available("topic-z")


def test_validate_topic_skipped_without_navigation():
    _validator(navigation=None).validate_topic_available("anything")


def test_validate_mission_identity_ok():
    _validator().validate_mission_identity(make_mission())


@pytest.mark.parametrize(
    ("field", "value", "exc"),
    [
        ("mission_id", "", InvalidSessionReference),
        ("learner_id", "", InvalidJourneyReference),
    ],
)
def test_validate_mission_identity_missing(field, value, exc):
    mission = make_mission(**{field: value})
    with pytest.raises(exc):
        _validator().validate_mission_identity(mission)


def test_validate_new_mission_full_gate():
    snap = make_snapshot()
    candidate = make_mission(mission_id="new", session_id="sess-1")
    _validator(navigation=FakeNavigation()).validate_new_mission([], candidate, snap)


def test_validate_new_mission_active_checks_capacity():
    existing = [make_mission(mission_id="active", state=MissionState.ACTIVE)]
    candidate = make_mission(
        mission_id="new",
        session_id="sess-2",
        state=MissionState.ACTIVE,
    )
    with pytest.raises(ActiveMissionExists):
        _validator().validate_new_mission(existing, candidate)


def test_valid_journey_states_in_set():
    from app.domain.learning_journey.value_objects.journey_state import JourneyState

    for state in (
        JourneyState.NOT_STARTED,
        JourneyState.ACTIVE,
        JourneyState.PAUSED,
        JourneyState.RESUMED,
        JourneyState.READY_FOR_COMPLETION,
        JourneyState.DEFERRED,
    ):
        assert state in MissionValidator.VALID_JOURNEY_STATES


def test_duplicate_same_date_different_session_ok():
    existing = [make_mission(session_id="sess-1")]
    candidate = make_mission(mission_id="m2", session_id="sess-2", scheduled_date=TODAY)
    _validator().validate_no_duplicate(existing, candidate)
