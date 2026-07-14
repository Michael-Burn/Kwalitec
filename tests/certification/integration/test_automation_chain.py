"""Integration certification — Automation Framework chain."""

from __future__ import annotations

from pathlib import Path

from app.automation import (
    AutomationContext,
    AutomationService,
    AutomationStatus,
)
from app.automation.registry import AutomationRegistry
from app.automation.workflows.founder_internal_alpha import (
    InternalAlphaAutomationWorkflow,
)
from tests.certification.helpers import CERT_NOW, make_workflow_service


class TestAutomationChain:
    def test_automation_runs_founder_internal_alpha_workflow(
        self, cert_full: tuple[Path, Path]
    ) -> None:
        _repo, alpha_root = cert_full
        workflow_service = make_workflow_service(alpha_root)
        registry = AutomationRegistry()
        registry.register(
            InternalAlphaAutomationWorkflow(service=workflow_service)
        )
        service = AutomationService(registry=registry)

        result = service.run(
            "founder.internal_alpha.workflow",
            AutomationContext.from_mapping(
                {"week": "week_001", "generated_at": CERT_NOW}
            ),
        )
        assert result.status == AutomationStatus.SUCCESS
        assert result.workflow_id == "founder.internal_alpha.workflow"
        assert result.outputs.get("workflow_success") is True
        assert result.outputs.get("week") == "week_001"
        assert result.duration_ms >= 0

    def test_default_registry_lists_founder_workflow(self) -> None:
        service = AutomationService()
        assert (
            "founder.internal_alpha.workflow" in service.registry.workflow_ids()
        )
