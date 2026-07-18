"""Mission pipeline — Mission Engine stage of the live-learner chain."""

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
from app.application.learning_orchestrator.ports.mission_port import MissionPort
from app.domain.learning_orchestrator.orchestration_context import (
    OrchestrationContext,
)
from app.domain.learning_orchestrator.pipeline_result import PipelineResult
from app.domain.learning_orchestrator.pipeline_stage import PipelineStageName


class MissionPipeline:
    """Invoke the MissionPort with decision + Twin payloads."""

    STAGE = PipelineStageName.MISSION

    def __init__(
        self,
        port: MissionPort | None = None,
        *,
        retry_policy: RetryPolicy | None = None,
    ) -> None:
        self._port = port
        self._retry = retry_policy or RetryPolicy.none()

    @property
    def port(self) -> MissionPort | None:
        """Currently bound mission port (may be None)."""
        return self._port

    def bind(self, port: MissionPort) -> None:
        """Replace the bound mission port."""
        self._port = port

    def execute(
        self,
        request: OrchestrationRequest,
        context: OrchestrationContext,
    ) -> PipelineResult:
        """Run mission application for ``request``."""
        if self._port is None:
            return PipelineResult.failure(
                self.STAGE,
                error="MissionPort is not bound",
                diagnostics={"component": "mission"},
            )
        decision_payload = dict(
            context.payload_for(PipelineStageName.DECISION)
        )
        twin_payload = dict(context.payload_for(PipelineStageName.TWIN))
        return self._call_with_retry(request, decision_payload, twin_payload)

    def _call_with_retry(
        self,
        request: OrchestrationRequest,
        decision_payload: dict,
        twin_payload: dict,
    ) -> PipelineResult:
        assert self._port is not None
        attempt = 0
        last_error = "unknown"
        started = time.perf_counter()
        while True:
            attempt += 1
            try:
                if not self._port.is_available():
                    raise PortUnavailable("MissionPort is unavailable")
                payload = self._port.apply_decision(
                    request,
                    decision_payload=decision_payload,
                    twin_payload=twin_payload,
                )
                if not isinstance(payload, dict):
                    raise PortError(
                        "MissionPort.apply_decision must return a dict"
                    )
                duration_ms = (time.perf_counter() - started) * 1000.0
                return PipelineResult.success(
                    self.STAGE,
                    duration_ms=duration_ms,
                    payload=payload,
                    diagnostics={
                        "component": "mission",
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
            diagnostics={"component": "mission", "attempt_count": attempt},
            attempt_count=attempt,
        )

    def skip(self, reason: str) -> PipelineResult:
        """Return a skipped stage result."""
        return PipelineResult.skip(self.STAGE, reason=reason)
