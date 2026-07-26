"""Evidence Shadow Validator orchestrator (MS-006 E5).

Pipeline (observational only):

  EvidenceRecord / ExperimentObservation / PolicyEvaluation /
  AnalyticsSummary / EvidenceProjection
  → DeterminismValidator
  → OperationalHealthMonitor
  → ReadinessEvaluator → ReadinessReport
  → Telemetry
  → Discard (no policy deployment / no educational authority)

Shadow outputs may be logged, measured, compared, and validated.
They must NOT change Experience, Runtime A, Twin, Adaptive, Strategy,
or governance deployment state.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from app.infrastructure.adapters.evidence_platform import (
    shadow_telemetry as telemetry,
)
from app.infrastructure.adapters.evidence_platform.contracts import (
    INVALID_STATE,
    UNAVAILABLE,
    AnalyticsSummary,
    EvidenceProjection,
    EvidenceRecord,
    ExperimentObservation,
    PolicyEvaluation,
)
from app.infrastructure.adapters.evidence_platform.shadow_determinism import (
    DeterminismValidationResult,
    DeterminismValidator,
    DriftSignal,
    build_determinism_validator,
)
from app.infrastructure.adapters.evidence_platform.shadow_health import (
    OperationalHealthMonitor,
    build_operational_health_monitor,
)
from app.infrastructure.adapters.evidence_platform.shadow_readiness import (
    READINESS_UNAVAILABLE,
    ReadinessEvaluator,
    ReadinessReport,
    ValidationCoverage,
    build_readiness_evaluator,
)
from app.infrastructure.events.registry import EventRegistry

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class EvidencePlatformState:
    """Frozen Evidence Platform artefacts for one shadow validation cycle."""

    evidence_records: tuple[EvidenceRecord, ...] = ()
    observations: tuple[ExperimentObservation, ...] = ()
    evaluations: tuple[PolicyEvaluation, ...] = ()
    analytics_summaries: tuple[AnalyticsSummary, ...] = ()
    projections: tuple[EvidenceProjection, ...] = ()

    def coverage(self) -> ValidationCoverage:
        subsystems: list[str] = []
        if self.evidence_records:
            subsystems.append("evidence_collection")
        if self.observations:
            subsystems.append("experiment_framework")
        if self.evaluations:
            subsystems.append("policy_evaluation")
        if self.analytics_summaries:
            subsystems.append("analytics")
        if self.projections:
            subsystems.append("projection")
        return ValidationCoverage(
            evidence_records=len(self.evidence_records),
            observations=len(self.observations),
            evaluations=len(self.evaluations),
            analytics_summaries=len(self.analytics_summaries),
            projections=len(self.projections),
            subsystems_covered=tuple(subsystems),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "analytics_summaries": len(self.analytics_summaries),
            "evaluations": len(self.evaluations),
            "evidence_records": len(self.evidence_records),
            "observations": len(self.observations),
            "projections": len(self.projections),
        }


@dataclass(frozen=True)
class EvidenceShadowObservation:
    """One observational Evidence shadow validation cycle (never deployed)."""

    ok: bool
    report: ReadinessReport | None
    state: EvidencePlatformState | None
    determinism: DeterminismValidationResult | None
    drift_signals: tuple[DriftSignal, ...]
    latency_ms: float
    determinism_ok: bool
    error_code: str = ""
    message: str = ""

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "determinism": None
            if self.determinism is None
            else self.determinism.to_canonical_dict(),
            "determinism_ok": self.determinism_ok,
            "drift_signals": [s.to_canonical_dict() for s in self.drift_signals],
            "error_code": self.error_code,
            "latency_ms": round(float(self.latency_ms), 3),
            "message": self.message,
            "ok": self.ok,
            "report": None if self.report is None else self.report.to_canonical_dict(),
            "state": None if self.state is None else self.state.to_canonical_dict(),
        }


class EvidenceShadowValidator:
    """Run validate → measure → readiness → discard.

    Observational only. Callers may inspect EvidenceShadowObservation /
    ReadinessReport for ops/readiness; Experience / Runtime A / Twin /
    Adaptive / Strategy / governance deployment paths must ignore it.
    """

    VALIDATOR_ID = "evidence_shadow_validator"
    VALIDATOR_VERSION = "1.0.0-e5"

    def __init__(
        self,
        *,
        adapter: Any | None = None,
        events: EventRegistry | None = None,
        enabled: bool = True,
        health: OperationalHealthMonitor | None = None,
        determinism_validator: DeterminismValidator | None = None,
        readiness_evaluator: ReadinessEvaluator | None = None,
        emit_health_on_complete: bool = True,
    ) -> None:
        self._adapter = adapter
        self._events = events or EventRegistry()
        self._enabled = bool(enabled)
        self._health = health or build_operational_health_monitor()
        self._determinism = determinism_validator or build_determinism_validator()
        self._readiness = readiness_evaluator or build_readiness_evaluator()
        self._emit_health_on_complete = bool(emit_health_on_complete)
        self._last_observation: EvidenceShadowObservation | None = None
        self._last_report: ReadinessReport | None = None

    @property
    def validator_id(self) -> str:
        return self.VALIDATOR_ID

    @property
    def validator_version(self) -> str:
        return self.VALIDATOR_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    @property
    def health(self) -> OperationalHealthMonitor:
        return self._health

    @property
    def last_observation(self) -> EvidenceShadowObservation | None:
        return self._last_observation

    @property
    def last_report(self) -> ReadinessReport | None:
        return self._last_report

    def health_snapshot(self):
        """Ops dashboard hook — current Evidence shadow health rates."""
        return self._health.snapshot()

    def validate_shadow(
        self,
        *,
        evidence_records: Sequence[EvidenceRecord] = (),
        observations: Sequence[ExperimentObservation] = (),
        evaluations: Sequence[PolicyEvaluation] = (),
        analytics_summaries: Sequence[AnalyticsSummary] = (),
        projections: Sequence[EvidenceProjection] = (),
        state: EvidencePlatformState | None = None,
        as_of: str | None = None,
        run_pipeline_replay: bool = True,
        version_metadata: Mapping[str, Any] | None = None,
    ) -> EvidenceShadowObservation:
        """Execute one observational Evidence shadow validation cycle.

        Never deploys policy. Never writes educational state. Never mutates
        input artefacts.
        """
        from app.infrastructure.adapters.adaptive_engine.traceability import (
            resolve_correlation_id,
        )
        from app.infrastructure.diagnostics.correlation import CorrelationContext

        self._last_observation = None
        self._last_report = None
        if not self._enabled:
            observation = EvidenceShadowObservation(
                ok=False,
                report=None,
                state=None,
                determinism=None,
                drift_signals=(),
                latency_ms=0.0,
                determinism_ok=False,
                error_code=UNAVAILABLE,
                message="Evidence shadow validation is disabled (feature flag OFF)",
            )
            self._last_observation = observation
            return observation

        if state is not None and not isinstance(state, EvidencePlatformState):
            observation = EvidenceShadowObservation(
                ok=False,
                report=None,
                state=None,
                determinism=None,
                drift_signals=(),
                latency_ms=0.0,
                determinism_ok=False,
                error_code=INVALID_STATE,
                message="state must be an EvidencePlatformState or None",
            )
            self._last_observation = observation
            return observation

        correlation_id = resolve_correlation_id(None)
        with CorrelationContext.bind(correlation_id=correlation_id):
            return self._validate_bound(
                evidence_records=evidence_records,
                observations=observations,
                evaluations=evaluations,
                analytics_summaries=analytics_summaries,
                projections=projections,
                state=state,
                as_of=as_of,
                run_pipeline_replay=run_pipeline_replay,
                version_metadata=version_metadata,
            )

    def validate_shadow_batch(
        self,
        states: Sequence[EvidencePlatformState],
        *,
        as_of: str | None = None,
        iterations: int = 1,
        run_pipeline_replay: bool = True,
    ) -> tuple[EvidenceShadowObservation, ...]:
        """Long-running observational replay helper (tests / shadow windows)."""
        results: list[EvidenceShadowObservation] = []
        repeats = max(1, int(iterations))
        for _ in range(repeats):
            for platform_state in states:
                results.append(
                    self.validate_shadow(
                        state=platform_state,
                        as_of=as_of,
                        run_pipeline_replay=run_pipeline_replay,
                    )
                )
        return tuple(results)

    def _validate_bound(
        self,
        *,
        evidence_records: Sequence[EvidenceRecord],
        observations: Sequence[ExperimentObservation],
        evaluations: Sequence[PolicyEvaluation],
        analytics_summaries: Sequence[AnalyticsSummary],
        projections: Sequence[EvidenceProjection],
        state: EvidencePlatformState | None,
        as_of: str | None,
        run_pipeline_replay: bool,
        version_metadata: Mapping[str, Any] | None,
    ) -> EvidenceShadowObservation:
        if state is not None:
            platform_state = state
        else:
            platform_state = EvidencePlatformState(
                evidence_records=tuple(evidence_records or ()),
                observations=tuple(observations or ()),
                evaluations=tuple(evaluations or ()),
                analytics_summaries=tuple(analytics_summaries or ()),
                projections=tuple(projections or ()),
            )

        coverage = platform_state.coverage()
        report_id_hint = f"pending-{coverage.serialize()[:16]}"
        telemetry.emit_requested(
            self._events,
            report_id=report_id_hint,
            as_of=as_of,
            coverage=coverage.to_canonical_dict(),
        )
        started = time.perf_counter()
        determinism: DeterminismValidationResult | None = None
        report: ReadinessReport | None = None
        drift_signals: tuple[DriftSignal, ...] = ()
        determinism_ok = False
        ok = False
        error_code = ""
        message = ""

        try:
            determinism = self._determinism.validate(
                evidence_records=platform_state.evidence_records,
                observations=platform_state.observations,
                evaluations=platform_state.evaluations,
                analytics_summaries=platform_state.analytics_summaries,
                projections=platform_state.projections,
                adapter=self._adapter,
                run_pipeline_replay=run_pipeline_replay,
            )
            determinism_ok = bool(determinism.success)
            drift_signals = determinism.drift_signals

            telemetry.emit_stability(
                self._events,
                report_id=report_id_hint,
                evidence_stable=bool(
                    determinism.evidence and determinism.evidence.success
                ),
                observation_stable=bool(
                    determinism.observation and determinism.observation.success
                ),
                evaluation_stable=bool(
                    determinism.evaluation and determinism.evaluation.success
                ),
                analytics_stable=bool(
                    determinism.analytics and determinism.analytics.success
                ),
                projection_stable=bool(
                    determinism.projection and determinism.projection.success
                ),
                detail="" if determinism_ok else determinism.detail,
            )
            if drift_signals:
                telemetry.emit_drift(
                    self._events,
                    report_id=report_id_hint,
                    drift_signals=tuple(
                        s.to_canonical_dict() for s in drift_signals
                    ),
                )

            health_snapshot = self._health.snapshot()
            cycle_health = {
                "analytics_ok": bool(
                    determinism.analytics is None or determinism.analytics.success
                ),
                "drift_count": len(drift_signals),
                "evaluation_ok": bool(
                    determinism.evaluation is None or determinism.evaluation.success
                ),
                "evidence_ok": bool(
                    determinism.evidence is None or determinism.evidence.success
                ),
                "observation_ok": bool(
                    determinism.observation is None
                    or determinism.observation.success
                ),
                "pipeline_ok": bool(
                    determinism.pipeline_replay is None
                    or determinism.pipeline_replay.success
                ),
                "projection_ok": bool(
                    determinism.projection is None or determinism.projection.success
                ),
            }
            report = self._readiness.evaluate(
                determinism=determinism,
                health=None,
                coverage=coverage,
                as_of=as_of,
                telemetry_summary={
                    "event_source": "evidence_shadow_validator",
                    "influences_student": False,
                    "deploys_policy": False,
                    "cycle_health": cycle_health,
                    # Cumulative rates are observational ops telemetry only;
                    # omitted from report body so identical platform state
                    # yields identical ReadinessReport every execution.
                    "ops_health_executions": health_snapshot.executions,
                },
                version_metadata={
                    "validator_id": self.VALIDATOR_ID,
                    "validator_version": self.VALIDATOR_VERSION,
                    **dict(version_metadata or {}),
                },
            )
            ok = bool(report.ok and determinism_ok)
            telemetry.emit_readiness(
                self._events, report=report.to_canonical_dict()
            )
            telemetry.emit_completed(
                self._events,
                report_id=report.report_id,
                ok=ok,
                determinism_ok=determinism_ok,
                readiness_status=report.readiness_status,
                coverage=coverage.to_canonical_dict(),
            )
            logger.debug(
                "evidence shadow validated report_id=%s readiness=%s "
                "discarded=1 deploys_policy=0",
                report.report_id,
                report.readiness_status,
            )
        except Exception as exc:  # noqa: BLE001 — shadow must not raise into UX
            logger.debug("evidence shadow validation failed", exc_info=True)
            error_code = type(exc).__name__
            message = str(exc)[:256]
            telemetry.emit_failed(
                self._events,
                error_code=error_code,
                message=message,
                report_id=report_id_hint,
            )
            ok = False

        latency_ms = (time.perf_counter() - started) * 1000.0
        report_id = report.report_id if report is not None else report_id_hint
        telemetry.emit_latency(
            self._events,
            report_id=report_id,
            latency_ms=latency_ms,
            ok=ok,
        )
        readiness_status = (
            report.readiness_status if report is not None else READINESS_UNAVAILABLE
        )
        self._health.record_execution(
            ok=ok,
            determinism_success=determinism_ok if determinism is not None else None,
            readiness_status=readiness_status,
            drift_signals=len(drift_signals),
            latency_ms=latency_ms,
            evidence_count=coverage.evidence_records,
            observation_count=coverage.observations,
            evaluation_count=coverage.evaluations,
            analytics_count=coverage.analytics_summaries,
            projection_count=coverage.projections,
        )
        if self._emit_health_on_complete:
            telemetry.emit_health(
                self._events,
                health=self._health.snapshot().to_canonical_dict(),
            )

        observation = EvidenceShadowObservation(
            ok=ok,
            report=report,
            state=platform_state,
            determinism=determinism,
            drift_signals=drift_signals,
            latency_ms=latency_ms,
            determinism_ok=determinism_ok,
            error_code=error_code,
            message=message,
        )
        self._last_observation = observation
        self._last_report = report
        return observation


def build_evidence_shadow_validator(
    *,
    enabled: bool,
    adapter: Any | None = None,
    events: EventRegistry | None = None,
    health: OperationalHealthMonitor | None = None,
) -> EvidenceShadowValidator | None:
    """DI helper — construct EvidenceShadowValidator only when flag is on."""
    if not enabled:
        return None
    return EvidenceShadowValidator(
        adapter=adapter,
        events=events,
        enabled=True,
        health=health,
    )


def build_evidence_shadow_ops_dashboard(
    validator: EvidenceShadowValidator | None,
    *,
    rollback_result: Any | None = None,
) -> dict[str, Any]:
    """Ops / Founder dashboard hook — observational Evidence shadow status."""
    if validator is None or not validator.is_enabled():
        return {
            "evidence_shadow_validation": {
                "enabled": False,
                "phase": "e5_shadow_validation",
                "health": None,
                "last_observation": None,
                "last_report": None,
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
    report = validator.last_report
    return {
        "evidence_shadow_validation": {
            "enabled": True,
            "phase": "e5_shadow_validation",
            "validator_id": validator.validator_id,
            "validator_version": validator.validator_version,
            "health": validator.health_snapshot().to_canonical_dict(),
            "last_observation": (
                None if last is None else last.to_canonical_dict()
            ),
            "last_report": None if report is None else report.to_canonical_dict(),
            "influences_student": False,
            "deploys_policy": False,
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
    "EvidencePlatformState",
    "EvidenceShadowObservation",
    "EvidenceShadowValidator",
    "build_evidence_shadow_ops_dashboard",
    "build_evidence_shadow_validator",
]
