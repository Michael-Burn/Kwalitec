"""Unit tests — Journey Read Adapter mapping, errors, DTOs."""

from __future__ import annotations

from types import SimpleNamespace

from app.infrastructure.adapters.educational_runtime_bridge import (
    AUTHORITY_JOURNEY_BRIDGE,
    FORBIDDEN,
    JOURNEY_BRIDGE_FAILURE,
    JOURNEY_BRIDGE_LATENCY,
    JOURNEY_BRIDGE_REQUESTED,
    JOURNEY_BRIDGE_SUCCESS,
    NO_ACTIVE_PLAN,
    UNAVAILABLE_RECOMMENDATION,
    BridgeResult,
    JourneyAdapter,
    build_trace_ref,
    empty_authentic_journey,
    map_journey_to_projection,
    map_topic_card,
    map_topic_status,
)
from app.infrastructure.events.registry import EventRegistry


def test_map_topic_status_completed_and_current():
    assert map_topic_status(completed=True, is_current=False) == "completed"
    assert map_topic_status(completed=False, is_current=True) == "current"
    assert map_topic_status(completed=False, is_current=False) == "upcoming"
    assert (
        map_topic_status(completed=False, is_current=False, stage="Mastered")
        == "completed"
    )


def test_map_topic_card_labels():
    card = map_topic_card(topic_id="7", title="Probability", status="current")
    assert card["topic_id"] == "7"
    assert card["status"] == "current"
    assert card["status_label"] == "Current"


def test_build_trace_ref_defaults_unavailable_recommendation():
    trace = build_trace_ref(
        what="Completed session",
        why_summary="Mission completed",
        reason_codes=["session_completed"],
        evidence_refs=[{"kind": "mission", "id": "1"}],
    )
    assert trace["what"] == "Completed session"
    assert trace["recommendation"]["unavailable_reason"] == "unavailable"
    assert trace["recommendation"]["changed"] is None
    assert trace["recommendation"]["prior_label"] is None


def test_empty_authentic_journey_never_demo():
    doc = empty_authentic_journey(student_id="9", error_code=NO_ACTIVE_PLAN)
    assert doc["has_journey"] is False
    assert doc["authority"] == AUTHORITY_JOURNEY_BRIDGE
    assert doc["progress"]["overall_progress_ratio"] == 0.0
    assert doc["topics"] == []
    assert doc["recommendation_focus"] is None
    assert doc["recommendation_history"] is None
    assert doc["progress"]["current_topic_title"] != "Core methods"


def test_map_journey_to_projection_clamps_ratio():
    projection = map_journey_to_projection(
        student_id="1",
        has_journey=True,
        overall_progress_ratio=1.5,
        examination_label="IFoA CM1",
        topics=[map_topic_card(topic_id="1", title="A", status="upcoming")],
        recommendation_history=None,
    )
    assert projection["progress"]["overall_progress_ratio"] == 1.0
    assert projection["authority"] == AUTHORITY_JOURNEY_BRIDGE
    assert projection["recommendation_history"] is None
    assert projection["next_action_authority"] is False


def test_adapter_forbidden_for_non_numeric_student_id():
    events = EventRegistry()
    adapter = JourneyAdapter(events=events)
    result = adapter.project_journey("not-a-user")
    assert isinstance(result, BridgeResult)
    assert result.ok is False
    assert result.error_code == FORBIDDEN
    types = [e.event_type for e in events.published()]
    assert JOURNEY_BRIDGE_REQUESTED in types
    assert JOURNEY_BRIDGE_FAILURE in types
    assert JOURNEY_BRIDGE_LATENCY in types


def test_adapter_empty_when_no_active_plan():
    events = EventRegistry()

    class _PlanSvc:
        @staticmethod
        def get_user_active_plan(user_id):
            return None

    adapter = JourneyAdapter(events=events, study_plan_service=_PlanSvc)
    result = adapter.project_journey("9")
    assert result.ok is True
    assert result.error_code == NO_ACTIVE_PLAN
    assert result.value is not None
    assert result.value["has_journey"] is False
    assert result.value["authority"] == AUTHORITY_JOURNEY_BRIDGE
    assert result.value["recommendation_history"] is None
    types = [e.event_type for e in events.published()]
    assert JOURNEY_BRIDGE_SUCCESS in types
    assert JOURNEY_BRIDGE_FAILURE not in types


def test_adapter_projects_plan_progress_and_null_recommendation_history():
    events = EventRegistry()
    plan = SimpleNamespace(
        id=1,
        user_id=5,
        exam_name="IFoA CM1",
        exam_sitting="April 2027",
        curriculum_id=None,
        preferred_session_minutes=45,
    )

    class _PlanSvc:
        @staticmethod
        def get_user_active_plan(user_id):
            return plan

    class _Lifecycle:
        @staticmethod
        def resolve(user_id, study_plan=None, today=None):
            return SimpleNamespace(stage="learning")

    class _MissionSvc:
        @staticmethod
        def get_today_mission(user_id, mission_date=None):
            return SimpleNamespace(
                id=11, title="Study Probability", user_id=5, status="Pending"
            )

    class _MissionModel:
        class query:  # noqa: N801
            @staticmethod
            def filter(*args, **kwargs):
                return _Query([])

    class _Query:
        def __init__(self, rows):
            self._rows = rows

        def order_by(self, *args, **kwargs):
            return self

        def limit(self, n):
            return self

        def all(self):
            return self._rows

    class _AttemptModel:
        class query:  # noqa: N801
            @staticmethod
            def filter_by(**kwargs):
                return _Query([])

    adapter = JourneyAdapter(
        events=events,
        study_plan_service=_PlanSvc,
        learning_lifecycle_service=_Lifecycle,
        mission_service=_MissionSvc,
        mission_model=_MissionModel,
        study_attempt_model=_AttemptModel,
        readiness_service=SimpleNamespace(
            calculate_readiness=lambda summary: None
        ),
        curriculum_engine_service=SimpleNamespace(
            build_student_curriculum=lambda plan: None
        ),
    )
    result = adapter.project_journey("5")
    assert result.ok is True
    assert result.value is not None
    assert result.value["has_journey"] is True
    assert result.value["progress"]["examination_label"] == "IFoA CM1"
    assert result.value["progress"]["lifecycle_stage"] == "learning"
    assert result.value["recommendation_history"] is None
    assert result.value["authority"] == AUTHORITY_JOURNEY_BRIDGE
    # Recommendation focus may be mission-aligned; history remains null.
    assert result.value["recommendation_focus"] is not None
    assert (
        result.value["recommendation_focus"]["recommendation"]
        == UNAVAILABLE_RECOMMENDATION
        or result.value["recommendation_focus"]["recommendation"][
            "unavailable_reason"
        ]
        == "unavailable"
    )
    types = [e.event_type for e in events.published()]
    assert JOURNEY_BRIDGE_SUCCESS in types


def test_unavailable_recommendation_contract_is_explicit_nulls():
    assert UNAVAILABLE_RECOMMENDATION["changed"] is None
    assert UNAVAILABLE_RECOMMENDATION["prior_label"] is None
    assert UNAVAILABLE_RECOMMENDATION["next_label"] is None
    assert UNAVAILABLE_RECOMMENDATION["decision_ids"] is None
    assert UNAVAILABLE_RECOMMENDATION["unavailable_reason"] == "unavailable"
