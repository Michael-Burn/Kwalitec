"""Tests for AutomationRegistry."""

from __future__ import annotations

import pytest

from app.automation.dto import DuplicateWorkflowError, UnknownWorkflowError
from app.automation.registry import AutomationRegistry
from app.automation.tests.helpers import MockWorkflow, make_registry


class TestAutomationRegistry:
    def test_register_and_get(self) -> None:
        workflow = MockWorkflow(workflow_id="alpha.one")
        registry = make_registry(workflow)
        assert registry.get("alpha.one") is workflow
        assert registry.contains("alpha.one")

    def test_duplicate_registration_raises(self) -> None:
        workflow = MockWorkflow(workflow_id="dup.id")
        registry = make_registry(workflow)
        with pytest.raises(DuplicateWorkflowError) as exc_info:
            registry.register(MockWorkflow(workflow_id="dup.id", name="Other"))
        assert exc_info.value.workflow_id == "dup.id"

    def test_unknown_lookup_raises(self) -> None:
        registry = AutomationRegistry()
        with pytest.raises(UnknownWorkflowError) as exc_info:
            registry.get("missing.id")
        assert exc_info.value.workflow_id == "missing.id"

    def test_metadata_is_immutable_snapshot(self) -> None:
        workflow = MockWorkflow(
            workflow_id="meta.id",
            name="Meta",
            description="Metadata check",
        )
        registry = make_registry(workflow)
        meta = registry.metadata("meta.id")
        assert meta.id == "meta.id"
        assert meta.name == "Meta"
        assert meta.description == "Metadata check"

    def test_list_metadata_sorted_by_id(self) -> None:
        registry = make_registry(
            MockWorkflow(workflow_id="z.workflow"),
            MockWorkflow(workflow_id="a.workflow"),
        )
        ids = [item.id for item in registry.list_metadata()]
        assert ids == ["a.workflow", "z.workflow"]

    def test_empty_id_rejected(self) -> None:
        registry = AutomationRegistry()
        with pytest.raises(ValueError, match="id must be"):
            registry.register(MockWorkflow(workflow_id="  "))

    def test_empty_name_rejected(self) -> None:
        registry = AutomationRegistry()
        with pytest.raises(ValueError, match="name must be"):
            registry.register(MockWorkflow(name=""))
