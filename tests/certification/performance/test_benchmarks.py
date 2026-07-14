"""Performance certification — soft budgets for Founder + Automation paths."""

from __future__ import annotations

from pathlib import Path

from app.automation import AutomationContext, AutomationStatus
from app.automation.registry import AutomationRegistry
from app.automation.services import AutomationService
from app.automation.workflows.founder_internal_alpha import (
    InternalAlphaAutomationWorkflow,
)
from app.founder.briefing import FounderWeeklyBriefingService
from app.founder.dashboard.providers import (
    OperationalStateProvider,
    RecommendationProvider,
    WeeklyBriefProvider,
)
from app.founder.dashboard.services import FounderDashboardService
from app.founder.knowledge_engine import KnowledgeQueryService
from app.founder.operational_state.services import FounderOperationalStateService
from app.founder.recommendations import FounderRecommendationService
from tests.certification.helpers import (
    CERT_NOW,
    PERF_BUDGETS_MS,
    enrich_knowledge_fixture,
    live_state_providers,
    make_workflow_service,
    time_call,
)


class TestPerformanceBudgets:
    """Measure certified paths and assert soft upper bounds.

    Values are recorded via pytest ``-s`` output and the certification report.
    Budgets are intentionally conservative for CI runners.
    """

    def test_knowledge_indexing_budget(self, cert_repo: Path) -> None:
        enrich_knowledge_fixture(cert_repo)

        def _run():
            service = KnowledgeQueryService(repo_root=cert_repo)
            return service.get_summary()

        summary, timing = time_call("knowledge_indexing", _run)
        print(
            f"[cert-perf] knowledge_indexing={timing.duration_ms:.2f}ms "
            f"budget={timing.budget_ms:.0f}ms artefacts={summary.indexed_artefacts}"
        )
        assert timing.within_budget

    def test_operational_state_budget(self, cert_repo: Path) -> None:
        def _run():
            return FounderOperationalStateService(
                **live_state_providers(cert_repo),
                clock=lambda: CERT_NOW,
            ).get_state()

        state, timing = time_call("operational_state", _run)
        print(
            f"[cert-perf] operational_state={timing.duration_ms:.2f}ms "
            f"budget={timing.budget_ms:.0f}ms snapshot={state.snapshot_version}"
        )
        assert timing.within_budget

    def test_recommendation_budget(self, cert_repo: Path) -> None:
        state = FounderOperationalStateService(
            **live_state_providers(cert_repo),
            clock=lambda: CERT_NOW,
        ).get_state()

        def _run():
            return FounderRecommendationService(
                clock=lambda: CERT_NOW
            ).recommend(state)

        recommendation_set, timing = time_call("recommendations", _run)
        print(
            f"[cert-perf] recommendations={timing.duration_ms:.2f}ms "
            f"budget={timing.budget_ms:.0f}ms "
            f"count={len(recommendation_set.recommendations)}"
        )
        assert timing.within_budget

    def test_weekly_briefing_budget(self, cert_repo: Path) -> None:
        state = FounderOperationalStateService(
            **live_state_providers(cert_repo),
            clock=lambda: CERT_NOW,
        ).get_state()
        recommendation_set = FounderRecommendationService(
            clock=lambda: CERT_NOW
        ).recommend(state)

        def _run():
            return FounderWeeklyBriefingService(
                clock=lambda: CERT_NOW
            ).generate_brief(state, recommendation_set)

        brief, timing = time_call("weekly_briefing", _run)
        print(
            f"[cert-perf] weekly_briefing={timing.duration_ms:.2f}ms "
            f"budget={timing.budget_ms:.0f}ms week={brief.week}"
        )
        assert timing.within_budget

    def test_dashboard_service_budget(self, cert_repo: Path) -> None:
        state_service = FounderOperationalStateService(
            **live_state_providers(cert_repo),
            clock=lambda: CERT_NOW,
        )
        recommendation_service = FounderRecommendationService(
            clock=lambda: CERT_NOW
        )
        briefing_service = FounderWeeklyBriefingService(clock=lambda: CERT_NOW)
        dashboard = FounderDashboardService(
            operational_state=OperationalStateProvider(service=state_service),
            recommendations=RecommendationProvider(
                service=recommendation_service
            ),
            weekly_brief=WeeklyBriefProvider(service=briefing_service),
        )

        def _run():
            return dashboard.build_page()

        page, timing = time_call("dashboard_service", _run)
        print(
            f"[cert-perf] dashboard_service={timing.duration_ms:.2f}ms "
            f"budget={timing.budget_ms:.0f}ms "
            f"snapshot={page.overview.snapshot_version}"
        )
        assert timing.within_budget

    def test_automation_execution_budget(
        self, cert_full: tuple[Path, Path]
    ) -> None:
        _repo, alpha_root = cert_full
        registry = AutomationRegistry()
        registry.register(
            InternalAlphaAutomationWorkflow(
                service=make_workflow_service(alpha_root)
            )
        )
        service = AutomationService(registry=registry)

        def _run():
            return service.run(
                "founder.internal_alpha.workflow",
                AutomationContext.from_mapping(
                    {"week": "week_001", "generated_at": CERT_NOW}
                ),
            )

        result, timing = time_call("automation_execution", _run)
        print(
            f"[cert-perf] automation_execution={timing.duration_ms:.2f}ms "
            f"budget={timing.budget_ms:.0f}ms status={result.status.value}"
        )
        assert result.status == AutomationStatus.SUCCESS
        assert timing.within_budget

    def test_budgets_are_documented(self) -> None:
        expected = {
            "knowledge_indexing",
            "operational_state",
            "recommendations",
            "weekly_briefing",
            "dashboard_service",
            "automation_execution",
        }
        assert set(PERF_BUDGETS_MS) == expected
