"""EP-003.2 Readiness quality contract tests."""

from __future__ import annotations

from unittest.mock import patch

from app.presentation.intelligence_surface.adapter import (
    RuntimeAPresentationAdapter,
)
from app.services.readiness_quality import (
    CONFIDENCE_CANNOT_ESTIMATE,
    CONFIDENCE_HIGH,
    CONFIDENCE_LOW,
    CONFIDENCE_MODERATE,
    apply_readiness_quality_contract,
    apply_readiness_quality_to_assessment,
    has_complete_readiness_explanation_schema,
)
from app.services.readiness_service import ReadinessService


def _legacy_surface(
    *,
    score: float = 62.0,
    coverage: float = 50.0,
    mastery: float = 55.0,
    review: float = 70.0,
    total: int = 20,
    started: int = 8,
) -> dict:
    return {
        "readiness": {
            "score": score,
            "coverage_pct": coverage,
            "avg_mastery": mastery,
            "review_discipline": review,
            "total_topics": total,
            "topics_started": started,
            "topics_mastered": 2,
        },
        "weakest_topics": [
            {"topic_id": 11, "topic_name": "Fractions", "mastery_score": 32.0}
        ],
        "strongest_topics": [
            {"topic_id": 10, "topic_name": "Algebra", "mastery_score": 88.0}
        ],
        "source_authority": "legacy",
        "confidence_level": "",
        "limitations_codes": [],
        "readiness_drivers": [],
        "recommended_next_actions": [],
        "explainability": {},
    }


class TestExplanationSchemaCompleteness:
    def test_schema_fields_attached(self):
        with patch(
            "app.services.readiness_quality._resolve_authorised_today_focus",
            return_value="Geometry proofs",
        ):
            result = apply_readiness_quality_contract(1, _legacy_surface())

        assert has_complete_readiness_explanation_schema(result)
        assert result["judgement"]
        assert result["why_this_estimate"]
        assert result["supporting_evidence"]
        assert result["suggested_next_action"]
        assert result["confidence_level"]
        assert result["review_point"]
        assert result["change_reasoning"]
        assert result["explanation_schema_version"] == "p001.2/v1"
        assert result["explanation_schema_complete"] is True
        assert len(result["readiness_drivers"]) >= 3
        # Score must not be recalculated.
        assert result["readiness"]["score"] == 62.0


class TestConfidenceHandling:
    def test_thin_history_uses_low_confidence(self):
        surface = _legacy_surface(started=1, coverage=5.0, score=12.0)
        with patch(
            "app.services.readiness_quality._resolve_authorised_today_focus",
            return_value=None,
        ):
            result = apply_readiness_quality_contract(1, surface)

        assert result["confidence_level"] == CONFIDENCE_LOW

    def test_dense_supportive_history_can_be_high(self):
        surface = _legacy_surface(
            started=12,
            total=20,
            coverage=60.0,
            mastery=75.0,
            review=80.0,
            score=70.0,
        )
        with patch(
            "app.services.readiness_quality._resolve_authorised_today_focus",
            return_value=None,
        ):
            result = apply_readiness_quality_contract(1, surface)

        assert result["confidence_level"] in {CONFIDENCE_HIGH, CONFIDENCE_MODERATE}

    def test_cold_start_honest_refusal(self):
        surface = _legacy_surface(
            score=0.0,
            coverage=0.0,
            mastery=0.0,
            review=0.0,
            total=20,
            started=0,
        )
        result = apply_readiness_quality_contract(1, surface)
        assert result["honest_refusal"] is True
        assert result["confidence_level"] == CONFIDENCE_CANNOT_ESTIMATE
        assert has_complete_readiness_explanation_schema(result)
        assert result["readiness"]["score"] == 0.0


class TestCalibrationAndDrivers:
    def test_explicit_drivers_from_composite_components(self):
        with patch(
            "app.services.readiness_quality._resolve_authorised_today_focus",
            return_value=None,
        ):
            result = apply_readiness_quality_contract(1, _legacy_surface())

        ids = {d["driver_id"] for d in result["readiness_drivers"]}
        assert "curriculum_coverage" in ids
        assert "knowledge_strength" in ids
        assert "mission_discipline" in ids
        assert all("rationale" in d for d in result["readiness_drivers"])

    def test_preserves_twin_drivers_and_maps_confidence(self):
        surface = _legacy_surface()
        surface["source_authority"] = "readiness_intelligence"
        surface["confidence_level"] = "medium"
        surface["readiness_drivers"] = [
            {
                "driver_id": "curriculum_coverage",
                "label": "Curriculum coverage",
                "influence": "mixed",
                "value": 55.0,
                "source": "canonical.study_state",
                "rationale": "Coverage 55%.",
            }
        ]
        with patch(
            "app.services.readiness_quality._resolve_authorised_today_focus",
            return_value=None,
        ):
            result = apply_readiness_quality_contract(1, surface)

        assert result["confidence_level"] == CONFIDENCE_MODERATE
        assert result["readiness_drivers"][0]["driver_id"] == "curriculum_coverage"

    def test_change_reasoning_with_previous_score(self):
        with patch(
            "app.services.readiness_quality._resolve_authorised_today_focus",
            return_value=None,
        ):
            result = apply_readiness_quality_contract(
                1,
                _legacy_surface(score=62.0),
                previous_score=50.0,
            )

        assert "up about 12 points" in result["change_reasoning"]


class TestEvidenceConsistency:
    def test_supporting_evidence_cites_components(self):
        with patch(
            "app.services.readiness_quality._resolve_authorised_today_focus",
            return_value=None,
        ):
            result = apply_readiness_quality_contract(1, _legacy_surface())

        blob = " ".join(result["supporting_evidence"]).lower()
        assert "syllabus" in blob or "topics started" in blob
        assert "fractions" in blob


