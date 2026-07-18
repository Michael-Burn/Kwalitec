"""MissionDispatcher delivery payload tests."""

from __future__ import annotations

from types import MappingProxyType

import pytest

from app.application.mission_engine_v2.dispatcher import MissionDispatcher
from app.application.mission_engine_v2.dto.mission_card import MissionCard
from app.application.mission_engine_v2.exceptions import DispatchError
from app.application.mission_engine_v2.lifecycle import (
    DispatchAction,
    MissionSlot,
    MissionState,
)
from app.application.mission_engine_v2.mission_factory import MissionFactory
from tests.application.mission_engine_v2.helpers import (
    NOW,
    TODAY,
    make_mission,
    make_session_plan,
    make_snapshot,
)

dispatcher = MissionDispatcher()


def test_dispatch_active_mission():
    mission = make_mission(state=MissionState.ACTIVE)
    execution = dispatcher.dispatch(mission)
    assert execution.action == DispatchAction.CONTINUE
    assert execution.mission_id == mission.mission_id
    assert execution.payload["action"] == DispatchAction.CONTINUE.value


def test_dispatch_today_ready():
    mission = make_mission(state=MissionState.READY)
    execution = dispatcher.dispatch(mission)
    assert execution.action == DispatchAction.TODAY


def test_dispatch_none_raises():
    mission = make_mission(state=MissionState.ARCHIVED)
    with pytest.raises(DispatchError, match="not dispatchable"):
        dispatcher.dispatch(mission)


def test_dispatch_future_raises():
    mission = make_mission(slot=MissionSlot.FUTURE, state=MissionState.PLANNED)
    with pytest.raises(DispatchError):
        dispatcher.dispatch(mission)


def test_dispatch_payload_frozen():
    mission = make_mission(state=MissionState.ACTIVE)
    execution = dispatcher.dispatch(mission)
    assert isinstance(execution.payload, MappingProxyType)


def test_dispatch_includes_objective_id():
    mission = make_mission(objective_id="obj-99", state=MissionState.ACTIVE)
    execution = dispatcher.dispatch(mission)
    assert execution.payload["objective_id"] == "obj-99"


def test_dispatch_resume_flag():
    mission = make_mission(state=MissionState.ACTIVE, is_resume=True)
    execution = dispatcher.dispatch(mission)
    assert execution.payload["is_resume"] == "true"


def test_dispatch_revision_flag():
    mission = make_mission(state=MissionState.PLANNED, is_revision=True, slot=MissionSlot.REVISION)  # noqa: E501
    execution = dispatcher.dispatch(mission, action=DispatchAction.REVISION)
    assert execution.payload["is_revision"] == "true"


def test_dispatch_explanation_keys():
    mission = make_mission(
        state=MissionState.ACTIVE,
        explanation_keys=("tag1", "tag2"),
    )
    execution = dispatcher.dispatch(mission)
    assert execution.payload["explanation_keys"] == "tag1,tag2"


def test_dispatch_extra_metadata():
    mission = make_mission(state=MissionState.ACTIVE)
    execution = dispatcher.dispatch(mission, extra={"source": "test"})
    assert execution.payload["source"] == "test"


def test_dispatch_card():
    factory = MissionFactory(clock=lambda: NOW, id_factory=lambda: "id1")
    snap = make_snapshot()
    plan = make_session_plan()
    mission = factory.create_from_snapshot(snap, scheduled_date=TODAY, session_plan=plan)  # noqa: E501
    card = factory.build_card(mission, runtime_phase="active")
    execution = dispatcher.dispatch_card(card)
    assert execution.mission_id == card.mission_id


def test_dispatch_card_none_raises():
    card = MissionCard(
        mission_id="m1",
        learner_id="l1",
        journey_id="j1",
        session_id="s1",
        topic_id="t1",
        scheduled_date=TODAY,
        slot=MissionSlot.FUTURE,
        state=MissionState.PLANNED,
        title="T",
        effort="medium",
        dispatch_action=DispatchAction.NONE,
        is_active=False,
        is_completed=False,
        is_resume=False,
        is_revision=False,
        objective_id=None,
        sequence_index=0,
    )
    with pytest.raises(DispatchError):
        dispatcher.dispatch_card(card)


def test_dispatch_today_convenience():
    mission = make_mission(state=MissionState.READY)
    execution = dispatcher.dispatch_today(mission)
    assert execution.action in {
        DispatchAction.TODAY,
        DispatchAction.RESUME,
        DispatchAction.CONTINUE,
    }


def test_dispatch_resume_convenience():
    mission = make_mission(state=MissionState.PAUSED)
    execution = dispatcher.dispatch_resume(mission)
    assert execution.action == DispatchAction.RESUME


def test_dispatch_continue_convenience():
    mission = make_mission(state=MissionState.ACTIVE)
    execution = dispatcher.dispatch_continue(mission)
    assert execution.action == DispatchAction.CONTINUE


def test_dispatch_forced_action():
    mission = make_mission(state=MissionState.READY)
    execution = dispatcher.dispatch(mission, action=DispatchAction.CONTINUE)
    assert execution.action == DispatchAction.CONTINUE
