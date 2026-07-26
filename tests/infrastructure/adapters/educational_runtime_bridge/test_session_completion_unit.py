"""Unit tests — Session Completion Adapter mapping, errors, DTOs."""

from __future__ import annotations

from types import SimpleNamespace

from app.infrastructure.adapters.educational_runtime_bridge import (
    AUTHORITY_STUDY_SESSION_SERVICE,
    EVIDENCE_REJECTED,
    FORBIDDEN,
    INVALID_STATE,
    NOT_FOUND,
    SESSION_COMPLETION_BRIDGE_FAILURE,
    SESSION_COMPLETION_BRIDGE_LATENCY,
    SESSION_COMPLETION_BRIDGE_REQUESTED,
    SESSION_COMPLETION_BRIDGE_SUCCESS,
    UNAVAILABLE,
    BridgeResult,
    SessionCompletionAdapter,
    map_mission_to_completion_result,
)
from app.infrastructure.events.registry import EventRegistry


def test_map_mission_to_completion_result_dto():
    task = SimpleNamespace(
        id=3, title="Practice", description=None, order=0, completed=True
    )
    mission = SimpleNamespace(
        id=42, title="Study Probability", status="Completed", tasks=[task]
    )
    completed = map_mission_to_completion_result(
        mission,
        student_id="1",
        estimated_minutes=45,
        evidence_accepted=True,
        mastery_updated=True,
        completed_at="2026-07-25T10:00:00Z",
    )
    assert completed["mission_id"] == "42"
    assert completed["session_id"] == "42"
    assert completed["experience_session_id"] == "es-42"
    assert completed["topic_title"] == "Study Probability"
    assert completed["status"] == "completed"
    assert completed["educational_complete"] is True
    assert completed["evidence_accepted"] is True
    assert completed["mastery_updated"] is True
    assert completed["estimated_minutes"] == 45
    assert completed["authority"] == AUTHORITY_STUDY_SESSION_SERVICE
    assert completed["next_action_authority"] is False
    assert completed["completed_at"] == "2026-07-25T10:00:00Z"


def test_adapter_forbidden_for_non_numeric_student_id():
    events = EventRegistry()
    adapter = SessionCompletionAdapter(events=events)
    result = adapter.complete_session("not-a-user", session_id="1")
    assert isinstance(result, BridgeResult)
    assert result.ok is False
    assert result.error_code == FORBIDDEN
    assert result.value is None
    types = [e.event_type for e in events.published()]
    assert SESSION_COMPLETION_BRIDGE_REQUESTED in types
    assert SESSION_COMPLETION_BRIDGE_FAILURE in types
    assert SESSION_COMPLETION_BRIDGE_LATENCY in types


def test_adapter_requires_session_id():
    adapter = SessionCompletionAdapter()
    result = adapter.complete_session("5")
    assert result.ok is False
    assert result.error_code == NOT_FOUND


def test_adapter_invalid_state_when_pending():
    events = EventRegistry()
    pending = SimpleNamespace(
        id=7, user_id=1, title="Not started", status="Pending", tasks=[]
    )

    class _Session:
        @staticmethod
        def get_owned_mission(mission_id, user_id):
            return pending

        @staticmethod
        def finish_session(**kwargs):
            raise AssertionError("must not finish Pending session")

    adapter = SessionCompletionAdapter(
        events=events, study_session_service=_Session
    )
    result = adapter.complete_session("1", session_id="7")
    assert result.ok is False
    assert result.error_code == INVALID_STATE
    types = [e.event_type for e in events.published()]
    assert SESSION_COMPLETION_BRIDGE_FAILURE in types


def test_adapter_invalid_state_when_already_completed():
    done = SimpleNamespace(
        id=8, user_id=1, title="Done", status="Completed", tasks=[]
    )

    class _Session:
        @staticmethod
        def get_owned_mission(mission_id, user_id):
            return done

    result = SessionCompletionAdapter(
        study_session_service=_Session
    ).complete_session("1", session_id="8")
    assert result.ok is False
    assert result.error_code == INVALID_STATE


def test_adapter_completes_without_practice_via_finish_session():
    events = EventRegistry()
    active = SimpleNamespace(
        id=99,
        user_id=5,
        title="Practice Distributions",
        status="In Progress",
        tasks=[],
    )
    completed = SimpleNamespace(
        id=99,
        user_id=5,
        title="Practice Distributions",
        status="Completed",
        tasks=[],
    )

    class _Session:
        @staticmethod
        def get_owned_mission(mission_id, user_id):
            assert mission_id == 99
            assert user_id == 5
            return active

        @staticmethod
        def finish_session(**kwargs):
            assert kwargs["mission_id"] == 99
            assert kwargs["user_id"] == 5
            assert kwargs["completion_status"] == "yes"
            return SimpleNamespace(
                mission=completed,
                completion_status="yes",
                study_progress_updated=False,
                mission_completed=True,
            )

        @staticmethod
        def validate_practice_outcome(*args, **kwargs):
            raise AssertionError("no practice path")

    class _PlanSvc:
        @staticmethod
        def get_user_active_plan(user_id):
            return SimpleNamespace(id=1, preferred_session_minutes=30)

    adapter = SessionCompletionAdapter(
        events=events,
        study_session_service=_Session,
        study_plan_service=_PlanSvc,
    )
    result = adapter.complete_session("5", session_id="99")
    assert result.ok is True
    assert result.value is not None
    assert result.value["mission_id"] == "99"
    assert result.value["status"] == "completed"
    assert result.value["educational_complete"] is True
    assert result.value["evidence_accepted"] is False
    assert result.value["authority"] == AUTHORITY_STUDY_SESSION_SERVICE
    assert result.value["estimated_minutes"] == 30
    types = [e.event_type for e in events.published()]
    assert SESSION_COMPLETION_BRIDGE_REQUESTED in types
    assert SESSION_COMPLETION_BRIDGE_SUCCESS in types
    assert SESSION_COMPLETION_BRIDGE_LATENCY in types


