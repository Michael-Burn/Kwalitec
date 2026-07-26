"""EP-002.8 Runtime A presentation consolidation tests."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from app.presentation.intelligence_surface import RuntimeAPresentationAdapter
from app.presentation.intelligence_surface.adapter import (
    SOURCE_AUTHORITY_DAILY_STUDY_PLAN,
    SOURCE_AUTHORITY_LEGACY,
    SOURCE_AUTHORITY_READINESS_INTELLIGENCE,
    SOURCE_AUTHORITY_STUDY_INSIGHTS,
)
from app.services.educational_explainability_service import (
    MissionNarrative,
    ReadinessNarrative,
)
from app.services.product_communication_service import ProductCommunicationService


def _legacy_readiness_surface() -> dict:
    return {
        "source_authority": SOURCE_AUTHORITY_LEGACY,
        "readiness": {
            "score": 60.0,
            "coverage_pct": 50.0,
            "avg_mastery": 70.0,
            "review_discipline": 80.0,
            "total_topics": 10,
            "topics_started": 5,
            "topics_mastered": 2,
        },
        "weakest_topics": [
            {
                "topic_id": "t1",
                "topic_name": "Fractions",
                "mastery_score": 30.0,
                "stage": "Needs Review",
                "revision_count": 1,
            }
        ],
        "strongest_topics": [
            {
                "topic_id": "t2",
                "topic_name": "Algebra",
                "mastery_score": 90.0,
                "stage": "Mastered",
                "revision_count": 0,
            }
        ],
        "readiness_drivers": [],
        "recommended_next_actions": [],
        "confidence_level": "",
    }


def _twin_readiness_surface() -> dict:
    return {
        "source_authority": SOURCE_AUTHORITY_READINESS_INTELLIGENCE,
        "readiness": {
            "score": 72.0,
            "coverage_pct": 55.0,
            "avg_mastery": 68.0,
            "review_discipline": 75.0,
            "total_topics": 10,
            "topics_started": 6,
            "topics_mastered": 3,
            "source_authority": SOURCE_AUTHORITY_READINESS_INTELLIGENCE,
            "confidence_level": "medium",
        },
        "weakest_topics": [
            {
                "topic_id": "w1",
                "topic_name": "Geometry",
                "mastery_score": 25.0,
                "stage": "",
                "revision_count": 0,
                "reason": "Weak area",
            }
        ],
        "strongest_topics": [
            {
                "topic_id": "s1",
                "topic_name": "Numbers",
                "mastery_score": 88.0,
                "stage": "",
                "revision_count": 0,
                "reason": "Strong area",
            }
        ],
        "readiness_drivers": [
            {"driver_id": "curriculum_coverage", "value": 55.0},
            {"driver_id": "knowledge_strength", "value": 68.0},
        ],
        "recommended_next_actions": [
            {"title": "Practise Geometry proofs"},
        ],
        "confidence_level": "medium",
        "explainability": {"source": "canonical_learner_state", "status": "available"},
    }


class TestTopicRows:
    def test_legacy_enriches_stage_labels(self):
        weak, strong = RuntimeAPresentationAdapter.topic_rows(
            _legacy_readiness_surface()
        )
        assert weak[0]["stage_label"] == "Needs more practice"
        assert strong[0]["stage_label"] == "Strong estimated knowledge"

    def test_twin_pass_through_without_enrich(self):
        surface = _twin_readiness_surface()
        weak, strong = RuntimeAPresentationAdapter.topic_rows(surface)
        assert weak[0]["topic_id"] == "w1"
        assert "stage_label" not in weak[0]
        assert strong[0]["reason"] == "Strong area"


class TestReadinessNarrative:
    def test_legacy_uses_eip003(self):
        narrative = RuntimeAPresentationAdapter.readiness_narrative(
            _legacy_readiness_surface()
        )
        assert isinstance(narrative, ReadinessNarrative)
        assert narrative.can_estimate is True
        assert narrative.percentage == 60.0
        assert narrative.label == ProductCommunicationService.ESTIMATED_READINESS_LABEL
        assert "syllabus coverage" in narrative.evidence_basis.lower()

    def test_twin_maps_drivers_and_confidence(self):
        narrative = RuntimeAPresentationAdapter.readiness_narrative(
            _twin_readiness_surface()
        )
        assert isinstance(narrative, ReadinessNarrative)
        assert narrative.percentage == 72.0
        assert narrative.can_estimate is True
        assert narrative.is_estimate is True
        assert "curriculum coverage" in narrative.evidence_basis.lower()
        assert "Confidence level: medium" in narrative.evidence_basis
        assert "Practise Geometry proofs" in narrative.explanation
        # Must not invent a second evaluation — score is projected.
        assert "readiness intelligence" in narrative.explanation.lower()

    def test_twin_missing_score_is_honest(self):
        surface = _twin_readiness_surface()
        surface["readiness"] = {"score": None, "total_topics": 10}
        narrative = RuntimeAPresentationAdapter.readiness_narrative(surface)
        assert narrative.can_estimate is False
        assert narrative.percentage is None
        unavailable = ProductCommunicationService.READINESS_UNAVAILABLE
        assert unavailable in narrative.explanation

    def test_empty_surface_falls_back_to_legacy_unavailable(self):
        narrative = RuntimeAPresentationAdapter.readiness_narrative(None)
        assert narrative.can_estimate is False


class TestRecommendations:
    def test_study_insights_pass_through(self):
        rows = [
            {
                "title": "Focus Geometry",
                "reason": "Twin insight",
                "source_authority": SOURCE_AUTHORITY_STUDY_INSIGHTS,
                "observed_facts": ["Observed A"],
                "next_action": "Practise",
            }
        ]
        today, enriched = RuntimeAPresentationAdapter.enrich_recommendations_if_needed(
            rows,
            today_recommendation=rows[0],
        )
        assert today is rows[0]
        assert enriched[0]["observed_facts"] == ["Observed A"]
        assert enriched[0]["next_action"] == "Practise"

    def test_legacy_enriches(self):
        rows = [
            {
                "title": "Review Fractions",
                "reason": "Weak topic",
                "category": "Review",
                "expected_benefit": "Strengthen basics",
                "source_authority": SOURCE_AUTHORITY_LEGACY,
            }
        ]
        today, enriched = RuntimeAPresentationAdapter.enrich_recommendations_if_needed(
            rows,
            today_recommendation=rows[0],
        )
        assert today is not None
        assert "observed_facts" in today
        assert "next_action" in today
        assert enriched[0]["observed_facts"]


class TestMissionNarrative:
    def test_legacy_builds_eip003_mission(self):
        mission = SimpleNamespace(title="Study Algebra", status="Pending")
        narrative = RuntimeAPresentationAdapter.mission_narrative(
            today_mission=mission,
            mission_surface={"source_authority": SOURCE_AUTHORITY_LEGACY},
            exam_name="GCSE Maths",
            completed_topics=2,
            total_topics=10,
            syllabus_coverage_pct=20.0,
            is_revision=False,
        )
        assert isinstance(narrative, MissionNarrative)
        assert narrative.next_action
        assert narrative.reason_for_selection

    def test_twin_builds_mission_narrative_from_slots(self):
        mission = SimpleNamespace(title="Geometry focus", status="Pending")
        surface = {
            "source_authority": SOURCE_AUTHORITY_DAILY_STUDY_PLAN,
            "today_missions_slots": [
                {
                    "topic_id": "geo-1",
                    "topic_name": "Circles",
                    "reason": "Weakest planner focus today",
                }
            ],
        }
        narrative = RuntimeAPresentationAdapter.mission_narrative(
            today_mission=mission,
            mission_surface=surface,
        )
        assert isinstance(narrative, MissionNarrative)
        assert narrative.next_action == "Geometry focus"
        assert narrative.reason_for_selection == "Weakest planner focus today"
        assert narrative.educational_purpose == "Weakest planner focus today"
        assert any("Circles" in fact for fact in narrative.observed_facts)
        assert narrative.estimates == ()

    def test_twin_fallback_copy_when_reason_missing(self):
        mission = SimpleNamespace(title="Today", status="Pending")
        narrative = RuntimeAPresentationAdapter.mission_narrative(
            today_mission=mission,
            mission_surface={
                "source_authority": SOURCE_AUTHORITY_DAILY_STUDY_PLAN,
                "today_missions_slots": [{"topic_id": "x"}],
            },
        )
        assert "Projected from Twin daily study plan" in narrative.reason_for_selection

    def test_none_mission_returns_none(self):
        assert (
            RuntimeAPresentationAdapter.mission_narrative(
                today_mission=None,
                mission_surface={"source_authority": SOURCE_AUTHORITY_LEGACY},
            )
            is None
        )


class TestNoBusinessLogicMigration:
    def test_twin_readiness_does_not_call_eip003_composite(self):
        with patch(
            "app.presentation.intelligence_surface.adapter."
            "EducationalExplainabilityService.explain_composite_readiness"
        ) as mock_explain:
            RuntimeAPresentationAdapter.readiness_narrative(_twin_readiness_surface())
            mock_explain.assert_not_called()

    def test_twin_mission_does_not_call_eip003_mission(self):
        mission = SimpleNamespace(title="T", status="Pending")
        with patch(
            "app.presentation.intelligence_surface.adapter."
            "EducationalExplainabilityService.build_mission_narrative"
        ) as mock_build:
            RuntimeAPresentationAdapter.mission_narrative(
                today_mission=mission,
                mission_surface={
                    "source_authority": SOURCE_AUTHORITY_DAILY_STUDY_PLAN,
                    "today_missions_slots": [{"reason": "Because"}],
                },
            )
            mock_build.assert_not_called()

    def test_study_insights_does_not_call_enrich(self):
        rows = [{"source_authority": SOURCE_AUTHORITY_STUDY_INSIGHTS, "title": "A"}]
        with patch(
            "app.presentation.intelligence_surface.adapter."
            "EducationalExplainabilityService.enrich_recommendations"
        ) as mock_enrich:
            RuntimeAPresentationAdapter.enrich_recommendations_if_needed(rows)
            mock_enrich.assert_not_called()


class TestFeatureFlagProductionOffBehaviour:
    """Presentation adapter is flag-agnostic; authority comes from surface DTO."""

    def test_legacy_authority_identical_outside_cutover(self):
        surface = _legacy_readiness_surface()
        a = RuntimeAPresentationAdapter.readiness_narrative(surface)
        b = RuntimeAPresentationAdapter.readiness_narrative(
            {**surface, "source_authority": "legacy"}
        )
        assert a.percentage == b.percentage
        assert a.explanation == b.explanation


class TestAccessibilityRegression:
    def test_explainability_macro_contract_fields_present_on_mission(self):
        mission = SimpleNamespace(title="Topic", status="Pending")
        narrative = RuntimeAPresentationAdapter.mission_narrative(
            today_mission=mission,
            mission_surface={
                "source_authority": SOURCE_AUTHORITY_DAILY_STUDY_PLAN,
                "today_missions_slots": [
                    {"topic_name": "A", "reason": "R"},
                ],
            },
        )
        # Template accesses these attributes for the explainability macro.
        assert hasattr(narrative, "observed_facts")
        assert hasattr(narrative, "estimates")
        assert hasattr(narrative, "next_action")
        assert hasattr(narrative, "reason_for_selection")

    def test_readiness_narrative_template_contract(self):
        narrative = RuntimeAPresentationAdapter.readiness_narrative(
            _twin_readiness_surface()
        )
        for attr in (
            "label",
            "percentage",
            "explanation",
            "evidence_basis",
            "can_estimate",
            "is_estimate",
        ):
            assert hasattr(narrative, attr)


@pytest.mark.usefixtures("ctx")
class TestRouteWiringSmoke:
    def test_adapter_importable_from_presentation_package(self):
        from app.presentation.intelligence_surface import (
            RuntimeAPresentationAdapter as Imported,
        )

        assert Imported is RuntimeAPresentationAdapter

    def test_dashboard_module_imports_adapter(self):
        import app.dashboard.routes as dashboard_routes

        assert hasattr(dashboard_routes, "RuntimeAPresentationAdapter")

    def test_analytics_module_imports_adapter(self):
        import app.analytics.routes as analytics_routes

        assert hasattr(analytics_routes, "RuntimeAPresentationAdapter")

    def test_mission_module_imports_adapter(self):
        import app.mission.routes as mission_routes

        assert hasattr(mission_routes, "RuntimeAPresentationAdapter")
