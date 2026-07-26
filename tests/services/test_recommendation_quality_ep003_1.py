"""EP-003.1 Recommendation quality contract tests."""

from __future__ import annotations

from unittest.mock import patch

from app.services.recommendation_quality import (
    CATEGORY_MOCK_EXAM,
    CATEGORY_NEW_TOPIC,
    CATEGORY_REST,
    CATEGORY_WEAK_TOPIC,
    CONFIDENCE_CANNOT_ESTIMATE,
    LADDER_BLOCKING_DEFICIT,
    LADDER_NEW_LEARNING,
    LADDER_SAFETY,
    LADDER_WEAK_TOPIC,
    PRIORITY_CRITICAL,
    PRIORITY_HIGH,
    PRIORITY_MEDIUM,
    apply_quality_contract,
    has_complete_explanation_schema,
)
from app.services.recommendation_service import RecommendationService


def _row(
    *,
    title: str,
    category: str,
    priority: str,
    reason: str = "Because evidence supports this step.",
    benefit: str = "Improve exam preparation.",
) -> dict:
    return {
        "title": title,
        "category": category,
        "priority": priority,
        "reason": reason,
        "expected_benefit": benefit,
        "generated_at": "2026-07-26T00:00:00",
    }


class TestDecisionLadderPrioritisation:
    def test_safety_rest_outranks_weak_topic_and_new_learning(self):
        rows = [
            _row(
                title="Study Algebra",
                category=CATEGORY_NEW_TOPIC,
                priority=PRIORITY_HIGH,
            ),
            _row(
                title="Practise Fractions",
                category=CATEGORY_WEAK_TOPIC,
                priority=PRIORITY_HIGH,
            ),
            _row(
                title="Take a rest day — study pattern notice",
                category=CATEGORY_REST,
                priority=PRIORITY_CRITICAL,
                reason="Heavy consecutive study days detected.",
            ),
        ]
        with (
            patch(
                "app.services.recommendation_quality._resolve_authorised_today_focus",
                return_value="Geometry proofs",
            ),
            patch(
                "app.services.recommendation_quality._estimate_evidence_density",
                return_value="dense",
            ),
        ):
            result = apply_quality_contract(1, rows, limit=3)

        assert result[0]["category"] == CATEGORY_REST
        assert result[0]["decision_ladder_rank"] == LADDER_SAFETY
        assert result[1]["decision_ladder_rank"] == LADDER_WEAK_TOPIC
        assert result[2]["decision_ladder_rank"] == LADDER_NEW_LEARNING

    def test_critical_weak_topic_maps_to_blocking_deficit(self):
        rows = [
            _row(
                title="Practise lower Estimated Knowledge: Fractions",
                category=CATEGORY_WEAK_TOPIC,
                priority=PRIORITY_CRITICAL,
            ),
            _row(
                title="Continue with Algebra",
                category=CATEGORY_NEW_TOPIC,
                priority=PRIORITY_MEDIUM,
            ),
        ]
        with (
            patch(
                "app.services.recommendation_quality._resolve_authorised_today_focus",
                return_value=None,
            ),
            patch(
                "app.services.recommendation_quality._estimate_evidence_density",
                return_value="moderate",
            ),
        ):
            result = apply_quality_contract(1, rows, limit=2)

        assert result[0]["decision_ladder_rank"] == LADDER_BLOCKING_DEFICIT
        assert result[1]["decision_ladder_rank"] == LADDER_NEW_LEARNING


class TestExplanationSchemaCompleteness:
    def test_schema_fields_attached(self):
        rows = [
            _row(
                title="Review overdue topics",
                category="Review",
                priority=PRIORITY_HIGH,
            )
        ]
        with (
            patch(
                "app.services.recommendation_quality._resolve_authorised_today_focus",
                return_value=None,
            ),
            patch(
                "app.services.recommendation_quality._estimate_evidence_density",
                return_value="moderate",
            ),
        ):
            result = apply_quality_contract(1, rows, limit=1)

        assert len(result) == 1
        assert has_complete_explanation_schema(result[0])
        assert result[0]["why_recommended"]
        assert result[0]["supporting_evidence"]
        assert result[0]["suggested_next_action"]
        assert result[0]["confidence_level"]
        assert result[0]["review_point"]
        assert result[0]["explanation_schema_version"] == "p001.2/v1"


