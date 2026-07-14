"""Architecture certification — public API encapsulation."""

from __future__ import annotations

import importlib

import app.automation as automation
import app.founder.briefing as briefing
import app.founder.capability_archive as capability_archive
import app.founder.internal_alpha as internal_alpha
import app.founder.internal_alpha_workflow as workflow
import app.founder.knowledge_engine as knowledge_engine
import app.founder.operational_state as operational_state
import app.founder.recommendations as recommendations
from app.founder.dashboard.services import FounderDashboardService

# Stable public surfaces certified for Version 1 production use.
_PUBLIC_SURFACES: dict[str, tuple[str, ...]] = {
    "app.founder.knowledge_engine": (
        "KnowledgeQueryService",
        "KnowledgeArtefactDTO",
        "KnowledgeIndexSummaryDTO",
    ),
    "app.founder.capability_archive": (
        "CapabilityArchiveQueryService",
        "CapabilityRecordDTO",
        "CapabilityArchiveSummaryDTO",
    ),
    "app.founder.internal_alpha": ("InternalAlphaPipelineService",),
    "app.founder.operational_state": (
        "FounderOperationalStateService",
        "FounderOperationalState",
    ),
    "app.founder.recommendations": (
        "FounderRecommendationService",
        "RecommendationSet",
        "Recommendation",
    ),
    "app.founder.briefing": (
        "FounderWeeklyBriefingService",
        "FounderWeeklyBrief",
    ),
    "app.founder.internal_alpha_workflow": (
        "InternalAlphaWorkflowService",
        "WorkflowResult",
        "WeekDiscoveryService",
    ),
    "app.automation": (
        "AutomationService",
        "AutomationContext",
        "AutomationResult",
        "AutomationStatus",
        "build_default_registry",
    ),
}


class TestPublicAPIStability:
    def test_declared_public_names_are_importable(self) -> None:
        missing: list[str] = []
        for module_name, names in _PUBLIC_SURFACES.items():
            module = importlib.import_module(module_name)
            exported = set(getattr(module, "__all__", ()))
            for name in names:
                if not hasattr(module, name):
                    missing.append(f"{module_name}.{name}")
                elif exported and name not in exported:
                    missing.append(f"{module_name}.{name} not in __all__")
        assert not missing, f"Public API gaps: {missing}"

    def test_package_all_lists_are_non_empty(self) -> None:
        packages = (
            knowledge_engine,
            capability_archive,
            internal_alpha,
            operational_state,
            recommendations,
            briefing,
            workflow,
            automation,
        )
        for package in packages:
            assert getattr(package, "__all__", ()), (
                f"{package.__name__} must declare a public __all__"
            )

    def test_dashboard_service_remains_public_coordinator(self) -> None:
        assert callable(FounderDashboardService)
        assert hasattr(FounderDashboardService, "build_page")
        assert hasattr(FounderDashboardService, "build_overview")

    def test_default_automation_registry_exposes_founder_workflow(self) -> None:
        registry = automation.build_default_registry()
        workflow_id = "founder.internal_alpha.workflow"
        assert registry.contains(workflow_id)
        assert workflow_id in registry.workflow_ids()
