"""Integration certification — end-to-end Founder operational chain."""

from __future__ import annotations

from pathlib import Path

from app.founder.briefing import FounderWeeklyBriefingService
from app.founder.capability_archive import CapabilityArchiveQueryService
from app.founder.dashboard.providers import (
    OperationalStateProvider,
    RecommendationProvider,
    WeeklyBriefProvider,
)
from app.founder.dashboard.services import FounderDashboardService
from app.founder.knowledge_engine import KnowledgeQueryService
from app.founder.operational_state.providers import (
    InternalAlphaProvider,
    StaticInternalAlphaSource,
)
from app.founder.operational_state.services import FounderOperationalStateService
from app.founder.operational_state.tests.helpers import make_alpha_dto
from app.founder.recommendations import FounderRecommendationService
from tests.certification.helpers import (
    CERT_NOW,
    enrich_knowledge_fixture,
    live_state_providers,
    make_workflow_service,
)


class TestOperationalChain:
    def test_knowledge_to_dashboard_chain(self, cert_repo: Path) -> None:
        enrich_knowledge_fixture(cert_repo)

        knowledge = KnowledgeQueryService(repo_root=cert_repo)
        archive = CapabilityArchiveQueryService(repo_root=cert_repo)
        k_summary = knowledge.get_summary()
        c_summary = archive.get_summary()
        assert k_summary.indexed_artefacts >= 5
        assert c_summary.total_count >= 2

        state_service = FounderOperationalStateService(
            **live_state_providers(cert_repo),
            clock=lambda: CERT_NOW,
        )
        state = state_service.get_state()
        assert state.knowledge.indexed_artefacts >= 5
        assert state.capability.total_count >= 2
        assert state.snapshot_version

        recommendation_service = FounderRecommendationService(
            clock=lambda: CERT_NOW
        )
        recommendation_set = recommendation_service.recommend(state)
        assert recommendation_set.snapshot_version == state.snapshot_version
        assert recommendation_set.overall_status in {
            "healthy",
            "attention",
            "critical",
        }

        briefing_service = FounderWeeklyBriefingService(clock=lambda: CERT_NOW)
        brief = briefing_service.generate_brief(state, recommendation_set)
        assert brief.ordered_sections()
        assert brief.snapshot_version == state.snapshot_version

        dashboard = FounderDashboardService(
            operational_state=OperationalStateProvider(service=state_service),
            recommendations=RecommendationProvider(
                service=recommendation_service
            ),
            weekly_brief=WeeklyBriefProvider(service=briefing_service),
        )
        page = dashboard.build_page()
        assert page.overview.snapshot_version == state.snapshot_version
        assert page.knowledge.indexed_artefacts == (
            state.knowledge.indexed_artefacts
        )
        assert page.capabilities.total_count == state.capability.total_count
        assert page.weekly_brief.available is True
        assert page.recommendations.available is True

    def test_recommendation_correctness_on_attention_state(
        self, cert_repo: Path
    ) -> None:
        providers = live_state_providers(cert_repo)
        providers["internal_alpha"] = InternalAlphaProvider(
            StaticInternalAlphaSource(
                make_alpha_dto(feedback_count=0, duplicate_count=0)
            )
        )
        state = FounderOperationalStateService(
            **providers,
            clock=lambda: CERT_NOW,
        ).get_state()
        recommendation_set = FounderRecommendationService(
            clock=lambda: CERT_NOW
        ).recommend(state)
        assert recommendation_set.overall_status == "attention"
        titles = " ".join(
            rec.title.lower() for rec in recommendation_set.recommendations
        )
        assert "internal alpha" in titles

    def test_weekly_briefing_generation(self, cert_repo: Path) -> None:
        state = FounderOperationalStateService(
            **live_state_providers(cert_repo),
            clock=lambda: CERT_NOW,
        ).get_state()
        recommendation_set = FounderRecommendationService(
            clock=lambda: CERT_NOW
        ).recommend(state)
        brief = FounderWeeklyBriefingService(
            clock=lambda: CERT_NOW
        ).generate_brief(state, recommendation_set)
        assert len(brief.ordered_sections()) >= 5
        assert brief.week
        assert brief.metadata.report_version

    def test_internal_alpha_workflow_chain(
        self, cert_full: tuple[Path, Path]
    ) -> None:
        _repo, alpha_root = cert_full
        service = make_workflow_service(alpha_root)
        result = service.run(week="week_001", generated_at=CERT_NOW)
        assert result.success is True
        assert result.pipeline_success is True
        assert result.operational_state_success is True
        assert result.recommendations_success is True
        assert result.briefing_success is True
        week = alpha_root / "week_001"
        assert (week / "decisions" / "recommendations.json").is_file()
        assert (week / "weekly_review" / "FOUNDER_WEEKLY_REPORT.md").is_file()
        assert (week / "archive" / "workflow_manifest.json").is_file()
