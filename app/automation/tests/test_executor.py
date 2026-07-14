"""Tests for AutomationExecutor."""

from __future__ import annotations

from types import MappingProxyType

from app.automation.models import AutomationStatus
from app.automation.tests.helpers import (
    FIXED_NOW,
    MockWorkflow,
    failing_validation,
    make_context,
    make_executor,
    make_payload,
)


class TestAutomationExecutor:
    def test_successful_execution(self) -> None:
        workflow = MockWorkflow(
            payload=make_payload({"value": 1}, warnings=("soft",))
        )
        result = make_executor().execute(workflow, make_context(x=1))
        assert result.status == AutomationStatus.SUCCESS
        assert result.workflow_id == workflow.id
        assert result.warnings == ("soft",)
        assert result.errors == ()
        assert dict(result.outputs) == {"value": 1}
        assert result.started_at == FIXED_NOW
        assert result.completed_at == FIXED_NOW
        assert result.duration_ms == 0
        assert len(workflow.execute_calls) == 1

    def test_workflow_validation_failure_skips_execute(self) -> None:
        workflow = MockWorkflow(validate_report=failing_validation())
        result = make_executor().execute(workflow, make_context())
        assert result.status == AutomationStatus.FAILED
        assert result.errors
        assert "bad_context" in result.errors[0]
        assert workflow.execute_calls == []

    def test_execute_exception_becomes_failed(self) -> None:
        workflow = MockWorkflow(raise_on_execute=RuntimeError("boom"))
        result = make_executor().execute(workflow)
        assert result.status == AutomationStatus.FAILED
        assert "boom" in result.errors[0]

    def test_partial_success_from_payload_status(self) -> None:
        workflow = MockWorkflow(
            payload=make_payload(
                {"stage": "pipeline"},
                errors=("recommendations failed",),
                status=AutomationStatus.PARTIAL_SUCCESS,
            )
        )
        result = make_executor().execute(workflow)
        assert result.status == AutomationStatus.PARTIAL_SUCCESS
        assert result.errors == ("recommendations failed",)
        assert dict(result.outputs) == {"stage": "pipeline"}

    def test_derived_partial_success_from_errors_and_outputs(self) -> None:
        workflow = MockWorkflow(
            payload=make_payload(
                {"kept": True},
                errors=("later stage failed",),
            )
        )
        result = make_executor().execute(workflow)
        assert result.status == AutomationStatus.PARTIAL_SUCCESS

    def test_derived_failed_from_errors_only(self) -> None:
        workflow = MockWorkflow(
            payload=make_payload(errors=("hard failure",))
        )
        result = make_executor().execute(workflow)
        assert result.status == AutomationStatus.FAILED
        assert result.outputs == MappingProxyType({})

    def test_default_empty_context(self) -> None:
        workflow = MockWorkflow()
        result = make_executor().execute(workflow)
        assert result.status == AutomationStatus.SUCCESS
        assert dict(workflow.execute_calls[0].parameters) == {}
