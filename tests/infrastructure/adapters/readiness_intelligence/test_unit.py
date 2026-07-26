"""Unit tests — Readiness Intelligence consumer (EP-001.3)."""

from __future__ import annotations

from types import MappingProxyType
from unittest.mock import MagicMock

import pytest

from app.infrastructure.adapters.digital_twin.contracts import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
)
from app.infrastructure.adapters.digital_twin.foundation import (
    FOUNDATION_VERSION,
    CanonicalLearnerState,
)
from app.infrastructure.adapters.readiness_intelligence import (
    READINESS_INTELLIGENCE_VERSION,
    CanonicalReadinessConsumer,
    ReadinessAssessmentAssembler,
)
from app.services.readiness_service import ReadinessService


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
                        "average_accuracy": 85.0,
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
        topic_progress=_block(
            {
                "topics": [
                    {
                        "topic_id": "10",
                        "topic_name": "Algebra",
                        "completed": True,
                        "revision_count": 2,
                    },
                    {
                        "topic_id": "11",
                        "topic_name": "Calculus",
                        "completed": False,
                        "revision_count": 1,
                    },
                    {
                        "topic_id": "12",
                        "topic_name": "Stats",
                        "completed": False,
                        "revision_count": 0,
                    },
                ],
                "topic_count": 3,
                "completed_count": 1,
            }
        ),
        learning_evidence=_block({"attempt_count": 5, "attempt_ids": ["100"]}),
        practice_performance=_block(
            {"attempt_count": 5, "mean_accuracy_pct": 72.0}
        ),
        mock_performance=_block({}, availability=AVAILABILITY_UNAVAILABLE),
        study_behaviour=_block(
            {
                "learning_rhythm": {"label": "steady"},
                "session_habits": {"label": "focused"},
                "persistence": {"label": "persistent"},
            }
        ),
        study_consistency=_block({"label": "consistent"}),
        streaks=_block({"current_streak": 4, "longest_streak": 7}),
        mission_completion=_block(
            {
                "completed_count": 3,
                "missed_count": 1,
                "history_count": 4,
            }
        ),
        facet_labels=MappingProxyType({"consistency": "consistent"}),
        limitations_codes=("mock_evidence_not_distinguished",),
        provenance_refs=("readiness", "topic_progress"),
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
                "reason": "Due for review",
                "priority": "high",
                "expected_benefit": "retention",
            }
        ],
        "revision_priorities": [
            {
                "topic_id": "11",
                "topic_name": "Calculus",
                "mastery_score": 40.0,
                "reason": "Weak completed topic",
                "rank": 1,
            }
        ],
    }


def test_consumer_projects_score_and_areas() -> None:
    inputs = CanonicalReadinessConsumer().project(_canonical_state())
    assert inputs.availability == AVAILABILITY_AVAILABLE
    assert inputs.readiness_score == 58.5
    assert inputs.coverage_pct == 50.0
    assert inputs.current_streak == 4
    assert inputs.consistency_label == "consistent"
    assert len(inputs.topic_areas) == 3
    assert inputs.topic_areas[0].topic_id == "10"


def test_consumer_includes_planner_outputs() -> None:
    inputs = CanonicalReadinessConsumer().project(
        _canonical_state(), daily_plan=_daily_plan()
    )
    assert inputs.planner_available is True
    assert len(inputs.planner_missions) == 1
    assert len(inputs.planner_revision_priorities) == 1


def test_consumer_marks_planner_unavailable_when_absent() -> None:
    inputs = CanonicalReadinessConsumer().project(_canonical_state())
    assert inputs.planner_available is False
    assert "planner_outputs_unavailable" in inputs.limitations_codes


def test_consumer_unavailable_state() -> None:
    state = CanonicalLearnerState(
        student_id="7",
        as_of=None,
        foundation_version=FOUNDATION_VERSION,
        twin_id="",
        study_state=_block({}, availability=AVAILABILITY_UNAVAILABLE),
        topic_mastery=_block({}, availability=AVAILABILITY_UNAVAILABLE),
        topic_progress=_block({}, availability=AVAILABILITY_UNAVAILABLE),
        learning_evidence=_block({}, availability=AVAILABILITY_UNAVAILABLE),
        practice_performance=_block({}, availability=AVAILABILITY_UNAVAILABLE),
        mock_performance=_block({}, availability=AVAILABILITY_UNAVAILABLE),
        study_behaviour=_block({}, availability=AVAILABILITY_UNAVAILABLE),
        study_consistency=_block({}, availability=AVAILABILITY_UNAVAILABLE),
        streaks=_block({}, availability=AVAILABILITY_UNAVAILABLE),
        mission_completion=_block({}, availability=AVAILABILITY_UNAVAILABLE),
        availability=AVAILABILITY_UNAVAILABLE,
        unavailable_reason="foundation_flag_off",
    )
    inputs = CanonicalReadinessConsumer().project(state)
    assert inputs.availability == AVAILABILITY_UNAVAILABLE
    assert inputs.unavailable_reason == "foundation_flag_off"


