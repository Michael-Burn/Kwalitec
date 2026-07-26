"""EP-002.2 — Shared Foundation DI unit and composition tests."""

from __future__ import annotations

from types import MappingProxyType
from unittest.mock import MagicMock

import pytest

from app.infrastructure.adapters.consumer_chain import (
    API_BUILD_DAILY_STUDY_PLAN,
    ASSEMBLE_SOURCE_ASSEMBLED,
    ASSEMBLE_SOURCE_INJECTED,
    SERVICE_PLANNING,
    assemble_shared_canonical_state,
    build_consumer_chain_telemetry,
    observe_build_api,
    resolve_enabled_twin_foundation,
    set_consumer_chain_telemetry,
)
from app.infrastructure.adapters.digital_twin.contracts import (
    AVAILABILITY_AVAILABLE,
)
from app.infrastructure.adapters.digital_twin.foundation import (
    FOUNDATION_VERSION,
    CanonicalLearnerState,
)
from app.infrastructure.diagnostics.logging import StructuredLogger
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import CONSUMER_CHAIN_FOUNDATION_ASSEMBLE
from app.services.planning_service import PlanningService
from app.services.readiness_service import ReadinessService
from app.services.recommendation_service import RecommendationService


def _block(payload: dict, *, availability: str = AVAILABILITY_AVAILABLE) -> dict:
    return {
        "availability": availability,
        "unavailable_reason": "" if availability == AVAILABILITY_AVAILABLE else "x",
        "authority": "runtime_a",
        "source_field": "test",
        "evidence_refs": [],
        "payload": payload,
    }


def _canonical_state() -> CanonicalLearnerState:
    return CanonicalLearnerState(
        student_id="42",
        as_of="2026-07-26T10:00:00",
        foundation_version=FOUNDATION_VERSION,
        twin_id="twin-foundation-42",
        study_state=_block(
            {
                "lifecycle_stage": "Learning",
                "examination_label": "CS2",
                "exam_countdown_days": 40,
                "exam_readiness": 58.5,
                "readiness_overall": {
                    "score": 58.5,
                    "coverage_pct": 50.0,
                    "avg_mastery": 65.0,
                    "review_discipline": 70.0,
                    "total_topics": 4,
                    "topics_started": 2,
                    "topics_mastered": 1,
                },
                "preferences": {
                    "planned_weekly_hours": 10.0,
                    "preferred_session_minutes": 50,
                },
            }
        ),
        topic_mastery=_block(
            {
                "topics": [
                    {
                        "topic_id": "10",
                        "topic_name": "Algebra",
                        "mastery_score": 82.0,
                        "average_accuracy": 80.0,
                        "current_stage": "Mastered",
                    },
                    {
                        "topic_id": "11",
                        "topic_name": "Calculus",
                        "mastery_score": 40.0,
                        "average_accuracy": 55.0,
                        "current_stage": "Learning",
                    },
                    {
                        "topic_id": "12",
                        "topic_name": "Stats",
                        "mastery_score": 55.0,
                        "average_accuracy": 60.0,
                        "current_stage": "Learning",
                    },
                ],
                "mastered_topic_ids": ["10"],
                "mastered_topic_count": 1,
            }
        ),
        topic_progress=_block({"topics": [], "topic_count": 3, "completed_count": 1}),
        learning_evidence=_block({"attempt_count": 4}),
        practice_performance=_block({"accuracy": 70.0}),
        mock_performance=_block({}, availability="unavailable"),
        study_behaviour=_block({"learning_rhythm": {}}),
        study_consistency=_block({"adherence": 0.8}),
        streaks=_block({"current_streak_days": 4, "longest_streak_days": 7}),
        mission_completion=_block({"completed_count": 3, "missed_count": 0}),
        facet_labels=MappingProxyType({}),
        limitations_codes=(),
        provenance_refs=("runtime_a:topic_progress",),
        availability=AVAILABILITY_AVAILABLE,
        unavailable_reason="",
    )


def _daily_plan() -> dict:
    return {
        "availability": AVAILABILITY_AVAILABLE,
        "today_missions": [
            {
                "slot": "review",
                "topic_id": "12",
                "topic_name": "Stats",
                "reason": "due",
                "expected_benefit": "retain",
            }
        ],
        "revision_priorities": [
            {"topic_id": "11", "topic_name": "Calculus", "priority": 1}
        ],
        "topic_ordering": [
            {"topic_id": "12", "topic_name": "Stats", "mastery_score": 55.0}
        ],
        "recommended_workload": {"suggested_minutes": 60},
        "foundation_version": FOUNDATION_VERSION,
        "study_plan_id": 1,
    }


@pytest.fixture
def telemetry():
    sink = build_consumer_chain_telemetry(
        structured=StructuredLogger("test.foundation_di"),
        events=EventRegistry(),
    )
    previous = set_consumer_chain_telemetry(sink)
    yield sink
    set_consumer_chain_telemetry(previous)


def test_resolve_enabled_twin_foundation_off(monkeypatch) -> None:
    monkeypatch.setenv("KWALITEC_DIGITAL_TWIN", "0")
    assert resolve_enabled_twin_foundation() is None


