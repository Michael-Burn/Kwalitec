"""Dashboard Educational Intelligence integration tests (Capability 3.5.1 / 3.5.2).

Verifies Stage A cutover and Internal Alpha daily-use glue: feature flags,
legacy fallback, recommendation card rendering, start-session CTA, invisible
legacy dual path when EI is live, and no educational reasoning in the Flask route.
"""

from __future__ import annotations

import ast
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch

from app.application.config import EducationalIntelligenceFeatureFlags
from app.application.dashboard import (
    DashboardViewModel,
    FeatureVisibilityViewModel,
    NavigationAffordancesViewModel,
    RecommendationCardViewModel,
)
from app.application.twin_repository import reset_shared_twin_repository
from app.domain.twin import DigitalTwin, GoalState, IdentityState
from app.extensions import db
from app.services.study_plan_service import StudyPlanService

ROUTES_PATH = (
    Path(__file__).resolve().parents[2] / "app" / "dashboard" / "routes.py"
)

FLAGS_OFF = EducationalIntelligenceFeatureFlags()
FLAGS_ON = EducationalIntelligenceFeatureFlags(
    ENABLE_EDUCATIONAL_ORCHESTRATOR=True,
    ENABLE_EI_RECOMMENDATIONS=True,
)


def _twin_for(user_id: int) -> DigitalTwin:
    return DigitalTwin.create(
        IdentityState.create(
            student_id=str(user_id),
            curriculum_id="1",
            current_exam="CM1",
            target_sitting=date(2027, 4, 1),
        ),
        goals=GoalState.create(
            target_pass_probability=0.8,
            target_completion_date=date(2027, 4, 1),
            planned_study_hours_per_week=10.0,
        ),
    )


def _ei_view_model() -> DashboardViewModel:
    return DashboardViewModel(
        recommendation_card=RecommendationCardViewModel(
            title="Study",
            subtitle="topic-a · deepen",
            primary_action="Start study",
            estimated_duration=None,
            reason_summary="coverage_gap",
            warning=None,
            show_explanation=False,
            show_start_button=True,
        ),
        mission_card=None,
        readiness_summary=None,
        progress_summary=None,
        warnings=(),
        empty_states=(),
        navigation=NavigationAffordancesViewModel(
            can_start_recommendation=True,
            can_open_mission=False,
            can_view_explanation=False,
            can_view_readiness=False,
            can_view_progress=False,
        ),
        feature_visibility=FeatureVisibilityViewModel(
            recommendations=True,
            missions=False,
            explainability=False,
            progress=False,
        ),
    )


def _patch_flags(flags: EducationalIntelligenceFeatureFlags):
    return patch("app.dashboard.routes.resolve_feature_flags", return_value=flags)


class TestDashboardFeatureFlagOff:
    def test_dashboard_renders_without_ei_card(self, logged_in_client) -> None:
        with _patch_flags(FLAGS_OFF):
            response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
        assert b'data-ei-recommendation-card="1"' not in response.data

    def test_flag_off_does_not_call_composer(self, logged_in_client) -> None:
        with (
            _patch_flags(FLAGS_OFF),
            patch(
                "app.dashboard.routes._compose_educational_dashboard"
            ) as compose_mock,
        ):
            response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
        compose_mock.assert_not_called()


