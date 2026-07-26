"""In-process health metrics for Daily Plan dual-run (EP-002.7).

Aggregates observational rates only. Never influences student UX.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from threading import Lock
from typing import Any


def _rate(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return round(float(numerator) / float(denominator), 6)


def _percentile(sorted_values: list[float], pct: float) -> float:
    if not sorted_values:
        return 0.0
    if len(sorted_values) == 1:
        return round(sorted_values[0], 3)
    rank = (len(sorted_values) - 1) * (pct / 100.0)
    low = int(rank)
    high = min(low + 1, len(sorted_values) - 1)
    weight = rank - low
    value = sorted_values[low] * (1.0 - weight) + sorted_values[high] * weight
    return round(float(value), 3)


def _avg(values: list[float]) -> float:
    if not values:
        return 0.0
    return round(sum(values) / float(len(values)), 3)


@dataclass(frozen=True)
class DailyPlanDualRunHealthSnapshot:
    """Immutable ops-facing daily-plan dual-run health projection."""

    dual_run_requests: int = 0
    legacy_success_count: int = 0
    twin_success_count: int = 0
    twin_unavailable_count: int = 0
    twin_exception_count: int = 0
    topic_agreement_count: int = 0
    divergence_count: int = 0
    behavioural_regressions: int = 0
    ownership_violations: int = 0
    legacy_success_rate: float = 0.0
    twin_success_rate: float = 0.0
    topic_agreement_rate: float = 0.0
    divergence_rate: float = 0.0
    average_legacy_latency_ms: float = 0.0
    average_twin_latency_ms: float = 0.0
    p95_legacy_latency_ms: float = 0.0
    p95_twin_latency_ms: float = 0.0
    limitation_code_frequency: tuple[tuple[str, int], ...] = ()
    overall_dual_run_readiness: str = "not_assessed"

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "average_legacy_latency_ms": self.average_legacy_latency_ms,
            "average_twin_latency_ms": self.average_twin_latency_ms,
            "behavioural_regressions": self.behavioural_regressions,
            "divergence_count": self.divergence_count,
            "divergence_rate": self.divergence_rate,
            "dual_run_requests": self.dual_run_requests,
            "legacy_success_count": self.legacy_success_count,
            "legacy_success_rate": self.legacy_success_rate,
            "limitation_code_frequency": {
                code: count for code, count in self.limitation_code_frequency
            },
            "overall_dual_run_readiness": self.overall_dual_run_readiness,
            "ownership_violations": self.ownership_violations,
            "p95_legacy_latency_ms": self.p95_legacy_latency_ms,
            "p95_twin_latency_ms": self.p95_twin_latency_ms,
            "topic_agreement_count": self.topic_agreement_count,
            "topic_agreement_rate": self.topic_agreement_rate,
            "twin_exception_count": self.twin_exception_count,
            "twin_success_count": self.twin_success_count,
            "twin_success_rate": self.twin_success_rate,
            "twin_unavailable_count": self.twin_unavailable_count,
        }


@dataclass
class DailyPlanDualRunHealthMetrics:
    """Mutable in-process daily-plan dual-run aggregator."""

    _lock: Lock = field(default_factory=Lock, repr=False)
    dual_run_requests: int = 0
    legacy_success_count: int = 0
    twin_success_count: int = 0
    twin_unavailable_count: int = 0
    twin_exception_count: int = 0
    topic_agreement_count: int = 0
    divergence_count: int = 0
    behavioural_regressions: int = 0
    ownership_violations: int = 0
    _legacy_latencies_ms: list[float] = field(default_factory=list, repr=False)
    _twin_latencies_ms: list[float] = field(default_factory=list, repr=False)
    _limitation_codes: Counter[str] = field(default_factory=Counter, repr=False)

    def reset(self) -> None:
        with self._lock:
            self.dual_run_requests = 0
            self.legacy_success_count = 0
            self.twin_success_count = 0
            self.twin_unavailable_count = 0
            self.twin_exception_count = 0
            self.topic_agreement_count = 0
            self.divergence_count = 0
            self.behavioural_regressions = 0
            self.ownership_violations = 0
            self._legacy_latencies_ms.clear()
            self._twin_latencies_ms.clear()
            self._limitation_codes.clear()

    def record(self, event: dict[str, Any]) -> None:
        with self._lock:
            self.dual_run_requests += 1
            if not bool(event.get("legacy_unavailable")):
                self.legacy_success_count += 1
            if bool(event.get("twin_exception")):
                self.twin_exception_count += 1
            elif bool(event.get("twin_unavailable")):
                self.twin_unavailable_count += 1
            else:
                self.twin_success_count += 1

            if bool(event.get("topic_agreement")):
                self.topic_agreement_count += 1
            elif not bool(event.get("twin_unavailable")) and not bool(
                event.get("twin_exception")
            ):
                self.divergence_count += 1

            for code in event.get("limitation_codes") or ():
                self._limitation_codes[str(code)] += 1

            legacy_ms = event.get("legacy_latency_ms")
            if legacy_ms is not None:
                self._legacy_latencies_ms.append(float(legacy_ms))
            twin_ms = event.get("twin_latency_ms")
            if twin_ms is not None:
                self._twin_latencies_ms.append(float(twin_ms))

    def record_behavioural_regression(self, count: int = 1) -> None:
        with self._lock:
            self.behavioural_regressions += max(0, int(count))

    def record_ownership_violation(self, count: int = 1) -> None:
        with self._lock:
            self.ownership_violations += max(0, int(count))

    def snapshot(self) -> DailyPlanDualRunHealthSnapshot:
        with self._lock:
            total = self.dual_run_requests
            legacy_sorted = sorted(self._legacy_latencies_ms)
            twin_sorted = sorted(self._twin_latencies_ms)
            readiness = "not_assessed"
            if self.behavioural_regressions > 0 or self.ownership_violations > 0:
                readiness = "blocked"
            elif total > 0:
                readiness = "observational_ready"
            return DailyPlanDualRunHealthSnapshot(
                dual_run_requests=total,
                legacy_success_count=self.legacy_success_count,
                twin_success_count=self.twin_success_count,
                twin_unavailable_count=self.twin_unavailable_count,
                twin_exception_count=self.twin_exception_count,
                topic_agreement_count=self.topic_agreement_count,
                divergence_count=self.divergence_count,
                behavioural_regressions=self.behavioural_regressions,
                ownership_violations=self.ownership_violations,
                legacy_success_rate=_rate(self.legacy_success_count, total),
                twin_success_rate=_rate(self.twin_success_count, total),
                topic_agreement_rate=_rate(self.topic_agreement_count, total),
                divergence_rate=_rate(self.divergence_count, total),
                average_legacy_latency_ms=_avg(legacy_sorted),
                average_twin_latency_ms=_avg(twin_sorted),
                p95_legacy_latency_ms=_percentile(legacy_sorted, 95.0),
                p95_twin_latency_ms=_percentile(twin_sorted, 95.0),
                limitation_code_frequency=tuple(
                    self._limitation_codes.most_common()
                ),
                overall_dual_run_readiness=readiness,
            )


_DEFAULT: DailyPlanDualRunHealthMetrics | None = None


def get_daily_plan_dual_run_health_metrics() -> DailyPlanDualRunHealthMetrics:
    global _DEFAULT
    if _DEFAULT is None:
        _DEFAULT = DailyPlanDualRunHealthMetrics()
    return _DEFAULT


def set_daily_plan_dual_run_health_metrics(
    metrics: DailyPlanDualRunHealthMetrics | None,
) -> DailyPlanDualRunHealthMetrics | None:
    global _DEFAULT
    previous = _DEFAULT
    _DEFAULT = metrics
    return previous


def build_daily_plan_dual_run_health_metrics() -> DailyPlanDualRunHealthMetrics:
    return DailyPlanDualRunHealthMetrics()
