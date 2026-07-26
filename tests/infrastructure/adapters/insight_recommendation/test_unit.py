"""Unit tests — Insight & Recommendation Layer consumer (EP-001.4)."""

from __future__ import annotations

from types import MappingProxyType
from unittest.mock import MagicMock

from app.infrastructure.adapters.digital_twin.contracts import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
)
from app.infrastructure.adapters.digital_twin.foundation import (
    FOUNDATION_VERSION,
    CanonicalLearnerState,
)
from app.infrastructure.adapters.insight_recommendation import (
    INSIGHT_LAYER_VERSION,
    CanonicalInsightConsumer,
    StudyInsightAssembler,
)
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
                    },
                    {
                        "topic_id": "11",
                        "topic_name": "Calculus",
                        "mastery_score": 40.0,
                    },
                ],
                "mastered_topic_ids": ["10"],
                "mastered_topic_count": 1,
            }
        ),
        topic_progress=_block({"topics": [], "topic_count": 2, "completed_count": 1}),
        learning_evidence=_block({"attempt_count": 5, "attempt_ids": ["100"]}),
        practice_performance=_block(
            {"attempt_count": 5, "mean_accuracy_pct": 72.0}
        ),
        mock_performance=_block({}, availability=AVAILABILITY_UNAVAILABLE),
        study_behaviour=_block({"learning_rhythm": {"label": "steady"}}),
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
        "recommended_workload": {
            "available_study_minutes": 90,
            "recommended_minutes": 60,
            "rationale": "Prefer a focused hour given consistent study habits.",
            "authority": "runtime_a",
        },
    }


def _readiness_intelligence() -> dict:
    return {
        "availability": AVAILABILITY_AVAILABLE,
        "readiness_score": 58.5,
        "confidence_level": "medium",
        "strongest_areas": [
            {
                "topic_id": "10",
                "topic_name": "Algebra",
                "mastery_score": 82.0,
                "reason": "Highest Estimated Knowledge among observed topics.",
            }
        ],
        "weakest_areas": [
            {
                "topic_id": "11",
                "topic_name": "Calculus",
                "mastery_score": 40.0,
                "reason": "Lowest Estimated Knowledge among observed topics.",
            }
        ],
        "readiness_drivers": [
            {
                "driver_id": "curriculum_coverage",
                "label": "Curriculum coverage",
                "influence": "mixed",
                "value": 50.0,
                "source": "canonical",
                "rationale": "Coverage 50.0% of syllabus leaves started.",
            },
            {
                "driver_id": "mastery",
                "label": "Estimated Knowledge",
                "influence": "mixed",
                "value": 65.0,
                "source": "canonical",
                "rationale": "Average Estimated Knowledge 65.0%.",
            },
        ],
        "recommended_next_actions": [
            {
                "action_id": "mission-review",
                "title": "Review Stats",
                "reason": "Due for review",
                "priority": "high",
                "topic_id": "12",
                "source": "adaptive_study_planner",
            }
        ],
    }


def test_consumer_projects_cls_and_upstream_packages() -> None:
    inputs = CanonicalInsightConsumer().project(
        _canonical_state(),
        daily_plan=_daily_plan(),
        readiness_intelligence=_readiness_intelligence(),
    )
    assert inputs.availability == AVAILABILITY_AVAILABLE
    assert inputs.current_streak == 4
    assert inputs.planner_available is True
    assert inputs.readiness_available is True
    assert inputs.readiness_score == 58.5
    assert len(inputs.planner_missions) == 1
    assert len(inputs.strongest_areas) == 1


def test_consumer_marks_missing_packages() -> None:
    inputs = CanonicalInsightConsumer().project(_canonical_state())
    assert inputs.planner_available is False
    assert inputs.readiness_available is False
    assert "planner_outputs_unavailable" in inputs.limitations_codes
    assert "readiness_intelligence_unavailable" in inputs.limitations_codes
    assert inputs.readiness_score == 58.5  # CLS pass-through only


