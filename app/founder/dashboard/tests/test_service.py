"""Unit tests for FounderDashboardService live integration (FSI-002)."""

from __future__ import annotations

from app.founder.dashboard.tests.helpers import (
    make_attention_bundle,
    make_healthy_state,
    make_recommendation,
    make_recommendation_set,
    make_service,
    make_state,
)


class TestFounderDashboardService:
    def test_build_overview_maps_operational_state(self) -> None:
        state = make_healthy_state()
        service = make_service(state=state)
        overview = service.build_overview()
        assert overview.engineering_health == 100
        assert overview.architecture_health == 100
        assert overview.capability_count == state.capability.total_count
        assert overview.completed_capabilities == state.capability.completed_count
        assert overview.active_capabilities == state.capability.active_count
        assert overview.internal_alpha_week == state.internal_alpha.current_week
        assert overview.feedback_count == state.internal_alpha.feedback_count
        assert overview.duplicate_feedback == state.internal_alpha.duplicate_count
        assert overview.current_release == state.release.current_release
        assert overview.snapshot_version == state.snapshot_version
        assert overview.recommendation_count == 0
        assert overview.brief_available is True

    def test_build_page_includes_live_sections(self) -> None:
        state, recommendation_set, brief = make_attention_bundle()
        service = make_service(
            state=state,
            recommendation_set=recommendation_set,
            brief=brief,
        )
        page = service.build_page()
        assert page.fos_version == "1.0"
        assert page.knowledge.engineering_standards == (
            state.knowledge.engineering_standards
        )
        assert page.capabilities.total_count == state.capability.total_count
        assert page.capabilities.recent_capability_ids == (
            state.capability.recent_capability_ids
        )
        assert page.internal_alpha.feedback_count == (
            state.internal_alpha.feedback_count
        )
        assert page.recommendations.available is True
        assert page.recommendations.count == 1
        assert page.recommendations.top[0].priority == "High"
        assert page.recommendations.overall_status == "attention"
        assert page.weekly_brief.available is True
        assert page.weekly_brief.week == brief.week
        assert page.weekly_brief.snapshot_version == brief.snapshot_version
        assert page.overview.snapshot_version == state.snapshot_version
        assert page.overview.recommendation_count == 1
        assert page.overview.brief_available is True

    def test_top_recommendations_capped_at_five(self) -> None:
        state = make_healthy_state()
        recommendations = tuple(
            make_recommendation(
                recommendation_id=f"rec-{index}",
                title=f"Recommendation {index}",
            )
            for index in range(7)
        )
        recommendation_set = make_recommendation_set(
            state=state,
            recommendations=recommendations,
            overall_status="attention",
        )
        service = make_service(
            state=state,
            recommendation_set=recommendation_set,
            brief=None,
        )
        page = service.build_page()
        assert page.recommendations.count == 7
        assert len(page.recommendations.top) == 5
        assert page.weekly_brief.available is False
        assert page.overview.brief_available is False

    def test_health_zero_when_engineering_signals_fail(self) -> None:
        state = make_state(
            knowledge_overrides={"tests_pass": False, "validation_errors": 2}
        )
        service = make_service(state=state)
        overview = service.build_overview()
        assert overview.engineering_health == 0
        assert overview.architecture_health == 0

    def test_latest_activity_uses_recent_capability(self) -> None:
        state = make_healthy_state()
        service = make_service(state=state)
        overview = service.build_overview()
        assert overview.latest_activity == state.capability.recent_capability_ids[0]

    def test_missing_operational_state_renders_empty_page(self) -> None:
        service = make_service(
            state=None,
            recommendation_set=None,
            brief=None,
        )
        page = service.build_page()
        assert page.overview.snapshot_version == ""
        assert page.overview.capability_count == 0
        assert page.overview.recommendation_count == 0
        assert page.overview.brief_available is False
        assert page.recommendations.available is False
        assert page.weekly_brief.available is False
        assert page.knowledge.indexed_artefacts == 0

    def test_missing_recommendations_still_renders_state(self) -> None:
        state = make_healthy_state()
        service = make_service(
            state=state,
            recommendation_set=None,
            brief=None,
        )
        page = service.build_page()
        assert page.overview.snapshot_version == state.snapshot_version
        assert page.capabilities.total_count == state.capability.total_count
        assert page.recommendations.available is False
        assert page.weekly_brief.available is False
        assert page.overview.recommendation_count == 0