class TestDashboardFeatureFlagOn:
    def test_missing_curriculum_falls_back(
        self, logged_in_client, study_plan, user
    ) -> None:
        study_plan.curriculum_id = None
        db.session.commit()

        with (
            _patch_flags(FLAGS_ON),
            patch(
                "app.dashboard.routes.build_twin_provider",
                return_value=__import__(
                    "app.application.twin", fromlist=["TwinProvider"]
                ).TwinProvider(
                    source=type(
                        "S",
                        (),
                        {
                            "load": staticmethod(
                                lambda student_id, *, context=None: _twin_for(user.id)
                            )
                        },
                    )()
                ),
            ),
        ):
            response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
        assert b'data-ei-recommendation-card="1"' not in response.data

    def test_recommendation_card_rendered_when_composer_succeeds(
        self, logged_in_client, study_plan, curriculum
    ) -> None:
        cur, _ = curriculum
        study_plan.curriculum_id = cur.id
        db.session.commit()

        with (
            _patch_flags(FLAGS_ON),
            patch(
                "app.dashboard.routes._compose_educational_dashboard",
                return_value=_ei_view_model(),
            ),
        ):
            response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
        assert b'data-ei-recommendation-card="1"' in response.data
        assert b"Today's Recommendation" in response.data
        assert b"Start study" in response.data
        assert b"coverage_gap" in response.data
        assert b'href="/missions/"' in response.data

    def test_legacy_recommendations_hidden_when_ei_card_live(
        self, logged_in_client, study_plan, curriculum
    ) -> None:
        cur, _ = curriculum
        study_plan.curriculum_id = cur.id
        db.session.commit()

        with (
            _patch_flags(FLAGS_ON),
            patch(
                "app.dashboard.routes._compose_educational_dashboard",
                return_value=_ei_view_model(),
            ),
            patch(
                "app.dashboard.routes.RecommendationService.generate_recommendations",
                return_value=[
                    {
                        "title": "Legacy Rec",
                        "priority": "High",
                        "category": "Review",
                        "reason": "Because",
                        "expected_benefit": "Progress",
                    }
                ],
            ) as legacy_mock,
        ):
            response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
        assert b'data-ei-recommendation-card="1"' in response.data
        assert b"Legacy Rec" not in response.data
        legacy_mock.assert_not_called()

    def test_legacy_recommendations_still_available_on_fallback(
        self, logged_in_client, study_plan, curriculum
    ) -> None:
        cur, _ = curriculum
        study_plan.curriculum_id = cur.id
        db.session.commit()

        with (
            _patch_flags(FLAGS_ON),
            patch(
                "app.dashboard.routes._compose_educational_dashboard",
                return_value=None,
            ),
            patch(
                "app.dashboard.routes.RecommendationService.generate_recommendations",
                return_value=[
                    {
                        "title": "Legacy Rec",
                        "priority": "High",
                        "category": "Review",
                        "reason": "Because",
                        "expected_benefit": "Progress",
                    }
                ],
            ),
            patch(
                "app.dashboard.routes.RecommendationService.generate_today_recommendation",
                return_value={
                    "title": "Legacy Rec",
                    "priority": "High",
                    "category": "Review",
                    "reason": "Because",
                    "expected_benefit": "Progress",
                },
            ),
        ):
            response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
        assert b"Legacy Rec" in response.data
        assert b'data-ei-recommendation-card="1"' not in response.data

    def test_dashboard_still_renders_on_composer_exception(
        self, logged_in_client
    ) -> None:
        with (
            _patch_flags(FLAGS_ON),
            patch(
                "app.dashboard.routes._compose_educational_dashboard",
                side_effect=RuntimeError("boom"),
            ),
        ):
            response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200


class TestInternalAlphaDailyPath:
    def test_alpha_env_renders_ei_card_with_real_composition(
        self, logged_in_client, user, monkeypatch
    ) -> None:
        """Internal Alpha daily path: Study Plan → Calibration → EI card.

        After durable Twin persistence, TwinProvider no longer fabricates a
        cold-start Twin on the read path. The real journey births a Twin via
        Student Calibration (beginner skip here), then Dashboard retrieves it.
        """
        reset_shared_twin_repository()
        monkeypatch.setenv("KWALITEC_EI_INTERNAL_ALPHA", "1")

        plan = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=90,
            current_stage="I haven't started",
            study_preference="Mixed",
            target_grade="Pass",
            preferred_session_minutes=60,
            curriculum_version="2026",
        )
        assert plan.curriculum_id is not None

        # Real Alpha journey: explicit beginner skip births empty-history Twin.
        cal = logged_in_client.post(
            f"/calibration/after-plan/{plan.id}",
            data={"skip_beginner": "I'm starting from scratch — skip detail"},
            follow_redirects=False,
        )
        assert cal.status_code == 302
        assert "/dashboard" in cal.headers["Location"]

        response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
        assert b'data-ei-recommendation-card="1"' in response.data
        assert b"Today's Recommendation" in response.data
        assert b'href="/missions/"' in response.data
        # Unfinished EI widgets stay hidden.
        assert b"data-ei-mission-card" not in response.data
        assert b"data-ei-progress" not in response.data
        # Legacy dual path stays invisible while EI card is live.
        assert b"All Recommendations" not in response.data

    def test_alpha_off_keeps_legacy_default(
        self, logged_in_client, study_plan, curriculum, monkeypatch
    ) -> None:
        cur, _ = curriculum
        study_plan.curriculum_id = cur.id
        db.session.commit()

        monkeypatch.delenv("KWALITEC_EI_INTERNAL_ALPHA", raising=False)
        response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
        assert b'data-ei-recommendation-card="1"' not in response.data


class TestDashboardRouteIntegrity:
    def test_no_educational_domain_reasoning_in_route(self) -> None:
        source = ROUTES_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)
        forbidden_modules = {
            "app.domain.decision",
            "app.domain.readiness",
            "app.domain.recommendation",
            "app.domain.mission",
            "app.domain.twin",
        }
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                assert node.module not in forbidden_modules
                assert not any(
                    node.module.startswith(f"{mod}.") for mod in forbidden_modules
                )

    def test_route_does_not_call_decision_or_readiness_engines(self) -> None:
        source = ROUTES_PATH.read_text(encoding="utf-8")
        assert "DecisionEngine" not in source
        assert "ReadinessAggregation" not in source
        assert "RecommendationEngine" not in source
        assert "MissionIntelligence" not in source
        assert "EducationalDashboardComposer" in source
        assert "RecommendationService" in source
        assert "resolve_feature_flags" in source
        assert "build_twin_provider" in source
