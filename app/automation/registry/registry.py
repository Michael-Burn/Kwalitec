"""AutomationRegistry — workflow catalog (no execution)."""

from __future__ import annotations

from app.automation.dto.metadata import WorkflowMetadata
from app.automation.dto.validation import DuplicateWorkflowError, UnknownWorkflowError
from app.automation.workflows.protocols import AutomationTask


class AutomationRegistry:
    """Register and look up automation workflows.

    Responsibilities:
    - Register workflows
    - Lookup workflows
    - Prevent duplicate registrations
    - Return immutable workflow metadata

    Does not execute workflows.
    """

    def __init__(self) -> None:
        self._workflows: dict[str, AutomationTask] = {}

    def register(self, workflow: AutomationTask) -> None:
        """Register ``workflow`` under its stable id.

        Args:
            workflow: AutomationTask implementation.

        Raises:
            DuplicateWorkflowError: When ``workflow.id`` is already registered.
            ValueError: When workflow id / name / description is empty.
        """
        workflow_id = str(getattr(workflow, "id", "") or "").strip()
        if not workflow_id:
            raise ValueError("automation workflow id must be a non-empty string")
        name = str(getattr(workflow, "name", "") or "").strip()
        if not name:
            raise ValueError(
                f"automation workflow {workflow_id!r} name must be non-empty"
            )
        description = str(getattr(workflow, "description", "") or "").strip()
        if not description:
            raise ValueError(
                f"automation workflow {workflow_id!r} description must be non-empty"
            )
        if workflow_id in self._workflows:
            raise DuplicateWorkflowError(workflow_id)
        self._workflows[workflow_id] = workflow

    def get(self, workflow_id: str) -> AutomationTask:
        """Return the registered workflow instance.

        Raises:
            UnknownWorkflowError: When ``workflow_id`` is not registered.
        """
        try:
            return self._workflows[workflow_id]
        except KeyError as exc:
            raise UnknownWorkflowError(workflow_id) from exc

    def contains(self, workflow_id: str) -> bool:
        """Return True when ``workflow_id`` is registered."""

        return workflow_id in self._workflows

    def metadata(self, workflow_id: str) -> WorkflowMetadata:
        """Return immutable metadata for ``workflow_id``.

        Raises:
            UnknownWorkflowError: When ``workflow_id`` is not registered.
        """
        workflow = self.get(workflow_id)
        return WorkflowMetadata(
            id=workflow.id,
            name=workflow.name,
            description=workflow.description,
        )

    def list_metadata(self) -> tuple[WorkflowMetadata, ...]:
        """Return immutable metadata for all registered workflows (sorted by id)."""

        return tuple(
            WorkflowMetadata(
                id=workflow.id,
                name=workflow.name,
                description=workflow.description,
            )
            for workflow_id, workflow in sorted(self._workflows.items())
        )

    def workflow_ids(self) -> tuple[str, ...]:
        """Return registered workflow ids in sorted order."""

        return tuple(sorted(self._workflows))