def test_adapter_evidence_before_completion_with_practice():
    """Evidence commit runs before mark-complete; order is enforced."""
    events = EventRegistry()
    active = SimpleNamespace(
        id=11, user_id=2, title="Bayes", status="In Progress", tasks=[]
    )
    completed = SimpleNamespace(
        id=11, user_id=2, title="Bayes", status="Completed", tasks=[]
    )
    order: list[str] = []

    class _Attempt:
        questions_attempted = 10
        questions_correct = 8

        def get_accuracy_percentage(self):
            return 80.0

    class _Session:
        @staticmethod
        def get_owned_mission(mission_id, user_id):
            return active if "complete" not in order else completed

        @staticmethod
        def validate_practice_outcome(attempted, correct):
            order.append("validate")
            assert attempted == 10
            assert correct == 8

        @staticmethod
        def mark_all_tasks_complete(mission):
            order.append("mark_tasks")

        @staticmethod
        def finish_session(**kwargs):
            raise AssertionError("practice path must not use finish_session")

        @staticmethod
        def _observe_session_completed(**kwargs):
            order.append("observe")

    class _Learning:
        @staticmethod
        def create_study_attempt(**kwargs):
            order.append("evidence")
            assert kwargs["questions_attempted"] == 10
            return _Attempt()

    class _MissionSvc:
        @staticmethod
        def complete_mission(mission_id, user_id):
            order.append("complete")
            return completed

    class _PlanSvc:
        @staticmethod
        def get_user_active_plan(user_id):
            return SimpleNamespace(preferred_session_minutes=45)

    adapter = SessionCompletionAdapter(
        events=events,
        study_session_service=_Session,
        learning_service=_Learning,
        mission_service=_MissionSvc,
        study_plan_service=_PlanSvc,
    )
    result = adapter.complete_session(
        "2",
        session_id="11",
        outcome={
            "questions_attempted": 10,
            "questions_correct": 8,
            "topic_id": 3,
            "duration_minutes": 25,
        },
    )
    assert result.ok is True
    assert result.value["evidence_accepted"] is True
    assert result.value["educational_complete"] is True
    assert order == ["validate", "evidence", "mark_tasks", "complete", "observe"]


def test_adapter_evidence_failure_leaves_session_active():
    """Evidence failures must not mark the session complete."""
    events = EventRegistry()
    active = SimpleNamespace(
        id=20, user_id=3, title="Survival", status="In Progress", tasks=[]
    )

    class _Session:
        @staticmethod
        def get_owned_mission(mission_id, user_id):
            return active

        @staticmethod
        def validate_practice_outcome(attempted, correct):
            return None

        @staticmethod
        def mark_all_tasks_complete(mission):
            raise AssertionError("must not mark complete after evidence failure")

        @staticmethod
        def finish_session(**kwargs):
            raise AssertionError("must not finish after evidence failure")

    class _Learning:
        @staticmethod
        def create_study_attempt(**kwargs):
            raise RuntimeError("evidence authority unavailable")

    class _MissionSvc:
        @staticmethod
        def complete_mission(mission_id, user_id):
            raise AssertionError("must not complete after evidence failure")

    adapter = SessionCompletionAdapter(
        events=events,
        study_session_service=_Session,
        learning_service=_Learning,
        mission_service=_MissionSvc,
    )
    result = adapter.complete_session(
        "3",
        session_id="20",
        outcome={"questions_attempted": 5, "questions_correct": 4},
    )
    assert result.ok is False
    assert result.error_code == EVIDENCE_REJECTED
    assert active.status == "In Progress"
    types = [e.event_type for e in events.published()]
    assert SESSION_COMPLETION_BRIDGE_FAILURE in types


def test_adapter_invalid_practice_does_not_complete():
    active = SimpleNamespace(
        id=21, user_id=4, title="X", status="In Progress", tasks=[]
    )

    class _Session:
        @staticmethod
        def get_owned_mission(mission_id, user_id):
            return active

        @staticmethod
        def validate_practice_outcome(attempted, correct):
            raise ValueError(
                "Questions Correct cannot exceed Questions Attempted."
            )

        @staticmethod
        def mark_all_tasks_complete(mission):
            raise AssertionError("invalid practice must not complete")

    result = SessionCompletionAdapter(
        study_session_service=_Session
    ).complete_session(
        "4",
        session_id="21",
        outcome={"questions_attempted": 3, "questions_correct": 9},
    )
    assert result.ok is False
    assert result.error_code == INVALID_STATE


def test_adapter_forbidden_on_ownership_mismatch():
    class _Session:
        @staticmethod
        def get_owned_mission(mission_id, user_id):
            raise ValueError(f"Mission {mission_id} does not belong to user {user_id}")

    result = SessionCompletionAdapter(
        study_session_service=_Session
    ).complete_session("9", session_id="1")
    assert result.ok is False
    assert result.error_code == FORBIDDEN


def test_adapter_unavailable_on_unexpected_error():
    class _Session:
        @staticmethod
        def get_owned_mission(mission_id, user_id):
            raise RuntimeError("db down")

    result = SessionCompletionAdapter(
        study_session_service=_Session
    ).complete_session("1", session_id="1")
    assert result.ok is False
    assert result.error_code == UNAVAILABLE
