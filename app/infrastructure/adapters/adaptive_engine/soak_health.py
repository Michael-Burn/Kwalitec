"""Health metrics for Adaptive Shadow Soak (MS-003 A6).

Aggregates observational rates only. Never influences recommendations,
missions, Planning, or Runtime A.
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
class SoakHealthSnapshot:
    """Immutable ops-facing soak health projection."""

    executions: int = 0
    agreement_count: int = 0
    divergence_count: int = 0
    explainability_pass_count: int = 0
    trace_creation_count: int = 0
    deterministic_replay_attempts: int = 0
    deterministic_replay_successes: int = 0
    fallback_count: int = 0
    drift_signal_count: int = 0
    failure_count: int = 0
    latency_ms_sum: float = 0.0
    latency_ms_count: int = 0
    recommendation_agreement_rate: float = 0.0
    recommendation_divergence_rate: float = 0.0
    explainability_pass_rate: float = 0.0
    trace_creation_rate: float = 0.0
    deterministic_replay_success_rate: float = 0.0
    fallback_frequency: float = 0.0
    mean_execution_latency_ms: float = 0.0

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "agreement_count": self.agreement_count,
            "deterministic_replay_attempts": self.deterministic_replay_attempts,
            "deterministic_replay_success_rate": (
                self.deterministic_replay_success_rate
            ),
            "deterministic_replay_successes": self.deterministic_replay_successes,
            "divergence_count": self.divergence_count,
            "drift_signal_count": self.drift_signal_count,
            "executions": self.executions,
            "explainability_pass_count": self.explainability_pass_count,
            "explainability_pass_rate": self.explainability_pass_rate,
            "failure_count": self.failure_count,
            "fallback_count": self.fallback_count,
            "fallback_frequency": self.fallback_frequency,
            "latency_ms_count": self.latency_ms_count,
            "latency_ms_sum": round(self.latency_ms_sum, 3),
            "mean_execution_latency_ms": self.mean_execution_latency_ms,
            "recommendation_agreement_rate": self.recommendation_agreement_rate,
            "recommendation_divergence_rate": self.recommendation_divergence_rate,
            "trace_creation_count": self.trace_creation_count,
            "trace_creation_rate": self.trace_creation_rate,
        }


@dataclass
class SoakHealthMetrics:
    """Mutable in-process soak health aggregator (observational)."""

    _lock: Lock = field(default_factory=Lock, repr=False)
    executions: int = 0
    agreement_count: int = 0
    divergence_count: int = 0
    explainability_pass_count: int = 0
    trace_creation_count: int = 0
    deterministic_replay_attempts: int = 0
    deterministic_replay_successes: int = 0
    fallback_count: int = 0
    drift_signal_count: int = 0
    failure_count: int = 0
    latency_ms_sum: float = 0.0
    latency_ms_count: int = 0

    def record_execution(
        self,
        *,
        ok: bool,
        agreed: bool | None = None,
        explainability_passed: bool = False,
        trace_created: bool = False,
        determinism_success: bool | None = None,
        fallback: bool = False,
        drift_signals: int = 0,
        latency_ms: float | None = None,
    ) -> None:
        """Record one soak execution observation."""
        with self._lock:
            self.executions += 1
            if not ok:
                self.failure_count += 1
            if agreed is True:
                self.agreement_count += 1
            elif agreed is False:
                self.divergence_count += 1
            if explainability_passed:
                self.explainability_pass_count += 1
            if trace_created:
                self.trace_creation_count += 1
            if determinism_success is not None:
                self.deterministic_replay_attempts += 1
                if determinism_success:
                    self.deterministic_replay_successes += 1
            if fallback:
                self.fallback_count += 1
            self.drift_signal_count += max(0, int(drift_signals))
            if latency_ms is not None:
                self.latency_ms_sum += float(latency_ms)
                self.latency_ms_count += 1

    def reset(self) -> None:
        """Clear counters (tests / ops drill)."""
        with self._lock:
            self.executions = 0
            self.agreement_count = 0
            self.divergence_count = 0
            self.explainability_pass_count = 0
            self.trace_creation_count = 0
            self.deterministic_replay_attempts = 0
            self.deterministic_replay_successes = 0
            self.fallback_count = 0
            self.drift_signal_count = 0
            self.failure_count = 0
            self.latency_ms_sum = 0.0
            self.latency_ms_count = 0

    def snapshot(self) -> SoakHealthSnapshot:
        """Project current rates into an immutable ops snapshot."""
        with self._lock:
            comparable = self.agreement_count + self.divergence_count
            mean_latency = (
                round(self.latency_ms_sum / self.latency_ms_count, 3)
                if self.latency_ms_count
                else 0.0
            )
            return SoakHealthSnapshot(
                executions=self.executions,
                agreement_count=self.agreement_count,
                divergence_count=self.divergence_count,
                explainability_pass_count=self.explainability_pass_count,
                trace_creation_count=self.trace_creation_count,
                deterministic_replay_attempts=self.deterministic_replay_attempts,
                deterministic_replay_successes=self.deterministic_replay_successes,
                fallback_count=self.fallback_count,
                drift_signal_count=self.drift_signal_count,
                failure_count=self.failure_count,
                latency_ms_sum=self.latency_ms_sum,
                latency_ms_count=self.latency_ms_count,
                recommendation_agreement_rate=_rate(self.agreement_count, comparable),
                recommendation_divergence_rate=_rate(
                    self.divergence_count, comparable
                ),
                explainability_pass_rate=_rate(
                    self.explainability_pass_count, self.executions
                ),
                trace_creation_rate=_rate(
                    self.trace_creation_count, self.executions
                ),
                deterministic_replay_success_rate=_rate(
                    self.deterministic_replay_successes,
                    self.deterministic_replay_attempts,
                ),
                fallback_frequency=_rate(self.fallback_count, self.executions),
                mean_execution_latency_ms=mean_latency,
            )


def build_soak_health_metrics() -> SoakHealthMetrics:
    """DI helper — fresh in-process health aggregator."""
    return SoakHealthMetrics()


__all__ = [
    "SoakHealthMetrics",
    "SoakHealthSnapshot",
    "build_soak_health_metrics",
]
