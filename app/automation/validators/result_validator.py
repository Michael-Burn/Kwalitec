"""Structural checks for AutomationResult completeness and status."""

from __future__ import annotations

from datetime import datetime
from types import MappingProxyType

from app.automation.dto.validation import ValidationIssue, ValidationReport
from app.automation.models.result import (
    ALLOWED_STATUSES,
    AutomationResult,
    AutomationStatus,
)


class AutomationResultValidator:
    """Validate execution status and result completeness."""

    def validate(self, result: AutomationResult | None) -> ValidationReport:
        """Return ok=False when ``result`` is incomplete or status is illegal."""

        issues: list[ValidationIssue] = []
        if result is None:
            issues.append(
                ValidationIssue(
                    code="missing_result",
                    message="AutomationResult is required",
                    field="result",
                )
            )
            return ValidationReport(ok=False, issues=tuple(issues))

        if not isinstance(result, AutomationResult):
            issues.append(
                ValidationIssue(
                    code="invalid_result_type",
                    message="result must be an AutomationResult instance",
                    field="result",
                )
            )
            return ValidationReport(ok=False, issues=tuple(issues))

        if not str(result.workflow_id or "").strip():
            issues.append(
                ValidationIssue(
                    code="missing_workflow_id",
                    message="workflow_id must be a non-empty string",
                    field="workflow_id",
                )
            )

        if not isinstance(result.status, AutomationStatus):
            issues.append(
                ValidationIssue(
                    code="invalid_status_type",
                    message="status must be an AutomationStatus",
                    field="status",
                )
            )
        elif result.status not in ALLOWED_STATUSES:
            issues.append(
                ValidationIssue(
                    code="invalid_status",
                    message=(
                        f"status {result.status!r} is not in "
                        f"{sorted(s.value for s in ALLOWED_STATUSES)}"
                    ),
                    field="status",
                )
            )

        if not isinstance(result.started_at, datetime):
            issues.append(
                ValidationIssue(
                    code="missing_started_at",
                    message="started_at must be a datetime",
                    field="started_at",
                )
            )
        if not isinstance(result.completed_at, datetime):
            issues.append(
                ValidationIssue(
                    code="missing_completed_at",
                    message="completed_at must be a datetime",
                    field="completed_at",
                )
            )
        if (
            isinstance(result.started_at, datetime)
            and isinstance(result.completed_at, datetime)
            and result.completed_at < result.started_at
        ):
            issues.append(
                ValidationIssue(
                    code="invalid_time_range",
                    message="completed_at must not be earlier than started_at",
                    field="completed_at",
                )
            )

        if not isinstance(result.duration_ms, int) or result.duration_ms < 0:
            issues.append(
                ValidationIssue(
                    code="invalid_duration_ms",
                    message="duration_ms must be a non-negative integer",
                    field="duration_ms",
                )
            )

        if not isinstance(result.warnings, tuple):
            issues.append(
                ValidationIssue(
                    code="invalid_warnings",
                    message="warnings must be a tuple of strings",
                    field="warnings",
                )
            )
        if not isinstance(result.errors, tuple):
            issues.append(
                ValidationIssue(
                    code="invalid_errors",
                    message="errors must be a tuple of strings",
                    field="errors",
                )
            )

        if not isinstance(result.outputs, MappingProxyType):
            issues.append(
                ValidationIssue(
                    code="invalid_outputs",
                    message="outputs must be a MappingProxyType",
                    field="outputs",
                )
            )

        if (
            result.status == AutomationStatus.SUCCESS
            and result.errors
        ):
            issues.append(
                ValidationIssue(
                    code="success_with_errors",
                    message="SUCCESS results must not carry errors",
                    field="errors",
                )
            )

        if (
            result.status == AutomationStatus.FAILED
            and not result.errors
        ):
            issues.append(
                ValidationIssue(
                    code="failed_without_errors",
                    message="FAILED results must carry at least one error",
                    field="errors",
                )
            )

        return ValidationReport(ok=len(issues) == 0, issues=tuple(issues))
