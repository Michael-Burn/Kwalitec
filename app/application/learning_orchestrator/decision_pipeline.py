"""Decision pipeline — Adaptive Decision Engine stage."""

from __future__ import annotations

import time

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
from app.application.learning_orchestrator.ports.adaptive_learning_port import (
    AdaptiveLearningPort,
)
from app.domain.learning_orchestrator.orchestration_context import (
    OrchestrationContext,
)
from app.domain.learning_orchestrator.pipeline_result import PipelineResult
from app.domain.learning_orchestrator.pipeline_stage import PipelineStageName


class DecisionPipeline:
    """Invoke the AdaptiveLearningPort with Twin + evidence payloads."""

    STAGE = PipelineStageName.DECISION

    def __init__(
        self,
        port: AdaptiveLearningPort | None = None,
        *,
        retry_policy: RetryPolicy | None = None,
    ) -> None:
        self._port = port
        self._retry = retry_policy or RetryPolicy.none()

    @property
    def port(self) -> AdaptiveLearningPort | None:
        """Currently bound adaptive learning port (may be None)."""
        return self._port

    def bind(self, port: AdaptiveLearningPort) -> None:
        """Replace the bound adaptive learning port."""
        self._port = port

    def execute(
        self,
        request: OrchestrationRequest,
        context: OrchestrationContext,
    ) -> PipelineResult:
        """Run adaptive decision for ``request``."""
        if self._port is None:
            return PipelineResult.failure(
                self.STAGE,
                error="AdaptiveLearningPort is not bound",
                diagnostics={"component": "adaptive_learning"},
            )
        twin_payload = dict(context.payload_for(PipelineStageName.TWIN))
        evidence_payload = dict(
            context.payload_for(PipelineStageName.EVIDENCE)
        )
        return self._call_with_retry(request, twin_payload, evidence_payload)

    def _call_with_retry(
        self,
        request: OrchestrationRequest,
        twin_payload: dict,
        evidence_payload: dict,
    ) -> PipelineResult:
        assert self._port is not None
        attempt = 0
        last_error = "unknown"
        started = time.perf_counter()
        while True:
            attempt += 1
            try:
                if not self._port.is_available():
                    raise PortUnavailable(
                        "AdaptiveLearningPort is unavailable"
                    )
                payload = self._port.decide(
                    request,
                    twin_payload=twin_payload,
                    evidence_payload=evidence_payload,
                )
                if not isinstance(payload, dict):
                    raise PortError(
                        "AdaptiveLearningPort.decide must return a dict"
                    )
                duration_ms = (time.perf_counter() - started) * 1000.0
                return PipelineResult.success(
                    self.STAGE,
                    duration_ms=duration_ms,
                    payload=payload,
                    diagnostics={
                        "component": "adaptive_learning",
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
            diagnostics={
                "component": "adaptive_learning",
                "attempt_count": attempt,
            },
            attempt_count=attempt,
        )

    def skip(self, reason: str) -> PipelineResult:
        """Return a skipped stage result."""
        return PipelineResult.skip(self.STAGE, reason=reason)
