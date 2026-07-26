"""Unit tests — Mission Resume Adapter mapping, errors, DTOs."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.infrastructure.adapters.educational_runtime_bridge import (
    AUTHORITY_STUDY_SESSION_SERVICE,
    FORBIDDEN,
    INVALID_STATE,
    MISSION_RESUME_BRIDGE_FAILURE,
    MISSION_RESUME_BRIDGE_LATENCY,
    MISSION_RESUME_BRIDGE_REQUESTED,
    MISSION_RESUME_BRIDGE_SUCCESS,
    NO_ACTIVE_PLAN,
    NOT_FOUND,
    OUTSIDE_PLAN_WINDOW,
    UNAVAILABLE,
    BridgeResult,
    MissionResumeAdapter,
    map_mission_to_resume_result,
)
from app.infrastructure.events.registry import EventRegistry


def test_map_mission_to_resume_result_dto():
    task = SimpleNamespace(
        id=3, title="Practice", description=None, order=0, completed=True
    )
    mission = SimpleNamespace(
        id=42, title="Study Probability", status="In Progress", tasks=[task]
    )
    resumed = map_mission_to_resume_result(
        mission,
        student_id="1",
        estimated_minutes=45,
    )
    assert resumed["mission_id"] == "42"
    assert resumed["session_id"] == "42"
    assert resumed["experience_session_id"] == "es-42"
    assert resumed["topic_title"] == "Study Probability"
    assert resumed["status"] == "in_progress"
    assert resumed["estimated_minutes"] == 45
    assert resumed["authority"] == AUTHORITY_STUDY_SESSION_SERVICE
    assert resumed["next_action_authority"] is False
    assert resumed["resumed"] is True
    assert resumed["tasks"][0]["completed"] is True
    assert resumed["tasks"][0]["id"] == "3"


def test_adapter_forbidden_for_non_numeric_student_id():
    events = EventRegistry()
    adapter = MissionResumeAdapter(events=events)
    result = adapter.resume_session("not-a-user")
    assert isinstance(result, BridgeResult)
    assert result.ok is False
    assert result.error_code == FORBIDDEN
    assert result.value is None
    types = [e.event_type for e in events.published()]
    assert MISSION_RESUME_BRIDGE_REQUESTED in types
    assert MISSION_RESUME_BRIDGE_FAILURE in types
    assert MISSION_RESUME_BRIDGE_LATENCY in types


def test_adapter_no_active_plan_contract():
    events = EventRegistry()

    class _MissionSvc:
        @staticmethod
        def get_today_mission(user_id, mission_date=None):
            return None

    class _PlanSvc:
        @staticmethod
        def get_user_active_plan(user_id):
            return None

        @staticmethod
        def get_current_week_plan(plan):
            return None

    adapter = MissionResumeAdapter(
        events=events,
        mission_service=_MissionSvc,
        study_plan_service=_PlanSvc,
    )
    result = adapter.resume_session("9")
    assert result.ok is True
    assert result.value is None
    assert result.error_code == NO_ACTIVE_PLAN
    assert result.fallback_used is False
    types = [e.event_type for e in events.published()]
    assert MISSION_RESUME_BRIDGE_SUCCESS in types
    assert MISSION_RESUME_BRIDGE_FAILURE not in types


def test_adapter_outside_window_contract():
    class _MissionSvc:
        @staticmethod
        def get_today_mission(user_id, mission_date=None):
            return None

    class _PlanSvc:
        @staticmethod
        def get_user_active_plan(user_id):
            return SimpleNamespace(id=1)

        @staticmethod
        def get_current_week_plan(plan):
            return None

    adapter = MissionResumeAdapter(
        mission_service=_MissionSvc,
        study_plan_service=_PlanSvc,
    )
    result = adapter.resume_session("3")
    assert result.ok is True
    assert result.value is None
    assert result.error_code == OUTSIDE_PLAN_WINDOW


def test_adapter_resumes_in_progress_via_study_session_service():
    events = EventRegistry()
    active = SimpleNamespace(
        id=99,
        user_id=5,
        title="Practice Distributions",
        status="In Progress",
        tasks=[],
    )

    class _MissionSvc:
        @staticmethod
        def get_today_mission(user_id, mission_date=None):
            assert user_id == 5
            return active

    class _Session:
        @staticmethod
        def get_owned_mission(mission_id, user_id):
            raise AssertionError("locate-today path must not load by id")

        @staticmethod
        def start_session(mission_id, user_id):
            raise AssertionError("resume must never start a session")

    class _PlanSvc:
        @staticmethod
        def get_user_active_plan(user_id):
            return SimpleNamespace(id=1, preferred_session_minutes=30)

        @staticmethod
        def get_current_week_plan(plan):
            return SimpleNamespace(id=1)

    adapter = MissionResumeAdapter(
        events=events,
        mission_service=_MissionSvc,
        study_session_service=_Session,
        study_plan_service=_PlanSvc,
    )
    result = adapter.resume_session("5")
    assert result.ok is True
    assert result.value is not None
    assert result.value["mission_id"] == "99"
    assert result.value["session_id"] == "99"
    assert result.value["status"] == "in_progress"
    assert result.value["authority"] == AUTHORITY_STUDY_SESSION_SERVICE
    assert result.value["estimated_minutes"] == 30
    assert result.value["resumed"] is True
    types = [e.event_type for e in events.published()]
    assert MISSION_RESUME_BRIDGE_REQUESTED in types
    assert MISSION_RESUME_BRIDGE_SUCCESS in types
    assert MISSION_RESUME_BRIDGE_LATENCY in types


def test_adapter_invalid_state_when_pending():
    events = EventRegistry()
    pending = SimpleNamespace(
        id=7, user_id=1, title="Not started", status="Pending", tasks=[]
    )

    class _MissionSvc:
        @staticmethod
        def get_today_mission(user_id, mission_date=None):
            return pending

    class _PlanSvc:
        @staticmethod
        def get_user_active_plan(user_id):
            return SimpleNamespace(id=1, preferred_session_minutes=60)

        @staticmethod
        def get_current_week_plan(plan):
            return SimpleNamespace(id=1)

    adapter = MissionResumeAdapter(
        events=events,
        mission_service=_MissionSvc,
        study_plan_service=_PlanSvc,
    )
    result = adapter.resume_session("1")
    assert result.ok is False
    assert result.error_code == INVALID_STATE
    assert MISSION_RESUME_BRIDGE_FAILURE in [
        e.event_type for e in events.published()
    ]


def test_adapter_invalid_state_when_completed():
    events = EventRegistry()
    completed = SimpleNamespace(
        id=8, user_id=1, title="Done", status="Completed", tasks=[]
    )

    class _Session:
        @staticmethod
        def get_owned_mission(mission_id, user_id):
            return completed

        @staticmethod
        def start_session(mission_id, user_id):
            raise AssertionError("resume must never start")

    adapter = MissionResumeAdapter(
        events=events,
        study_session_service=_Session,
    )
    result = adapter.resume_session("1", session_id="8")
    assert result.ok is False
    assert result.error_code == INVALID_STATE


def test_adapter_uses_explicit_session_id_without_today_lookup():
    mission = SimpleNamespace(
        id=12, user_id=2, title="Topic", status="In Progress", tasks=[]
    )
    looked_up = {"called": False}

    class _MissionSvc:
        @staticmethod
        def get_today_mission(user_id, mission_date=None):
            looked_up["called"] = True
            return None

    class _Session:
        @staticmethod
        def get_owned_mission(mission_id, user_id):
            assert mission_id == 12
            return mission

        @staticmethod
        def start_session(mission_id, user_id):
            raise AssertionError("resume must never start")

    class _PlanSvc:
        @staticmethod
        def get_user_active_plan(user_id):
            return SimpleNamespace(id=1, preferred_session_minutes=20)

        @staticmethod
        def get_current_week_plan(plan):
            return SimpleNamespace(id=1)

    adapter = MissionResumeAdapter(
        mission_service=_MissionSvc,
        study_session_service=_Session,
        study_plan_service=_PlanSvc,
    )
    result = adapter.resume_session("2", session_id="12")
    assert result.ok is True
    assert result.value["mission_id"] == "12"
    assert looked_up["called"] is False


def test_adapter_unavailable_on_service_exception():
    events = EventRegistry()

    class _MissionSvc:
        @staticmethod
        def get_today_mission(user_id, mission_date=None):
            raise RuntimeError("db down")

    adapter = MissionResumeAdapter(events=events, mission_service=_MissionSvc)
    result = adapter.resume_session("1")
    assert result.ok is False
    assert result.error_code == UNAVAILABLE
    assert result.fallback_used is False
    assert MISSION_RESUME_BRIDGE_FAILURE in [
        e.event_type for e in events.published()
    ]


def test_adapter_forbidden_foreign_session_id():
    class _MissionSvc:
        @staticmethod
        def get_today_mission(user_id, mission_date=None):
            raise AssertionError("must not locate when session_id given")

    class _Session:
        @staticmethod
        def get_owned_mission(mission_id, user_id):
            raise ValueError(f"Mission {mission_id} does not belong to user {user_id}")

    adapter = MissionResumeAdapter(
        mission_service=_MissionSvc,
        study_session_service=_Session,
    )
    result = adapter.resume_session("1", session_id="99")
    assert result.ok is False
    assert result.error_code == FORBIDDEN


def test_get_session_status_delegates_to_resume():
    mission = SimpleNamespace(
        id=4, user_id=1, title="T", status="In Progress", tasks=[]
    )

    class _Session:
        @staticmethod
        def get_owned_mission(mission_id, user_id):
            return mission

    class _PlanSvc:
        @staticmethod
        def get_user_active_plan(user_id):
            return SimpleNamespace(id=1, preferred_session_minutes=15)

        @staticmethod
        def get_current_week_plan(plan):
            return SimpleNamespace(id=1)

    adapter = MissionResumeAdapter(
        study_session_service=_Session,
        study_plan_service=_PlanSvc,
    )
    result = adapter.get_session_status("1", session_id="4")
    assert result.ok is True
    assert result.value["session_id"] == "4"
    assert result.value["status"] == "in_progress"


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
