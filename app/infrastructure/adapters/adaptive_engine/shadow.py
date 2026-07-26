"""Adaptive Shadow Execution orchestrator (MS-003 A2 / A3).

Pipeline:
  Runtime A → AdaptiveInputAssembler → AdaptiveEngineExecutor
  → AdaptiveOutputBundle → ExplainabilityGate (optional A3)
  → Discard (observational only)

Shadow outputs may be logged, measured, compared, and validated.
They must NOT change recommendations, missions, planning, Runtime A,
or Experience behaviour.
"""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING, Any

from app.infrastructure.adapters.adaptive_engine import shadow_telemetry as telemetry
from app.infrastructure.adapters.adaptive_engine.contracts import (
    INVALID_STATE,
    UNAVAILABLE,
    AdaptiveDecisionResult,
    AdaptiveInputBundle,
    AdaptiveOutputBundle,
)
from app.infrastructure.adapters.adaptive_engine.executor import AdaptiveEngineExecutor
from app.infrastructure.events.registry import EventRegistry

if TYPE_CHECKING:
    from app.infrastructure.adapters.adaptive_engine.gate import (
        ExplainabilityGate,
        ExplainabilityGateResult,
    )

logger = logging.getLogger(__name__)


def explanation_is_complete(output: AdaptiveOutputBundle) -> bool:
    """Return True when ExplanationBundle has required A2 facets populated."""
    explanation = output.explanation
    if not explanation.rule_refs:
        return False
    if explanation.confidence.band == "" and explanation.confidence.score is None:
        return False
    # Inputs accounting always required (may be empty tuples when provenance absent).
    if explanation.inputs_used is None or explanation.inputs_unavailable is None:
        return False
    if not (explanation.recommendation_rationale or explanation.why_summary):
        return False
    return True


