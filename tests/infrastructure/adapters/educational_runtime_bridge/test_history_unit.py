"""Unit tests — History Read Adapter mapping, errors, DTOs."""

from __future__ import annotations

from datetime import date
from types import SimpleNamespace

from app.infrastructure.adapters.educational_runtime_bridge import (
    AUTHORITY_HISTORY_BRIDGE,
    FORBIDDEN,
    HISTORY_BRIDGE_FAILURE,
    HISTORY_BRIDGE_LATENCY,
    HISTORY_BRIDGE_REQUESTED,
    HISTORY_BRIDGE_SUCCESS,
    UNAVAILABLE_RECOMMENDATION,
    BridgeResult,
    HistoryAdapter,
    clamp_limit,
    empty_authentic_history,
    map_completed_session,
    map_history_to_projection,
    map_page_meta,
)
from app.infrastructure.events.registry import EventRegistry


def test_clamp_limit_default_and_hard_max():
    assert clamp_limit(None) == 20
    assert clamp_limit(5) == 5
    assert clamp_limit(500) == 100
    assert clamp_limit(-1) == 0


def test_empty_authentic_history_never_demo():
    doc = empty_authentic_history(student_id="9")
    assert doc["authority"] == AUTHORITY_HISTORY_BRIDGE
    assert doc["completed_sessions"] == []
    assert doc["total_study_minutes"] == 0
    assert doc["readiness_progression"] is None
    assert doc["readiness_progression_meta"]["unavailable_reason"] == "unavailable"
    assert doc["recommendation_history"] is None
    assert doc["recommendation_history_meta"]["unavailable_reason"] == "unavailable"
    assert doc["page"]["has_more"] is False


def test_map_history_null_recommendation_and_readiness():
    projection = map_history_to_projection(
        student_id="1",
        completed_sessions=[
            map_completed_session(
                session_id="11",
                mission_id="11",
                topic_title="Probability",
                completed_at="2026-07-20",
                study_minutes=30,
            )
        ],
        total_study_minutes=30,
        readiness_progression=None,
        recommendation_history=None,
        page=map_page_meta(limit=20, offset=0, has_more=False),
    )
    assert projection["authority"] == AUTHORITY_HISTORY_BRIDGE
    assert projection["session_count"] == 1
    assert projection["recommendation_history"] is None
    assert projection["readiness_progression"] is None
    assert projection["readiness_progression_meta"]["unavailable_reason"] == (
        "unavailable"
    )


def test_adapter_forbidden_for_non_numeric_student_id():
    events = EventRegistry()
    adapter = HistoryAdapter(events=events)
    result = adapter.project_history("not-a-user")
    assert isinstance(result, BridgeResult)
    assert result.ok is False
    assert result.error_code == FORBIDDEN
    types = [e.event_type for e in events.published()]
    assert HISTORY_BRIDGE_REQUESTED in types
    assert HISTORY_BRIDGE_FAILURE in types
    assert HISTORY_BRIDGE_LATENCY in types


def test_adapter_empty_history_when_no_completed_missions():
    events = EventRegistry()

    class _Col:
        def desc(self):
            return self

        def __lt__(self, other):
            return self

        def __le__(self, other):
            return self

        def __gt__(self, other):
            return self

        def __ge__(self, other):
            return self

        def __eq__(self, other):
            return self

        def __and__(self, other):
            return self

        def __or__(self, other):
            return self

        def __bool__(self):
            return True

    class _MissionModel:
        user_id = _Col()
        status = _Col()
        mission_date = _Col()
        id = _Col()

        class query:  # noqa: N801
            @staticmethod
            def filter(*args, **kwargs):
                return _Query([])

    class _Query:
        def __init__(self, rows):
            self._rows = rows

        def filter(self, *args, **kwargs):
            return self

        def order_by(self, *args, **kwargs):
            return self

        def limit(self, n):
            return self

        def all(self):
            return self._rows

    class _Lifecycle:
        @staticmethod
        def resolve(user_id, study_plan=None, today=None):
            return SimpleNamespace(stage="learning")

    class _PlanSvc:
        @staticmethod
        def get_user_active_plan(user_id):
            return None

    class _Adaptive:
        @staticmethod
        def get_mastered_topics(user_id):
            return []

    class _AttemptModel:
        class query:  # noqa: N801
            @staticmethod
            def filter_by(**kwargs):
                return _Query([])

    class _ProgressModel:
        class query:  # noqa: N801
            @staticmethod
            def filter(*args, **kwargs):
                return _Query([])

    adapter = HistoryAdapter(
        events=events,
        mission_model=_MissionModel,
        study_attempt_model=_AttemptModel,
        topic_progress_model=_ProgressModel,
        learning_lifecycle_service=_Lifecycle,
        study_plan_service=_PlanSvc,
        adaptive_learning_service=_Adaptive,
    )
    result = adapter.project_history("9")
    assert result.ok is True
    assert result.value is not None
    assert result.value["authority"] == AUTHORITY_HISTORY_BRIDGE
    assert result.value["completed_sessions"] == []
    assert result.value["recommendation_history"] is None
    assert result.value["readiness_progression"] is None
    types = [e.event_type for e in events.published()]
    assert HISTORY_BRIDGE_SUCCESS in types
    assert HISTORY_BRIDGE_FAILURE not in types


