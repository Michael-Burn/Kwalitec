"""AutomationService — public coordinator for workflow execution."""

from __future__ import annotations

from datetime import UTC, datetime
from types import MappingProxyType

from app.automation.dto.validation import UnknownWorkflowError
from app.automation.executors.executor import AutomationExecutor
from app.automation.models.context import AutomationContext
from app.automation.models.result import AutomationResult, AutomationStatus
from app.automation.registry.bootstrap import build_default_registry
from app.automation.registry.registry import AutomationRegistry


class AutomationService:
    """Run a registered automation workflow by id.

    Coordinator only — registry lookup + executor delegation.
    """

    def __init__(
        self,
        *,
        registry: AutomationRegistry | None = None,
        executor: AutomationExecutor | None = None,
    ) -> None:
        self._registry = registry if registry is not None else build_default_registry()
        self._executor = executor or AutomationExecutor()

    @property
    def registry(self) -> AutomationRegistry:
        """Expose the underlying registry (for metadata / listing)."""

        return self._registry

    def run(
        self,
        workflow_id: str,
        context: AutomationContext | None = None,
    ) -> AutomationResult:
        """Execute the workflow identified by ``workflow_id``.

        Args:
            workflow_id: Registered automation id.
            context: Optional execution inputs; defaults to empty context.

        Returns:
            AutomationResult from the executor. Unknown workflow ids yield a
            FAILED result (not an exception) for consistent caller handling.
        """
        try:
            workflow = self._registry.get(workflow_id)
        except UnknownWorkflowError as exc:
            now = datetime.now(UTC)
            return AutomationResult(
                workflow_id=workflow_id,
                status=AutomationStatus.FAILED,
                started_at=now,
                completed_at=now,
                duration_ms=0,
                warnings=(),
                errors=(str(exc),),
                outputs=MappingProxyType({}),
            )

        return self._executor.execute(workflow, context)

    def run_with_retries(
        self,
        workflow_id: str,
        context: AutomationContext | None = None,
        *,
        max_attempts: int = 3,
    ):
        """Execute ``workflow_id`` via JobRunner (retries + dead-letter).

        Returns the underlying AutomationResult on success, or the JobResult
        when dead-lettered.
        """
        from app.services.job_runner import JobRunner

        runner = JobRunner(max_attempts=max_attempts)
        job = runner.run(
            f"automation:{workflow_id}",
            lambda: self.run(workflow_id, context),
            payload={"workflow_id": workflow_id},
        )
        if job.status == "succeeded":
            return job.value
        return job
