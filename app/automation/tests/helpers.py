"""Shared builders for Automation Framework tests (FSI-004).

Uses mocked workflows only — no Founder live execution.
"""

from __future__ import annotations

from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any

from app.automation.dto.validation import ValidationIssue, ValidationReport
from app.automation.executors import AutomationExecutor
from app.automation.models import (
    AutomationContext,
    AutomationResult,
    AutomationStatus,
    WorkflowExecutionPayload,
)
from app.automation.registry import AutomationRegistry
from app.automation.services import AutomationService

FIXED_NOW = datetime(2026, 7, 14, 18, 0, 0, tzinfo=UTC)


class MockWorkflow:
    """Configurable AutomationTask double for unit tests."""

    def __init__(
        self,
        *,
        workflow_id: str = "test.mock.workflow",
        name: str = "Mock Workflow",
        description: str = "Test double for Automation Framework tests",
        validate_report: ValidationReport | None = None,
        payload: WorkflowExecutionPayload | None = None,
        raise_on_execute: Exception | None = None,
        execute_calls: list[AutomationContext] | None = None,
    ) -> None:
        self._id = workflow_id
        self._name = name
        self._description = description
        self._validate_report = validate_report or ValidationReport(
            ok=True, issues=()
        )
        self._payload = payload or WorkflowExecutionPayload.from_mapping(
            {"ok": True}
        )
        self._raise_on_execute = raise_on_execute
        self.execute_calls = execute_calls if execute_calls is not None else []

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    def validate(self, context: AutomationContext) -> ValidationReport:
        return self._validate_report

    def execute(self, context: AutomationContext) -> WorkflowExecutionPayload:
        self.execute_calls.append(context)
        if self._raise_on_execute is not None:
            raise self._raise_on_execute
        return self._payload


def make_context(**parameters: Any) -> AutomationContext:
    return AutomationContext.from_mapping(parameters)


def make_payload(
    outputs: dict[str, Any] | None = None,
    *,
    warnings: tuple[str, ...] = (),
    errors: tuple[str, ...] = (),
    status: AutomationStatus | None = None,
) -> WorkflowExecutionPayload:
    return WorkflowExecutionPayload.from_mapping(
        outputs,
        warnings=warnings,
        errors=errors,
        status=status,
    )


def make_result(**overrides: Any) -> AutomationResult:
    base: dict[str, Any] = {
        "workflow_id": "test.mock.workflow",
        "status": AutomationStatus.SUCCESS,
        "started_at": FIXED_NOW,
        "completed_at": FIXED_NOW,
        "duration_ms": 0,
        "warnings": (),
        "errors": (),
        "outputs": MappingProxyType({"ok": True}),
    }
    base.update(overrides)
    return AutomationResult(**base)


def make_registry(*workflows: MockWorkflow) -> AutomationRegistry:
    registry = AutomationRegistry()
    for workflow in workflows:
        registry.register(workflow)
    return registry


def make_executor(**kwargs: Any) -> AutomationExecutor:
    return AutomationExecutor(
        clock=lambda: FIXED_NOW,
        monotonic=lambda: 0.0,
        **kwargs,
    )


def make_service(
    *workflows: MockWorkflow,
    registry: AutomationRegistry | None = None,
    executor: AutomationExecutor | None = None,
) -> AutomationService:
    resolved_registry = registry or make_registry(*workflows)
    return AutomationService(
        registry=resolved_registry,
        executor=executor or make_executor(),
    )


def failing_validation(
    code: str = "bad_context",
    message: str = "context rejected",
    field: str | None = "parameters",
) -> ValidationReport:
    return ValidationReport(
        ok=False,
        issues=(ValidationIssue(code=code, message=message, field=field),),
    )