def test_resolve_enabled_twin_foundation_on(monkeypatch) -> None:
    monkeypatch.setenv("KWALITEC_DIGITAL_TWIN", "1")
    foundation = resolve_enabled_twin_foundation()
    assert foundation is not None
    assert foundation.is_enabled() is True


def test_assemble_shared_skips_when_injected(telemetry) -> None:
    foundation = MagicMock()
    state = _canonical_state()
    result = assemble_shared_canonical_state(
        foundation,
        "42",
        canonical_state=state,
        service_name="Test",
        api_name="test",
        telemetry=telemetry,
    )
    assert result is state
    foundation.assemble.assert_not_called()
    records = [
        r
        for r in telemetry.records
        if r["message"] == "consumer_chain.foundation_assemble"
    ]
    assert len(records) == 1
    assert records[0]["assemble_source"] == ASSEMBLE_SOURCE_INJECTED
    assert records[0]["assembled"] is False


def test_assemble_shared_calls_foundation_when_missing(telemetry) -> None:
    foundation = MagicMock()
    state = _canonical_state()
    foundation.assemble.return_value = state
    result = assemble_shared_canonical_state(
        foundation,
        "42",
        service_name="Test",
        api_name="test",
        telemetry=telemetry,
    )
    assert result is state
    foundation.assemble.assert_called_once_with("42")
    records = [
        r
        for r in telemetry.records
        if r["message"] == "consumer_chain.foundation_assemble"
    ]
    assert len(records) == 1
    assert records[0]["assemble_source"] == ASSEMBLE_SOURCE_ASSEMBLED
    assert records[0]["assembled"] is True
    assert any(
        e.event_type == CONSUMER_CHAIN_FOUNDATION_ASSEMBLE
        for e in telemetry.events.published()
    )


def test_insight_nested_compose_assembles_cls_once(telemetry, monkeypatch) -> None:
    """Full Insight → Planner → Readiness chain: one Foundation.assemble."""
    foundation = MagicMock()
    foundation.is_enabled.return_value = True
    foundation.assemble.return_value = _canonical_state()
    plan = _daily_plan()

    def fake_planner(
        user_id,
        today=None,
        *,
        foundation=None,
        canonical_state=None,
    ):
        def body():
            assemble_shared_canonical_state(
                foundation,
                str(user_id),
                canonical_state=canonical_state,
                service_name=SERVICE_PLANNING,
                api_name=API_BUILD_DAILY_STUDY_PLAN,
            )
            return plan

        return observe_build_api(
            service_name=SERVICE_PLANNING,
            api_name=API_BUILD_DAILY_STUDY_PLAN,
            user_id=user_id,
            call=body,
        )

    monkeypatch.setattr(
        PlanningService, "build_daily_study_plan", staticmethod(fake_planner)
    )

    result = RecommendationService.build_study_insights(
        42,
        foundation=foundation,
        include_planner=True,
        include_readiness=True,
    )
    assert result is not None
    assert foundation.assemble.call_count == 1
    assemble_events = [
        r
        for r in telemetry.records
        if r["message"] == "consumer_chain.foundation_assemble"
    ]
    assembled = [r for r in assemble_events if r["assembled"] is True]
    injected = [r for r in assemble_events if r["assembled"] is False]
    assert len(assembled) == 1
    assert len(injected) == 2  # planner + readiness reuse


def test_readiness_forwards_canonical_state_to_planner(
    telemetry, monkeypatch
) -> None:
    foundation = MagicMock()
    foundation.is_enabled.return_value = True
    foundation.assemble.return_value = _canonical_state()

    seen: dict[str, object] = {}

    def capture_plan(
        user_id,
        today=None,
        *,
        foundation=None,
        canonical_state=None,
    ):
        seen["canonical_state"] = canonical_state
        seen["foundation"] = foundation
        return _daily_plan()

    monkeypatch.setattr(
        PlanningService, "build_daily_study_plan", staticmethod(capture_plan)
    )

    result = ReadinessService.build_readiness_intelligence(
        42,
        foundation=foundation,
        include_planner=True,
    )
    assert result is not None
    assert seen["foundation"] is foundation
    assert seen["canonical_state"] is foundation.assemble.return_value
    assert foundation.assemble.call_count == 1


def test_planner_accepts_canonical_state_kwarg() -> None:
    foundation = MagicMock()
    foundation.is_enabled.return_value = False
    # Disabled foundation → None without DB; kwargs must be accepted.
    result = PlanningService.build_daily_study_plan(
        42, foundation=foundation, canonical_state=_canonical_state()
    )
    assert result is None
    foundation.assemble.assert_not_called()


@pytest.mark.parametrize(
    ("twin", "authority"),
    [
        ("0", "0"),
        ("1", "0"),
        ("1", "1"),
        ("0", "1"),
    ],
)
def test_twin_authority_matrix_insights_fail_open(
    monkeypatch, twin, authority
) -> None:
    monkeypatch.setenv("KWALITEC_DIGITAL_TWIN", twin)
    monkeypatch.setenv("KWALITEC_DIGITAL_TWIN_AUTHORITY", authority)
    if twin != "1":
        assert RecommendationService.build_study_insights(1) is None
    else:
        RecommendationService.build_study_insights(
            1, include_planner=False, include_readiness=False
        )
