"""Default registry bootstrap — registers Version 1 workflows."""

from __future__ import annotations

from app.automation.registry.registry import AutomationRegistry
from app.automation.workflows.founder_internal_alpha import (
    InternalAlphaAutomationWorkflow,
)


def build_default_registry() -> AutomationRegistry:
    """Return a registry with Version 1 platform workflows registered.

    Currently registers:
    - founder.internal_alpha.workflow (Internal Alpha Live Workflow)
    """
    registry = AutomationRegistry()
    registry.register(InternalAlphaAutomationWorkflow())
    return registry
