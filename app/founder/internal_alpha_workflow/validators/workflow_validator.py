"""Workflow validators for Internal Alpha Live Workflow (FSI-003)."""

from __future__ import annotations

from pathlib import Path

from app.founder.briefing.models import FounderWeeklyBrief
from app.founder.internal_alpha.models import PipelineResult
from app.founder.internal_alpha_workflow.config import (
    InternalAlphaWorkflowConfig,
    default_config,
)
from app.founder.internal_alpha_workflow.dto import (
    WeekReference,
    WorkflowValidationIssue,
    WorkflowValidationReport,
)
from app.founder.operational_state.models import FounderOperationalState
from app.founder.recommendations.models import RecommendationSet


class WorkflowValidator:
    """Validate week preconditions and stage outputs (no business logic)."""

    def __init__(self, config: InternalAlphaWorkflowConfig | None = None) -> None:
        self._config = config or default_config()

    def validate_week_exists(self, week: WeekReference) -> WorkflowValidationReport:
        if not week.path.is_dir():
            return WorkflowValidationReport(
                ok=False,
                issues=(
                    WorkflowValidationIssue(
                        code="week_missing",
                        message=f"Week does not exist: {week.label}",
                        path=str(week.path),
                    ),
                ),
            )
        return WorkflowValidationReport(ok=True)

    def validate_pipeline(
        self, result: PipelineResult
    ) -> WorkflowValidationReport:
        if not result.success:
            messages = result.warnings or ("Pipeline did not complete successfully",)
            return WorkflowValidationReport(
                ok=False,
                issues=tuple(
                    WorkflowValidationIssue(code="pipeline_failed", message=m)
                    for m in messages
                ),
            )
        if not result.output_files:
            return WorkflowValidationReport(
                ok=False,
                issues=(
                    WorkflowValidationIssue(
                        code="pipeline_no_outputs",
                        message="Pipeline reported success without output files",
                    ),
                ),
            )
        return WorkflowValidationReport(ok=True)

    def validate_snapshot(
        self, state: FounderOperationalState | None
    ) -> WorkflowValidationReport:
        if state is None:
            return WorkflowValidationReport(
                ok=False,
                issues=(
                    WorkflowValidationIssue(
                        code="snapshot_missing",
                        message="Operational State snapshot was not generated",
                    ),
                ),
            )
        return WorkflowValidationReport(ok=True)

    def validate_recommendations(
        self, recommendation_set: RecommendationSet | None
    ) -> WorkflowValidationReport:
        if recommendation_set is None:
            return WorkflowValidationReport(
                ok=False,
                issues=(
                    WorkflowValidationIssue(
                        code="recommendations_missing",
                        message="Recommendation set was not generated",
                    ),
                ),
            )
        return WorkflowValidationReport(ok=True)

    def validate_brief(
        self, brief: FounderWeeklyBrief | None
    ) -> WorkflowValidationReport:
        if brief is None:
            return WorkflowValidationReport(
                ok=False,
                issues=(
                    WorkflowValidationIssue(
                        code="brief_missing",
                        message="Weekly brief was not generated",
                    ),
                ),
            )
        return WorkflowValidationReport(ok=True)

    def validate_exports(
        self, exported_files: tuple[str, ...]
    ) -> WorkflowValidationReport:
        if not exported_files:
            return WorkflowValidationReport(
                ok=False,
                issues=(
                    WorkflowValidationIssue(
                        code="exports_missing",
                        message="No export files were written",
                    ),
                ),
            )
        missing = [p for p in exported_files if not Path(p).is_file()]
        if missing:
            return WorkflowValidationReport(
                ok=False,
                issues=tuple(
                    WorkflowValidationIssue(
                        code="export_file_missing",
                        message=f"Expected export file missing: {path}",
                        path=path,
                    )
                    for path in missing
                ),
            )
        return WorkflowValidationReport(ok=True)
