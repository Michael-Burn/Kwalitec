"""Adaptive Shadow Soak orchestrator (MS-003 A6).

Pipeline (observational only):

  RecommendationService → Baseline Recommendation
  Adaptive Engine (shadow) → Adaptive Recommendation
  Compare → Measure → Record
  Never influence the student

Uses existing adaptive flags only (Engine / Shadow). No new authority.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Any

from app.infrastructure.adapters.adaptive_engine import (
    soak_telemetry as telemetry,
)
from app.infrastructure.adapters.adaptive_engine.contracts import (
    INVALID_STATE,
    UNAVAILABLE,
    AdaptiveDecisionResult,
    AdaptiveInputBundle,
    AdaptiveOutputBundle,
)
from app.infrastructure.adapters.adaptive_engine.shadow import (
    AdaptiveShadowOrchestrator,
    explanation_is_complete,
)
from app.infrastructure.adapters.adaptive_engine.soak_health import (
    SoakHealthMetrics,
    SoakHealthSnapshot,
    build_soak_health_metrics,
)
from app.infrastructure.adapters.adaptive_engine.soak_monitors import (
    DeterminismMonitor,
    DeterminismReplayResult,
    DriftDetectionMonitor,
    DriftSignal,
    RecommendationComparison,
    RecommendationComparisonMonitor,
)
from app.infrastructure.events.registry import EventRegistry

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SoakObservation:
    """One observational soak cycle result (never fed to Experience)."""

    ok: bool
    student_id: str
    baseline: dict[str, Any] | None
    adaptive_result: AdaptiveDecisionResult | None
    comparison: RecommendationComparison | None
    determinism: DeterminismReplayResult | None
    drift_signals: tuple[DriftSignal, ...]
    latency_ms: float
    explainability_passed: bool
    trace_created: bool
    error_code: str = ""
    message: str = ""

    @property
    def adaptive_output(self) -> AdaptiveOutputBundle | None:
        if self.adaptive_result is None or not self.adaptive_result.ok:
            return None
        value = self.adaptive_result.value
        return value if isinstance(value, AdaptiveOutputBundle) else None

    def to_canonical_dict(self) -> dict[str, Any]:
        decision_id = None
        if self.adaptive_output is not None:
            decision_id = self.adaptive_output.decision_id
        return {
            "adaptive_decision_id": decision_id,
            "comparison": (
                None
                if self.comparison is None
                else self.comparison.to_canonical_dict()
            ),
            "determinism": (
                None
                if self.determinism is None
                else self.determinism.to_canonical_dict()
            ),
            "drift_signals": [s.to_canonical_dict() for s in self.drift_signals],
            "error_code": self.error_code,
            "explainability_passed": self.explainability_passed,
            "latency_ms": round(float(self.latency_ms), 3),
            "message": self.message,
            "ok": self.ok,
            "student_id": self.student_id,
            "trace_created": self.trace_created,
        }


class ShadowSoakOrchestrator:
    """Run baseline + adaptive shadow, compare, measure, record — discard for UX.

    Observational only. Callers may inspect SoakObservation for ops/readiness;
    Experience / Runtime A paths must ignore soak outputs.
    """

    ORCHESTRATOR_ID = "adaptive_shadow_soak_orchestrator"
    ORCHESTRATOR_VERSION = "1.0.0-a6"

    def __init__(
        self,
        *,
        shadow: AdaptiveShadowOrchestrator,
        events: EventRegistry | None = None,
        enabled: bool = True,
        health: SoakHealthMetrics | None = None,
        comparison_monitor: RecommendationComparisonMonitor | None = None,
        determinism_monitor: DeterminismMonitor | None = None,
        drift_monitor: DriftDetectionMonitor | None = None,
        recommendation_service: Any | None = None,
        emit_health_on_complete: bool = True,
    ) -> None:
        self._shadow = shadow
        self._events = events or EventRegistry()
        self._enabled = bool(enabled)
        self._health = health or build_soak_health_metrics()
        self._comparison = comparison_monitor or RecommendationComparisonMonitor()
        self._determinism = determinism_monitor or DeterminismMonitor()
        self._drift = drift_monitor or DriftDetectionMonitor()
        self._recommendation_service = recommendation_service
        self._emit_health_on_complete = bool(emit_health_on_complete)
        self._last_observation: SoakObservation | None = None
        self._last_adaptive_topic_by_student: dict[str, str] = {}

    @property
    def orchestrator_id(self) -> str:
        return self.ORCHESTRATOR_ID

    @property
    def orchestrator_version(self) -> str:
        return self.ORCHESTRATOR_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    @property
    def health(self) -> SoakHealthMetrics:
        return self._health

    @property
    def last_observation(self) -> SoakObservation | None:
        return self._last_observation

    def health_snapshot(self) -> SoakHealthSnapshot:
        """Ops dashboard hook — current soak health rates."""
        return self._health.snapshot()

    def execute_soak(
        self,
        student_id: str,
        *,
        as_of: str | None = None,
        inputs: AdaptiveInputBundle | None = None,
        prior_adaptive_topic_code: str | None = None,
        run_determinism_replay: bool = True,
    ) -> SoakObservation:
        """Execute one observational soak cycle.

        Never returns adaptive recommendations to Experience. Never writes
        Runtime A educational state.
        """
        from app.infrastructure.adapters.adaptive_engine.traceability import (
            resolve_correlation_id,
        )
        from app.infrastructure.diagnostics.correlation import CorrelationContext

        sid = (student_id or "").strip()
        self._last_observation = None
        if not sid:
            observation = SoakObservation(
                ok=False,
                student_id="",
                baseline=None,
                adaptive_result=None,
                comparison=None,
                determinism=None,
                drift_signals=(),
                latency_ms=0.0,
                explainability_passed=False,
                trace_created=False,
                error_code=INVALID_STATE,
                message="student_id must be a non-empty string",
            )
            self._last_observation = observation
            return observation
        if not self._enabled:
            observation = SoakObservation(
                ok=False,
                student_id=sid,
                baseline=None,
                adaptive_result=None,
                comparison=None,
                determinism=None,
                drift_signals=(),
                latency_ms=0.0,
                explainability_passed=False,
                trace_created=False,
                error_code=UNAVAILABLE,
                message="Adaptive shadow soak is disabled (feature flag OFF)",
            )
            self._last_observation = observation
            return observation

        correlation_id = resolve_correlation_id(None)
        with CorrelationContext.bind(correlation_id=correlation_id):
            return self._execute_soak_bound(
                sid,
                as_of=as_of,
                inputs=inputs,
                prior_adaptive_topic_code=prior_adaptive_topic_code,
                run_determinism_replay=run_determinism_replay,
            )

    def execute_soak_batch(
        self,
        student_ids: list[str] | tuple[str, ...],
        *,
        as_of: str | None = None,
        iterations: int = 1,
        run_determinism_replay: bool = True,
    ) -> tuple[SoakObservation, ...]:
        """Long-running observational replay helper (tests / soak windows)."""
        results: list[SoakObservation] = []
        repeats = max(1, int(iterations))
        for _ in range(repeats):
            for sid in student_ids:
                results.append(
                    self.execute_soak(
                        sid,
                        as_of=as_of,
                        run_determinism_replay=run_determinism_replay,
                    )
                )
        return tuple(results)

    def _execute_soak_bound(
        self,
        sid: str,
        *,
        as_of: str | None,
        inputs: AdaptiveInputBundle | None,
        prior_adaptive_topic_code: str | None,
        run_determinism_replay: bool,
    ) -> SoakObservation:
        telemetry.emit_requested(self._events, student_id=sid, as_of=as_of)
        started = time.perf_counter()
        baseline: dict[str, Any] | None = None
        adaptive_result: AdaptiveDecisionResult | None = None
        comparison: RecommendationComparison | None = None
        determinism: DeterminismReplayResult | None = None
        drift_signals: tuple[DriftSignal, ...] = ()
        explainability_passed = False
        trace_created = False
        ok = False
        error_code = ""
        message = ""

        try:
            baseline = self._fetch_baseline(sid)
            adaptive_result = self._shadow.execute_shadow(
                sid, as_of=as_of, inputs=inputs
            )
            adaptive_output = (
                adaptive_result.value
                if adaptive_result.ok
                and isinstance(adaptive_result.value, AdaptiveOutputBundle)
                else None
            )
            comparison = self._comparison.compare(baseline, adaptive_output)

            bundle_for_replay = inputs
            if bundle_for_replay is None and adaptive_output is not None:
                # Prefer assembler re-read of the same as_of for determinism when
                # shadow succeeded; fall back to skipping when unavailable.
                assembler = getattr(self._shadow, "_assembler", None)
                if assembler is not None:
                    try:
                        bundle_for_replay = assembler.assemble(sid, as_of=as_of)
                    except Exception:  # noqa: BLE001 — observational
                        bundle_for_replay = None

            if run_determinism_replay and isinstance(
                bundle_for_replay, AdaptiveInputBundle
            ):
                executor = getattr(self._shadow, "_executor", None)
                determinism = self._determinism.verify_replay(
                    executor, bundle_for_replay
                )

            gate_result = getattr(self._shadow, "last_gate_result", None)
            gate_passed: bool | None = None
            if gate_result is not None:
                gate_passed = bool(getattr(gate_result, "passed", False))
                explainability_passed = gate_passed
            elif adaptive_output is not None:
                explainability_passed = explanation_is_complete(adaptive_output)
                gate_passed = explainability_passed

            last_trace = getattr(self._shadow, "last_trace", None)
            trace_created = last_trace is not None
            # Trace drift only when traceability is wired and adaptive succeeded.
            traceability = getattr(self._shadow, "_traceability", None)
            trace_ok: bool | None
            if not adaptive_result.ok or traceability is None:
                trace_ok = None
            else:
                trace_ok = last_trace is not None

            prior = prior_adaptive_topic_code
            if prior is None:
                prior = self._last_adaptive_topic_by_student.get(sid)

            drift_signals = self._drift.detect(
                student_id=sid,
                comparison=comparison,
                determinism=determinism,
                adaptive=adaptive_output,
                gate_passed=gate_passed,
                trace_ok=trace_ok,
                prior_adaptive_topic_code=prior if adaptive_result.ok else None,
            )

            if adaptive_output is not None:
                code = (adaptive_output.recommendation.topic_code or "").strip()
                if code:
                    self._last_adaptive_topic_by_student[sid] = code

            telemetry.emit_compare(
                self._events,
                student_id=sid,
                comparison=comparison.to_canonical_dict(),
            )
            if drift_signals:
                telemetry.emit_drift(
                    self._events,
                    student_id=sid,
                    signals=[s.to_canonical_dict() for s in drift_signals],
                )

            ok = bool(adaptive_result.ok)
            if not ok:
                error_code = adaptive_result.error_code or "SHADOW_FAILED"
                message = adaptive_result.message or ""

            telemetry.emit_completed(
                self._events,
                student_id=sid,
                decision_id=(
                    None if adaptive_output is None else adaptive_output.decision_id
                ),
                agreed=None if comparison is None else comparison.agreed,
                explainability_passed=explainability_passed,
                trace_created=trace_created,
                determinism_success=(
                    None if determinism is None else determinism.success
                ),
                drift_count=len(drift_signals),
            )
            logger.debug(
                "adaptive soak completed student_id=%s ok=%s agreed=%s "
                "discarded=1 influences_student=0",
                sid,
                ok,
                None if comparison is None else comparison.agreed,
            )
        except Exception as exc:  # noqa: BLE001 — soak must not raise into UX
            logger.debug("adaptive soak failed student_id=%s", sid, exc_info=True)
            ok = False
            error_code = type(exc).__name__
            message = str(exc)[:256]
            telemetry.emit_failed(
                self._events,
                student_id=sid,
                error_code=error_code,
                message=message,
            )

        latency_ms = (time.perf_counter() - started) * 1000.0
        telemetry.emit_latency(
            self._events,
            student_id=sid,
            latency_ms=latency_ms,
            ok=ok,
        )

        agreed_flag: bool | None = None
        if comparison is not None and comparison.comparable:
            agreed_flag = comparison.agreed

        # Fallback frequency: adaptive failure would route to RecommendationService.
        would_fallback = not ok

        self._health.record_execution(
            ok=ok,
            agreed=agreed_flag,
            explainability_passed=explainability_passed,
            trace_created=trace_created,
            determinism_success=(
                None if determinism is None else determinism.success
            ),
            fallback=would_fallback,
            drift_signals=len(drift_signals),
            latency_ms=latency_ms,
        )
        if self._emit_health_on_complete:
            telemetry.emit_health(
                self._events,
                snapshot=self._health.snapshot().to_canonical_dict(),
            )

        observation = SoakObservation(
            ok=ok,
            student_id=sid,
            baseline=baseline,
            adaptive_result=adaptive_result,
            comparison=comparison,
            determinism=determinism,
            drift_signals=drift_signals,
            latency_ms=latency_ms,
            explainability_passed=explainability_passed,
            trace_created=trace_created,
            error_code=error_code,
            message=message,
        )
        self._last_observation = observation
        return observation

    def _fetch_baseline(self, student_id: str) -> dict[str, Any] | None:
        """Read RecommendationService primary recommendation (observational)."""
        try:
            user_id = int(student_id)
        except (TypeError, ValueError):
            return None
        try:
            svc = self._resolve_recommendation_service()
            rows = svc.generate_recommendations(user_id, limit=1)
        except Exception:  # noqa: BLE001 — baseline absence is measurable
            logger.debug(
                "soak baseline RecommendationService unavailable student_id=%s",
                student_id,
                exc_info=True,
            )
            return None
        if not rows:
            return None
        primary = rows[0]
        if not isinstance(primary, dict):
            return None
        return dict(primary)

    def _resolve_recommendation_service(self) -> Any:
        if self._recommendation_service is not None:
            return self._recommendation_service
        from app.services.recommendation_service import RecommendationService

        return RecommendationService


def build_shadow_soak_orchestrator(
    *,
    enabled: bool,
    shadow: AdaptiveShadowOrchestrator | None,
    events: EventRegistry | None = None,
    health: SoakHealthMetrics | None = None,
    recommendation_service: Any | None = None,
) -> ShadowSoakOrchestrator | None:
    """DI helper — construct soak only when shadow soak prerequisites exist."""
    if not enabled or shadow is None:
        return None
    return ShadowSoakOrchestrator(
        shadow=shadow,
        events=events,
        enabled=True,
        health=health,
        recommendation_service=recommendation_service,
    )


def build_soak_ops_dashboard(
    soak: ShadowSoakOrchestrator | None,
    *,
    rollback_result: Any | None = None,
) -> dict[str, Any]:
    """Ops / Founder dashboard hook — observational soak status payload."""
    if soak is None or not soak.is_enabled():
        return {
            "adaptive_shadow_soak": {
                "enabled": False,
                "phase": "a6_shadow_soak",
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
    last = soak.last_observation
    return {
        "adaptive_shadow_soak": {
            "enabled": True,
            "phase": "a6_shadow_soak",
            "orchestrator_id": soak.orchestrator_id,
            "orchestrator_version": soak.orchestrator_version,
            "health": soak.health_snapshot().to_canonical_dict(),
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
    "ShadowSoakOrchestrator",
    "SoakObservation",
    "build_shadow_soak_orchestrator",
    "build_soak_ops_dashboard",
]
