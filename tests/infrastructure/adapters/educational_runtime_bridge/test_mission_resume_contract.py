"""Contract tests — Mission Resume Bridge interface stability."""

from __future__ import annotations

from datetime import date
from types import SimpleNamespace

import pytest

from app.application.student_experience.ports.mission_port import MissionPort
from app.infrastructure.adapters.educational_runtime_bridge import (
    AUTHORITY_STUDY_SESSION_SERVICE,
    BRIDGE_ERROR_CODES,
    MISSION_RESUME_BRIDGE_EVENT_TYPES,
    BridgeResult,
    MissionResumeAdapter,
    MissionResumeBridge,
    map_mission_to_resume_result,
)
from app.infrastructure.adapters.mission.experience_adapter import (
    ExperienceMissionAdapter,
)
from app.infrastructure.events.types import EVENT_TYPES

REQUIRED_RESUME_KEYS = frozenset(
    {
        "student_id",
        "mission_id",
        "session_id",
        "experience_session_id",
        "topic_title",
        "estimated_minutes",
        "status",
        "tasks",
        "authority",
        "next_action_authority",
        "resumed",
    }
)


def test_mission_resume_adapter_satisfies_bridge_protocol():
    adapter = MissionResumeAdapter()
    assert isinstance(adapter, MissionResumeBridge)


def test_experience_adapter_with_resume_bridge_still_mission_port():
    adapter = ExperienceMissionAdapter(mission_resume=MissionResumeAdapter())
    assert isinstance(adapter, MissionPort)


def test_error_codes_catalogue_stable():
    expected = {
        "UNAVAILABLE",
        "NO_ACTIVE_PLAN",
        "OUTSIDE_PLAN_WINDOW",
        "NOT_FOUND",
        "FORBIDDEN",
        "INVALID_STATE",
        "EVIDENCE_REJECTED",
    }
    assert set(BRIDGE_ERROR_CODES) == expected


def test_resume_telemetry_event_types_registered():
    for event_type in MISSION_RESUME_BRIDGE_EVENT_TYPES:
        assert event_type in EVENT_TYPES


def test_resume_result_contract_keys():
    mission = SimpleNamespace(
        id=1, title="T", user_id=1, status="In Progress", tasks=[]
    )
    resumed = map_mission_to_resume_result(mission, student_id="1")
    assert REQUIRED_RESUME_KEYS.issubset(resumed.keys())
    assert resumed["authority"] == AUTHORITY_STUDY_SESSION_SERVICE
    assert resumed["status"] == "in_progress"
    assert resumed["next_action_authority"] is False
    assert resumed["resumed"] is True


def test_resume_session_signature_accepts_as_of_date():
    adapter = MissionResumeAdapter()
    result = adapter.resume_session("x", as_of_date=date(2026, 1, 1))
    assert isinstance(result, BridgeResult)


def test_bridged_resume_authority_never_demo_seed():
    mission = SimpleNamespace(
        id=3, title="Syllabus topic", user_id=1, status="In Progress", tasks=[]
    )
    resumed = map_mission_to_resume_result(mission, student_id="1")
    assert resumed["authority"] != "mission_engine"
    assert "seeded" not in resumed["authority"]
    assert resumed["authority"] == AUTHORITY_STUDY_SESSION_SERVICE


@pytest.mark.parametrize("method", ["resume_session", "get_session_status"])
def test_bridge_exposes_resume_surface_only(method):
    adapter = MissionResumeAdapter()
    assert hasattr(adapter, method)
    # Start / complete / generate are intentionally absent on Mission Resume.
    assert not hasattr(adapter, "start_session")
    assert not hasattr(adapter, "complete_session")
    assert not hasattr(adapter, "generate_today_mission")


def test_lifecycle_invariants_keys_present_on_success_shape():
    """Resume DTO carries identity keys required for continuity."""
    mission = SimpleNamespace(
        id=55,
        title="Continuity topic",
        user_id=9,
        status="In Progress",
        tasks=[
            SimpleNamespace(
                id=1, title="A", description=None, order=0, completed=False
            )
        ],
    )
    resumed = map_mission_to_resume_result(mission, student_id="9")
    assert resumed["student_id"] == "9"
    assert resumed["mission_id"] == "55"
    assert resumed["session_id"] == "55"
    assert resumed["status"] == "in_progress"
    assert isinstance(resumed["tasks"], list)
