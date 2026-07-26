"""Unit tests — Adaptive Study Planner consumer (EP-001.2)."""

from __future__ import annotations

from datetime import date
from types import MappingProxyType
from unittest.mock import MagicMock

import pytest

from app.infrastructure.adapters.adaptive_study_planner import (
    PLANNER_CONSUMER_VERSION,
    CanonicalPlannerConsumer,
    DailyStudyPlanAssembler,
)
from app.infrastructure.adapters.digital_twin.contracts import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
)
from app.infrastructure.adapters.digital_twin.foundation import (
    FOUNDATION_VERSION,
    CanonicalLearnerState,
)


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
                        "mastery_score": 72.0,
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
        topic_progress=_block(
            {
                "topics": [
                    {
                        "topic_id": "10",
                        "topic_name": "Algebra",
                        "current_stage": "Mastered",
                        "completed": True,
                        "revision_count": 2,
                        "next_review_date": "2026-07-20",
                    },
                    {
                        "topic_id": "11",
                        "topic_name": "Calculus",
                        "current_stage": "Learning",
                        "completed": False,
                        "revision_count": 0,
                        "next_review_date": None,
                    },
                    {
                        "topic_id": "12",
                        "topic_name": "Stats",
                        "current_stage": "Learning",
                        "completed": False,
                        "revision_count": 0,
                        "next_review_date": "2026-07-26",
                    },
                ],
                "topic_count": 3,
                "completed_count": 1,
            }
        ),
        learning_evidence=_block({"attempt_count": 1, "attempt_ids": ["100"]}),
        practice_performance=_block(
            {"attempt_count": 1, "mean_accuracy_pct": 80.0}
        ),
        mock_performance=_block({}, availability=AVAILABILITY_UNAVAILABLE),
        study_behaviour=_block(
            {
                "learning_rhythm": _block({"label": "steady", "note": ""}),
                "session_habits": _block({"label": "focused", "note": ""}),
                "persistence": _block({"label": "resilient", "note": ""}),
            }
        ),
        study_consistency=_block({"label": "consistent", "note": ""}),
        streaks=_block({"current_streak": 4, "longest_streak": 7}),
        mission_completion=_block(
            {"completed_count": 3, "missed_count": 1, "history_count": 4}
        ),
        facet_labels=MappingProxyType({"consistency": "consistent"}),
        limitations_codes=("mock_evidence_not_distinguished",),
        provenance_refs=("topic_progress",),
        availability=AVAILABILITY_AVAILABLE,
    )


class TestCanonicalPlannerConsumer:
    def test_project_pass_through_and_determinism(self) -> None:
        consumer = CanonicalPlannerConsumer()
        state = _canonical_state()
        a = consumer.project(state)
        b = consumer.project(state)
        assert a.serialize() == b.serialize()
        assert a.availability == AVAILABILITY_AVAILABLE
        assert a.current_streak == 4
        assert a.preferred_session_minutes == 50
        assert a.consistency_label == "consistent"
        assert a.behaviour_labels["learning_rhythm"] == "steady"
        assert len(a.topics) == 3
        # Incomplete topics ordered before completed.
        assert a.topics[0].completed is False
        assert a.topics[-1].completed is True

    def test_unavailable_state(self) -> None:
        consumer = CanonicalPlannerConsumer()
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
            availability=AVAILABILITY_UNAVAILABLE,
            unavailable_reason="foundation_flag_off",
        )
        inputs = consumer.project(state)
        assert inputs.availability == AVAILABILITY_UNAVAILABLE
        assert inputs.topics == ()


class TestDailyStudyPlanAssembler:
    def test_assembles_missions_revision_ordering_workload(self) -> None:
        inputs = CanonicalPlannerConsumer().project(_canonical_state())
        plan = DailyStudyPlanAssembler().assemble(
            inputs,
            plan_date=date(2026, 7, 26),
            available_study_minutes=90,
        )
        assert plan.availability == AVAILABILITY_AVAILABLE
        assert plan.consumer_version == PLANNER_CONSUMER_VERSION
        slots = {m.slot for m in plan.today_missions}
        assert "review" in slots  # topic 12 due today / topic 10 overdue
        # Canonical fixture has missed_count=1 → recovery mode (no progression).
        assert "recovery" in slots
        assert "progression" not in slots
        assert plan.explainability.get("recovery_mode") is True
        assert plan.revision_priorities
        assert plan.revision_priorities[0].topic_id == "10"
        assert len(plan.topic_ordering) == 3
        # Preferred session minutes caps workload; recovery lightens further.
        assert plan.recommended_workload.available_study_minutes == 90
        assert plan.recommended_workload.recommended_minutes == 47
        assert all(m.allocated_minutes is not None for m in plan.today_missions)
        assert plan.serialize() == DailyStudyPlanAssembler().assemble(
            inputs,
            plan_date=date(2026, 7, 26),
            available_study_minutes=90,
        ).serialize()

    def test_progression_when_no_missed_sessions(self) -> None:
        import dataclasses

        inputs = CanonicalPlannerConsumer().project(_canonical_state())
        inputs = dataclasses.replace(inputs, mission_missed_count=0)
        plan = DailyStudyPlanAssembler().assemble(
            inputs,
            plan_date=date(2026, 7, 26),
            available_study_minutes=90,
        )
        slots = {m.slot for m in plan.today_missions}
        assert "review" in slots
        assert "weak" in slots
        assert "progression" in slots
        assert plan.explainability.get("recovery_mode") is False
        assert plan.recommended_workload.recommended_minutes == 50

    def test_light_load_on_irregular_consistency(self) -> None:
        import dataclasses

        inputs = CanonicalPlannerConsumer().project(_canonical_state())
        inputs = dataclasses.replace(
            inputs,
            consistency_label="irregular",
            preferred_session_minutes=None,
            mission_missed_count=0,
        )
        plan = DailyStudyPlanAssembler().assemble(
            inputs,
            plan_date=date(2026, 7, 26),
            available_study_minutes=100,
        )
        assert plan.recommended_workload.recommended_minutes == 90


class TestPlanningServiceBuildDailyStudyPlan:
    def test_returns_none_when_twin_off(self, monkeypatch: pytest.MonkeyPatch) -> None:
        from app.services.planning_service import PlanningService

        monkeypatch.setattr(
            PlanningService,
            "_resolve_twin_foundation",
            staticmethod(lambda: None),
        )
        assert PlanningService.build_daily_study_plan(1) is None

    def test_builds_from_injected_foundation(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        from app.services.planning_service import PlanningService

        plan = MagicMock()
        plan.id = 7
        plan.weekday_study_minutes = 60
        plan.weekend_study_minutes = 90
        monkeypatch.setattr(
            "app.services.study_plan_service.StudyPlanService.get_user_active_plan",
            staticmethod(lambda _uid: plan),
        )

        foundation = MagicMock()
        foundation.is_enabled.return_value = True
        foundation.assemble.return_value = _canonical_state()

        result = PlanningService.build_daily_study_plan(
            42, today=date(2026, 7, 26), foundation=foundation
        )
        assert result is not None
        assert result["availability"] == AVAILABILITY_AVAILABLE
        assert result["study_plan_id"] == 7
        assert result["today_missions"]
        assert result["recommended_workload"]["available_study_minutes"] == 90
