"""EP-004.3 Adaptive planning personalisation tests."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import patch

from app.presentation.intelligence_surface.adapter import (
    RuntimeAPresentationAdapter,
)
from app.services.planning_personalisation import (
    ATTR_CONSISTENCY_TREND,
    ATTR_PLANNING_COMPLETION_RATE,
    ATTR_PREFERRED_SESSION_DURATION,
    ATTR_PREFERRED_STUDY_WINDOWS,
    ATTR_RECOVERY_EFFECTIVENESS,
    ATTR_REVISION_ADHERENCE,
    MIN_CONFIDENCE,
    apply_profile_personalisation,
)
from app.services.planning_quality import (
    apply_planning_quality_contract,
    has_complete_plan_explanation_schema,
)


def _slot(
    *,
    slot: str = "weak",
    topic: str = "Calculus",
    topic_id: str = "11",
    reason: str = "Weak topic (mastery 40%)",
    minutes: int = 25,
) -> dict:
    return {
        "slot": slot,
        "topic_id": topic_id,
        "topic_name": topic,
        "reason": reason,
        "priority": "high",
        "expected_benefit": "Improve weakest area.",
        "allocated_minutes": minutes,
    }


def _attr(
    *,
    status: str = "available",
    kind: str = "derived_indicator",
    claim_boundary: str = "behaviour_summary",
    value: dict | None = None,
    confidence: float = 0.8,
    sample_size: int = 8,
    explanation: str = "Observed behavioural summary.",
) -> dict:
    return {
        "status": status,
        "kind": kind,
        "claim_boundary": claim_boundary,
        "value": value or {},
        "confidence": confidence,
        "sample_size": sample_size,
        "explanation": explanation,
        "limitations": [],
    }


def _profile(attributes: dict) -> dict:
    return {
        "profile_id": "plp-plan-001",
        "student_id": "1",
        "authority": "personal_learning_profile",
        "contract_version": "ep004.1.1",
        "attributes": attributes,
        "limitations": [],
        "evidence_event_count": 12,
    }


def _surface(
    *,
    slots: list[dict] | None = None,
    recommended_minutes: int = 60,
    available: int = 90,
    revision_priorities: list[dict] | None = None,
) -> dict:
    slots = slots or [
        _slot(slot="review", topic="Stats", topic_id="1", reason="Due for review"),
        _slot(slot="weak", topic="Calculus", topic_id="11"),
        _slot(
            slot="progression",
            topic="Geometry",
            topic_id="21",
            reason="Next incomplete",
            minutes=20,
        ),
    ]
    plan = {
        "availability": "available",
        "plan_date": "2026-07-26",
        "today_missions": slots,
        "recommended_workload": {
            "available_study_minutes": available,
            "recommended_minutes": recommended_minutes,
            "rationale": f"Plan capacity for today is {available} minutes.",
        },
        "revision_priorities": revision_priorities or [],
        "topic_ordering": [],
        "explainability": {
            "source": "canonical_learner_state",
            "evidence_attempt_count": 8,
            "recovery_mode": False,
            "mission_missed_count": 0,
        },
    }
    return {
        "today_mission": SimpleNamespace(title="Stats", status="active"),
        "source_authority": "daily_study_plan",
        "daily_plan": plan,
        "today_missions_slots": list(slots),
        "recommended_workload": dict(plan["recommended_workload"]),
        "topic_ordering": [],
        "revision_priorities": list(revision_priorities or []),
        "limitations_codes": [],
        "explainability": dict(plan["explainability"]),
        "plan_date": "2026-07-26",
        "availability": "available",
        "judgement": "Today's plan: Stats",
        "why_this_plan": "Priorities: review, weak, progression.",
        "supporting_evidence": ["Stats: Due for review"],
        "observed_facts": ["Stats: Due for review"],
        "confidence_level": "Moderate confidence",
        "expected_benefit": "Balanced day.",
        "suggested_next_action": "Start with Stats (review)",
        "next_action": "Start with Stats (review)",
        "review_point": "Refresh after completing today's mission.",
        "plan_drivers": [{"driver_id": "slot_review", "label": "Stats"}],
        "change_reasoning": "Includes due review.",
        "explanation_summary": "Today's plan: Stats.",
        "explanation_schema_version": "p001.2/v1",
        "explanation_level": "level_2",
        "explanation_schema_complete": True,
        "honest_refusal": False,
    }


class TestProfileDrivenPlanning:
    def test_session_duration_aligns_recommended_minutes(self):
        surface = _surface(recommended_minutes=60)
        profile = _profile(
            {
                ATTR_PREFERRED_SESSION_DURATION: _attr(
                    kind="observed_fact",
                    claim_boundary="declared_preference",
                    confidence=1.0,
                    sample_size=1,
                    value={"declared_session_minutes": 40},
                )
            }
        )
        result = apply_profile_personalisation(surface, profile)
        assert result["personalisation_applied"] is True
        assert result["recommended_workload"]["recommended_minutes"] == 40
        assert any(
            f["effect"] == "session_duration_alignment"
            for f in result["personalisation_factors"]
        )
        assert "session_sizing_guidance" in result

    def test_low_completion_rate_lightens_pacing(self):
        surface = _surface(recommended_minutes=50)
        profile = _profile(
            {
                ATTR_PLANNING_COMPLETION_RATE: _attr(
                    value={
                        "completion_rate": 0.25,
                        "completed_count": 2,
                        "missed_count": 6,
                    }
                )
            }
        )
        result = apply_profile_personalisation(surface, profile)
        assert result["recommended_workload"]["recommended_minutes"] == 45
        assert any(
            f["effect"] == "pace_reduce_when_completion_low"
            for f in result["personalisation_factors"]
        )

    def test_recovery_follow_through_emphasises_repair_minutes(self):
        surface = _surface()
        before_weak = surface["today_missions_slots"][1]["allocated_minutes"]
        before_prog = surface["today_missions_slots"][2]["allocated_minutes"]
        profile = _profile(
            {
                ATTR_RECOVERY_EFFECTIVENESS: _attr(
                    value={
                        "follow_through_rate": 0.8,
                        "recovery_count": 8,
                        "followed_by_completion_count": 6,
                    }
                )
            }
        )
        result = apply_profile_personalisation(surface, profile)
        slots = result["today_missions_slots"]
        assert [s["slot"] for s in slots] == ["review", "weak", "progression"]
        assert slots[1]["allocated_minutes"] > before_weak
        assert slots[2]["allocated_minutes"] < before_prog
        assert any(
            f["effect"] == "recovery_emphasise_follow_through"
            for f in result["personalisation_factors"]
        )

    def test_revision_adherence_protects_review_timing(self):
        surface = _surface()
        profile = _profile(
            {
                ATTR_REVISION_ADHERENCE: _attr(
                    value={
                        "adherence_rate": 0.9,
                        "adhered_count": 9,
                        "deferred_count": 1,
                    }
                )
            }
        )
        result = apply_profile_personalisation(surface, profile)
        assert any(
            f["effect"] == "revision_boost_adherence"
            for f in result["personalisation_factors"]
        )
        assert "review" in result["suggested_next_action"].lower() or "Stats" in (
            result["suggested_next_action"] or ""
        )

    def test_equivalent_repair_topic_when_follow_through_low(self):
        priorities = [
            {
                "topic_id": "11",
                "topic_name": "Calculus",
                "mastery_score": 40.0,
                "reason": "Revision priority",
                "rank": 1,
            },
            {
                "topic_id": "12",
                "topic_name": "Algebra",
                "mastery_score": 45.0,
                "reason": "Revision priority",
                "rank": 2,
            },
        ]
        surface = _surface(revision_priorities=priorities)
        profile = _profile(
            {
                ATTR_RECOVERY_EFFECTIVENESS: _attr(
                    value={
                        "follow_through_rate": 0.15,
                        "recovery_count": 8,
                        "followed_by_completion_count": 1,
                    }
                )
            }
        )
        result = apply_profile_personalisation(surface, profile)
        weak = next(s for s in result["today_missions_slots"] if s["slot"] == "weak")
        assert weak["topic_id"] == "12"
        assert weak["topic_name"] == "Algebra"
        assert [s["slot"] for s in result["today_missions_slots"]] == [
            "review",
            "weak",
            "progression",
        ]
        assert any(
            f["effect"] == "equivalent_repair_topic_preference"
            for f in result["personalisation_factors"]
        )


class TestUnsupportedAndConfidence:
    def test_unsupported_attributes_ignored(self):
        surface = _surface(recommended_minutes=50)
        baseline = apply_profile_personalisation(surface, None)
        profile = _profile(
            {
                ATTR_PREFERRED_STUDY_WINDOWS: _attr(
                    status="unsupported",
                    kind="unsupported",
                    claim_boundary="unsupported_assumption",
                    confidence=0.0,
                    sample_size=0,
                )
            }
        )
        result = apply_profile_personalisation(surface, profile)
        assert result["personalisation_applied"] is False
        assert result["recommended_workload"]["recommended_minutes"] == baseline[
            "recommended_workload"
        ]["recommended_minutes"]

    def test_low_confidence_ignored(self):
        surface = _surface(recommended_minutes=50)
        profile = _profile(
            {
                ATTR_PLANNING_COMPLETION_RATE: _attr(
                    confidence=MIN_CONFIDENCE - 0.1,
                    sample_size=2,
                    value={"completion_rate": 0.1},
                )
            }
        )
        result = apply_profile_personalisation(surface, profile)
        assert result["personalisation_applied"] is False
        assert result["recommended_workload"]["recommended_minutes"] == 50

    def test_declining_consistency_lightens_load(self):
        surface = _surface(recommended_minutes=50)
        profile = _profile(
            {
                ATTR_CONSISTENCY_TREND: _attr(
                    value={"direction": "declining", "streak_delta": -2}
                )
            }
        )
        result = apply_profile_personalisation(surface, profile)
        assert result["recommended_workload"]["recommended_minutes"] == 45
        assert any(
            f["effect"] == "pace_reduce_when_consistency_declining"
            for f in result["personalisation_factors"]
        )


class TestExplanationAndOwnership:
    def test_explanation_completeness_when_personalised(self):
        surface = _surface(recommended_minutes=50)
        profile = _profile(
            {
                ATTR_PLANNING_COMPLETION_RATE: _attr(
                    value={"completion_rate": 0.2}
                )
            }
        )
        result = apply_profile_personalisation(surface, profile)
        assert has_complete_plan_explanation_schema(result)
        assert result["personalisation_applied"] is True
        assert result["personalisation_factors"]
        assert any(
            "Personalisation evidence" in str(line)
            for line in result["supporting_evidence"]
        )
        assert (
            "Personalised using your observed study habits"
            in result["why_this_plan"]
        )
        assert result["personalisation_profile_id"] == "plp-plan-001"

    def test_educational_slot_order_preserved(self):
        surface = _surface()
        profile = _profile(
            {
                ATTR_REVISION_ADHERENCE: _attr(
                    value={
                        "adherence_rate": 0.95,
                        "adhered_count": 10,
                        "deferred_count": 0,
                    }
                ),
                ATTR_RECOVERY_EFFECTIVENESS: _attr(
                    value={
                        "follow_through_rate": 0.9,
                        "recovery_count": 9,
                        "followed_by_completion_count": 8,
                    }
                ),
            }
        )
        result = apply_profile_personalisation(surface, profile)
        order = [s["slot"] for s in result["today_missions_slots"]]
        assert order == ["review", "weak", "progression"]

    def test_presentation_pass_through_unchanged(self):
        surface = _surface(recommended_minutes=50)
        with patch(
            "app.services.readiness_service.ReadinessService.get_overall_readiness",
            return_value={"score": 55.0, "topics_started": 4},
        ), patch(
            "app.services.recommendation_service.RecommendationService.generate_recommendations",
            return_value=[],
        ):
            enriched = apply_planning_quality_contract(
                1,
                surface,
                profile_view=_profile(
                    {
                        ATTR_PLANNING_COMPLETION_RATE: _attr(
                            value={"completion_rate": 0.2}
                        )
                    }
                ),
            )
        assert enriched["personalisation_applied"] is True
        narrative = RuntimeAPresentationAdapter.mission_narrative(
            today_mission=surface["today_mission"],
            mission_surface=enriched,
        )
        assert narrative is not None
        assert "Personalised using your observed study habits" in (
            narrative.educational_purpose or ""
        )
        # Presentation must not strip personalisation trail on the surface.
        assert enriched["personalisation_factors"]

    def test_missing_profile_fail_open(self):
        surface = _surface(recommended_minutes=50)
        result = apply_profile_personalisation(surface, None)
        assert result["personalisation_applied"] is False
        assert result["recommended_workload"]["recommended_minutes"] == 50
        assert has_complete_plan_explanation_schema(result) or result.get(
            "explanation_schema_complete"
        )


class TestConstitutionalOwnership:
    def test_quality_contract_wires_profile_without_delegating(self):
        surface = _surface(recommended_minutes=50)
        with patch(
            "app.services.readiness_service.ReadinessService.get_overall_readiness",
            return_value={"score": 60.0, "topics_started": 5},
        ), patch(
            "app.services.recommendation_service.RecommendationService.generate_recommendations",
            return_value=[],
        ):
            result = apply_planning_quality_contract(
                42,
                surface,
                profile_view=_profile(
                    {
                        ATTR_PREFERRED_SESSION_DURATION: _attr(
                            kind="observed_fact",
                            confidence=1.0,
                            sample_size=1,
                            value={"declared_session_minutes": 35},
                        )
                    }
                ),
            )
        assert result["personalisation_applied"] is True
        assert result["recommended_workload"]["recommended_minutes"] == 35
        # Educational priorities remain review → weak → progression.
        assert [s["slot"] for s in result["today_missions_slots"]] == [
            "review",
            "weak",
            "progression",
        ]
        assert has_complete_plan_explanation_schema(result)
