"""Integration tests for Internal Alpha Live Workflow (FSI-003).

Uses temporary repositories — never the real project research tree.
"""

from __future__ import annotations

from pathlib import Path

from app.founder.briefing.dto import BriefingValidationError, ValidationReport
from app.founder.briefing.services import FounderWeeklyBriefingService
from app.founder.internal_alpha.models import PipelineResult
from app.founder.internal_alpha.services import InternalAlphaPipelineService
from app.founder.internal_alpha_workflow import WeekDiscoveryService
from app.founder.internal_alpha_workflow.tests.helpers import (
    FIXED_NOW,
    build_week,
    make_workflow_service,
)


class TestWeekDiscovery:
    def test_list_and_latest_week(self, alpha_root: Path) -> None:
        build_week(alpha_root, "week_001")
        build_week(alpha_root, "week_002")
        build_week(alpha_root, "week_010")
        discovery = WeekDiscoveryService(root=alpha_root)
        weeks = discovery.list_weeks()
        assert [w.label for w in weeks] == ["week_001", "week_002", "week_010"]
        assert discovery.latest_week() is not None
        assert discovery.latest_week().label == "week_010"

    def test_ignores_week_template(self, alpha_root: Path) -> None:
        build_week(alpha_root, "week_001")
        (alpha_root / "week_template").mkdir()
        discovery = WeekDiscoveryService(root=alpha_root)
        assert [w.label for w in discovery.list_weeks()] == ["week_001"]

    def test_validate_structure_reports_missing_folders(self, alpha_root: Path) -> None:
        week_path = build_week(
            alpha_root, "week_001", with_output_dirs=False, with_feedback=True
        )
        discovery = WeekDiscoveryService(root=alpha_root)
        week = discovery.get_week("week_001")
        report = discovery.validate_structure(week)
        assert report.ok is False
        codes = {issue.code for issue in report.issues}
        assert "folder_missing" in codes
        assert week_path.is_dir()


class TestSuccessfulWorkflow:
    def test_successful_workflow(self, alpha_root: Path, week_001: Path) -> None:
        service = make_workflow_service(alpha_root)
        result = service.run(week="week_001", generated_at=FIXED_NOW)

        assert result.success is True
        assert result.week == "week_001"
        assert result.pipeline_success is True
        assert result.operational_state_success is True
        assert result.recommendations_success is True
        assert result.briefing_success is True
        assert result.errors == ()
        assert result.exported_files

        assert (week_001 / "processed" / "classified_feedback.json").is_file()
        assert (week_001 / "processed" / "WEEK_SUMMARY.md").is_file()
        assert (week_001 / "findings" / "WEEK_SUMMARY.md").is_file()
        assert (week_001 / "findings" / "architecture.md").is_file()
        assert (week_001 / "decisions" / "recommendations.json").is_file()
        assert (week_001 / "decisions" / "proposed_actions.md").is_file()
        assert (week_001 / "weekly_review" / "FOUNDER_WEEKLY_REPORT.md").is_file()
        assert (week_001 / "weekly_review" / "founder_weekly_report.json").is_file()
        assert (week_001 / "release" / "release_readiness.md").is_file()
        assert (week_001 / "archive" / "workflow_manifest.json").is_file()

    def test_creates_missing_output_folders(self, alpha_root: Path) -> None:
        week = build_week(
            alpha_root,
            "week_001",
            with_feedback=True,
            with_output_dirs=False,
        )
        assert not (week / "findings").exists()
        service = make_workflow_service(alpha_root)
        result = service.run(week="week_001", generated_at=FIXED_NOW)
        assert result.success is True
        assert (week / "findings").is_dir()
        assert (week / "decisions").is_dir()
        assert (week / "weekly_review").is_dir()
        assert (week / "release").is_dir()
        assert (week / "archive").is_dir()
        assert (week / "processed").is_dir()


