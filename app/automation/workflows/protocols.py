"""AutomationTask protocol — every registered workflow must implement this."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from app.automation.dto.validation import ValidationReport
from app.automation.models.context import AutomationContext
from app.automation.models.payload import WorkflowExecutionPayload


@runtime_checkable
class AutomationTask(Protocol):
    """Executable automation workflow.

    Public interface is intentionally closed:
    id, name, description, validate(context), execute(context).
    """

    @property
    def id(self) -> str:
        """Stable unique workflow identifier."""

    @property
    def name(self) -> str:
        """Human-readable workflow name."""

    @property
    def description(self) -> str:
        """Short description of what the workflow does."""

    def validate(self, context: AutomationContext) -> ValidationReport:
        """Validate that ``context`` is acceptable for this workflow.

        Args:
            context: Immutable execution inputs.

        Returns:
            ValidationReport with ok=False when the run must not proceed.
        """

    def execute(self, context: AutomationContext) -> WorkflowExecutionPayload:
        """Run the workflow against ``context``.

        Args:
            context: Immutable execution inputs (already validated).

        Returns:
            WorkflowExecutionPayload with outputs, warnings, and errors.
        """
