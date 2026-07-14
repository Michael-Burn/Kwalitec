"""Founder Internal Alpha Live Workflow adapter (registration only).

Wraps ``InternalAlphaWorkflowService`` without modifying FSI-003.
"""

from __future__ import annotations

from types import MappingProxyType

from app.automation.dto.validation import ValidationIssue, ValidationReport
from app.automation.models.context import AutomationContext
from app.automation.models.payload import WorkflowExecutionPayload
from app.automation.models.result import AutomationStatus
from app.founder.internal_alpha_workflow import InternalAlphaWorkflowService
from app.founder.internal_alpha_workflow.dto import WorkflowResult

FOUNDER_INTERNAL_ALPHA_WORKFLOW_ID = "founder.internal_alpha.workflow"


class InternalAlphaAutomationWorkflow:
    """AutomationTask adapter for the Internal Alpha Live Workflow.

    Does not alter InternalAlphaWorkflowService. Translates AutomationContext
    parameters into ``run(week=..., generated_at=...)`` and maps WorkflowResult
    into WorkflowExecutionPayload.
    """

    def __init__(
        self,
        *,
        service: InternalAlphaWorkflowService | None = None,
    ) -> None:
        self._service = service

    @property
    def id(self) -> str:
        return FOUNDER_INTERNAL_ALPHA_WORKFLOW_ID

    @property
    def name(self) -> str:
        return "Internal Alpha Live Workflow"

    @property
    def description(self) -> str:
        return (
            "Run the Founder Internal Alpha live week workflow: "
            "pipeline → operational state → recommendations → briefing → export."
        )

    def validate(self, context: AutomationContext) -> ValidationReport:
        """Accept empty context or optional week / generated_at parameters."""

        issues: list[ValidationIssue] = []
        week = context.parameters.get("week")
        if week is not None and not isinstance(week, str):
            issues.append(
                ValidationIssue(
                    code="invalid_week_parameter",
                    message="parameter 'week' must be a string when provided",
                    field="parameters.week",
                )
            )
        elif isinstance(week, str) and not week.strip():
            issues.append(
                ValidationIssue(
                    code="empty_week_parameter",
                    message="parameter 'week' must be non-empty when provided",
                    field="parameters.week",
                )
            )

        generated_at = context.parameters.get("generated_at")
        if generated_at is not None and not hasattr(generated_at, "isoformat"):
            issues.append(
                ValidationIssue(
                    code="invalid_generated_at_parameter",
                    message=(
                        "parameter 'generated_at' must be a datetime when provided"
                    ),
                    field="parameters.generated_at",
                )
            )

        return ValidationReport(ok=len(issues) == 0, issues=tuple(issues))

    def execute(self, context: AutomationContext) -> WorkflowExecutionPayload:
        """Delegate to InternalAlphaWorkflowService.run."""

        service = self._service or InternalAlphaWorkflowService()
        week = context.parameters.get("week")
        generated_at = context.parameters.get("generated_at")
        result = service.run(week=week, generated_at=generated_at)
        return self._map_result(result)

    def _map_result(self, result: WorkflowResult) -> WorkflowExecutionPayload:
        outputs = MappingProxyType(
            {
                "week": result.week,
                "pipeline_success": result.pipeline_success,
                "operational_state_success": result.operational_state_success,
                "recommendations_success": result.recommendations_success,
                "briefing_success": result.briefing_success,
                "exported_files": result.exported_files,
                "workflow_success": result.success,
            }
        )
        errors = tuple(result.errors)
        warnings = tuple(result.warnings)

        if result.success and not errors:
            status = AutomationStatus.SUCCESS
        elif self._any_stage_succeeded(result) and errors:
            status = AutomationStatus.PARTIAL_SUCCESS
        else:
            status = AutomationStatus.FAILED

        return WorkflowExecutionPayload(
            outputs=outputs,
            warnings=warnings,
            errors=errors,
            status=status,
        )

    @staticmethod
    def _any_stage_succeeded(result: WorkflowResult) -> bool:
        return (
            result.pipeline_success
            or result.operational_state_success
            or result.recommendations_success
            or result.briefing_success
            or bool(result.exported_files)
        )
