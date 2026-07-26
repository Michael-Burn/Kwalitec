"""Operational health monitoring for Evidence Shadow Validation (MS-006 E5).

Aggregates observational rates only. Never influences Experience, Adaptive,
Twin, Strategy, Runtime A, or policy deployment.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Any


def _rate(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return round(float(numerator) / float(denominator), 6)


@dataclass(frozen=True)
class OperationalHealthSnapshot:
    """Immutable ops-facing Evidence shadow health projection."""

    executions: int = 0
    validation_success_count: int = 0
    determinism_success_count: int = 0
    determinism_attempts: int = 0
    readiness_ready_count: int = 0
    readiness_degraded_count: int = 0
    readiness_not_ready_count: int = 0
    rollback_attempts: int = 0
    rollback_successes: int = 0
    feature_flag_isolation_checks: int = 0
    feature_flag_isolation_passes: int = 0
    drift_signal_count: int = 0
    failure_count: int = 0
    evidence_coverage_count: int = 0
    observation_coverage_count: int = 0
    evaluation_coverage_count: int = 0
    analytics_coverage_count: int = 0
    projection_coverage_count: int = 0
    latency_ms_sum: float = 0.0
    latency_ms_count: int = 0
    validation_success_rate: float = 0.0
    determinism_success_rate: float = 0.0
    rollback_success_rate: float = 0.0
    feature_flag_isolation_pass_rate: float = 0.0
    mean_execution_latency_ms: float = 0.0

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "analytics_coverage_count": self.analytics_coverage_count,
            "determinism_attempts": self.determinism_attempts,
            "determinism_success_count": self.determinism_success_count,
            "determinism_success_rate": self.determinism_success_rate,
            "drift_signal_count": self.drift_signal_count,
            "evaluation_coverage_count": self.evaluation_coverage_count,
            "evidence_coverage_count": self.evidence_coverage_count,
            "executions": self.executions,
            "failure_count": self.failure_count,
            "feature_flag_isolation_checks": self.feature_flag_isolation_checks,
            "feature_flag_isolation_pass_rate": (
                self.feature_flag_isolation_pass_rate
            ),
            "feature_flag_isolation_passes": self.feature_flag_isolation_passes,
            "latency_ms_count": self.latency_ms_count,
            "latency_ms_sum": round(self.latency_ms_sum, 3),
            "mean_execution_latency_ms": self.mean_execution_latency_ms,
            "observation_coverage_count": self.observation_coverage_count,
            "projection_coverage_count": self.projection_coverage_count,
            "readiness_degraded_count": self.readiness_degraded_count,
            "readiness_not_ready_count": self.readiness_not_ready_count,
            "readiness_ready_count": self.readiness_ready_count,
            "rollback_attempts": self.rollback_attempts,
            "rollback_success_rate": self.rollback_success_rate,
            "rollback_successes": self.rollback_successes,
            "validation_success_count": self.validation_success_count,
            "validation_success_rate": self.validation_success_rate,
        }


@dataclass
class OperationalHealthMonitor:
    """Mutable in-process Evidence shadow health aggregator (observational)."""

    _lock: Lock = field(default_factory=Lock, repr=False)
    executions: int = 0
    validation_success_count: int = 0
    determinism_success_count: int = 0
    determinism_attempts: int = 0
    readiness_ready_count: int = 0
    readiness_degraded_count: int = 0
    readiness_not_ready_count: int = 0
    rollback_attempts: int = 0
    rollback_successes: int = 0
    feature_flag_isolation_checks: int = 0
    feature_flag_isolation_passes: int = 0
    drift_signal_count: int = 0
    failure_count: int = 0
    evidence_coverage_count: int = 0
    observation_coverage_count: int = 0
    evaluation_coverage_count: int = 0
    analytics_coverage_count: int = 0
    projection_coverage_count: int = 0
    latency_ms_sum: float = 0.0
    latency_ms_count: int = 0

    def record_execution(
        self,
        *,
        ok: bool,
        determinism_success: bool | None = None,
        readiness_status: str = "",
        drift_signals: int = 0,
        latency_ms: float | None = None,
        evidence_count: int = 0,
        observation_count: int = 0,
        evaluation_count: int = 0,
        analytics_count: int = 0,
        projection_count: int = 0,
    ) -> None:
        """Record one Evidence shadow validation observation."""
        with self._lock:
            self.executions += 1
            if not ok:
                self.failure_count += 1
            else:
                self.validation_success_count += 1
            if determinism_success is not None:
                self.determinism_attempts += 1
                if determinism_success:
                    self.determinism_success_count += 1
            status = (readiness_status or "").strip().lower()
            if status == "ready":
                self.readiness_ready_count += 1
            elif status == "degraded":
                self.readiness_degraded_count += 1
            elif status:
                self.readiness_not_ready_count += 1
            self.drift_signal_count += max(0, int(drift_signals))
            if evidence_count > 0:
                self.evidence_coverage_count += 1
            if observation_count > 0:
                self.observation_coverage_count += 1
            if evaluation_count > 0:
                self.evaluation_coverage_count += 1
            if analytics_count > 0:
                self.analytics_coverage_count += 1
            if projection_count > 0:
                self.projection_coverage_count += 1
            if latency_ms is not None:
                self.latency_ms_sum += float(latency_ms)
                self.latency_ms_count += 1

    def record_rollback(self, *, ok: bool) -> None:
        """Record one rollback verification drill."""
        with self._lock:
            self.rollback_attempts += 1
            if ok:
                self.rollback_successes += 1

    def record_feature_flag_isolation(self, *, passed: bool) -> None:
        """Record one feature-flag isolation check."""
        with self._lock:
            self.feature_flag_isolation_checks += 1
            if passed:
                self.feature_flag_isolation_passes += 1

    def reset(self) -> None:
        """Clear counters (tests / ops drill)."""
        with self._lock:
            self.executions = 0
            self.validation_success_count = 0
            self.determinism_success_count = 0
            self.determinism_attempts = 0
            self.readiness_ready_count = 0
            self.readiness_degraded_count = 0
            self.readiness_not_ready_count = 0
            self.rollback_attempts = 0
            self.rollback_successes = 0
            self.feature_flag_isolation_checks = 0
            self.feature_flag_isolation_passes = 0
            self.drift_signal_count = 0
            self.failure_count = 0
            self.evidence_coverage_count = 0
            self.observation_coverage_count = 0
            self.evaluation_coverage_count = 0
            self.analytics_coverage_count = 0
            self.projection_coverage_count = 0
            self.latency_ms_sum = 0.0
            self.latency_ms_count = 0

    def snapshot(self) -> OperationalHealthSnapshot:
        """Project current rates into an immutable ops snapshot."""
        with self._lock:
            mean_latency = (
                round(self.latency_ms_sum / self.latency_ms_count, 3)
                if self.latency_ms_count
                else 0.0
            )
            return OperationalHealthSnapshot(
                executions=self.executions,
                validation_success_count=self.validation_success_count,
                determinism_success_count=self.determinism_success_count,
                determinism_attempts=self.determinism_attempts,
                readiness_ready_count=self.readiness_ready_count,
                readiness_degraded_count=self.readiness_degraded_count,
                readiness_not_ready_count=self.readiness_not_ready_count,
                rollback_attempts=self.rollback_attempts,
                rollback_successes=self.rollback_successes,
                feature_flag_isolation_checks=self.feature_flag_isolation_checks,
                feature_flag_isolation_passes=self.feature_flag_isolation_passes,
                drift_signal_count=self.drift_signal_count,
                failure_count=self.failure_count,
                evidence_coverage_count=self.evidence_coverage_count,
                observation_coverage_count=self.observation_coverage_count,
                evaluation_coverage_count=self.evaluation_coverage_count,
                analytics_coverage_count=self.analytics_coverage_count,
                projection_coverage_count=self.projection_coverage_count,
                latency_ms_sum=self.latency_ms_sum,
                latency_ms_count=self.latency_ms_count,
                validation_success_rate=_rate(
                    self.validation_success_count, self.executions
                ),
                determinism_success_rate=_rate(
                    self.determinism_success_count, self.determinism_attempts
                ),
                rollback_success_rate=_rate(
                    self.rollback_successes, self.rollback_attempts
                ),
                feature_flag_isolation_pass_rate=_rate(
                    self.feature_flag_isolation_passes,
                    self.feature_flag_isolation_checks,
                ),
                mean_execution_latency_ms=mean_latency,
            )


def build_operational_health_monitor() -> OperationalHealthMonitor:
    """DI helper — fresh in-process health aggregator."""
    return OperationalHealthMonitor()


__all__ = [
    "OperationalHealthMonitor",
    "OperationalHealthSnapshot",
    "build_operational_health_monitor",
]
