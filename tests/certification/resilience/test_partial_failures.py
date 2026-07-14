"""Resilience certification — partial failures and graceful degradation."""

from __future__ import annotations

from pathlib import Path

from app.automation import AutomationContext, AutomationStatus
from app.automation.registry import AutomationRegistry
from app.automation.services import AutomationService
from app.automation.workflows.founder_internal_alpha import (
    InternalAlphaAutomationWorkflow,
)
from app.founder.briefing.dto import BriefingValidationError, ValidationReport
from app.founder.briefing.services import FounderWeeklyBriefingService
from app.founder.dashboard.tests.helpers import make_service as make_dashboard
from app.founder.internal_alpha.models import PipelineResult
from app.founder.internal_alpha.services import InternalAlphaPipelineService
from app.founder.internal_alpha_workflow.tests.helpers import build_week
from tests.certification.helpers import CERT_NOW, make_workflow_service


class TestPartialFailures:
    def test_pipeline_failure_stops_downstream(self, tmp_path: Path) -> None:
        alpha_root = tmp_path / "research" / "internal_alpha"
        alpha_root.mkdir(parents=True)
        build_week(alpha_root, "week_001", with_feedback=True)

        class FailingPipeline(InternalAlphaPipelineService):
            def run(self, *args, **kwargs) -> PipelineResult:
                return PipelineResult(
                    success=False,
                    processed_items=(),
                    warnings=("pipeline_boom: forced failure",),
                    output_files=(),
                )

        result = make_workflow_service(
            alpha_root, pipeline=FailingPipeline()
        ).run(week="week_001", generated_at=CERT_NOW)
        assert result.success is False
        assert result.pipeline_success is False
        assert result.operational_state_success is False
        assert result.recommendations_success is False
        assert result.briefing_success is False

    def test_briefing_failure_preserves_pipeline_outputs(
        self, tmp_path: Path
    ) -> None:
        alpha_root = tmp_path / "research" / "internal_alpha"
        alpha_root.mkdir(parents=True)
        week = build_week(alpha_root, "week_001", with_feedback=True)

        class FailingBriefing(FounderWeeklyBriefingService):
            def generate(self, *args, **kwargs):
                raise BriefingValidationError(
                    ValidationReport(ok=False, issues=())
                )

        result = make_workflow_service(
            alpha_root, briefing=FailingBriefing()
        ).run(week="week_001", generated_at=CERT_NOW)
        assert result.pipeline_success is True
        assert result.operational_state_success is True
        assert result.recommendations_success is True
        assert result.briefing_success is False
        assert result.success is False
        assert (week / "processed" / "WEEK_SUMMARY.md").is_file()
        assert not (week / "decisions" / "recommendations.json").exists()

    def test_dashboard_degrades_when_state_unavailable(self) -> None:
        page = make_dashboard(
            state=None, recommendation_set=None, brief=None
        ).build_page()
        assert page.fos_version == "1.0"
        assert page.overview.snapshot_version == ""
        assert page.recommendations.available is False
        assert page.weekly_brief.available is False

    def test_dashboard_degrades_when_recommendations_unavailable(self) -> None:
        page = make_dashboard(
            recommendation_set=None, brief=None
        ).build_page()
        assert page.overview.snapshot_version
        assert page.recommendations.available is False
        assert page.weekly_brief.available is False

    def test_automation_unknown_workflow_fails_softly(self) -> None:
        result = AutomationService().run("certification.does.not.exist")
        assert result.status == AutomationStatus.FAILED
        assert result.errors

    def test_automation_maps_workflow_failure(self, tmp_path: Path) -> None:
        alpha_root = tmp_path / "research" / "internal_alpha"
        alpha_root.mkdir(parents=True)
        build_week(alpha_root, "week_001", with_feedback=False)
        registry = AutomationRegistry()
        registry.register(
            InternalAlphaAutomationWorkflow(
                service=make_workflow_service(alpha_root)
            )
        )
        result = AutomationService(registry=registry).run(
            "founder.internal_alpha.workflow",
            AutomationContext.from_mapping({"week": "week_001"}),
        )
        assert result.status == AutomationStatus.FAILED
        assert result.errors