def test_adapter_projects_completed_session_with_trace():
    events = EventRegistry()
    mission = SimpleNamespace(
        id=11,
        user_id=5,
        title="Study Probability",
        status="Completed",
        mission_date=date(2026, 7, 20),
    )
    attempt = SimpleNamespace(
        id=21,
        user_id=5,
        mission_id=11,
        duration_minutes=45,
        study_date=date(2026, 7, 20),
        questions_attempted=10,
        confidence_before="Low",
        confidence_after="Medium",
    )

    class _Col:
        def desc(self):
            return self

        def __lt__(self, other):
            return self

        def __le__(self, other):
            return self

        def __gt__(self, other):
            return self

        def __ge__(self, other):
            return self

        def __eq__(self, other):
            return self

        def __and__(self, other):
            return self

        def __or__(self, other):
            return self

        def __bool__(self):
            return True

    class _Query:
        def __init__(self, rows):
            self._rows = rows

        def filter(self, *args, **kwargs):
            return self

        def order_by(self, *args, **kwargs):
            return self

        def limit(self, n):
            return self

        def all(self):
            return self._rows

        def first(self):
            return self._rows[0] if self._rows else None

    class _MissionModel:
        user_id = _Col()
        status = _Col()
        mission_date = _Col()
        id = _Col()

        class query:  # noqa: N801
            @staticmethod
            def filter(*args, **kwargs):
                return _Query([mission])

    class _AttemptModel:
        class query:  # noqa: N801
            @staticmethod
            def filter_by(**kwargs):
                return _Query([attempt])

    class _Lifecycle:
        @staticmethod
        def resolve(user_id, study_plan=None, today=None):
            return SimpleNamespace(stage="learning")

    class _PlanSvc:
        @staticmethod
        def get_user_active_plan(user_id):
            return None

    class _Adaptive:
        @staticmethod
        def get_mastered_topics(user_id):
            return []

    class _ProgressModel:
        completed = _Col()
        current_stage = _Col()
        user_id = _Col()
        id = _Col()

        class query:  # noqa: N801
            @staticmethod
            def filter(*args, **kwargs):
                return _Query([])

    adapter = HistoryAdapter(
        events=events,
        mission_model=_MissionModel,
        study_attempt_model=_AttemptModel,
        topic_progress_model=_ProgressModel,
        learning_lifecycle_service=_Lifecycle,
        study_plan_service=_PlanSvc,
        adaptive_learning_service=_Adaptive,
    )
    result = adapter.project_history("5")
    assert result.ok is True
    assert result.value["authority"] == AUTHORITY_HISTORY_BRIDGE
    assert result.value["session_count"] == 1
    session = result.value["completed_sessions"][0]
    assert session["mission_id"] == "11"
    assert session["study_minutes"] == 45
    assert session["trace"]["recommendation"] == UNAVAILABLE_RECOMMENDATION
    assert result.value["recommendation_history"] is None
    assert result.value["total_study_minutes"] == 45


def test_pagination_stable_page_contract():
    page = map_page_meta(
        limit=2, offset=0, has_more=True, next_offset=2, next_cursor="abc"
    )
    assert page["limit"] == 2
    assert page["offset"] == 0
    assert page["has_more"] is True
    assert page["next_offset"] == 2
    assert page["next_cursor"] == "abc"
