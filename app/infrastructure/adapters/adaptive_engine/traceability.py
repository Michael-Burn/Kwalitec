"""Observational Adaptive Decision Traceability (MS-003 A5).

Every shadow or authoritative adaptive execution can produce a DecisionTrace
for reconstruction, analysis, and audit — without influencing educational
state, RecommendationService algorithms, Planning, schemas, or UI.

Persistence is in-memory / telemetric only (no educational tables, no
student-facing history).
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any
from uuid import uuid4

from app.infrastructure.adapters.adaptive_engine import (
    trace_telemetry as telemetry,
)
from app.infrastructure.adapters.adaptive_engine.contracts import (
    AdaptiveInputBundle,
    AdaptiveOutputBundle,
    serialize_canonical,
)
from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.registry import EventRegistry

# Lineage stages (directive reconstruction workflow).
LINEAGE_EVIDENCE = "evidence"
LINEAGE_INPUT_BUNDLE = "adaptive_input_bundle"
LINEAGE_OUTPUT_BUNDLE = "adaptive_output_bundle"
LINEAGE_EXPLAINABILITY = "explainability_result"
LINEAGE_ROUTING = "routing_decision"
LINEAGE_DELIVERY = "recommendation_delivered_or_shadow_only"

LINEAGE_STAGES: tuple[str, ...] = (
    LINEAGE_EVIDENCE,
    LINEAGE_INPUT_BUNDLE,
    LINEAGE_OUTPUT_BUNDLE,
    LINEAGE_EXPLAINABILITY,
    LINEAGE_ROUTING,
    LINEAGE_DELIVERY,
)

# Authority / delivery status values (observational).
AUTHORITY_SHADOW_ONLY = "shadow_only"
AUTHORITY_ADAPTIVE_DELIVERED = "adaptive_engine"
AUTHORITY_RECOMMENDATION_FALLBACK = "recommendation_fallback"
AUTHORITY_GATE_INELIGIBLE = "gate_ineligible"
AUTHORITY_INACTIVE = "inactive"
AUTHORITY_FAILED = "failed"

DELIVERY_DELIVERED = "delivered"
DELIVERY_SHADOW_ONLY = "shadow_only"
DELIVERY_NONE = "none"

ROUTING_AUTHORITATIVE = "authoritative"
ROUTING_SHADOW_ONLY = "shadow_only"
ROUTING_FALLBACK = "fallback"
ROUTING_FAILED = "failed"
ROUTING_INACTIVE = "inactive"


def new_correlation_id() -> str:
    """Allocate a correlation id for an adaptive decision lifecycle."""
    return CorrelationContext.new_correlation_id()


def resolve_correlation_id(explicit: str | None = None) -> str:
    """Return explicit, then current context, else a newly generated id."""
    if explicit is not None and (explicit or "").strip():
        return explicit.strip()
    current = CorrelationContext.get_correlation_id()
    if current:
        return current
    return new_correlation_id()


def runtime_a_snapshot_id(inputs: AdaptiveInputBundle | None) -> str:
    """Stable Runtime A snapshot identifier from AdaptiveInputBundle material."""
    if inputs is None:
        return "snap-unavailable"
    digest = hashlib.sha256(inputs.serialize().encode("utf-8")).hexdigest()[:16]
    return f"snap-{digest}"


def input_bundle_ref(inputs: AdaptiveInputBundle | None) -> str:
    """Reference fingerprint for an AdaptiveInputBundle."""
    if inputs is None:
        return "input-unavailable"
    digest = hashlib.sha256(inputs.serialize().encode("utf-8")).hexdigest()[:16]
    return f"input-{digest}"


def output_bundle_ref(output: AdaptiveOutputBundle | None) -> str:
    """Reference fingerprint for an AdaptiveOutputBundle."""
    if output is None:
        return "output-unavailable"
    digest = hashlib.sha256(output.serialize().encode("utf-8")).hexdigest()[:16]
    return f"output-{digest}"


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    return MappingProxyType(dict(value or {}))


@dataclass(frozen=True)
class FeatureFlagSnapshot:
    """Observational snapshot of adaptive feature flags at decision time."""

    engine_enabled: bool = False
    shadow_enabled: bool = False
    authority_enabled: bool = False

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "authority_enabled": bool(self.authority_enabled),
            "engine_enabled": bool(self.engine_enabled),
            "shadow_enabled": bool(self.shadow_enabled),
        }


@dataclass(frozen=True)
class DecisionLineage:
    """Reconstructable adaptive decision lineage (observational).

    Evidence → AdaptiveInputBundle → AdaptiveOutputBundle →
    Explainability Result → Routing Decision → Recommendation Delivered
    (or Shadow Only).
    """

    stages: tuple[str, ...] = LINEAGE_STAGES
    evidence_ref_ids: tuple[str, ...] = ()
    input_bundle_ref: str = ""
    output_bundle_ref: str = ""
    explainability_passed: bool | None = None
    explainability_error_code: str | None = None
    routing_decision: str = ROUTING_INACTIVE
    delivery_status: str = DELIVERY_NONE
    runtime_a_snapshot_id: str = ""

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "delivery_status": self.delivery_status,
            "evidence_ref_ids": list(self.evidence_ref_ids),
            "explainability_error_code": self.explainability_error_code,
            "explainability_passed": self.explainability_passed,
            "input_bundle_ref": self.input_bundle_ref,
            "output_bundle_ref": self.output_bundle_ref,
            "routing_decision": self.routing_decision,
            "runtime_a_snapshot_id": self.runtime_a_snapshot_id,
            "stages": list(self.stages),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class DecisionTrace:
    """Complete observational Adaptive Decision Trace (A5).

    No educational writes. No student-facing persistence.
    """

    decision_id: str
    correlation_id: str
    engine_version: str
    feature_flag_state: FeatureFlagSnapshot
    runtime_a_snapshot_id: str
    input_bundle_ref: str
    output_bundle_ref: str
    explainability_gate_result: Mapping[str, Any]
    authority_status: str
    executed_at: str
    student_id: str
    lineage: DecisionLineage
    input_serialize: str = ""
    output_serialize: str = ""
    error_code: str | None = None
    message: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "explainability_gate_result",
            _freeze_mapping(self.explainability_gate_result),
        )
        if not (self.decision_id or "").strip():
            raise ValueError("decision_id must be a non-empty string")
        if not (self.correlation_id or "").strip():
            raise ValueError("correlation_id must be a non-empty string")
        if not isinstance(self.feature_flag_state, FeatureFlagSnapshot):
            raise TypeError("feature_flag_state must be a FeatureFlagSnapshot")
        if not isinstance(self.lineage, DecisionLineage):
            raise TypeError("lineage must be a DecisionLineage")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "authority_status": self.authority_status,
            "correlation_id": self.correlation_id,
            "decision_id": self.decision_id,
            "engine_version": self.engine_version,
            "error_code": self.error_code,
            "executed_at": self.executed_at,
            "explainability_gate_result": dict(self.explainability_gate_result),
            "feature_flag_state": self.feature_flag_state.to_canonical_dict(),
            "input_bundle_ref": self.input_bundle_ref,
            "input_serialize": self.input_serialize,
            "lineage": self.lineage.to_canonical_dict(),
            "message": self.message,
            "output_bundle_ref": self.output_bundle_ref,
            "output_serialize": self.output_serialize,
            "runtime_a_snapshot_id": self.runtime_a_snapshot_id,
            "student_id": self.student_id,
        }

    def serialize(self) -> str:
        """Deterministic serialization excluding wall-clock executed_at noise.

        Material reconstruction uses lineage + bundle refs + decision identity.
        ``executed_at`` remains on the DTO for observational audit.
        """
        material = dict(self.to_canonical_dict())
        material.pop("executed_at", None)
        return serialize_canonical(material)


def build_decision_lineage(
    *,
    inputs: AdaptiveInputBundle | None,
    output: AdaptiveOutputBundle | None,
    gate_result: Any | None,
    routing_decision: str,
    delivery_status: str,
) -> DecisionLineage:
    """Build reconstructable lineage from pipeline artefacts."""
    evidence_ids: list[str] = []
    if output is not None:
        for ref in output.explanation.evidence_refs or ():
            kind = (ref.kind or "").strip()
            rid = (ref.id or "").strip()
            if kind and rid:
                evidence_ids.append(f"{kind}:{rid}")
    elif inputs is not None:
        attempts = inputs.evidence.get("attempts") if inputs.evidence else None
        if isinstance(attempts, list | tuple):
            for item in attempts:
                if isinstance(item, Mapping):
                    aid = str(
                        item.get("id") or item.get("attempt_id") or ""
                    ).strip()
                    if aid:
                        evidence_ids.append(f"study_attempt:{aid}")

    explainability_passed: bool | None = None
    explainability_error: str | None = None
    if gate_result is not None:
        explainability_passed = bool(getattr(gate_result, "passed", False))
        explainability_error = getattr(gate_result, "error_code", None)

    return DecisionLineage(
        stages=LINEAGE_STAGES,
        evidence_ref_ids=tuple(evidence_ids),
        input_bundle_ref=input_bundle_ref(inputs),
        output_bundle_ref=output_bundle_ref(output),
        explainability_passed=explainability_passed,
        explainability_error_code=explainability_error,
        routing_decision=routing_decision,
        delivery_status=delivery_status,
        runtime_a_snapshot_id=runtime_a_snapshot_id(inputs),
    )


class TraceabilityService:
    """Create, store (in-memory), and reconstruct observational DecisionTraces.

    Does not mutate Runtime A. Does not alter recommendation behaviour.
    """

    SERVICE_ID = "adaptive_traceability_service"
    SERVICE_VERSION = "1.0.0-a5"

    def __init__(
        self,
        *,
        events: EventRegistry | None = None,
        enabled: bool = True,
        feature_flags: FeatureFlagSnapshot | None = None,
        engine_version: str = "1.0.0-a2",
    ) -> None:
        self._events = events or EventRegistry()
        self._enabled = bool(enabled)
        self._feature_flags = feature_flags or FeatureFlagSnapshot()
        self._engine_version = engine_version
        self._traces_by_decision: dict[str, DecisionTrace] = {}
        self._traces_by_correlation: dict[str, list[str]] = {}
        self._seen_decision_ids: set[str] = set()

    @property
    def service_id(self) -> str:
        return self.SERVICE_ID

    @property
    def service_version(self) -> str:
        return self.SERVICE_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    def get_trace(self, decision_id: str) -> DecisionTrace | None:
        """Return stored DecisionTrace by decision_id, if any."""
        return self._traces_by_decision.get((decision_id or "").strip())

    def traces_for_correlation(self, correlation_id: str) -> tuple[DecisionTrace, ...]:
        """Return traces sharing a correlation id (decision lifecycle)."""
        ids = self._traces_by_correlation.get((correlation_id or "").strip(), [])
        return tuple(
            self._traces_by_decision[did]
            for did in ids
            if did in self._traces_by_decision
        )

    def all_traces(self) -> tuple[DecisionTrace, ...]:
        return tuple(self._traces_by_decision.values())

    def ensure_unique_decision_id(self, candidate: str) -> str:
        """Return a non-empty decision id; mint one when missing.

        Executor decision ids are deterministic per input snapshot. When the
        candidate is empty, allocate a unique observational id. Collisions of
        identical deterministic ids for the same snapshot are intentional.
        """
        did = (candidate or "").strip()
        if did:
            self._seen_decision_ids.add(did)
            return did
        minted = f"a5-{uuid4().hex[:16]}"
        while minted in self._seen_decision_ids:
            minted = f"a5-{uuid4().hex[:16]}"
        self._seen_decision_ids.add(minted)
        return minted

    def record_decision(
        self,
        *,
        student_id: str,
        inputs: AdaptiveInputBundle | None = None,
        output: AdaptiveOutputBundle | None = None,
        gate_result: Any | None = None,
        authority_status: str = AUTHORITY_SHADOW_ONLY,
        routing_decision: str = ROUTING_SHADOW_ONLY,
        delivery_status: str = DELIVERY_SHADOW_ONLY,
        correlation_id: str | None = None,
        feature_flags: FeatureFlagSnapshot | None = None,
        engine_version: str | None = None,
        error_code: str | None = None,
        message: str = "",
        executed_at: str | None = None,
    ) -> DecisionTrace | None:
        """Build and store a complete DecisionTrace; emit observational telemetry.

        Returns None when the service is disabled (flags off).
        """
        if not self._enabled:
            return None

        sid = (student_id or "").strip()
        corr = resolve_correlation_id(correlation_id)
        flags = feature_flags or self._feature_flags
        version = (
            (engine_version or self._engine_version).strip()
            or self._engine_version
        )
        when = (executed_at or "").strip() or datetime.now(tz=UTC).isoformat()

        decision_id = ""
        if output is not None and (output.decision_id or "").strip():
            decision_id = output.decision_id.strip()
        decision_id = self.ensure_unique_decision_id(decision_id)

        gate_dict: dict[str, Any] = {}
        if gate_result is not None:
            to_dict = getattr(gate_result, "to_canonical_dict", None)
            if callable(to_dict):
                gate_dict = dict(to_dict())
            else:
                gate_dict = {
                    "passed": bool(getattr(gate_result, "passed", False)),
                    "decision_id": getattr(gate_result, "decision_id", "") or "",
                    "error_code": getattr(gate_result, "error_code", None),
                    "eligible_for_future_authority": bool(
                        getattr(gate_result, "eligible_for_future_authority", False)
                    ),
                    "observational_only": bool(
                        getattr(gate_result, "observational_only", True)
                    ),
                }

        lineage = build_decision_lineage(
            inputs=inputs,
            output=output,
            gate_result=gate_result,
            routing_decision=routing_decision,
            delivery_status=delivery_status,
        )

        try:
            trace = DecisionTrace(
                decision_id=decision_id,
                correlation_id=corr,
                engine_version=version,
                feature_flag_state=flags,
                runtime_a_snapshot_id=runtime_a_snapshot_id(inputs),
                input_bundle_ref=input_bundle_ref(inputs),
                output_bundle_ref=output_bundle_ref(output),
                explainability_gate_result=gate_dict,
                authority_status=authority_status,
                executed_at=when,
                student_id=sid,
                lineage=lineage,
                input_serialize="" if inputs is None else inputs.serialize(),
                output_serialize="" if output is None else output.serialize(),
                error_code=error_code,
                message=(message or "")[:256],
            )
        except Exception as exc:  # noqa: BLE001 — tracing must not break UX
            telemetry.emit_failed(
                self._events,
                student_id=sid,
                correlation_id=corr,
                error_code=type(exc).__name__,
                message=str(exc),
                decision_id=decision_id,
            )
            return None

        self._store(trace)

        if error_code:
            telemetry.emit_failed(
                self._events,
                student_id=sid,
                correlation_id=corr,
                error_code=error_code,
                message=message,
                decision_id=decision_id,
            )
        else:
            telemetry.emit_created(
                self._events,
                student_id=sid,
                decision_id=decision_id,
                correlation_id=corr,
                authority_status=authority_status,
                runtime_a_snapshot_id=trace.runtime_a_snapshot_id,
            )
        return trace

    def reconstruct_lineage(self, decision_id: str) -> DecisionLineage | None:
        """Reconstruct DecisionLineage for a stored decision (deterministic)."""
        trace = self.get_trace(decision_id)
        if trace is None:
            telemetry.emit_failed(
                self._events,
                student_id="",
                correlation_id=resolve_correlation_id(None),
                error_code="NOT_FOUND",
                message=f"no DecisionTrace for decision_id={decision_id}",
                decision_id=(decision_id or "").strip(),
            )
            return None

        # Rebuild from frozen material fields — identical to stored lineage.
        rebuilt = DecisionLineage(
            stages=tuple(trace.lineage.stages),
            evidence_ref_ids=tuple(trace.lineage.evidence_ref_ids),
            input_bundle_ref=trace.lineage.input_bundle_ref,
            output_bundle_ref=trace.lineage.output_bundle_ref,
            explainability_passed=trace.lineage.explainability_passed,
            explainability_error_code=trace.lineage.explainability_error_code,
            routing_decision=trace.lineage.routing_decision,
            delivery_status=trace.lineage.delivery_status,
            runtime_a_snapshot_id=trace.lineage.runtime_a_snapshot_id,
        )
        telemetry.emit_reconstructed(
            self._events,
            student_id=trace.student_id,
            decision_id=trace.decision_id,
            correlation_id=trace.correlation_id,
            lineage_stages=rebuilt.stages,
        )
        return rebuilt

    def _store(self, trace: DecisionTrace) -> None:
        self._traces_by_decision[trace.decision_id] = trace
        bucket = self._traces_by_correlation.setdefault(trace.correlation_id, [])
        if trace.decision_id not in bucket:
            bucket.append(trace.decision_id)


def build_traceability_service(
    *,
    enabled: bool,
    events: EventRegistry | None = None,
    feature_flags: FeatureFlagSnapshot | None = None,
    engine_version: str = "1.0.0-a2",
) -> TraceabilityService | None:
    """DI helper — construct TraceabilityService when adaptive flags allow."""
    if not enabled:
        return None
    return TraceabilityService(
        events=events,
        enabled=True,
        feature_flags=feature_flags or FeatureFlagSnapshot(),
        engine_version=engine_version,
    )


__all__ = [
    "AUTHORITY_ADAPTIVE_DELIVERED",
    "AUTHORITY_FAILED",
    "AUTHORITY_GATE_INELIGIBLE",
    "AUTHORITY_INACTIVE",
    "AUTHORITY_RECOMMENDATION_FALLBACK",
    "AUTHORITY_SHADOW_ONLY",
    "DELIVERY_DELIVERED",
    "DELIVERY_NONE",
    "DELIVERY_SHADOW_ONLY",
    "DecisionLineage",
    "DecisionTrace",
    "FeatureFlagSnapshot",
    "LINEAGE_STAGES",
    "ROUTING_AUTHORITATIVE",
    "ROUTING_FAILED",
    "ROUTING_FALLBACK",
    "ROUTING_INACTIVE",
    "ROUTING_SHADOW_ONLY",
    "TraceabilityService",
    "build_decision_lineage",
    "build_traceability_service",
    "input_bundle_ref",
    "new_correlation_id",
    "output_bundle_ref",
    "resolve_correlation_id",
    "runtime_a_snapshot_id",
]
