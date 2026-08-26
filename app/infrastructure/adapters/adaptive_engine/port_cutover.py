"""Experience AdaptiveDecisionPort cutover routing (MS-003 A4).

Routing precedence:
  1. Default → RecommendationService (ExperienceAdaptiveAdapter prior path)
  2. ENGINE + SHADOW + AUTHORITY → attempt adaptive pipeline
  3. Explainability Gate PASS (eligible) → expose AdaptiveOutputBundle via port
  4. Gate FAIL / any adaptive failure → fallback to RecommendationService

Adaptive authority is disabled by default. Runtime A remains read-only.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from app.infrastructure.adapters.adaptive_engine import (
    port_cutover_telemetry as telemetry,
)
from app.infrastructure.adapters.adaptive_engine.contracts import (
    AUTHORITY_ADAPTIVE_ENGINE,
    AdaptiveInputBundle,
    AdaptiveOutputBundle,
)
from app.infrastructure.adapters.adaptive_engine.gate import ExplainabilityGateResult
from app.infrastructure.adapters.adaptive_engine.mission_alignment import (
    apply_mission_alignment_to_projection,
    resolve_mission_for_alignment,
    resolve_today_as_of,
)
from app.infrastructure.events.registry import EventRegistry

logger = logging.getLogger(__name__)


def adaptive_experience_cutover_active(
    *,
    engine_enabled: bool,
    shadow_enabled: bool,
    authority_enabled: bool,
) -> bool:
    """True when Experience may attempt adaptive recommendation routing."""
    return bool(engine_enabled and shadow_enabled and authority_enabled)


def map_adaptive_output_to_recommendation(
    output: AdaptiveOutputBundle,
    *,
    student_id: str,
    mission: Any | None = None,
) -> dict[str, Any] | None:
    """Project AdaptiveOutputBundle into Experience recommendation OpaqueDict.

    Compatible with Recommendation Bridge Home fields. Returns None when the
    bundle cannot form a student-facing recommendation label.

    When ``mission`` is provided (today's SQL mission), applies MS-001 hard
    override so the primary identity equals the mission regardless of the
    Engine's independent pick (Learning and Revision alike).
    """
    if not isinstance(output, AdaptiveOutputBundle):
        raise TypeError("output must be an AdaptiveOutputBundle")

    sid = (student_id or "").strip()
    if not sid:
        return None

    rec = output.recommendation
    explanation = output.explanation
    label = (
        (rec.label or "").strip()
        or (rec.title or "").strip()
        or (rec.topic_code or "").strip()
    )
    if not label:
        return None

    topic_title = (rec.title or "").strip() or label
    topic_code = (rec.topic_code or "").strip()
    summary = (
        (explanation.why_summary or "").strip()
        or (explanation.recommendation_rationale or "").strip()
        or label
    )
    mission_aligned = explanation.mission_aligned
    if mission_aligned is None:
        mission_aligned = False

    mission_id = None
    rule_or_model_ids = [
        str(ref.rule_or_model_id)
        for ref in (explanation.rule_refs or ())
        if (ref.rule_or_model_id or "").strip()
    ]
    alternatives: list[dict[str, Any]] = []
    for topic in explanation.topic_refs or ():
        code = (topic.topic_code or "").strip()
        title = (topic.title or "").strip()
        role = (topic.role or "").strip().lower()
        if role in {"primary", "selected", ""}:
            continue
        if not code and not title:
            continue
        alternatives.append(
            {
                "topic_code": code,
                "title": title or code,
                "recommendation_label": title or code,
                "reason": explanation.alternatives_rationale or "",
            }
        )

    explanation_payload = {
        "summary": summary,
        "authority": AUTHORITY_ADAPTIVE_ENGINE,
        "why_summary": explanation.why_summary,
        "recommendation_rationale": explanation.recommendation_rationale,
        "input_summary": explanation.input_summary,
        "mission_note": explanation.mission_note,
        "limitations_summary": explanation.limitations_summary,
        "inputs_used": list(explanation.inputs_used),
        "inputs_unavailable": list(explanation.inputs_unavailable),
        "rule_or_model_ids": rule_or_model_ids,
        "confidence": output.confidence.to_canonical_dict(),
        "evidence_refs": [
            ref.to_canonical_dict() for ref in (explanation.evidence_refs or ())
        ],
    }

    projected = {
        "student_id": sid,
        "decision_id": output.decision_id or "",
        "recommendation_label": label,
        "title": label,
        "topic_code": topic_code,
        "topic_title": topic_title,
        "summary": summary,
        "rationale": summary,
        "explanation_summary": summary,
        "estimated_minutes": None,
        "expected_benefit_delta": None,
        "expected_readiness_improvement": None,
        "mission_id": mission_id,
        "explanation": explanation_payload,
        "alternatives": alternatives,
        "authority": AUTHORITY_ADAPTIVE_ENGINE,
        "next_action_authority": True,
        "mission_aligned": bool(mission_aligned),
        "fallback_used": False,
        "confidence_score": output.confidence.score,
        "confidence_band": output.confidence.band,
        "category": (rec.decision_kind or "").strip() or "Adaptive",
        "priority": "",
        "expected_benefit": "",
        "rule_or_model_ids": rule_or_model_ids,
        "decision_kind": (rec.decision_kind or "").strip(),
    }
    return apply_mission_alignment_to_projection(projected, mission)


class AdaptiveExperiencePortRouter:
    """Attempt adaptive recommendation; fall back on ineligibility or failure.

    Does not mutate Runtime A. Does not rewrite RecommendationService.
    """

    ROUTER_ID = "adaptive_experience_port_router"
    ROUTER_VERSION = "1.0.0-a4"

    def __init__(
        self,
        *,
        assembler: Any | None = None,
        engine: Any | None = None,
        gate: Any | None = None,
        events: EventRegistry | None = None,
        cutover_active: bool = False,
        traceability: Any | None = None,
    ) -> None:
        self._assembler = assembler
        self._engine = engine
        self._gate = gate
        self._events = events or EventRegistry()
        self._cutover_active = bool(cutover_active)
        self._traceability = traceability
        self.last_gate_result: ExplainabilityGateResult | None = None
        self.last_fallback_reason: str | None = None
        self.last_trace: Any | None = None

    @property
    def router_id(self) -> str:
        return self.ROUTER_ID

    @property
    def cutover_active(self) -> bool:
        return self._cutover_active

    def try_adaptive_recommendation(
        self, student_id: str
    ) -> dict[str, Any] | None:
        """Return Experience-shaped adaptive recommendation when eligible.

        Returns None to signal automatic RecommendationService fallback.
        """
        from app.infrastructure.adapters.adaptive_engine.traceability import (
            AUTHORITY_ADAPTIVE_DELIVERED,
            AUTHORITY_FAILED,
            AUTHORITY_GATE_INELIGIBLE,
            AUTHORITY_RECOMMENDATION_FALLBACK,
            DELIVERY_DELIVERED,
            DELIVERY_NONE,
            ROUTING_AUTHORITATIVE,
            ROUTING_FAILED,
            ROUTING_FALLBACK,
            resolve_correlation_id,
        )
        from app.infrastructure.diagnostics.correlation import CorrelationContext

        sid = (student_id or "").strip()
        self.last_gate_result = None
        self.last_fallback_reason = None
        self.last_trace = None

        if not self._cutover_active:
            self.last_fallback_reason = "cutover_inactive"
            return None
        if not sid:
            self.last_fallback_reason = "invalid_student_id"
            return None
        if self._assembler is None or self._engine is None or self._gate is None:
            self.last_fallback_reason = "pipeline_unavailable"
            telemetry.emit_failure(
                self._events,
                student_id=sid,
                error_code="UNAVAILABLE",
                message="adaptive pipeline components missing",
            )
            return None

        correlation_id = resolve_correlation_id(None)
        with CorrelationContext.bind(correlation_id=correlation_id):
            return self._try_adaptive_bound(
                sid,
                correlation_id=correlation_id,
                statuses={
                    "delivered": AUTHORITY_ADAPTIVE_DELIVERED,
                    "gate": AUTHORITY_GATE_INELIGIBLE,
                    "fallback": AUTHORITY_RECOMMENDATION_FALLBACK,
                    "failed": AUTHORITY_FAILED,
                    "routing_authoritative": ROUTING_AUTHORITATIVE,
                    "routing_fallback": ROUTING_FALLBACK,
                    "routing_failed": ROUTING_FAILED,
                    "delivery_delivered": DELIVERY_DELIVERED,
                    "delivery_none": DELIVERY_NONE,
                },
            )

    def _record_trace(
        self,
        *,
        student_id: str,
        inputs: Any,
        output: AdaptiveOutputBundle | None,
        correlation_id: str,
        authority_status: str,
        routing_decision: str,
        delivery_status: str,
        error_code: str | None = None,
        message: str = "",
    ) -> None:
        if self._traceability is None:
            return
        engine_version = getattr(self._engine, "adapter_version", None) or "1.0.0-a4"
        self.last_trace = self._traceability.record_decision(
            student_id=student_id,
            inputs=inputs,
            output=output,
            gate_result=self.last_gate_result,
            authority_status=authority_status,
            routing_decision=routing_decision,
            delivery_status=delivery_status,
            correlation_id=correlation_id,
            engine_version=str(engine_version),
            error_code=error_code,
            message=message,
        )

    def _try_adaptive_bound(
        self,
        sid: str,
        *,
        correlation_id: str,
        statuses: dict[str, str],
    ) -> dict[str, Any] | None:
        telemetry.emit_requested(self._events, student_id=sid)
        started = time.perf_counter()
        inputs = None
        output: AdaptiveOutputBundle | None = None
        as_of = resolve_today_as_of()
        try:
            # Pass today's as_of so MissionCollector can populate mission.today
            # and RULE_MISSION_ALIGNED can fire (Authority previously omitted it).
            inputs = self._assembler.assemble(sid, as_of=as_of)
            decide = self._engine.decide(
                sid, inputs=inputs, include_explanation=True
            )
            decide_ok = getattr(decide, "ok", False)
            decide_value = getattr(decide, "value", None)
            if not decide_ok or decide_value is None:
                self.last_fallback_reason = "decide_failed"
                error_code = str(
                    getattr(decide, "error_code", None) or "UNAVAILABLE"
                )
                telemetry.emit_failure(
                    self._events,
                    student_id=sid,
                    error_code=error_code,
                    message=str(getattr(decide, "message", "") or "")[:256],
                )
                telemetry.emit_fallback(
                    self._events,
                    student_id=sid,
                    reason=self.last_fallback_reason,
                    error_code=error_code,
                )
                self._record_trace(
                    student_id=sid,
                    inputs=inputs,
                    output=None,
                    correlation_id=correlation_id,
                    authority_status=statuses["fallback"],
                    routing_decision=statuses["routing_fallback"],
                    delivery_status=statuses["delivery_none"],
                    error_code=error_code,
                    message=str(getattr(decide, "message", "") or "")[:256],
                )
                return None

            output = decide.value
            gate_result = self._gate.validate(output, student_id=sid)
            self.last_gate_result = gate_result
            if not gate_result.passed:
                self.last_fallback_reason = "explainability_ineligible"
                telemetry.emit_fallback(
                    self._events,
                    student_id=sid,
                    reason=self.last_fallback_reason,
                    error_code=gate_result.error_code or "EXPLAINABILITY_INCOMPLETE",
                    decision_id=gate_result.decision_id,
                )
                self._record_trace(
                    student_id=sid,
                    inputs=inputs,
                    output=output,
                    correlation_id=correlation_id,
                    authority_status=statuses["gate"],
                    routing_decision=statuses["routing_fallback"],
                    delivery_status=statuses["delivery_none"],
                    error_code=gate_result.error_code or "EXPLAINABILITY_INCOMPLETE",
                )
                return None

            mission = resolve_mission_for_alignment(
                sid,
                as_of=as_of,
                inputs=inputs if isinstance(inputs, AdaptiveInputBundle) else None,
            )
            projected = map_adaptive_output_to_recommendation(
                output, student_id=sid, mission=mission
            )
            if projected is None:
                self.last_fallback_reason = "projection_empty"
                telemetry.emit_fallback(
                    self._events,
                    student_id=sid,
                    reason=self.last_fallback_reason,
                    error_code="INVALID_STATE",
                    decision_id=output.decision_id,
                )
                self._record_trace(
                    student_id=sid,
                    inputs=inputs,
                    output=output,
                    correlation_id=correlation_id,
                    authority_status=statuses["fallback"],
                    routing_decision=statuses["routing_fallback"],
                    delivery_status=statuses["delivery_none"],
                    error_code="INVALID_STATE",
                    message="projection_empty",
                )
                return None

            telemetry.emit_success(
                self._events,
                student_id=sid,
                decision_id=str(projected.get("decision_id") or ""),
                confidence_band=str(projected.get("confidence_band") or ""),
                topic_code=str(projected.get("topic_code") or ""),
            )
            self._record_trace(
                student_id=sid,
                inputs=inputs,
                output=output,
                correlation_id=correlation_id,
                authority_status=statuses["delivered"],
                routing_decision=statuses["routing_authoritative"],
                delivery_status=statuses["delivery_delivered"],
            )
            return projected
        except Exception as exc:  # noqa: BLE001 — cutover must never degrade UX
            logger.exception(
                "adaptive experience cutover failed for student_id=%s", sid
            )
            self.last_fallback_reason = "adaptive_exception"
            telemetry.emit_failure(
                self._events,
                student_id=sid,
                error_code="UNAVAILABLE",
                message=str(exc)[:256],
            )
            telemetry.emit_fallback(
                self._events,
                student_id=sid,
                reason=self.last_fallback_reason,
                error_code="UNAVAILABLE",
            )
            self._record_trace(
                student_id=sid,
                inputs=inputs,
                output=output,
                correlation_id=correlation_id,
                authority_status=statuses["failed"],
                routing_decision=statuses["routing_failed"],
                delivery_status=statuses["delivery_none"],
                error_code="UNAVAILABLE",
                message=str(exc)[:256],
            )
            return None
        finally:
            latency_ms = (time.perf_counter() - started) * 1000.0
            telemetry.emit_latency(
                self._events,
                student_id=sid,
                latency_ms=latency_ms,
                fallback_used=self.last_fallback_reason is not None,
            )


def build_adaptive_experience_port_router(
    *,
    enabled: bool,
    assembler: Any | None = None,
    engine: Any | None = None,
    gate: Any | None = None,
    events: EventRegistry | None = None,
    traceability: Any | None = None,
) -> AdaptiveExperiencePortRouter | None:
    """DI helper — construct router only when Experience cutover is active."""
    if not enabled:
        return None
    return AdaptiveExperiencePortRouter(
        assembler=assembler,
        engine=engine,
        gate=gate,
        events=events,
        cutover_active=True,
        traceability=traceability,
    )


__all__ = [
    "AdaptiveExperiencePortRouter",
    "adaptive_experience_cutover_active",
    "build_adaptive_experience_port_router",
    "map_adaptive_output_to_recommendation",
]
