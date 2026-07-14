"""AutomationExecutor — deterministic workflow execution (no business logic)."""

from __future__ import annotations

import time
from collections.abc import Callable
from datetime import UTC, datetime
from types import MappingProxyType

from app.automation.dto.validation import ValidationReport
from app.automation.models.context import AutomationContext
from app.automation.models.payload import WorkflowExecutionPayload
from app.automation.models.result import AutomationResult, AutomationStatus
from app.automation.validators.context_validator import AutomationContextValidator
from app.automation.validators.result_validator import AutomationResultValidator
from app.automation.workflows.protocols import AutomationTask


class AutomationExecutor:
    """Execute a single AutomationTask.

    Responsibilities:
    - Validate context (framework + workflow)
    - Execute workflow
    - Capture execution result
    - Measure execution duration
    - Return AutomationResult

    No domain / business logic.
    """

    def __init__(
        self,
        *,
        context_validator: AutomationContextValidator | None = None,
        result_validator: AutomationResultValidator | None = None,
        clock: Callable[[], datetime] | None = None,
        monotonic: Callable[[], float] | None = None,
    ) -> None:
        self._context_validator = context_validator or AutomationContextValidator()
        self._result_validator = result_validator or AutomationResultValidator()
        self._clock = clock or (lambda: datetime.now(UTC))
        self._monotonic = monotonic or time.perf_counter

    def execute(
        self,
        workflow: AutomationTask,
        context: AutomationContext | None = None,
    ) -> AutomationResult:
        """Validate and run ``workflow`` against ``context``.

        Args:
            workflow: Registered AutomationTask implementation.
            context: Execution inputs; defaults to an empty context.

        Returns:
            AutomationResult describing status, timing, warnings, errors,
            and outputs. Validation failures and execution exceptions become
            FAILED results rather than raised exceptions.
        """
        resolved = context if context is not None else AutomationContext.empty()
        started_at = self._clock()
        t0 = self._monotonic()

        framework_report = self._context_validator.validate(resolved)
        if not framework_report.ok:
            return self._finish(
                workflow_id=workflow.id,
                started_at=started_at,
                t0=t0,
                status=AutomationStatus.FAILED,
                warnings=(),
                errors=self._issues_to_messages(framework_report),
                outputs=MappingProxyType({}),
            )

        workflow_report = workflow.validate(resolved)
        if not workflow_report.ok:
            return self._finish(
                workflow_id=workflow.id,
                started_at=started_at,
                t0=t0,
                status=AutomationStatus.FAILED,
                warnings=(),
                errors=self._issues_to_messages(workflow_report),
                outputs=MappingProxyType({}),
            )

        try:
            payload = workflow.execute(resolved)
        except Exception as exc:  # noqa: BLE001 — capture into FAILED result
            return self._finish(
                workflow_id=workflow.id,
                started_at=started_at,
                t0=t0,
                status=AutomationStatus.FAILED,
                warnings=(),
                errors=(f"workflow execution raised: {exc}",),
                outputs=MappingProxyType({}),
            )

        if not isinstance(payload, WorkflowExecutionPayload):
            return self._finish(
                workflow_id=workflow.id,
                started_at=started_at,
                t0=t0,
                status=AutomationStatus.FAILED,
                warnings=(),
                errors=(
                    "workflow execute() must return WorkflowExecutionPayload",
                ),
                outputs=MappingProxyType({}),
            )

        status = self._derive_status(payload)
        return self._finish(
            workflow_id=workflow.id,
            started_at=started_at,
            t0=t0,
            status=status,
            warnings=tuple(payload.warnings),
            errors=tuple(payload.errors),
            outputs=payload.outputs,
        )

    def _finish(
        self,
        *,
        workflow_id: str,
        started_at: datetime,
        t0: float,
        status: AutomationStatus,
        warnings: tuple[str, ...],
        errors: tuple[str, ...],
        outputs: MappingProxyType,
    ) -> AutomationResult:
        completed_at = self._clock()
        duration_ms = max(0, int((self._monotonic() - t0) * 1000))
        result = AutomationResult(
            workflow_id=workflow_id,
            status=status,
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=duration_ms,
            warnings=warnings,
            errors=errors,
            outputs=outputs,
        )
        report = self._result_validator.validate(result)
        if not report.ok:
            # Structural repair path should never trigger for executor-built
            # results; if it does, force a FAILED envelope with validator notes.
            return AutomationResult(
                workflow_id=workflow_id or "unknown",
                status=AutomationStatus.FAILED,
                started_at=started_at,
                completed_at=completed_at,
                duration_ms=duration_ms,
                warnings=warnings,
                errors=errors + self._issues_to_messages(report),
                outputs=(
                    outputs
                    if isinstance(outputs, MappingProxyType)
                    else MappingProxyType({})
                ),
            )
        return result

    @staticmethod
    def _derive_status(payload: WorkflowExecutionPayload) -> AutomationStatus:
        if payload.status is not None:
            return payload.status
        if payload.errors and payload.outputs:
            return AutomationStatus.PARTIAL_SUCCESS
        if payload.errors:
            return AutomationStatus.FAILED
        return AutomationStatus.SUCCESS

    @staticmethod
    def _issues_to_messages(report: ValidationReport) -> tuple[str, ...]:
        messages: list[str] = []
        for issue in report.issues:
            if issue.field:
                messages.append(f"{issue.code}: {issue.message} ({issue.field})")
            else:
                messages.append(f"{issue.code}: {issue.message}")
        return tuple(messages)
