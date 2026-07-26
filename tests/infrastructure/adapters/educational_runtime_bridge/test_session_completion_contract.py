"""Contract tests — Session Completion Bridge interface stability."""

from __future__ import annotations

from types import SimpleNamespace

from app.application.student_experience.ports.mission_port import MissionPort
from app.infrastructure.adapters.educational_runtime_bridge import (
    AUTHORITY_STUDY_SESSION_SERVICE,
    BRIDGE_ERROR_CODES,
    SESSION_COMPLETION_BRIDGE_EVENT_TYPES,
    BridgeResult,
    SessionCompletionAdapter,
    SessionCompletionBridge,
    map_mission_to_completion_result,
)
from app.infrastructure.adapters.mission.experience_adapter import (
    ExperienceMissionAdapter,
)
from app.infrastructure.events.types import EVENT_TYPES

REQUIRED_COMPLETION_KEYS = frozenset(
    {
        "student_id",
        "mission_id",
        "session_id",
        "experience_session_id",
        "topic_title",
        "estimated_minutes",
        "status",
        "completed_at",
        "educational_complete",
        "evidence_accepted",
        "mastery_updated",
        "tasks",
        "authority",
        "next_action_authority",
    }
)


def test_session_completion_adapter_satisfies_bridge_protocol():
    adapter = SessionCompletionAdapter()
    assert isinstance(adapter, SessionCompletionBridge)


def test_experience_adapter_with_completion_bridge_still_mission_port():
    adapter = ExperienceMissionAdapter(
        session_completion=SessionCompletionAdapter()
    )
    assert isinstance(adapter, MissionPort)


def test_error_codes_include_evidence_rejected():
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


def test_completion_telemetry_event_types_registered():
    for event_type in SESSION_COMPLETION_BRIDGE_EVENT_TYPES:
        assert event_type in EVENT_TYPES


def test_completion_result_contract_keys():
    mission = SimpleNamespace(
        id=1, title="T", user_id=1, status="Completed", tasks=[]
    )
    completed = map_mission_to_completion_result(mission, student_id="1")
    assert REQUIRED_COMPLETION_KEYS.issubset(completed.keys())
    assert completed["authority"] == AUTHORITY_STUDY_SESSION_SERVICE
    assert completed["status"] == "completed"
    assert completed["educational_complete"] is True
    assert completed["next_action_authority"] is False


def test_complete_session_signature_accepts_outcome():
    adapter = SessionCompletionAdapter()
    result = adapter.complete_session(
        "x",
        session_id="1",
        outcome={"questions_attempted": 1, "questions_correct": 1},
    )
    assert isinstance(result, BridgeResult)


def test_bridged_completion_authority_never_demo_seed():
    mission = SimpleNamespace(
        id=3, title="Syllabus topic", user_id=1, status="Completed", tasks=[]
    )
    completed = map_mission_to_completion_result(mission, student_id="1")
    assert completed["authority"] != "mission_engine"
    assert "seeded" not in completed["authority"]
    assert completed["authority"] == AUTHORITY_STUDY_SESSION_SERVICE


def test_bridge_exposes_complete_surface_only():
    adapter = SessionCompletionAdapter()
    assert hasattr(adapter, "complete_session")
    assert not hasattr(adapter, "start_session")
    assert not hasattr(adapter, "resume_session")
    assert not hasattr(adapter, "generate_today_mission")
    assert not hasattr(adapter, "get_todays_session")


def test_lifecycle_invariants_keys_present_on_success_shape():
    """Completion DTO carries identity keys required for educational integrity."""
    mission = SimpleNamespace(
        id=55,
        title="Continuity topic",
        user_id=9,
        status="Completed",
        tasks=[
            SimpleNamespace(
                id=1, title="A", description=None, order=0, completed=True
            )
        ],
    )
    completed = map_mission_to_completion_result(
        mission, student_id="9", evidence_accepted=True
    )
    assert completed["student_id"] == "9"
    assert completed["mission_id"] == "55"
    assert completed["session_id"] == "55"
    assert completed["status"] == "completed"
    assert completed["educational_complete"] is True
    assert isinstance(completed["tasks"], list)