class TestNextActionGuidance:
    def test_uses_today_mission_when_available(self):
        with patch(
            "app.services.readiness_quality._resolve_authorised_today_focus",
            return_value="Geometry proofs",
        ):
            result = apply_readiness_quality_contract(1, _legacy_surface())

        assert "Geometry proofs" in result["suggested_next_action"]

    def test_uses_planner_action_when_present(self):
        surface = _legacy_surface()
        surface["recommended_next_actions"] = [
            {"title": "Today's mission — Algebra", "reason": "Planner slot"}
        ]
        with patch(
            "app.services.readiness_quality._resolve_authorised_today_focus",
            return_value="Ignored because planner wins",
        ):
            result = apply_readiness_quality_contract(1, surface)

        assert result["suggested_next_action"] == "Today's mission — Algebra"


class TestAssessmentEnrichment:
    def test_assessment_receives_schema(self):
        assessment = {
            "student_id": "1",
            "readiness_score": 58.5,
            "confidence_level": "medium",
            "strongest_areas": [],
            "weakest_areas": [
                {
                    "topic_id": "11",
                    "topic_name": "Fractions",
                    "mastery_score": 30.0,
                    "reason": "Weak",
                }
            ],
            "readiness_drivers": [
                {
                    "driver_id": "curriculum_coverage",
                    "label": "Curriculum coverage",
                    "influence": "mixed",
                    "value": 40.0,
                    "source": "canonical",
                    "rationale": "Coverage 40%.",
                }
            ],
            "recommended_next_actions": [
                {"title": "Today's mission — Algebra", "reason": "Planner"}
            ],
            "explainability": {"status": "available"},
            "limitations_codes": [],
        }
        with patch(
            "app.services.readiness_quality._resolve_authorised_today_focus",
            return_value=None,
        ):
            result = apply_readiness_quality_to_assessment(1, assessment)

        assert result["readiness_score"] == 58.5
        assert result["explanation_schema_complete"] is True
        assert result["confidence_level"] == CONFIDENCE_MODERATE
        assert result["suggested_next_action"]
        assert result["why_this_estimate"]
        assert result["supporting_evidence"]


class TestPresentationPassThrough:
    def test_schema_complete_surface_uses_service_speech(self):
        with patch(
            "app.services.readiness_quality._resolve_authorised_today_focus",
            return_value=None,
        ):
            surface = apply_readiness_quality_contract(1, _legacy_surface())

        narrative = RuntimeAPresentationAdapter.readiness_narrative(surface)
        assert narrative.can_estimate is True
        assert narrative.percentage == 62.0
        assert narrative.is_estimate is True
        assert surface["confidence_level"] in narrative.evidence_basis
        assert "Suggested focus" in narrative.explanation or surface[
            "suggested_next_action"
        ] in narrative.explanation

    def test_incomplete_legacy_surface_still_uses_eip003(self):
        surface = _legacy_surface()
        narrative = RuntimeAPresentationAdapter.readiness_narrative(surface)
        assert narrative.can_estimate is True
        assert "syllabus coverage" in narrative.evidence_basis.lower()


class TestConstitutionalOwnership:
    def test_quality_module_does_not_call_recommendation_service(self):
        import ast
        from pathlib import Path

        path = Path(__file__).resolve().parents[2] / "app/services/readiness_quality.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imported.add(alias.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imported.add(alias.name.split(".")[0])
        assert "RecommendationService" not in imported
        assert "recommendation_service" not in imported

    def test_get_overall_readiness_unchanged_by_quality_contract(self, ctx):
        """Collector recursion safety: overall readiness remains bare composite."""
        raw = ReadinessService.get_overall_readiness(1)
        assert set(raw.keys()) >= {
            "score",
            "coverage_pct",
            "avg_mastery",
            "review_discipline",
            "total_topics",
            "topics_started",
            "topics_mastered",
        }
        assert "explanation_schema_version" not in raw
        assert "why_this_estimate" not in raw

    def test_dashboard_surface_attaches_schema(self, ctx):
        with (
            patch(
                "app.infrastructure.adapters.consumer_chain.readiness_cutover."
                "is_readiness_intelligence_cutover_eligible",
                return_value=False,
            ),
            patch(
                "app.infrastructure.adapters.consumer_chain.readiness_cutover."
                "is_readiness_cutover_active",
                return_value=False,
            ),
            patch.object(
                ReadinessService,
                "get_overall_readiness",
                return_value={
                    "score": 55.0,
                    "coverage_pct": 40.0,
                    "avg_mastery": 50.0,
                    "review_discipline": 60.0,
                    "total_topics": 10,
                    "topics_started": 4,
                    "topics_mastered": 1,
                },
            ),
            patch.object(ReadinessService, "get_weakest_topics", return_value=[]),
            patch.object(ReadinessService, "get_strongest_topics", return_value=[]),
            patch.object(ReadinessService, "_maybe_readiness_dual_run"),
            patch(
                "app.services.readiness_quality._resolve_authorised_today_focus",
                return_value=None,
            ),
        ):
            surface = ReadinessService.get_dashboard_readiness_surface(9)

        assert has_complete_readiness_explanation_schema(surface)
        assert surface["readiness"]["score"] == 55.0


class TestRegression:
    def test_fail_open_mission_lookup(self):
        with patch(
            "app.services.planning_service.PlanningService.get_dashboard_mission_surface",
            side_effect=RuntimeError("boom"),
        ):
            result = apply_readiness_quality_contract(1, _legacy_surface())
        assert has_complete_readiness_explanation_schema(result)
        assert result["suggested_next_action"]
