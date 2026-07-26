"""Strategy Shadow Validator orchestrator (MS-005 S3).

Pipeline (observational only):

  Runtime A (+ Twin / Adaptive consumed inputs)
  → StrategyContextAssembler → StrategyContext
  → Strategy Engine → LearningIntervention
  → StrategyExplainabilityService → StrategyExplanationBundle
  → StrategyProjector → StrategyProjection
  → Monitors (stability / consistency) → Health / Telemetry
  → Discard (no Experience UX authority)

Shadow outputs may be logged, measured, compared, and validated.
They must NOT change Experience StrategyInterventionPort, Runtime A,
Twin, Adaptive authority, or student-visible behaviour.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from app.infrastructure.adapters.strategy_engine import (
    shadow_telemetry as telemetry,
)
from app.infrastructure.adapters.strategy_engine.contracts import (
    INVALID_STATE,
    UNAVAILABLE,
    LearningIntervention,
    StrategyContext,
    StrategyExplanationBundle,
    StrategyProjection,
)
from app.infrastructure.adapters.strategy_engine.explainability import (
    explanation_is_complete,
)
from app.infrastructure.adapters.strategy_engine.shadow_health import (
    StrategyShadowHealth,
    build_strategy_shadow_health,
)
from app.infrastructure.adapters.strategy_engine.shadow_monitors import (
    DriftSignal,
    ExplainabilityConsistencyMonitor,
    InterventionStabilityMonitor,
    PlannerConsistencyMonitor,
    ProjectionConsistencyMonitor,
    StabilityResult,
    StrategyDriftDetectionMonitor,
)
from app.infrastructure.events.registry import EventRegistry

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class StrategyShadowObservation:
    """One observational Strategy shadow validation cycle (never fed to Experience)."""

    ok: bool
    student_id: str
    context: StrategyContext | None
    intervention: LearningIntervention | None
    explanation: StrategyExplanationBundle | None
    projection: StrategyProjection | None
    intervention_stability: StabilityResult | None
    projection_stability: StabilityResult | None
    explainability_stability: StabilityResult | None
    planner_consistency: StabilityResult | None
    drift_signals: tuple[DriftSignal, ...]
    latency_ms: float
    intervention_ok: bool
    projection_ok: bool
    explainability_ok: bool
    planner_consistency_ok: bool
    determinism_ok: bool
    error_code: str = ""
    message: str = ""

    def to_canonical_dict(self) -> dict[str, Any]:
        intervention_id = ""
        if self.intervention is not None:
            intervention_id = self.intervention.intervention_id
        return {
            "determinism_ok": self.determinism_ok,
            "drift_signals": [s.to_canonical_dict() for s in self.drift_signals],
            "error_code": self.error_code,
            "explainability_ok": self.explainability_ok,
            "explainability_stability": (
                None
                if self.explainability_stability is None
                else self.explainability_stability.to_canonical_dict()
            ),
            "intervention_id": intervention_id,
            "intervention_ok": self.intervention_ok,
            "intervention_stability": (
                None
                if self.intervention_stability is None
                else self.intervention_stability.to_canonical_dict()
            ),
            "latency_ms": round(float(self.latency_ms), 3),
            "message": self.message,
            "ok": self.ok,
            "planner_consistency": (
                None
                if self.planner_consistency is None
                else self.planner_consistency.to_canonical_dict()
            ),
            "planner_consistency_ok": self.planner_consistency_ok,
            "projection_ok": self.projection_ok,
            "projection_stability": (
                None
                if self.projection_stability is None
                else self.projection_stability.to_canonical_dict()
            ),
            "student_id": self.student_id,
        }


class StrategyShadowValidator:
    """Run assemble → evaluate → explain → project → measure → discard.

    Observational only. Callers may inspect StrategyShadowObservation for
    ops/readiness; Experience / Runtime A / Twin / Adaptive paths must ignore it.
    """

    VALIDATOR_ID = "strategy_shadow_validator"
    VALIDATOR_VERSION = "1.0.0-s3"

    def __init__(
        self,
        *,
        adapter: Any,
        explainability: Any | None = None,
        projector: Any | None = None,
        events: EventRegistry | None = None,
        enabled: bool = True,
        health: StrategyShadowHealth | None = None,
        intervention_monitor: InterventionStabilityMonitor | None = None,
        projection_monitor: ProjectionConsistencyMonitor | None = None,
        explainability_monitor: ExplainabilityConsistencyMonitor | None = None,
        planner_monitor: PlannerConsistencyMonitor | None = None,
        drift_monitor: StrategyDriftDetectionMonitor | None = None,
        emit_health_on_complete: bool = True,
    ) -> None:
        self._adapter = adapter
        self._explainability = explainability
        self._projector = projector
        self._events = events or EventRegistry()
        self._enabled = bool(enabled)
        self._health = health or build_strategy_shadow_health()
        self._intervention_monitor = (
            intervention_monitor or InterventionStabilityMonitor()
        )
        self._projection_monitor = (
            projection_monitor or ProjectionConsistencyMonitor()
        )
        self._explainability_monitor = (
            explainability_monitor or ExplainabilityConsistencyMonitor()
        )
        self._planner_monitor = planner_monitor or PlannerConsistencyMonitor()
        self._drift = drift_monitor or StrategyDriftDetectionMonitor()
        self._emit_health_on_complete = bool(emit_health_on_complete)
        self._last_observation: StrategyShadowObservation | None = None

    @property
    def validator_id(self) -> str:
        return self.VALIDATOR_ID

    @property
    def validator_version(self) -> str:
        return self.VALIDATOR_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    @property
    def health(self) -> StrategyShadowHealth:
        return self._health

    @property
    def last_observation(self) -> StrategyShadowObservation | None:
        return self._last_observation

    def health_snapshot(self):
        """Ops dashboard hook — current Strategy shadow health rates."""
        return self._health.snapshot()

    def validate_shadow(
        self,
        student_id: str,
        *,
        as_of: str | None = None,
        context: StrategyContext | None = None,
        runtime_a: Mapping[str, Any] | Any | None = None,
        twin: Mapping[str, Any] | Any | None = None,
        adaptive: Mapping[str, Any] | Any | None = None,
        run_stability_replay: bool = True,
    ) -> StrategyShadowObservation:
        """Execute one observational Strategy shadow validation cycle.

        Never returns Strategy projections to Experience UX authority. Never
        writes Runtime A educational state. Never mutates Twin or Adaptive.
        """
        from app.infrastructure.adapters.adaptive_engine.traceability import (
            resolve_correlation_id,
        )
        from app.infrastructure.diagnostics.correlation import CorrelationContext

        sid = (student_id or "").strip()
        self._last_observation = None
        if not sid:
            observation = StrategyShadowObservation(
                ok=False,
                student_id="",
                context=None,
                intervention=None,
                explanation=None,
                projection=None,
                intervention_stability=None,
                projection_stability=None,
                explainability_stability=None,
                planner_consistency=None,
                drift_signals=(),
                latency_ms=0.0,
                intervention_ok=False,
                projection_ok=False,
                explainability_ok=False,
                planner_consistency_ok=False,
                determinism_ok=False,
                error_code=INVALID_STATE,
                message="student_id must be a non-empty string",
            )
            self._last_observation = observation
            return observation
        if not self._enabled:
            observation = StrategyShadowObservation(
                ok=False,
                student_id=sid,
                context=None,
                intervention=None,
                explanation=None,
                projection=None,
                intervention_stability=None,
                projection_stability=None,
                explainability_stability=None,
                planner_consistency=None,
                drift_signals=(),
                latency_ms=0.0,
                intervention_ok=False,
                projection_ok=False,
                explainability_ok=False,
                planner_consistency_ok=False,
                determinism_ok=False,
                error_code=UNAVAILABLE,
                message="Strategy shadow validation is disabled (feature flag OFF)",
            )
            self._last_observation = observation
            return observation

        correlation_id = resolve_correlation_id(None)
        with CorrelationContext.bind(correlation_id=correlation_id):
            return self._validate_bound(
                sid,
                as_of=as_of,
                context=context,
                runtime_a=runtime_a,
                twin=twin,
                adaptive=adaptive,
                run_stability_replay=run_stability_replay,
            )

    def validate_shadow_batch(
        self,
        student_ids: list[str] | tuple[str, ...],
        *,
        as_of: str | None = None,
        runtime_a: Mapping[str, Any] | Any | None = None,
        twin: Mapping[str, Any] | Any | None = None,
        adaptive: Mapping[str, Any] | Any | None = None,
        iterations: int = 1,
        run_stability_replay: bool = True,
    ) -> tuple[StrategyShadowObservation, ...]:
        """Long-running observational replay helper (tests / shadow windows)."""
        results: list[StrategyShadowObservation] = []
        repeats = max(1, int(iterations))
        for _ in range(repeats):
            for sid in student_ids:
                results.append(
                    self.validate_shadow(
                        sid,
                        as_of=as_of,
                        runtime_a=runtime_a,
                        twin=twin,
                        adaptive=adaptive,
                        run_stability_replay=run_stability_replay,
                    )
                )
        return tuple(results)

    def _validate_bound(
        self,
        sid: str,
        *,
        as_of: str | None,
        context: StrategyContext | None,
        runtime_a: Mapping[str, Any] | Any | None,
        twin: Mapping[str, Any] | Any | None,
        adaptive: Mapping[str, Any] | Any | None,
        run_stability_replay: bool,
    ) -> StrategyShadowObservation:
        telemetry.emit_requested(self._events, student_id=sid, as_of=as_of)
        started = time.perf_counter()
        assembled: StrategyContext | None = context
        intervention: LearningIntervention | None = None
        explanation: StrategyExplanationBundle | None = None
        projection: StrategyProjection | None = None
        intervention_stability: StabilityResult | None = None
        projection_stability: StabilityResult | None = None
        explainability_stability: StabilityResult | None = None
        planner_consistency: StabilityResult | None = None
        drift_signals: tuple[DriftSignal, ...] = ()
        intervention_ok = False
        projection_ok = False
        explainability_ok = False
        planner_consistency_ok = False
        determinism_ok = False
        ok = False
        error_code = ""
        message = ""

        try:
            if self._adapter is None:
                raise RuntimeError("StrategyEngineAdapter is not configured")
            if assembled is None:
                assembled = self._adapter.assemble_context(
                    sid,
                    as_of=as_of,
                    runtime_a=runtime_a,
                    twin=twin,
                    adaptive=adaptive,
                )
            if not isinstance(assembled, StrategyContext):
                raise TypeError("assembler must return a StrategyContext")
            if assembled.student_id != sid:
                raise ValueError("context.student_id must match student_id")

            intervention = self._adapter.evaluate(assembled)
            if not isinstance(intervention, LearningIntervention):
                raise TypeError("engine must return a LearningIntervention")
            intervention_ok = bool((intervention.kind or "").strip())

            if self._explainability is not None:
                explanation = self._explainability.explain(intervention)
                if not isinstance(explanation, StrategyExplanationBundle):
                    raise TypeError(
                        "explainability must return a StrategyExplanationBundle"
                    )
                explainability_ok = explanation_is_complete(explanation)

            if self._projector is not None:
                projection = self._projector.project(
                    intervention,
                    explanation=explanation,
                    student_id=sid,
                    as_of=as_of,
                )
                if not isinstance(projection, StrategyProjection):
                    raise TypeError(
                        "projector must return a StrategyProjection"
                    )
                projection_ok = (
                    projection.availability == "available"
                    or projection.student_id == sid
                )

            planner_consistency = self._planner_monitor.verify(
                intervention, assembled
            )
            planner_consistency_ok = bool(planner_consistency.success)

            if run_stability_replay:
                intervention_stability = self._intervention_monitor.verify_replay(
                    self._adapter.engine,
                    assembled,
                    intervention=intervention,
                )
                if self._explainability is not None and explanation is not None:
                    explainability_stability = (
                        self._explainability_monitor.verify_replay(
                            self._explainability,
                            intervention,
                            explanation=explanation,
                        )
                    )
                if self._projector is not None and projection is not None:
                    projection_stability = self._projection_monitor.verify_replay(
                        self._projector,
                        intervention,
                        explanation=explanation,
                        student_id=sid,
                        as_of=as_of,
                        projection=projection,
                    )
                determinism_ok = bool(
                    intervention_stability.success
                    and planner_consistency_ok
                    and (
                        explainability_stability is None
                        or explainability_stability.success
                    )
                    and (
                        projection_stability is None
                        or projection_stability.success
                    )
                )
                telemetry.emit_stability(
                    self._events,
                    student_id=sid,
                    intervention_stable=bool(
                        intervention_stability and intervention_stability.success
                    ),
                    projection_stable=bool(
                        projection_stability is None
                        or projection_stability.success
                    ),
                    explainability_stable=bool(
                        explainability_stability is None
                        or explainability_stability.success
                    ),
                    planner_consistent=planner_consistency_ok,
                    detail=(
                        ""
                        if determinism_ok
                        else "one_or_more_stability_checks_failed"
                    ),
                )

            drift_signals = self._drift.detect(
                student_id=sid,
                intervention_stability=intervention_stability,
                projection_stability=projection_stability,
                explainability_stability=explainability_stability,
                planner_consistency=planner_consistency,
                explanation=explanation,
                determinism_success=(
                    determinism_ok if run_stability_replay else None
                ),
            )
            if drift_signals:
                telemetry.emit_drift(
                    self._events,
                    student_id=sid,
                    drift_signals=tuple(
                        s.to_canonical_dict() for s in drift_signals
                    ),
                )

            ok = intervention_ok and planner_consistency_ok and (
                not run_stability_replay or determinism_ok
            )
            # Explicit discard contract: result is observational; no UX wiring.
            logger.debug(
                "strategy shadow validated student_id=%s intervention_id=%s "
                "discarded=1 intervention_ok=%s projection_ok=%s "
                "explainability_ok=%s",
                sid,
                intervention.intervention_id,
                intervention_ok,
                projection_ok,
                explainability_ok,
            )
            telemetry.emit_completed(
                self._events,
                student_id=sid,
                intervention_id=intervention.intervention_id,
                intervention_ok=intervention_ok,
                projection_ok=projection_ok,
                explainability_ok=explainability_ok,
                planner_consistency_ok=planner_consistency_ok,
                determinism_ok=determinism_ok if run_stability_replay else None,
            )
        except Exception as exc:  # noqa: BLE001 — shadow must not raise into UX
            logger.debug(
                "strategy shadow validation failed student_id=%s",
                sid,
                exc_info=True,
            )
            error_code = type(exc).__name__
            message = str(exc)[:256]
            telemetry.emit_failed(
                self._events,
                student_id=sid,
                error_code=error_code,
                message=message,
            )
            ok = False

        latency_ms = (time.perf_counter() - started) * 1000.0
        telemetry.emit_latency(
            self._events,
            student_id=sid,
            latency_ms=latency_ms,
            ok=ok,
        )
        self._health.record_execution(
            ok=ok,
            intervention_ok=intervention_ok,
            projection_ok=projection_ok,
            explainability_ok=explainability_ok,
            planner_consistency_ok=planner_consistency_ok,
            determinism_success=(
                determinism_ok if run_stability_replay else None
            ),
            drift_signals=len(drift_signals),
            latency_ms=latency_ms,
        )
        if self._emit_health_on_complete:
            telemetry.emit_health(
                self._events,
                health=self._health.snapshot().to_canonical_dict(),
            )

        observation = StrategyShadowObservation(
            ok=ok,
            student_id=sid,
            context=assembled,
            intervention=intervention,
            explanation=explanation,
            projection=projection,
            intervention_stability=intervention_stability,
            projection_stability=projection_stability,
            explainability_stability=explainability_stability,
            planner_consistency=planner_consistency,
            drift_signals=drift_signals,
            latency_ms=latency_ms,
            intervention_ok=intervention_ok,
            projection_ok=projection_ok,
            explainability_ok=explainability_ok,
            planner_consistency_ok=planner_consistency_ok,
            determinism_ok=determinism_ok,
            error_code=error_code,
            message=message,
        )
        self._last_observation = observation
        return observation


def build_strategy_shadow_validator(
    *,
    enabled: bool,
    adapter: Any | None,
    explainability: Any | None = None,
    projector: Any | None = None,
    events: EventRegistry | None = None,
    health: StrategyShadowHealth | None = None,
) -> StrategyShadowValidator | None:
    """DI helper — construct StrategyShadowValidator only when Strategy flag is on."""
    if not enabled or adapter is None:
        return None
    return StrategyShadowValidator(
        adapter=adapter,
        explainability=explainability,
        projector=projector,
        events=events,
        enabled=True,
        health=health,
    )


def build_strategy_shadow_ops_dashboard(
    validator: StrategyShadowValidator | None,
    *,
    rollback_result: Any | None = None,
) -> dict[str, Any]:
    """Ops / Founder dashboard hook — observational Strategy shadow status payload."""
    if validator is None or not validator.is_enabled():
        return {
            "strategy_shadow_validation": {
                "enabled": False,
                "phase": "s3_shadow_validation",
                "health": None,
                "last_observation": None,
                "rollback": None
                if rollback_result is None
                else getattr(
                    rollback_result,
                    "to_canonical_dict",
                    lambda: rollback_result,
                )(),
            }
        }
    last = validator.last_observation
    return {
        "strategy_shadow_validation": {
            "enabled": True,
            "phase": "s3_shadow_validation",
            "validator_id": validator.validator_id,
            "validator_version": validator.validator_version,
            "health": validator.health_snapshot().to_canonical_dict(),
            "last_observation": (
                None if last is None else last.to_canonical_dict()
            ),
            "influences_student": False,
            "rollback": None
            if rollback_result is None
            else getattr(
                rollback_result,
                "to_canonical_dict",
                lambda: rollback_result,
            )(),
        }
    }


__all__ = [
    "StrategyShadowObservation",
    "StrategyShadowValidator",
    "build_strategy_shadow_ops_dashboard",
    "build_strategy_shadow_validator",
]