class AdaptiveShadowOrchestrator:
    """Assemble → execute → optional Explainability Gate → telemetry → discard.

    Observational only. Callers may inspect the returned AdaptiveDecisionResult
    for measurement; Experience / Runtime A paths must ignore it.
    """

    ORCHESTRATOR_ID = "adaptive_shadow_orchestrator"
    ORCHESTRATOR_VERSION = "1.0.0-a3"

    def __init__(
        self,
        *,
        assembler: Any,
        executor: AdaptiveEngineExecutor,
        events: EventRegistry | None = None,
        enabled: bool = True,
        explainability_gate: ExplainabilityGate | None = None,
        traceability: Any | None = None,
    ) -> None:
        self._assembler = assembler
        self._executor = executor
        self._events = events or EventRegistry()
        self._enabled = bool(enabled)
        self._explainability_gate = explainability_gate
        self._traceability = traceability
        self._last_gate_result: ExplainabilityGateResult | None = None
        self._last_trace: Any | None = None

    @property
    def orchestrator_id(self) -> str:
        return self.ORCHESTRATOR_ID

    @property
    def orchestrator_version(self) -> str:
        return self.ORCHESTRATOR_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    @property
    def explainability_gate(self) -> ExplainabilityGate | None:
        return self._explainability_gate

    @property
    def last_gate_result(self) -> ExplainabilityGateResult | None:
        """Most recent A3 gate result (observational; not Experience authority)."""
        return self._last_gate_result

    @property
    def last_trace(self) -> Any | None:
        """Most recent A5 DecisionTrace (observational; no educational writes)."""
        return self._last_trace

    def execute_shadow(
        self,
        student_id: str,
        *,
        as_of: str | None = None,
        inputs: AdaptiveInputBundle | None = None,
    ) -> AdaptiveDecisionResult:
        """Run shadow pipeline and emit observational telemetry.

        The AdaptiveOutputBundle is returned for observation only — it must not
        be fed into Experience AdaptiveDecisionPort or Runtime A writes.
        When an ExplainabilityGate is wired (A3), validation runs without
        mutation; failed bundles remain observational only.
        """
        from app.infrastructure.adapters.adaptive_engine.traceability import (
            AUTHORITY_FAILED,
            AUTHORITY_SHADOW_ONLY,
            DELIVERY_NONE,
            DELIVERY_SHADOW_ONLY,
            ROUTING_FAILED,
            ROUTING_SHADOW_ONLY,
            resolve_correlation_id,
        )
        from app.infrastructure.diagnostics.correlation import CorrelationContext

        sid = (student_id or "").strip()
        self._last_gate_result = None
        self._last_trace = None
        if not sid:
            return AdaptiveDecisionResult(
                ok=False,
                error_code=INVALID_STATE,
                message="student_id must be a non-empty string",
            )
        if not self._enabled:
            return AdaptiveDecisionResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="Adaptive shadow execution is disabled (feature flag OFF)",
            )

        correlation_id = resolve_correlation_id(None)
        with CorrelationContext.bind(correlation_id=correlation_id):
            return self._execute_shadow_bound(
                sid,
                as_of=as_of,
                inputs=inputs,
                correlation_id=correlation_id,
                authority_status=AUTHORITY_SHADOW_ONLY,
                routing_decision=ROUTING_SHADOW_ONLY,
                delivery_status=DELIVERY_SHADOW_ONLY,
                failed_authority=AUTHORITY_FAILED,
                failed_routing=ROUTING_FAILED,
                failed_delivery=DELIVERY_NONE,
            )

    def _execute_shadow_bound(
        self,
        sid: str,
        *,
        as_of: str | None,
        inputs: AdaptiveInputBundle | None,
        correlation_id: str,
        authority_status: str,
        routing_decision: str,
        delivery_status: str,
        failed_authority: str,
        failed_routing: str,
        failed_delivery: str,
    ) -> AdaptiveDecisionResult:
        telemetry.emit_requested(self._events, student_id=sid, as_of=as_of)
        started = time.perf_counter()
        ok = False
        bundle: AdaptiveInputBundle | None = inputs
        try:
            if bundle is None:
                if self._assembler is None:
                    raise RuntimeError("AdaptiveInputAssembler is not configured")
                bundle = self._assembler.assemble(sid, as_of=as_of)
            if not isinstance(bundle, AdaptiveInputBundle):
                raise TypeError("assembled inputs must be an AdaptiveInputBundle")
            if bundle.student_id != sid:
                return AdaptiveDecisionResult(
                    ok=False,
                    error_code=INVALID_STATE,
                    message="inputs.student_id must match student_id",
                )

            output = self._executor.evaluate(bundle)
            before_gate = output.serialize()
            if self._explainability_gate is not None:
                self._last_gate_result = self._explainability_gate.validate(
                    output,
                    student_id=sid,
                )
                # Gate must never mutate the AdaptiveOutputBundle.
                if output.serialize() != before_gate:
                    raise RuntimeError(
                        "ExplainabilityGate mutated AdaptiveOutputBundle"
                    )
            complete = explanation_is_complete(output)
            if self._last_gate_result is not None:
                complete = complete and self._last_gate_result.passed
            telemetry.emit_completed(
                self._events,
                student_id=sid,
                decision_id=output.decision_id,
                topic_code=output.recommendation.topic_code,
                decision_kind=output.recommendation.decision_kind,
                confidence_band=output.confidence.band,
                explainability_complete=complete,
            )
            if self._traceability is not None:
                self._last_trace = self._traceability.record_decision(
                    student_id=sid,
                    inputs=bundle,
                    output=output,
                    gate_result=self._last_gate_result,
                    authority_status=authority_status,
                    routing_decision=routing_decision,
                    delivery_status=delivery_status,
                    correlation_id=correlation_id,
                    engine_version=self._executor.EXECUTOR_VERSION,
                )
            ok = True
            # Explicit discard contract: result is observational; no UX wiring.
            logger.debug(
                "adaptive shadow completed student_id=%s decision_id=%s "
                "discarded=1 gate_passed=%s",
                sid,
                output.decision_id,
                None
                if self._last_gate_result is None
                else self._last_gate_result.passed,
            )
            return AdaptiveDecisionResult(ok=True, value=output)
        except Exception as exc:  # noqa: BLE001 — shadow must not raise into UX
            logger.debug(
                "adaptive shadow failed student_id=%s", sid, exc_info=True
            )
            error_code = type(exc).__name__
            telemetry.emit_failed(
                self._events,
                student_id=sid,
                error_code=error_code,
                message=str(exc),
            )
            if self._traceability is not None:
                self._last_trace = self._traceability.record_decision(
                    student_id=sid,
                    inputs=bundle if isinstance(bundle, AdaptiveInputBundle) else None,
                    output=None,
                    gate_result=self._last_gate_result,
                    authority_status=failed_authority,
                    routing_decision=failed_routing,
                    delivery_status=failed_delivery,
                    correlation_id=correlation_id,
                    engine_version=self._executor.EXECUTOR_VERSION,
                    error_code=error_code,
                    message=str(exc)[:256],
                )
            return AdaptiveDecisionResult(
                ok=False,
                error_code=error_code,
                message=str(exc)[:256],
            )
        finally:
            latency_ms = (time.perf_counter() - started) * 1000.0
            telemetry.emit_latency(
                self._events,
                student_id=sid,
                latency_ms=latency_ms,
                ok=ok,
            )


def build_adaptive_shadow_orchestrator(
    *,
    enabled: bool,
    assembler: Any | None,
    executor: AdaptiveEngineExecutor | None,
    events: EventRegistry | None = None,
    explainability_gate: ExplainabilityGate | None = None,
    traceability: Any | None = None,
) -> AdaptiveShadowOrchestrator | None:
    """DI helper — construct shadow orchestrator only when shadow flag is on."""
    if not enabled or assembler is None or executor is None:
        return None
    return AdaptiveShadowOrchestrator(
        assembler=assembler,
        executor=executor,
        events=events,
        enabled=True,
        explainability_gate=explainability_gate,
        traceability=traceability,
    )