class TestFailureModes:
    def test_missing_week_folder(self, alpha_root: Path) -> None:
        service = make_workflow_service(alpha_root)
        result = service.run(week="week_999", generated_at=FIXED_NOW)
        assert result.success is False
        assert result.pipeline_success is False
        assert any("week_missing" in err for err in result.errors)

    def test_missing_feedback(self, alpha_root: Path) -> None:
        build_week(alpha_root, "week_001", with_feedback=False)
        service = make_workflow_service(alpha_root)
        result = service.run(week="week_001", generated_at=FIXED_NOW)
        assert result.success is False
        assert result.pipeline_success is False
        assert result.operational_state_success is False
        assert any("raw_feedback" in err for err in result.errors)

    def test_pipeline_failure_stops_workflow(
        self, alpha_root: Path, week_001: Path
    ) -> None:
        class FailingPipeline(InternalAlphaPipelineService):
            def run(self, *args, **kwargs) -> PipelineResult:
                return PipelineResult(
                    success=False,
                    processed_items=(),
                    warnings=("pipeline_boom: forced failure",),
                    output_files=(),
                )

        service = make_workflow_service(alpha_root, pipeline=FailingPipeline())
        result = service.run(week="week_001", generated_at=FIXED_NOW)
        assert result.success is False
        assert result.pipeline_success is False
        assert result.operational_state_success is False
        assert result.recommendations_success is False
        assert result.briefing_success is False
        assert result.exported_files == ()
        assert any("pipeline" in err for err in result.errors)
        assert not (week_001 / "decisions" / "recommendations.json").exists()
        assert not (week_001 / "weekly_review" / "FOUNDER_WEEKLY_REPORT.md").exists()

    def test_brief_generation_failure_preserves_pipeline(
        self, alpha_root: Path, week_001: Path
    ) -> None:
        class FailingBriefing(FounderWeeklyBriefingService):
            def generate(self, *args, **kwargs):
                raise BriefingValidationError(
                    ValidationReport(
                        ok=False,
                        issues=(),
                    )
                )

        service = make_workflow_service(alpha_root, briefing=FailingBriefing())
        result = service.run(week="week_001", generated_at=FIXED_NOW)
        assert result.success is False
        assert result.pipeline_success is True
        assert result.operational_state_success is True
        assert result.recommendations_success is True
        assert result.briefing_success is False
        assert result.exported_files == ()
        assert (week_001 / "processed" / "WEEK_SUMMARY.md").is_file()
        assert not (week_001 / "decisions" / "recommendations.json").exists()
        assert not (week_001 / "weekly_review" / "FOUNDER_WEEKLY_REPORT.md").exists()

    def test_partial_export_prevention_on_brief_failure(
        self, alpha_root: Path, week_001: Path
    ) -> None:
        """Downstream folder exports must not run when briefing fails."""

        class FailingBriefing(FounderWeeklyBriefingService):
            def generate(self, *args, **kwargs):
                raise RuntimeError("brief boom")

        # Unrelated pre-existing file must survive.
        leftover = week_001 / "decisions" / "human_notes.md"
        leftover.write_text("do not touch\n", encoding="utf-8")

        service = make_workflow_service(alpha_root, briefing=FailingBriefing())
        result = service.run(week="week_001", generated_at=FIXED_NOW)
        assert result.briefing_success is False
        assert result.exported_files == ()
        assert leftover.read_text(encoding="utf-8") == "do not touch\n"
        assert not (week_001 / "findings" / "WEEK_SUMMARY.md").exists()
        assert not (week_001 / "release" / "release_readiness.md").exists()
        assert not (week_001 / "archive" / "workflow_manifest.json").exists()


class TestOutputHygiene:
    def test_does_not_overwrite_unrelated_files(
        self, alpha_root: Path, week_001: Path
    ) -> None:
        notes = week_001 / "findings" / "analyst_notes.md"
        notes.write_text("keep me\n", encoding="utf-8")
        service = make_workflow_service(alpha_root)
        result = service.run(week="week_001", generated_at=FIXED_NOW)
        assert result.success is True
        assert notes.read_text(encoding="utf-8") == "keep me\n"
        assert (week_001 / "findings" / "WEEK_SUMMARY.md").is_file()


class _BrokenExportManager:
    """Stub that raises once export begins."""

    def ensure_directories(self, week) -> None:
        for dirname in (
            "processed",
            "findings",
            "decisions",
            "weekly_review",
            "release",
            "archive",
        ):
            (week.path / dirname).mkdir(parents=True, exist_ok=True)

    def export_all(self, *args, **kwargs):
        raise OSError("disk full")


class TestExportFailure:
    def test_export_failure_preserves_pipeline_outputs(
        self, alpha_root: Path, week_001: Path
    ) -> None:
        service = make_workflow_service(
            alpha_root, output_manager=_BrokenExportManager()
        )
        result = service.run(week="week_001", generated_at=FIXED_NOW)
        assert result.success is False
        assert result.pipeline_success is True
        assert result.briefing_success is True
        assert result.exported_files == ()
        assert any("export_failed" in err for err in result.errors)
        assert (week_001 / "processed" / "WEEK_SUMMARY.md").is_file()
