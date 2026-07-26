"""Unit tests — Mission Start Adapter mapping, errors, DTOs."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.infrastructure.adapters.educational_runtime_bridge import (
    AUTHORITY_STUDY_SESSION_SERVICE,
    FORBIDDEN,
    INVALID_STATE,
    MISSION_START_BRIDGE_FAILURE,
    MISSION_START_BRIDGE_LATENCY,
    MISSION_START_BRIDGE_REQUESTED,
    MISSION_START_BRIDGE_SUCCESS,
    NO_ACTIVE_PLAN,
    NOT_FOUND,
    OUTSIDE_PLAN_WINDOW,
    UNAVAILABLE,
    BridgeResult,
    MissionStartAdapter,
    map_mission_to_start_result,
)
from app.infrastructure.events.registry import EventRegistry


def test_map_mission_to_start_result_dto():
    mission = SimpleNamespace(id=42, title="Study Probability", user_id=1)
    started = map_mission_to_start_result(
        mission,
        student_id="1",
        estimated_minutes=45,
        started_at="2026-07-25T10:00:00Z",
    )
    assert started["mission_id"] == "42"
    assert started["session_id"] == "42"
    assert started["experience_session_id"] == "es-42"
    assert started["topic_title"] == "Study Probability"
    assert started["status"] == "in_progress"
    assert started["estimated_minutes"] == 45
    assert started["started_at"] == "2026-07-25T10:00:00Z"
    assert started["authority"] == AUTHORITY_STUDY_SESSION_SERVICE
    assert started["next_action_authority"] is False


def test_adapter_forbidden_for_non_numeric_student_id():
    events = EventRegistry()
    adapter = MissionStartAdapter(events=events)
    result = adapter.start_session("not-a-user")
    assert isinstance(result, BridgeResult)
    assert result.ok is False
    assert result.error_code == FORBIDDEN
    assert result.value is None
    types = [e.event_type for e in events.published()]
    assert MISSION_START_BRIDGE_REQUESTED in types
    assert MISSION_START_BRIDGE_FAILURE in types
    assert MISSION_START_BRIDGE_LATENCY in types


def test_adapter_no_active_plan_contract():
    events = EventRegistry()

    class _Planning:
        @staticmethod
        def generate_today_mission(user_id, today=None):
            return None

    class _PlanSvc:
        @staticmethod
        def get_user_active_plan(user_id):
            return None

        @staticmethod
        def get_current_week_plan(plan):
            return None

    adapter = MissionStartAdapter(
        events=events,
        planning_service=_Planning,
        study_plan_service=_PlanSvc,
    )
    result = adapter.start_session("9")
    assert result.ok is True
    assert result.value is None
    assert result.error_code == NO_ACTIVE_PLAN
    assert result.fallback_used is False
    types = [e.event_type for e in events.published()]
    assert MISSION_START_BRIDGE_SUCCESS in types
    assert MISSION_START_BRIDGE_FAILURE not in types


def test_adapter_outside_window_contract():
    class _Planning:
        @staticmethod
        def generate_today_mission(user_id, today=None):
            return None

    class _PlanSvc:
        @staticmethod
        def get_user_active_plan(user_id):
            return SimpleNamespace(id=1)

        @staticmethod
        def get_current_week_plan(plan):
            return None

    adapter = MissionStartAdapter(
        planning_service=_Planning,
        study_plan_service=_PlanSvc,
    )
    result = adapter.start_session("3")
    assert result.ok is True
    assert result.value is None
    assert result.error_code == OUTSIDE_PLAN_WINDOW


def test_adapter_starts_via_study_session_service():
    events = EventRegistry()
    pending = SimpleNamespace(
        id=99, user_id=5, title="Practice Distributions", status="Pending"
    )
    started = SimpleNamespace(
        id=99, user_id=5, title="Practice Distributions", status="In Progress"
    )

    class _Planning:
        @staticmethod
        def generate_today_mission(user_id, today=None):
            assert user_id == 5
            return pending

    class _Session:
        @staticmethod
        def start_session(mission_id, user_id):
            assert mission_id == 99
            assert user_id == 5
            return started

        @staticmethod
        def get_owned_mission(mission_id, user_id):
            return pending

    class _PlanSvc:
        @staticmethod
        def get_user_active_plan(user_id):
            return SimpleNamespace(id=1, preferred_session_minutes=30)

        @staticmethod
        def get_current_week_plan(plan):
            return SimpleNamespace(id=1)

    adapter = MissionStartAdapter(
        events=events,
        planning_service=_Planning,
        study_session_service=_Session,
        study_plan_service=_PlanSvc,
    )
    result = adapter.start_session("5")
    assert result.ok is True
    assert result.value is not None
    assert result.value["mission_id"] == "99"
    assert result.value["status"] == "in_progress"
    assert result.value["authority"] == AUTHORITY_STUDY_SESSION_SERVICE
    assert result.value["estimated_minutes"] == 30
    types = [e.event_type for e in events.published()]
    assert MISSION_START_BRIDGE_REQUESTED in types
    assert MISSION_START_BRIDGE_SUCCESS in types
    assert MISSION_START_BRIDGE_LATENCY in types


def test_adapter_invalid_state_when_completed():
    events = EventRegistry()
    completed = SimpleNamespace(
        id=7, user_id=1, title="Done", status="Completed"
    )

    class _Planning:
        @staticmethod
        def generate_today_mission(user_id, today=None):
            return completed

    class _Session:
        @staticmethod
        def start_session(mission_id, user_id):
            raise ValueError("This study session has already been recorded.")

    class _PlanSvc:
        @staticmethod
        def get_user_active_plan(user_id):
            return SimpleNamespace(id=1, preferred_session_minutes=60)

        @staticmethod
        def get_current_week_plan(plan):
            return SimpleNamespace(id=1)

    adapter = MissionStartAdapter(
        events=events,
        planning_service=_Planning,
        study_session_service=_Session,
        study_plan_service=_PlanSvc,
    )
    result = adapter.start_session("1")
    assert result.ok is False
    assert result.error_code == INVALID_STATE
    assert MISSION_START_BRIDGE_FAILURE in [
        e.event_type for e in events.published()
    ]


def test_adapter_uses_explicit_mission_id_without_generate():
    mission = SimpleNamespace(
        id=12, user_id=2, title="Topic", status="Pending"
    )
    started = SimpleNamespace(
        id=12, user_id=2, title="Topic", status="In Progress"
    )
    generated = {"called": False}

    class _Planning:
        @staticmethod
        def generate_today_mission(user_id, today=None):
            generated["called"] = True
            return None

    class _Session:
        @staticmethod
        def get_owned_mission(mission_id, user_id):
            assert mission_id == 12
            return mission

        @staticmethod
        def start_session(mission_id, user_id):
            return started

    class _PlanSvc:
        @staticmethod
        def get_user_active_plan(user_id):
            return SimpleNamespace(id=1, preferred_session_minutes=20)

        @staticmethod
        def get_current_week_plan(plan):
            return SimpleNamespace(id=1)

    adapter = MissionStartAdapter(
        planning_service=_Planning,
        study_session_service=_Session,
        study_plan_service=_PlanSvc,
    )
    result = adapter.start_session("2", mission_id="12")
    assert result.ok is True
    assert result.value["mission_id"] == "12"
    assert generated["called"] is False


def test_adapter_unavailable_on_service_exception():
    events = EventRegistry()

    class _Planning:
        @staticmethod
        def generate_today_mission(user_id, today=None):
            raise RuntimeError("db down")

    adapter = MissionStartAdapter(events=events, planning_service=_Planning)
    result = adapter.start_session("1")
    assert result.ok is False
    assert result.error_code == UNAVAILABLE
    assert result.fallback_used is False
    assert MISSION_START_BRIDGE_FAILURE in [
        e.event_type for e in events.published()
    ]


def test_adapter_forbidden_foreign_mission_id():
    class _Planning:
        @staticmethod
        def generate_today_mission(user_id, today=None):
            raise AssertionError("must not generate when mission_id given")

    class _Session:
        @staticmethod
        def get_owned_mission(mission_id, user_id):
            raise ValueError(f"Mission {mission_id} does not belong to user {user_id}")

    adapter = MissionStartAdapter(
        planning_service=_Planning,
        study_session_service=_Session,
    )
    result = adapter.start_session("1", mission_id="99")
    assert result.ok is False
    assert result.error_code == FORBIDDEN


@pytest.mark.parametrize(
    "code",
    [
        UNAVAILABLE,
        NO_ACTIVE_PLAN,
        OUTSIDE_PLAN_WINDOW,
        NOT_FOUND,
        FORBIDDEN,
        INVALID_STATE,
    ],
)
def test_error_codes_stable(code):
    assert isinstance(code, str)
    assert code
