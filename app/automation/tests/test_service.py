"""Tests for AutomationService."""

from __future__ import annotations

from app.automation.models import AutomationStatus
from app.automation.registry import AutomationRegistry
from app.automation.tests.helpers import (
    MockWorkflow,
    failing_validation,
    make_context,
    make_payload,
    make_service,
)


class TestAutomationService:
    def test_run_by_id(self) -> None:
        workflow = MockWorkflow(
            workflow_id="svc.run",
            payload=make_payload({"ran": True}),
        )
        service = make_service(workflow)
        result = service.run("svc.run", make_context(flag=True))
        assert result.status == AutomationStatus.SUCCESS
        assert dict(result.outputs) == {"ran": True}

    def test_unknown_workflow_returns_failed_result(self) -> None:
        service = make_service()
        result = service.run("does.not.exist")
        assert result.status == AutomationStatus.FAILED
        assert result.workflow_id == "does.not.exist"
        assert result.errors
        assert "unknown automation workflow" in result.errors[0]

    def test_validation_failure_via_service(self) -> None:
        workflow = MockWorkflow(
            workflow_id="svc.invalid",
            validate_report=failing_validation(code="nope"),
        )
        result = make_service(workflow).run("svc.invalid")
        assert result.status == AutomationStatus.FAILED
        assert "nope" in result.errors[0]

    def test_empty_registry_service(self) -> None:
        service = make_service(registry=AutomationRegistry())
        result = service.run("any.id")
        assert result.status == AutomationStatus.FAILED
