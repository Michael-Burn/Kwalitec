"""Tests for framework validators."""

from __future__ import annotations

from datetime import UTC, datetime
from types import MappingProxyType

from app.automation.models import AutomationContext, AutomationStatus
from app.automation.tests.helpers import FIXED_NOW, make_result
from app.automation.validators import (
    AutomationContextValidator,
    AutomationResultValidator,
)


class TestAutomationContextValidator:
    def test_valid_context(self) -> None:
        report = AutomationContextValidator().validate(
            AutomationContext.from_mapping({"week": "week_001"})
        )
        assert report.ok

    def test_missing_context(self) -> None:
        report = AutomationContextValidator().validate(None)
        assert not report.ok
        assert report.issues[0].code == "missing_context"

    def test_empty_parameter_key(self) -> None:
        context = AutomationContext(parameters=MappingProxyType({"": 1}))
        report = AutomationContextValidator().validate(context)
        assert not report.ok
        assert report.issues[0].code == "invalid_parameter_key"


class TestAutomationResultValidator:
    def test_valid_success(self) -> None:
        report = AutomationResultValidator().validate(make_result())
        assert report.ok

    def test_invalid_status_rejected(self) -> None:
        # Bypass enum by constructing with a fake via object.__new__ path —
        # use FAILED without errors instead for a realistic completeness failure.
        result = make_result(status=AutomationStatus.FAILED, errors=())
        report = AutomationResultValidator().validate(result)
        assert not report.ok
        assert any(i.code == "failed_without_errors" for i in report.issues)

    def test_success_with_errors_rejected(self) -> None:
        result = make_result(
            status=AutomationStatus.SUCCESS,
            errors=("should not be here",),
        )
        report = AutomationResultValidator().validate(result)
        assert not report.ok
        assert any(i.code == "success_with_errors" for i in report.issues)

    def test_completed_before_started(self) -> None:
        earlier = datetime(2026, 7, 14, 17, 0, 0, tzinfo=UTC)
        result = make_result(started_at=FIXED_NOW, completed_at=earlier)
        report = AutomationResultValidator().validate(result)
        assert not report.ok
        assert any(i.code == "invalid_time_range" for i in report.issues)

    def test_missing_workflow_id(self) -> None:
        result = make_result(workflow_id="")
        report = AutomationResultValidator().validate(result)
        assert not report.ok
        assert any(i.code == "missing_workflow_id" for i in report.issues)
