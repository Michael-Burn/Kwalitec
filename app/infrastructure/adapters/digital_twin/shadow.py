"""Twin Shadow Validator orchestrator (MS-004 T6).

Pipeline (observational only):

  Runtime A → TwinSnapshotBuilder → TwinSnapshot
  → TwinExplainabilityService → SnapshotExplanation
  → StudentTwinProjector → StudentTwinProjection
  → Monitors (stability / consistency) → Health / Telemetry
  → Discard (no Experience UX authority)

Shadow outputs may be logged, measured, compared, and validated.
They must NOT change Experience TwinPort, Adaptive authority, Runtime A,
or student-visible behaviour.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Any

from app.infrastructure.adapters.digital_twin import (
    shadow_telemetry as telemetry,
)
from app.infrastructure.adapters.digital_twin.contracts import (
    INVALID_STATE,
    UNAVAILABLE,
    SnapshotExplanation,
    StudentTwinProjection,
    TwinSnapshot,
)
from app.infrastructure.adapters.digital_twin.shadow_health import (
    TwinShadowHealthMetrics,
    TwinShadowHealthSnapshot,
    build_twin_shadow_health_metrics,
)
from app.infrastructure.adapters.digital_twin.shadow_monitors import (
    DriftSignal,
    ExplainabilityConsistencyMonitor,
    ProjectionConsistencyMonitor,
    SnapshotStabilityMonitor,
    StabilityResult,
    TwinDriftDetectionMonitor,
    explanation_is_complete,
)
from app.infrastructure.events.registry import EventRegistry

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TwinShadowObservation:
    """One observational Twin shadow validation cycle (never fed to Experience)."""

    ok: bool
    student_id: str
    snapshot: TwinSnapshot | None
    explanation: SnapshotExplanation | None
    projection: StudentTwinProjection | None
    snapshot_stability: StabilityResult | None
    projection_stability: StabilityResult | None
    explainability_stability: StabilityResult | None
    drift_signals: tuple[DriftSignal, ...]
    latency_ms: float
    snapshot_ok: bool
    projection_ok: bool
    explainability_ok: bool
    unavailable_facet_count: int
    determinism_ok: bool
    error_code: str = ""
    message: str = ""

    def to_canonical_dict(self) -> dict[str, Any]:
        twin_id = ""
        if self.snapshot is not None:
            twin_id = self.snapshot.twin_id
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
            "latency_ms": round(float(self.latency_ms), 3),
            "message": self.message,
            "ok": self.ok,
            "projection_ok": self.projection_ok,
            "projection_stability": (
                None
                if self.projection_stability is None
                else self.projection_stability.to_canonical_dict()
            ),
            "snapshot_ok": self.snapshot_ok,
            "snapshot_stability": (
                None
                if self.snapshot_stability is None
                else self.snapshot_stability.to_canonical_dict()
            ),
            "student_id": self.student_id,
            "twin_id": twin_id,
            "unavailable_facet_count": self.unavailable_facet_count,
        }


class TwinShadowValidator:
    """Run Twin synthesis → snapshot → explain → project → measure → discard.

    Observational only. Callers may inspect TwinShadowObservation for
    ops/readiness; Experience / Runtime A / Adaptive paths must ignore it.
    """

    VALIDATOR_ID = "twin_shadow_validator"
    VALIDATOR_VERSION = "1.0.0-t6"

    def __init__(
        self,
        *,
        snapshot_builder: Any,
        explainability: Any | None = None,
        projector: Any | None = None,
        events: EventRegistry | None = None,
        enabled: bool = True,
        health: TwinShadowHealthMetrics | None = None,
        snapshot_monitor: SnapshotStabilityMonitor | None = None,
        projection_monitor: ProjectionConsistencyMonitor | None = None,
        explainability_monitor: ExplainabilityConsistencyMonitor | None = None,
        drift_monitor: TwinDriftDetectionMonitor | None = None,
        emit_health_on_complete: bool = True,
    ) -> None:
        self._snapshot_builder = snapshot_builder
        self._explainability = explainability
        self._projector = projector
        self._events = events or EventRegistry()
        self._enabled = bool(enabled)
        self._health = health or build_twin_shadow_health_metrics()
        self._snapshot_monitor = snapshot_monitor or SnapshotStabilityMonitor()
        self._projection_monitor = (
            projection_monitor or ProjectionConsistencyMonitor()
        )
        self._explainability_monitor = (
            explainability_monitor or ExplainabilityConsistencyMonitor()
        )
        self._drift = drift_monitor or TwinDriftDetectionMonitor()
        self._emit_health_on_complete = bool(emit_health_on_complete)
        self._last_observation: TwinShadowObservation | None = None

    @property
    def validator_id(self) -> str:
        return self.VALIDATOR_ID

    @property
    def validator_version(self) -> str:
        return self.VALIDATOR_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    @property
    def health(self) -> TwinShadowHealthMetrics:
        return self._health

    @property
    def last_observation(self) -> TwinShadowObservation | None:
        return self._last_observation

    def health_snapshot(self) -> TwinShadowHealthSnapshot:
        """Ops dashboard hook — current Twin shadow health rates."""
        return self._health.snapshot()

    def validate_shadow(
        self,
        student_id: str,
        *,
        as_of: str | None = None,
        snapshot: TwinSnapshot | None = None,
        run_stability_replay: bool = True,
    ) -> TwinShadowObservation:
        """Execute one observational Twin shadow validation cycle.

        Never returns Twin projections to Experience UX authority. Never writes
        Runtime A educational state. Never changes Adaptive authority.
        """
        from app.infrastructure.adapters.adaptive_engine.traceability import (
            resolve_correlation_id,
        )
        from app.infrastructure.diagnostics.correlation import CorrelationContext

        sid = (student_id or "").strip()
        self._last_observation = None
        if not sid:
            observation = TwinShadowObservation(
                ok=False,
                student_id="",
                snapshot=None,
                explanation=None,
                projection=None,
                snapshot_stability=None,
                projection_stability=None,
                explainability_stability=None,
                drift_signals=(),
                latency_ms=0.0,
                snapshot_ok=False,
                projection_ok=False,
                explainability_ok=False,
                unavailable_facet_count=0,
                determinism_ok=False,
                error_code=INVALID_STATE,
                message="student_id must be a non-empty string",
            )
            self._last_observation = observation
            return observation
        if not self._enabled:
            observation = TwinShadowObservation(
                ok=False,
                student_id=sid,
                snapshot=None,
                explanation=None,
                projection=None,
                snapshot_stability=None,
                projection_stability=None,
                explainability_stability=None,
                drift_signals=(),
                latency_ms=0.0,
                snapshot_ok=False,
                projection_ok=False,
                explainability_ok=False,
                unavailable_facet_count=0,
                determinism_ok=False,
                error_code=UNAVAILABLE,
                message="Twin shadow validation is disabled (feature flag OFF)",
            )
            self._last_observation = observation
            return observation

        correlation_id = resolve_correlation_id(None)
        with CorrelationContext.bind(correlation_id=correlation_id):
            return self._validate_bound(
                sid,
                as_of=as_of,
                snapshot=snapshot,
                run_stability_replay=run_stability_replay,
            )

    def validate_shadow_batch(
        self,
        student_ids: list[str] | tuple[str, ...],
        *,
        as_of: str | None = None,
        iterations: int = 1,
        run_stability_replay: bool = True,
    ) -> tuple[TwinShadowObservation, ...]:
        """Long-running observational replay helper (tests / shadow windows)."""
        results: list[TwinShadowObservation] = []
        repeats = max(1, int(iterations))
        for _ in range(repeats):
            for sid in student_ids:
                results.append(
                    self.validate_shadow(
                        sid,
                        as_of=as_of,
                        run_stability_replay=run_stability_replay,
                    )
                )
        return tuple(results)

    def _validate_bound(
        self,
        sid: str,
        *,
        as_of: str | None,
        snapshot: TwinSnapshot | None,
        run_stability_replay: bool,
    ) -> TwinShadowObservation:
        telemetry.emit_requested(self._events, student_id=sid, as_of=as_of)
        started = time.perf_counter()
        built: TwinSnapshot | None = snapshot
        explanation: SnapshotExplanation | None = None
        projection: StudentTwinProjection | None = None
        snapshot_stability: StabilityResult | None = None
        projection_stability: StabilityResult | None = None
        explainability_stability: StabilityResult | None = None
        drift_signals: tuple[DriftSignal, ...] = ()
        snapshot_ok = False
        projection_ok = False
        explainability_ok = False
        unavailable_facet_count = 0
        determinism_ok = False
        ok = False
        error_code = ""
        message = ""

        try:
            if self._snapshot_builder is None:
                raise RuntimeError("TwinSnapshotBuilder is not configured")
            if built is None:
                built = self._snapshot_builder.build(sid, as_of=as_of)
            if not isinstance(built, TwinSnapshot):
                raise TypeError("snapshot builder must return a TwinSnapshot")
            snapshot_ok = True
            unavailable_facet_count = len(
                tuple(built.completeness.facets_unavailable or ())
            )

            if self._explainability is not None:
                explanation = self._explainability.explain_snapshot(built)
                if not isinstance(explanation, SnapshotExplanation):
                    raise TypeError(
                        "explainability must return a SnapshotExplanation"
                    )
                explainability_ok = explanation_is_complete(explanation)

            if self._projector is not None:
                projection = self._projector.project(
                    built, explanation=explanation, as_of=as_of
                )
                if not isinstance(projection, StudentTwinProjection):
                    raise TypeError(
                        "projector must return a StudentTwinProjection"
                    )
                projection_ok = projection.availability == "available" or (
                    projection.student_id == sid
                )

            if run_stability_replay:
                snapshot_stability = self._snapshot_monitor.verify_replay(
                    self._snapshot_builder,
                    sid,
                    as_of=as_of,
                    snapshot=built,
                )
                if self._explainability is not None and explanation is not None:
                    explainability_stability = (
                        self._explainability_monitor.verify_replay(
                            self._explainability,
                            built,
                            explanation=explanation,
                        )
                    )
                if self._projector is not None and projection is not None:
                    projection_stability = self._projection_monitor.verify_replay(
                        self._projector,
                        built,
                        explanation=explanation,
                        as_of=as_of,
                        projection=projection,
                    )
                determinism_ok = bool(
                    snapshot_stability.success
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
                    snapshot_stable=bool(
                        snapshot_stability and snapshot_stability.success
                    ),
                    projection_stable=bool(
                        projection_stability is None
                        or projection_stability.success
                    ),
                    explainability_stable=bool(
                        explainability_stability is None
                        or explainability_stability.success
                    ),
                    detail=(
                        ""
                        if determinism_ok
                        else "one_or_more_stability_checks_failed"
                    ),
                )

            drift_signals = self._drift.detect(
                student_id=sid,
                snapshot_stability=snapshot_stability,
                projection_stability=projection_stability,
                explainability_stability=explainability_stability,
                explanation=explanation,
                snapshot=built,
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

            ok = snapshot_ok and (
                not run_stability_replay or determinism_ok
            )
            # Explicit discard contract: result is observational; no UX wiring.
            logger.debug(
                "twin shadow validated student_id=%s twin_id=%s discarded=1 "
                "snapshot_ok=%s projection_ok=%s explainability_ok=%s",
                sid,
                built.twin_id,
                snapshot_ok,
                projection_ok,
                explainability_ok,
            )
            telemetry.emit_completed(
                self._events,
                student_id=sid,
                twin_id=built.twin_id,
                snapshot_ok=snapshot_ok,
                projection_ok=projection_ok,
                explainability_ok=explainability_ok,
                unavailable_facet_count=unavailable_facet_count,
                determinism_ok=determinism_ok if run_stability_replay else None,
            )
        except Exception as exc:  # noqa: BLE001 — shadow must not raise into UX
            logger.debug(
                "twin shadow validation failed student_id=%s", sid, exc_info=True
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
            snapshot_ok=snapshot_ok,
            projection_ok=projection_ok,
            explainability_ok=explainability_ok,
            unavailable_facet_count=unavailable_facet_count,
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

        observation = TwinShadowObservation(
            ok=ok,
            student_id=sid,
            snapshot=built,
            explanation=explanation,
            projection=projection,
            snapshot_stability=snapshot_stability,
            projection_stability=projection_stability,
            explainability_stability=explainability_stability,
            drift_signals=drift_signals,
            latency_ms=latency_ms,
            snapshot_ok=snapshot_ok,
            projection_ok=projection_ok,
            explainability_ok=explainability_ok,
            unavailable_facet_count=unavailable_facet_count,
            determinism_ok=determinism_ok,
            error_code=error_code,
            message=message,
        )
        self._last_observation = observation
        return observation


def build_twin_shadow_validator(
    *,
    enabled: bool,
    snapshot_builder: Any | None,
    explainability: Any | None = None,
    projector: Any | None = None,
    events: EventRegistry | None = None,
    health: TwinShadowHealthMetrics | None = None,
) -> TwinShadowValidator | None:
    """DI helper — construct TwinShadowValidator only when Twin flag is on."""
    if not enabled or snapshot_builder is None:
        return None
    return TwinShadowValidator(
        snapshot_builder=snapshot_builder,
        explainability=explainability,
        projector=projector,
        events=events,
        enabled=True,
        health=health,
    )


def build_twin_shadow_ops_dashboard(
    validator: TwinShadowValidator | None,
    *,
    rollback_result: Any | None = None,
) -> dict[str, Any]:
    """Ops / Founder dashboard hook — observational Twin shadow status payload."""
    if validator is None or not validator.is_enabled():
        return {
            "twin_shadow_validation": {
                "enabled": False,
                "phase": "t6_shadow_validation",
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
        "twin_shadow_validation": {
            "enabled": True,
            "phase": "t6_shadow_validation",
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
    "TwinShadowObservation",
    "TwinShadowValidator",
    "build_twin_shadow_ops_dashboard",
    "build_twin_shadow_validator",
]
