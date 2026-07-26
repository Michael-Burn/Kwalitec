"""EP-003.3 Planning quality contract tests."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import patch

from app.presentation.intelligence_surface.adapter import (
    RuntimeAPresentationAdapter,
)
from app.services.planning_quality import (
    COHERENCE_ALIGNED,
    COHERENCE_RECOVERY,
    CONFIDENCE_CANNOT_ESTIMATE,
    CONFIDENCE_LOW,
    CONFIDENCE_MODERATE,
    apply_planning_quality_contract,
    apply_planning_quality_to_daily_plan,
    has_complete_plan_explanation_schema,
)


def _slot(
    *,
    slot: str = "weak",
    topic: str = "Calculus",
    reason: str = "Weak topic (mastery 40%)",
    minutes: int = 25,
) -> dict:
    return {
        "slot": slot,
        "topic_id": "11",
        "topic_name": topic,
        "reason": reason,
        "priority": "high",
        "expected_benefit": "Improve weakest area.",
        "allocated_minutes": minutes,
    }


def _legacy_surface(*, mission_title: str = "Study Calculus") -> dict:
    return {
        "today_mission": SimpleNamespace(title=mission_title, status="active"),
        "source_authority": "legacy",
        "daily_plan": None,
        "today_missions_slots": [],
        "recommended_workload": {},
        "topic_ordering": [],
        "revision_priorities": [],
        "limitations_codes": [],
        "explainability": {},
        "plan_date": None,
        "availability": None,
    }


def _twin_surface(
    *,
    slots: list[dict] | None = None,
    recovery: bool = False,
    recommended_minutes: int = 50,
) -> dict:
    slots = slots or [
        _slot(slot="review", topic="Stats", reason="Due for review"),
        _slot(slot="weak", topic="Calculus"),
        _slot(slot="progression", topic="Geometry", reason="Next incomplete"),
    ]
    if recovery:
        slots = [
            _slot(slot="review", topic="Stats", reason="Due for review"),
            _slot(
                slot="recovery",
                topic="Calculus",
                reason="Recovery focus after 2 missed session(s)",
            ),
        ]
    plan = {
        "availability": "available",
        "plan_date": "2026-07-26",
        "today_missions": slots,
        "recommended_workload": {
            "available_study_minutes": 90,
            "recommended_minutes": recommended_minutes,
            "rationale": "Plan capacity for today is 90 minutes.",
        },
        "revision_priorities": [],
        "topic_ordering": [],
        "explainability": {
            "source": "canonical_learner_state",
            "evidence_attempt_count": 8,
            "recovery_mode": recovery,
            "mission_missed_count": 2 if recovery else 0,
            "plan_coherence": "recovery" if recovery else "aligned",
            "recommendation_aware_order": True,
        },
    }
    return {
        "today_mission": SimpleNamespace(title="Stats", status="active"),
        "source_authority": "daily_study_plan",
        "daily_plan": plan,
        "today_missions_slots": slots,
        "recommended_workload": dict(plan["recommended_workload"]),
        "topic_ordering": [],
        "revision_priorities": [],
        "limitations_codes": [],
        "explainability": dict(plan["explainability"]),
        "plan_date": "2026-07-26",
        "availability": "available",
    }


class TestExplanationSchemaCompleteness:
    def test_schema_fields_attached(self):
        with (
            patch(
                "app.services.planning_quality._resolve_overall_readiness",
                return_value={
                    "score": 58.0,
                    "coverage_pct": 40.0,
                    "avg_mastery": 50.0,
                    "review_discipline": 60.0,
                    "total_topics": 10,
                    "topics_started": 5,
                    "topics_mastered": 1,
                },
            ),
            patch(
                "app.services.planning_quality._resolve_recommendation_titles",
                return_value=("Review Stats",),
            ),
        ):
            result = apply_planning_quality_contract(1, _twin_surface())

        assert has_complete_plan_explanation_schema(result)
        assert result["judgement"]
        assert result["why_this_plan"]
        assert result["supporting_evidence"]
        assert result["suggested_next_action"]
        assert result["confidence_level"]
        assert result["review_point"]
        assert result["change_reasoning"]
        assert result["plan_drivers"]
        assert result["explanation_schema_version"] == "p001.2/v1"
        assert result["explanation_schema_complete"] is True
        assert result["plan_coherence"]
        assert result["readiness_alignment"]
        assert result["recommendation_alignment"]


class TestWorkloadBalancing:
    def test_readiness_informed_lighter_load(self):
        surface = _twin_surface(recommended_minutes=50)
        with (
            patch(
                "app.services.planning_quality._resolve_overall_readiness",
                return_value={
                    "score": 30.0,
                    "total_topics": 10,
                    "topics_started": 3,
                },
            ),
            patch(
                "app.services.planning_quality._resolve_recommendation_titles",
                return_value=(),
            ),
        ):
            result = apply_planning_quality_contract(1, surface)

        workload = result["recommended_workload"]
        assert workload["recommended_minutes"] == 45
        assert workload.get("readiness_informed") is True
        assert "Readiness about 30%" in workload["rationale"]


class TestRecommendationIntegration:
    def test_topic_overlap_marks_aligned(self):
        with (
            patch(
                "app.services.planning_quality._resolve_overall_readiness",
                return_value={"score": 60.0, "topics_started": 4},
            ),
            patch(
                "app.services.planning_quality._resolve_recommendation_titles",
                return_value=("Practice Calculus today",),
            ),
        ):
            result = apply_planning_quality_contract(1, _twin_surface())

        assert result["recommendation_alignment"] == COHERENCE_ALIGNED
        evidence = result["supporting_evidence"]
        assert any("Calculus" in e or "tip" in e.lower() for e in evidence)

    def test_ladder_order_without_tips_still_labels(self):
        with (
            patch(
                "app.services.planning_quality._resolve_overall_readiness",
                return_value={},
            ),
            patch(
                "app.services.planning_quality._resolve_recommendation_titles",
                return_value=(),
            ),
        ):
            result = apply_planning_quality_contract(1, _twin_surface())

        assert result["recommendation_alignment"] in {
            COHERENCE_ALIGNED,
            "advisory",
        }


class TestReadinessIntegration:
    def test_low_readiness_with_weak_slots_aligned(self):
        with (
            patch(
                "app.services.planning_quality._resolve_overall_readiness",
                return_value={
                    "score": 35.0,
                    "topics_started": 2,
                    "total_topics": 10,
                },
            ),
            patch(
                "app.services.planning_quality._resolve_recommendation_titles",
                return_value=(),
            ),
        ):
            result = apply_planning_quality_contract(1, _twin_surface())

        assert result["readiness_alignment"] == COHERENCE_ALIGNED
        assert any("readiness" in e.lower() for e in result["supporting_evidence"])


class TestAdaptiveRecovery:
    def test_recovery_surface_change_reasoning(self):
        with (
            patch(
                "app.services.planning_quality._resolve_overall_readiness",
                return_value={"score": 40.0, "topics_started": 3},
            ),
            patch(
                "app.services.planning_quality._resolve_recommendation_titles",
                return_value=(),
            ),
        ):
            result = apply_planning_quality_contract(
                1, _twin_surface(recovery=True)
            )

        assert result["plan_coherence"] == COHERENCE_RECOVERY
        assert "missed session" in result["change_reasoning"].lower()
        assert result["confidence_level"] == CONFIDENCE_MODERATE


class TestHonestRefusal:
    def test_empty_surface_refuses_honestly(self):
        result = apply_planning_quality_contract(
            1,
            {
                "today_mission": None,
                "source_authority": "legacy",
                "daily_plan": None,
                "today_missions_slots": [],
                "recommended_workload": {},
                "explainability": {},
            },
        )
        assert result["honest_refusal"] is True
        assert result["confidence_level"] == CONFIDENCE_CANNOT_ESTIMATE
        assert has_complete_plan_explanation_schema(result)


class TestDailyPlanPayload:
    def test_apply_to_daily_plan_preserves_slots(self):
        payload = {
            "availability": "available",
            "today_missions": [_slot()],
            "recommended_workload": {
                "available_study_minutes": 60,
                "recommended_minutes": 50,
                "rationale": "Capacity 60.",
            },
            "explainability": {"evidence_attempt_count": 2},
            "revision_priorities": [],
            "topic_ordering": [],
        }
        with (
            patch(
                "app.services.planning_quality._resolve_overall_readiness",
                return_value={"score": 50.0, "topics_started": 2},
            ),
            patch(
                "app.services.planning_quality._resolve_recommendation_titles",
                return_value=(),
            ),
        ):
            result = apply_planning_quality_to_daily_plan(1, payload)

        assert has_complete_plan_explanation_schema(result)
        assert result["today_missions"][0]["topic_name"] == "Calculus"
        assert result["confidence_level"] in {
            CONFIDENCE_LOW,
            CONFIDENCE_MODERATE,
        }


class TestPresentationPassThrough:
    def test_schema_complete_surface_uses_service_speech(self):
        with (
            patch(
                "app.services.planning_quality._resolve_overall_readiness",
                return_value={"score": 55.0, "topics_started": 4},
            ),
            patch(
                "app.services.planning_quality._resolve_recommendation_titles",
                return_value=(),
            ),
        ):
            surface = apply_planning_quality_contract(1, _twin_surface())

        mission = SimpleNamespace(title="Stats", status="active")
        narrative = RuntimeAPresentationAdapter.mission_narrative(
            today_mission=mission,
            mission_surface=surface,
        )
        assert narrative is not None
        assert surface["why_this_plan"] in narrative.reason_for_selection
        assert surface["suggested_next_action"] == narrative.next_action

    def test_incomplete_legacy_surface_still_uses_eip003(self):
        surface = _legacy_surface()
        mission = surface["today_mission"]
        narrative = RuntimeAPresentationAdapter.mission_narrative(
            today_mission=mission,
            mission_surface=surface,
            exam_name="CS2",
            completed_topics=1,
            total_topics=10,
            syllabus_coverage_pct=10.0,
        )
        assert narrative is not None
        assert narrative.topic_title == "Study Calculus"


class TestConstitutionalOwnership:
    def test_quality_does_not_call_generate_today_mission(self):
        with (
            patch(
                "app.services.planning_quality._resolve_overall_readiness",
                return_value={"score": 50.0, "topics_started": 2},
            ),
            patch(
                "app.services.planning_quality._resolve_recommendation_titles",
                return_value=(),
            ),
            patch(
                "app.services.planning_service.PlanningService.generate_today_mission",
                side_effect=AssertionError("must not generate missions"),
            ),
            patch(
                "app.services.readiness_service.ReadinessService.build_readiness_intelligence",
                side_effect=AssertionError("must not rebuild readiness"),
            ),
        ):
            result = apply_planning_quality_contract(1, _twin_surface())
        assert has_complete_plan_explanation_schema(result)

    def test_uses_bare_overall_readiness_not_dashboard(self):
        """Collector / recursion safety: only get_overall_readiness."""
        with (
            patch(
                "app.services.readiness_service.ReadinessService.get_overall_readiness",
                return_value={
                    "score": 52.0,
                    "topics_started": 3,
                    "total_topics": 10,
                },
            ) as overall,
            patch(
                "app.services.readiness_service.ReadinessService.get_dashboard_readiness_surface",
                side_effect=AssertionError("dashboard readiness forbidden"),
            ),
            patch(
                "app.services.planning_quality._resolve_recommendation_titles",
                return_value=(),
            ),
        ):
            result = apply_planning_quality_contract(1, _twin_surface())
        overall.assert_called()
        assert has_complete_plan_explanation_schema(result)

    def test_fail_open_sibling_lookups(self):
        with (
            patch(
                "app.services.planning_quality._resolve_overall_readiness",
                side_effect=RuntimeError("boom"),
            ),
            patch(
                "app.services.planning_quality._resolve_recommendation_titles",
                side_effect=RuntimeError("boom"),
            ),
        ):
            # Direct contract still works when helpers raise before catch —
            # exercise the public helpers' fail-open via real call paths.
            pass

        with (
            patch(
                "app.services.readiness_service.ReadinessService.get_overall_readiness",
                side_effect=RuntimeError("boom"),
            ),
            patch(
                "app.services.recommendation_service.RecommendationService.generate_recommendations",
                side_effect=RuntimeError("boom"),
            ),
        ):
            result = apply_planning_quality_contract(1, _twin_surface())
        assert has_complete_plan_explanation_schema(result)
        assert result["suggested_next_action"]


class TestRegression:
    def test_legacy_mission_surface_gets_schema(self):
        with (
            patch(
                "app.services.planning_quality._resolve_overall_readiness",
                return_value={"score": 60.0, "topics_started": 5},
            ),
            patch(
                "app.services.planning_quality._resolve_recommendation_titles",
                return_value=(),
            ),
        ):
            result = apply_planning_quality_contract(1, _legacy_surface())

        assert has_complete_plan_explanation_schema(result)
        assert "Calculus" in result["judgement"] or "Calculus" in result[
            "suggested_next_action"
        ]
