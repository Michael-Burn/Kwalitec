"""Health metrics for Twin Shadow Validation (MS-004 T6).

Aggregates observational rates only. Never influences Experience,
Adaptive Engine, Planning, or Runtime A.
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
class TwinShadowHealthSnapshot:
    """Immutable ops-facing Twin shadow health projection."""

    executions: int = 0
    snapshot_success_count: int = 0
    projection_success_count: int = 0
    explainability_success_count: int = 0
    unavailable_facet_total: int = 0
    deterministic_replay_attempts: int = 0
    deterministic_replay_successes: int = 0
    rollback_attempts: int = 0
    rollback_successes: int = 0
    feature_flag_isolation_checks: int = 0
    feature_flag_isolation_passes: int = 0
    drift_signal_count: int = 0
    failure_count: int = 0
    latency_ms_sum: float = 0.0
    latency_ms_count: int = 0
    snapshot_generation_success_rate: float = 0.0
    projection_success_rate: float = 0.0
    explainability_success_rate: float = 0.0
    unavailable_facet_frequency: float = 0.0
    deterministic_replay_success_rate: float = 0.0
    rollback_success_rate: float = 0.0
    feature_flag_isolation_pass_rate: float = 0.0
    mean_execution_latency_ms: float = 0.0

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "deterministic_replay_attempts": self.deterministic_replay_attempts,
            "deterministic_replay_success_rate": (
                self.deterministic_replay_success_rate
            ),
            "deterministic_replay_successes": self.deterministic_replay_successes,
            "drift_signal_count": self.drift_signal_count,
            "executions": self.executions,
            "explainability_success_count": self.explainability_success_count,
            "explainability_success_rate": self.explainability_success_rate,
            "failure_count": self.failure_count,
            "feature_flag_isolation_checks": self.feature_flag_isolation_checks,
            "feature_flag_isolation_pass_rate": (
                self.feature_flag_isolation_pass_rate
            ),
            "feature_flag_isolation_passes": self.feature_flag_isolation_passes,
            "latency_ms_count": self.latency_ms_count,
            "latency_ms_sum": round(self.latency_ms_sum, 3),
            "mean_execution_latency_ms": self.mean_execution_latency_ms,
            "projection_success_count": self.projection_success_count,
            "projection_success_rate": self.projection_success_rate,
            "rollback_attempts": self.rollback_attempts,
            "rollback_success_rate": self.rollback_success_rate,
            "rollback_successes": self.rollback_successes,
            "snapshot_generation_success_rate": (
                self.snapshot_generation_success_rate
            ),
            "snapshot_success_count": self.snapshot_success_count,
            "unavailable_facet_frequency": self.unavailable_facet_frequency,
            "unavailable_facet_total": self.unavailable_facet_total,
        }


@dataclass
class TwinShadowHealthMetrics:
    """Mutable in-process Twin shadow health aggregator (observational)."""

    _lock: Lock = field(default_factory=Lock, repr=False)
    executions: int = 0
    snapshot_success_count: int = 0
    projection_success_count: int = 0
    explainability_success_count: int = 0
    unavailable_facet_total: int = 0
    deterministic_replay_attempts: int = 0
    deterministic_replay_successes: int = 0
    rollback_attempts: int = 0
    rollback_successes: int = 0
    feature_flag_isolation_checks: int = 0
    feature_flag_isolation_passes: int = 0
    drift_signal_count: int = 0
    failure_count: int = 0
    latency_ms_sum: float = 0.0
    latency_ms_count: int = 0

    def record_execution(
        self,
        *,
        ok: bool,
        snapshot_ok: bool = False,
        projection_ok: bool = False,
        explainability_ok: bool = False,
        unavailable_facet_count: int = 0,
        determinism_success: bool | None = None,
        drift_signals: int = 0,
        latency_ms: float | None = None,
    ) -> None:
        """Record one Twin shadow validation observation."""
        with self._lock:
            self.executions += 1
            if not ok:
                self.failure_count += 1
            if snapshot_ok:
                self.snapshot_success_count += 1
            if projection_ok:
                self.projection_success_count += 1
            if explainability_ok:
                self.explainability_success_count += 1
            self.unavailable_facet_total += max(0, int(unavailable_facet_count))
            if determinism_success is not None:
                self.deterministic_replay_attempts += 1
                if determinism_success:
                    self.deterministic_replay_successes += 1
            self.drift_signal_count += max(0, int(drift_signals))
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
            self.snapshot_success_count = 0
            self.projection_success_count = 0
            self.explainability_success_count = 0
            self.unavailable_facet_total = 0
            self.deterministic_replay_attempts = 0
            self.deterministic_replay_successes = 0
            self.rollback_attempts = 0
            self.rollback_successes = 0
            self.feature_flag_isolation_checks = 0
            self.feature_flag_isolation_passes = 0
            self.drift_signal_count = 0
            self.failure_count = 0
            self.latency_ms_sum = 0.0
            self.latency_ms_count = 0

    def snapshot(self) -> TwinShadowHealthSnapshot:
        """Project current rates into an immutable ops snapshot."""
        with self._lock:
            mean_latency = (
                round(self.latency_ms_sum / self.latency_ms_count, 3)
                if self.latency_ms_count
                else 0.0
            )
            return TwinShadowHealthSnapshot(
                executions=self.executions,
                snapshot_success_count=self.snapshot_success_count,
                projection_success_count=self.projection_success_count,
                explainability_success_count=self.explainability_success_count,
                unavailable_facet_total=self.unavailable_facet_total,
                deterministic_replay_attempts=self.deterministic_replay_attempts,
                deterministic_replay_successes=self.deterministic_replay_successes,
                rollback_attempts=self.rollback_attempts,
                rollback_successes=self.rollback_successes,
                feature_flag_isolation_checks=self.feature_flag_isolation_checks,
                feature_flag_isolation_passes=self.feature_flag_isolation_passes,
                drift_signal_count=self.drift_signal_count,
                failure_count=self.failure_count,
                latency_ms_sum=self.latency_ms_sum,
                latency_ms_count=self.latency_ms_count,
                snapshot_generation_success_rate=_rate(
                    self.snapshot_success_count, self.executions
                ),
                projection_success_rate=_rate(
                    self.projection_success_count, self.executions
                ),
                explainability_success_rate=_rate(
                    self.explainability_success_count, self.executions
                ),
                unavailable_facet_frequency=_rate(
                    self.unavailable_facet_total, self.executions
                ),
                deterministic_replay_success_rate=_rate(
                    self.deterministic_replay_successes,
                    self.deterministic_replay_attempts,
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


def build_twin_shadow_health_metrics() -> TwinShadowHealthMetrics:
    """DI helper — fresh in-process health aggregator."""
    return TwinShadowHealthMetrics()


__all__ = [
    "TwinShadowHealthMetrics",
    "TwinShadowHealthSnapshot",
    "build_twin_shadow_health_metrics",
]
