"""Orchestration service — coordinates Educational Core execution order.

Never performs educational reasoning. Delegates port calls to the
WorkflowExecutor according to OrchestrationPolicy step order.
"""

from __future__ import annotations

from app.application.education_platform.dependency_registry import DependencyRegistry
from app.application.education_platform.dto.education_request import EducationRequest
from app.application.education_platform.dto.education_response import EducationResponse
from app.application.education_platform.exceptions import OrchestrationError
from app.application.education_platform.platform_validator import PlatformValidator
from app.application.education_platform.policies.orchestration_policy import (
    OrchestrationPolicy,
)
from app.application.education_platform.workflow_executor import WorkflowExecutor


class OrchestrationService:
    """Coordinate workflow execution across registered ports.

    Owns execution order only — educational decisions stay in engines.
    """

    def __init__(
        self,
        *,
        registry: DependencyRegistry,
        executor: WorkflowExecutor | None = None,
        validator: PlatformValidator | None = None,
    ) -> None:
        self._registry = registry
        self._executor = executor or WorkflowExecutor()
        self._validator = validator or PlatformValidator()

    def execute(self, request: EducationRequest) -> EducationResponse:
        """Execute ``request.workflow`` in policy-defined port order.

        Raises:
            OrchestrationError: Unknown workflow.
            ValidationError: Workflow not ready / ports unavailable.
        """
        workflow = request.workflow
        if not OrchestrationPolicy.is_known_workflow(workflow):
            raise OrchestrationError(f"Unknown workflow: {workflow!r}")
        self._validator.require_workflow(self._registry, workflow)
        steps = OrchestrationPolicy.steps_for(workflow)
        return self._executor.run(
            request=request,
            steps=steps,
            registry=self._registry,
        )
