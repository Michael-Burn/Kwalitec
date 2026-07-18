"""Analytics pipeline — final observation stage of the live-learner chain."""

from __future__ import annotations

import time
from types import MappingProxyType

from app.application.learning_orchestrator.dto.orchestration_request import (
    OrchestrationRequest,
)
from app.application.learning_orchestrator.exceptions import (
    PortError,
    PortUnavailable,
)
from app.application.learning_orchestrator.policies.retry_policy import (
    RetryPolicy,
)
from app.application.learning_orchestrator.ports.analytics_port import (
    AnalyticsPort,
)
from app.domain.learning_orchestrator.orchestration_context import (
    OrchestrationContext,
)
from app.domain.learning_orchestrator.pipeline_result import PipelineResult
from app.domain.learning_orchestrator.pipeline_stage import PipelineStageName


class AnalyticsPipeline:
    """Invoke the AnalyticsPort with accumulated stage payloads."""

    STAGE = PipelineStageName.ANALYTICS

    def __init__(
        self,
        port: AnalyticsPort | None = None,
        *,
        retry_policy: RetryPolicy | None = None,
    ) -> None:
        self._port = port
        self._retry = retry_policy or RetryPolicy.none()

    @property
    def port(self) -> AnalyticsPort | None:
        """Currently bound analytics port (may be None)."""
        return self._port

    def bind(self, port: AnalyticsPort) -> None:
        """Replace the bound analytics port."""
        self._port = port

    def execute(
        self,
        request: OrchestrationRequest,
        context: OrchestrationContext,
    ) -> PipelineResult:
        """Record orchestration observation for ``request``."""
        if self._port is None:
            return PipelineResult.failure(
                self.STAGE,
                error="AnalyticsPort is not bound",
                diagnostics={"component": "analytics"},
            )
        stage_payloads = {
            k: dict(v) if isinstance(v, dict | MappingProxyType) else v
            for k, v in dict(context.stage_payloads or {}).items()
        }
        execution_summary = {
            "orchestration_id": context.orchestration_id,
            "event_id": context.event.event_id,
            "learner_id": context.learner_id,
            "event_type": context.event.event_type.value,
            "executed_stages": [s.value for s in context.executed_stages],
            "warnings": list(context.warnings),
        }
        return self._call_with_retry(
            request, stage_payloads, execution_summary
        )

    def _call_with_retry(
        self,
        request: OrchestrationRequest,
        stage_payloads: dict,
        execution_summary: dict,
    ) -> PipelineResult:
        assert self._port is not None
        attempt = 0
        last_error = "unknown"
        started = time.perf_counter()
        while True:
            attempt += 1
            try:
                if not self._port.is_available():
                    raise PortUnavailable("AnalyticsPort is unavailable")
                payload = self._port.record_execution(
                    request,
                    stage_payloads=stage_payloads,
                    execution_summary=execution_summary,
                )
                if not isinstance(payload, dict):
                    raise PortError(
                        "AnalyticsPort.record_execution must return a dict"
                    )
                duration_ms = (time.perf_counter() - started) * 1000.0
                return PipelineResult.success(
                    self.STAGE,
                    duration_ms=duration_ms,
                    payload=payload,
                    diagnostics={
                        "component": "analytics",
                        "component_version": self._port.component_version,
                        "attempt_count": attempt,
                    },
                    attempt_count=attempt,
                )
            except PortUnavailable as exc:
                last_error = str(exc)
                if not self._retry.should_retry(
                    attempt=attempt, error_kind="unavailable"
                ):
                    break
            except PortError as exc:
                last_error = str(exc)
                if not self._retry.should_retry(
                    attempt=attempt, error_kind="port_error"
                ):
                    break
            except Exception as exc:  # noqa: BLE001 — isolate port failures
                last_error = f"{type(exc).__name__}: {exc}"
                if not self._retry.should_retry(
                    attempt=attempt, error_kind="other"
                ):
                    break
        duration_ms = (time.perf_counter() - started) * 1000.0
        return PipelineResult.failure(
            self.STAGE,
            error=last_error,
            duration_ms=duration_ms,
            diagnostics={"component": "analytics", "attempt_count": attempt},
            attempt_count=attempt,
        )

    def skip(self, reason: str) -> PipelineResult:
        """Return a skipped stage result."""
        return PipelineResult.skip(self.STAGE, reason=reason)
