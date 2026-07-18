"""Lifecycle vocabulary and LifecyclePolicy tests."""

from __future__ import annotations

import pytest

from app.application.mission_engine_v2.exceptions import InvalidMissionState
from app.application.mission_engine_v2.lifecycle import (
    LAWFUL_MISSION_TRANSITIONS,
    MissionState,
    MissionTransitionEvent,
    is_active_mission_state,
    is_open_mission_state,
    is_terminal_mission_state,
    next_mission_state,
)
from app.application.mission_engine_v2.policies.lifecycle_policy import LifecyclePolicy

LAWFUL_CASES = [
    (MissionState.PLANNED, MissionTransitionEvent.PREPARE, MissionState.READY),
    (MissionState.PLANNED, MissionTransitionEvent.ACTIVATE, MissionState.ACTIVE),
    (MissionState.READY, MissionTransitionEvent.ACTIVATE, MissionState.ACTIVE),
    (MissionState.ACTIVE, MissionTransitionEvent.PAUSE, MissionState.PAUSED),
    (MissionState.ACTIVE, MissionTransitionEvent.COMPLETE, MissionState.COMPLETED),
    (MissionState.PAUSED, MissionTransitionEvent.RESUME, MissionState.ACTIVE),
    (MissionState.PAUSED, MissionTransitionEvent.COMPLETE, MissionState.COMPLETED),
    (MissionState.COMPLETED, MissionTransitionEvent.ARCHIVE, MissionState.ARCHIVED),
]

INVALID_CASES = [
    (MissionState.READY, MissionTransitionEvent.PREPARE),
    (MissionState.ARCHIVED, MissionTransitionEvent.RESUME),
    (MissionState.PLANNED, MissionTransitionEvent.COMPLETE),
]


@pytest.mark.parametrize("current,event,expected", LAWFUL_CASES)
def test_next_mission_state_lawful(current, event, expected):
    assert next_mission_state(current, event) == expected


@pytest.mark.parametrize("current,event", INVALID_CASES)
def test_next_mission_state_invalid_returns_none(current, event):
    assert next_mission_state(current, event) is None


@pytest.mark.parametrize(
    ("state", "terminal", "open_", "active"),
    [
        (MissionState.PLANNED, False, True, False),
        (MissionState.READY, False, True, False),
        (MissionState.ACTIVE, False, True, True),
        (MissionState.PAUSED, False, True, True),
        (MissionState.COMPLETED, True, False, False),
        (MissionState.ARCHIVED, True, False, False),
    ],
)
def test_mission_state_helpers(state, terminal, open_, active):
    assert is_terminal_mission_state(state) is terminal
    assert is_open_mission_state(state) is open_
    assert is_active_mission_state(state) is active


@pytest.mark.parametrize("current,event,expected", LAWFUL_CASES)
def test_lifecycle_policy_resolve_and_can_transition(current, event, expected):
    assert LifecyclePolicy.resolve(current, event) == expected
    assert LifecyclePolicy.can_transition(current, event) is True


@pytest.mark.parametrize("current,event", INVALID_CASES[:1])
def test_lifecycle_policy_resolve_raises(current, event):
    with pytest.raises(InvalidMissionState):
        LifecyclePolicy.resolve(current, event)


def test_lifecycle_policy_can_transition_false():
    assert (
        LifecyclePolicy.can_transition(
            MissionState.ARCHIVED,
            MissionTransitionEvent.ARCHIVE,
        )
        is False
    )


@pytest.mark.parametrize("state", [MissionState.COMPLETED, MissionState.ARCHIVED])
def test_lifecycle_policy_assert_not_terminal_raises(state):
    with pytest.raises(InvalidMissionState):
        LifecyclePolicy.assert_not_terminal(state)


def test_lifecycle_policy_assert_not_terminal_ok():
    LifecyclePolicy.assert_not_terminal(MissionState.ACTIVE)


@pytest.mark.parametrize("state", [MissionState.ACTIVE, MissionState.PAUSED])
def test_lifecycle_policy_assert_completable_ok(state):
    LifecyclePolicy.assert_completable(state)


@pytest.mark.parametrize("state", [MissionState.PLANNED, MissionState.ARCHIVED])
def test_lifecycle_policy_assert_completable_raises(state):
    with pytest.raises(InvalidMissionState):
        LifecyclePolicy.assert_completable(state)


def test_lifecycle_policy_assert_archivable_ok():
    LifecyclePolicy.assert_archivable(MissionState.COMPLETED)


@pytest.mark.parametrize("state", [MissionState.ACTIVE, MissionState.PLANNED])
def test_lifecycle_policy_assert_archivable_raises(state):
    with pytest.raises(InvalidMissionState):
        LifecyclePolicy.assert_archivable(state)


def test_lawful_transitions_map_count():
    assert len(LAWFUL_MISSION_TRANSITIONS) == 8
