"""Twin pipeline — Digital Twin stage of the live-learner chain."""

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
from app.application.learning_orchestrator.ports.twin_port import TwinPort
from app.domain.learning_orchestrator.orchestration_context import (
    OrchestrationContext,
)
from app.domain.learning_orchestrator.pipeline_result import PipelineResult
from app.domain.learning_orchestrator.pipeline_stage import PipelineStageName


class TwinPipeline:
    """Invoke the TwinPort with prior evidence payload."""

    STAGE = PipelineStageName.TWIN

    def __init__(
        self,
        port: TwinPort | None = None,
        *,
        retry_policy: RetryPolicy | None = None,
    ) -> None:
        self._port = port
        self._retry = retry_policy or RetryPolicy.none()

    @property
    def port(self) -> TwinPort | None:
        """Currently bound Twin port (may be None)."""
        return self._port

    def bind(self, port: TwinPort) -> None:
        """Replace the bound Twin port."""
        self._port = port

    def execute(
        self,
        request: OrchestrationRequest,
        context: OrchestrationContext,
    ) -> PipelineResult:
        """Run Twin update for ``request`` using evidence payload."""
        if self._port is None:
            return PipelineResult.failure(
                self.STAGE,
                error="TwinPort is not bound",
                diagnostics={"component": "twin"},
            )
        evidence_payload = dict(
            context.payload_for(PipelineStageName.EVIDENCE)
        )
        return self._call_with_retry(request, evidence_payload)

    def _call_with_retry(
        self,
        request: OrchestrationRequest,
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
                    raise PortUnavailable("TwinPort is unavailable")
                payload = self._port.update_from_evidence(
                    request, evidence_payload=evidence_payload
                )
                if not isinstance(payload, dict):
                    raise PortError(
                        "TwinPort.update_from_evidence must return a dict"
                    )
                duration_ms = (time.perf_counter() - started) * 1000.0
                return PipelineResult.success(
                    self.STAGE,
                    duration_ms=duration_ms,
                    payload=payload,
                    diagnostics={
                        "component": "twin",
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
            diagnostics={"component": "twin", "attempt_count": attempt},
            attempt_count=attempt,
        )

    def skip(self, reason: str) -> PipelineResult:
        """Return a skipped stage result."""
        return PipelineResult.skip(self.STAGE, reason=reason)
