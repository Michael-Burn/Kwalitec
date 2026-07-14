"""DTO cargo for the Automation Framework."""

from __future__ import annotations

from app.automation.dto.metadata import WorkflowMetadata
from app.automation.dto.validation import (
    AutomationValidationError,
    DuplicateWorkflowError,
    UnknownWorkflowError,
    ValidationIssue,
    ValidationReport,
)

__all__ = [
    "AutomationValidationError",
    "DuplicateWorkflowError",
    "UnknownWorkflowError",
    "ValidationIssue",
    "ValidationReport",
    "WorkflowMetadata",
]
