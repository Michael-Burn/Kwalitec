"""Kwalitec Automation Framework (FSI-004).

Deterministic, manually triggered execution of registered automation
workflows. Platform subsystem — generic; Founder workflows are the first
registered consumers.

No scheduling, background jobs, file watching, or AI.
"""

from __future__ import annotations

from app.automation.dto import (
    AutomationValidationError,
    DuplicateWorkflowError,
    UnknownWorkflowError,
    ValidationIssue,
    ValidationReport,
    WorkflowMetadata,
)
from app.automation.executors import AutomationExecutor
from app.automation.models import (
    AutomationContext,
    AutomationResult,
    AutomationStatus,
    WorkflowExecutionPayload,
)
from app.automation.registry import AutomationRegistry, build_default_registry
from app.automation.services import AutomationService
from app.automation.workflows import AutomationTask

__all__ = [
    "AutomationContext",
    "AutomationExecutor",
    "AutomationRegistry",
    "AutomationResult",
    "AutomationService",
    "AutomationStatus",
    "AutomationTask",
    "AutomationValidationError",
    "DuplicateWorkflowError",
    "UnknownWorkflowError",
    "ValidationIssue",
    "ValidationReport",
    "WorkflowExecutionPayload",
    "WorkflowMetadata",
    "build_default_registry",
]
