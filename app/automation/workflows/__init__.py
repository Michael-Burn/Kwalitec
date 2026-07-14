"""Registered automation workflows and the AutomationTask protocol."""

from __future__ import annotations

from app.automation.workflows.founder_internal_alpha import (
    FOUNDER_INTERNAL_ALPHA_WORKFLOW_ID,
    InternalAlphaAutomationWorkflow,
)
from app.automation.workflows.protocols import AutomationTask

__all__ = [
    "FOUNDER_INTERNAL_ALPHA_WORKFLOW_ID",
    "AutomationTask",
    "InternalAlphaAutomationWorkflow",
]