def test_consumer_unavailable_state() -> None:
    state = CanonicalLearnerState(
        student_id="42",
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
        facet_labels=MappingProxyType({}),
        limitations_codes=(),
        provenance_refs=(),
        availability=AVAILABILITY_UNAVAILABLE,
        unavailable_reason="canonical_learner_state_unavailable",
    )
    inputs = CanonicalInsightConsumer().project(state)
    assert inputs.availability == AVAILABILITY_UNAVAILABLE


def test_assembler_composes_all_guidance_fields() -> None:
    inputs = CanonicalInsightConsumer().project(
        _canonical_state(),
        daily_plan=_daily_plan(),
        readiness_intelligence=_readiness_intelligence(),
    )
    guidance = StudyInsightAssembler().assemble(inputs)
    assert guidance.availability == AVAILABILITY_AVAILABLE
    assert guidance.consumer_version == INSIGHT_LAYER_VERSION
    assert guidance.todays_key_focus is not None
    assert "Stats" in guidance.todays_key_focus.message
    assert guidance.strongest_area is not None
    assert "Algebra" in guidance.strongest_area.message
    assert guidance.greatest_risk is not None
    assert "Calculus" in guidance.greatest_risk.message
    assert guidance.recommended_next_action is not None
    assert "Review Stats" in guidance.recommended_next_action.message
    assert guidance.workload_explanation is not None
    assert "60" in guidance.workload_explanation.message
    assert guidance.readiness_explanation is not None
    assert "58%" in guidance.readiness_explanation.message
    assert guidance.motivational_progress_summary is not None
    assert "4-day" in guidance.motivational_progress_summary.message
    assert guidance.explainability["calculates_intelligence"] is False


def test_assembler_focus_falls_back_to_revision() -> None:
    plan = _daily_plan()
    plan["today_missions"] = []
    inputs = CanonicalInsightConsumer().project(
        _canonical_state(),
        daily_plan=plan,
        readiness_intelligence=_readiness_intelligence(),
    )
    guidance = StudyInsightAssembler().assemble(inputs)
    assert guidance.todays_key_focus is not None
    assert "Calculus" in guidance.todays_key_focus.message
    assert guidance.todays_key_focus.source.endswith("revision_priorities")


def test_assembler_does_not_invent_when_upstream_empty() -> None:
    inputs = CanonicalInsightConsumer().project(_canonical_state())
    guidance = StudyInsightAssembler().assemble(inputs)
    assert guidance.strongest_area is None
    assert guidance.greatest_risk is None
    assert guidance.workload_explanation is None
    assert "strongest_area_unavailable" in guidance.limitations_codes
    assert guidance.readiness_explanation is not None  # CLS score still explained
    assert guidance.motivational_progress_summary is not None


def test_guidance_serialize_deterministic() -> None:
    inputs = CanonicalInsightConsumer().project(
        _canonical_state(),
        daily_plan=_daily_plan(),
        readiness_intelligence=_readiness_intelligence(),
    )
    guidance = StudyInsightAssembler().assemble(inputs)
    assert guidance.serialize() == guidance.serialize()
    payload = guidance.to_dict()
    assert payload["source_service"] == "insight_recommendation"
    assert payload["todays_key_focus"]["field_id"] == "todays_key_focus"


def test_recommendation_service_returns_none_when_twin_off(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        RecommendationService,
        "_resolve_twin_foundation",
        staticmethod(lambda: None),
    )
    assert RecommendationService.build_study_insights(42) is None


def test_recommendation_service_assembles_when_twin_on(monkeypatch) -> None:
    foundation = MagicMock()
    foundation.is_enabled.return_value = True
    foundation.assemble.return_value = _canonical_state()
    monkeypatch.setattr(
        RecommendationService,
        "_resolve_twin_foundation",
        staticmethod(lambda: foundation),
    )
    result = RecommendationService.build_study_insights(
        42,
        foundation=foundation,
        daily_plan=_daily_plan(),
        readiness_intelligence=_readiness_intelligence(),
    )
    assert result is not None
    assert result["availability"] == AVAILABILITY_AVAILABLE
    assert result["todays_key_focus"]["topic_id"] == "12"
    assert result["explainability"]["calculates_intelligence"] is False
    foundation.assemble.assert_called_once_with("42")
