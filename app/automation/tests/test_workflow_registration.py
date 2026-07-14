"""Tests for Founder workflow registration (no Founder execution)."""

from __future__ import annotations

import pytest

from app.automation.dto import DuplicateWorkflowError
from app.automation.registry import build_default_registry
from app.automation.workflows import (
    FOUNDER_INTERNAL_ALPHA_WORKFLOW_ID,
    InternalAlphaAutomationWorkflow,
)


class TestWorkflowRegistration:
    def test_default_registry_includes_internal_alpha(self) -> None:
        registry = build_default_registry()
        assert registry.contains(FOUNDER_INTERNAL_ALPHA_WORKFLOW_ID)
        meta = registry.metadata(FOUNDER_INTERNAL_ALPHA_WORKFLOW_ID)
        assert meta.id == "founder.internal_alpha.workflow"
        assert meta.name == "Internal Alpha Live Workflow"
        assert "Internal Alpha" in meta.description

    def test_registered_instance_is_adapter(self) -> None:
        registry = build_default_registry()
        workflow = registry.get(FOUNDER_INTERNAL_ALPHA_WORKFLOW_ID)
        assert isinstance(workflow, InternalAlphaAutomationWorkflow)

    def test_duplicate_founder_registration_blocked(self) -> None:
        registry = build_default_registry()
        with pytest.raises(DuplicateWorkflowError) as exc_info:
            registry.register(InternalAlphaAutomationWorkflow())
        assert exc_info.value.workflow_id == FOUNDER_INTERNAL_ALPHA_WORKFLOW_ID