def test_consumer_deterministic_serialize() -> None:
    consumer = CanonicalReadinessConsumer()
    plan = _daily_plan()
    a = consumer.project(_canonical_state(), daily_plan=plan)
    b = consumer.project(_canonical_state(), daily_plan=plan)
    assert a.serialize() == b.serialize()


def test_assessment_produces_full_intelligence_package() -> None:
    inputs = CanonicalReadinessConsumer().project(
        _canonical_state(), daily_plan=_daily_plan()
    )
    assessment = ReadinessAssessmentAssembler().assemble(inputs)
    payload = assessment.to_dict()
    assert payload["consumer_version"] == READINESS_INTELLIGENCE_VERSION
    assert payload["readiness_score"] == 58.5
    assert payload["confidence_level"] in {
        "very_low",
        "low",
        "medium",
        "high",
    }
    assert payload["confidence_level"] in {"medium", "high"}
    assert payload["strongest_areas"][0]["topic_id"] == "10"
    assert payload["weakest_areas"][0]["topic_id"] == "11"
    driver_ids = {d["driver_id"] for d in payload["readiness_drivers"]}
    assert "curriculum_coverage" in driver_ids
    assert "knowledge_strength" in driver_ids
    assert "mission_discipline" in driver_ids
    assert "study_consistency" in driver_ids
    assert "streaks" in driver_ids
    assert len(payload["recommended_next_actions"]) >= 2
    assert assessment.serialize() == ReadinessAssessmentAssembler().assemble(
        inputs
    ).serialize()


def test_assessment_composes_score_when_overall_missing() -> None:
    base = _canonical_state()
    state = CanonicalLearnerState(
        student_id=base.student_id,
        as_of=base.as_of,
        foundation_version=base.foundation_version,
        twin_id=base.twin_id,
        study_state=_block(
            {
                "lifecycle_stage": "Learning",
                "examination_label": "CS2",
                "exam_countdown_days": 40,
                "readiness_overall": {
                    "coverage_pct": 40.0,
                    "avg_mastery": 50.0,
                    "review_discipline": 60.0,
                },
            }
        ),
        topic_mastery=dict(base.topic_mastery),
        topic_progress=dict(base.topic_progress),
        learning_evidence=dict(base.learning_evidence),
        practice_performance=dict(base.practice_performance),
        mock_performance=dict(base.mock_performance),
        study_behaviour=dict(base.study_behaviour),
        study_consistency=dict(base.study_consistency),
        streaks=dict(base.streaks),
        mission_completion=dict(base.mission_completion),
        facet_labels=dict(base.facet_labels),
        limitations_codes=base.limitations_codes,
        provenance_refs=base.provenance_refs,
        availability=AVAILABILITY_AVAILABLE,
        unavailable_reason="",
    )
    inputs = CanonicalReadinessConsumer().project(state)
    # 40*0.5 + 50*0.3 + 60*0.2 = 20 + 15 + 12 = 47.0
    assert inputs.readiness_score == 47.0


def test_readiness_service_returns_none_when_twin_off(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        ReadinessService,
        "_resolve_twin_foundation",
        staticmethod(lambda: None),
    )
    assert ReadinessService.build_readiness_intelligence(1) is None


def test_readiness_service_builds_assessment_when_twin_on() -> None:
    foundation = MagicMock()
    foundation.is_enabled.return_value = True
    foundation.assemble.return_value = _canonical_state()

    result = ReadinessService.build_readiness_intelligence(
        42,
        foundation=foundation,
        daily_plan=_daily_plan(),
        include_planner=False,
    )
    assert result is not None
    assert result["readiness_score"] == 58.5
    assert result["student_id"] == "42"
    assert result["source_service"] == "readiness_intelligence"
    foundation.assemble.assert_called_once_with("42")