class TestConfidenceHandling:
    def test_thin_evidence_uses_low_confidence(self):
        rows = [
            _row(
                title="Continue with Algebra",
                category=CATEGORY_NEW_TOPIC,
                priority=PRIORITY_HIGH,
            )
        ]
        with (
            patch(
                "app.services.recommendation_quality._resolve_authorised_today_focus",
                return_value=None,
            ),
            patch(
                "app.services.recommendation_quality._estimate_evidence_density",
                return_value="thin",
            ),
        ):
            result = apply_quality_contract(1, rows, limit=1)

        assert "Low confidence" in result[0]["confidence_level"]

    def test_thin_evidence_filters_mock_exam_and_may_refuse(self):
        rows = [
            _row(
                title="Take a mock exam this week",
                category=CATEGORY_MOCK_EXAM,
                priority=PRIORITY_MEDIUM,
            )
        ]
        with (
            patch(
                "app.services.recommendation_quality._resolve_authorised_today_focus",
                return_value=None,
            ),
            patch(
                "app.services.recommendation_quality._estimate_evidence_density",
                return_value="thin",
            ),
        ):
            result = apply_quality_contract(1, rows, limit=1)

        assert result[0]["honest_refusal"] is True
        assert result[0]["confidence_level"] == CONFIDENCE_CANNOT_ESTIMATE


class TestPlanCoherence:
    def test_weak_topic_labelled_advisory_when_mission_active(self):
        rows = [
            _row(
                title="Practise Fractions",
                category=CATEGORY_WEAK_TOPIC,
                priority=PRIORITY_HIGH,
            )
        ]
        with (
            patch(
                "app.services.recommendation_quality._resolve_authorised_today_focus",
                return_value="Study Algebra",
            ),
            patch(
                "app.services.recommendation_quality._estimate_evidence_density",
                return_value="dense",
            ),
        ):
            result = apply_quality_contract(1, rows, limit=1)

        assert result[0]["plan_coherence"] == "advisory"
        assert "does not replace Today’s Mission" in result[0]["reason"]
        assert "Study Algebra" in result[0]["plan_coherence_label"]


class TestHonestRefusal:
    def test_empty_candidates_emit_honest_refusal(self):
        with (
            patch(
                "app.services.recommendation_quality._resolve_authorised_today_focus",
                return_value=None,
            ),
            patch(
                "app.services.recommendation_quality._estimate_evidence_density",
                return_value="thin",
            ),
        ):
            result = apply_quality_contract(1, [], limit=1)

        assert len(result) == 1
        assert result[0]["honest_refusal"] is True
        assert result[0]["title"] == "No recommendation yet"
        assert has_complete_explanation_schema(result[0])


class TestConstitutionalOwnership:
    def test_quality_module_does_not_call_planning_generate_mission(self):
        rows = [
            _row(
                title="Continue with Algebra",
                category=CATEGORY_NEW_TOPIC,
                priority=PRIORITY_HIGH,
            )
        ]
        with (
            patch(
                "app.services.planning_service.PlanningService.get_dashboard_mission_surface",
                return_value={"today_mission": None},
            ) as mission_surface,
            patch(
                "app.services.planning_service.PlanningService.generate_today_mission"
            ) as generate_mission,
            patch(
                "app.services.readiness_service.ReadinessService.get_overall_readiness",
                return_value={
                    "total_topics": 10,
                    "topics_started": 4,
                    "coverage_pct": 40.0,
                },
            ),
            patch(
                "app.services.readiness_service.ReadinessService.get_weakest_topics"
            ) as weak,
            patch(
                "app.services.readiness_service.ReadinessService.get_curriculum_coverage"
            ) as coverage,
        ):
            apply_quality_contract(7, rows, limit=1)
            mission_surface.assert_called()
            generate_mission.assert_not_called()
            weak.assert_not_called()
            coverage.assert_not_called()

    def test_recommendation_service_remains_export_boundary(self, db, user):
        recs = RecommendationService.generate_recommendations(user.id, limit=3)
        assert isinstance(recs, list)
        if recs:
            assert has_complete_explanation_schema(recs[0])


class TestPresentationPassThrough:
    def test_adapter_skips_enrich_when_schema_complete(self):
        from app.presentation.intelligence_surface import RuntimeAPresentationAdapter

        with (
            patch(
                "app.services.recommendation_quality._resolve_authorised_today_focus",
                return_value=None,
            ),
            patch(
                "app.services.recommendation_quality._estimate_evidence_density",
                return_value="moderate",
            ),
        ):
            rows = apply_quality_contract(
                1,
                [
                    _row(
                        title="Continue with Algebra",
                        category=CATEGORY_NEW_TOPIC,
                        priority=PRIORITY_HIGH,
                    )
                ],
                limit=1,
            )

        with patch(
            "app.presentation.intelligence_surface.adapter."
            "EducationalExplainabilityService.enrich_recommendations"
        ) as enrich:
            today, all_rows = (
                RuntimeAPresentationAdapter.enrich_recommendations_if_needed(
                    rows,
                    today_recommendation=rows[0],
                )
            )
            enrich.assert_not_called()
            assert today == rows[0]
            assert all_rows == rows
