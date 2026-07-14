"""Domain models for the Automation Framework."""

from __future__ import annotations

from app.automation.models.context import AutomationContext
from app.automation.models.payload import WorkflowExecutionPayload
from app.automation.models.result import AutomationResult, AutomationStatus

__all__ = [
    "AutomationContext",
    "AutomationResult",
    "AutomationStatus",
    "WorkflowExecutionPayload",
]
