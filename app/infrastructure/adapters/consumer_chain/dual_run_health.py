"""In-process health metrics for Study Insights dual-run (EP-002.4).

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
class StudyInsightsDualRunHealthSnapshot:
    """Immutable ops-facing dual-run health projection."""

    dual_run_requests: int = 0
    legacy_success_count: int = 0
    twin_success_count: int = 0
    twin_unavailable_count: int = 0
    twin_exception_count: int = 0
    divergence_count: int = 0
    behavioural_regressions: int = 0
    ownership_violations: int = 0
    legacy_success_rate: float = 0.0
    twin_success_rate: float = 0.0
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
            "twin_exception_count": self.twin_exception_count,
            "twin_success_count": self.twin_success_count,
            "twin_success_rate": self.twin_success_rate,
            "twin_unavailable_count": self.twin_unavailable_count,
        }


@dataclass
class StudyInsightsDualRunHealthMetrics:
    """Mutable in-process dual-run aggregator (observational)."""

    _lock: Lock = field(default_factory=Lock, repr=False)
    dual_run_requests: int = 0
    legacy_success_count: int = 0
    twin_success_count: int = 0
    twin_unavailable_count: int = 0
    twin_exception_count: int = 0
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
            self.divergence_count = 0
            self.behavioural_regressions = 0
            self.ownership_violations = 0
            self._legacy_latencies_ms.clear()
            self._twin_latencies_ms.clear()
            self._limitation_codes.clear()

    def record(self, comparison: dict[str, Any]) -> None:
        """Record one dual-run comparison (diagnostic only)."""
        with self._lock:
            self.dual_run_requests += 1
            legacy_unavailable = bool(comparison.get("legacy_unavailable"))
            twin_unavailable = bool(comparison.get("twin_unavailable"))
            twin_exception = bool(comparison.get("twin_exception"))
            if not legacy_unavailable:
                self.legacy_success_count += 1
            if twin_exception:
                self.twin_exception_count += 1
            elif twin_unavailable:
                self.twin_unavailable_count += 1
            else:
                self.twin_success_count += 1
            if not bool(comparison.get("fingerprints_match")):
                self.divergence_count += 1
            legacy_ms = comparison.get("legacy_latency_ms")
            twin_ms = comparison.get("twin_latency_ms")
            if legacy_ms is not None:
                self._legacy_latencies_ms.append(float(legacy_ms))
            if twin_ms is not None:
                self._twin_latencies_ms.append(float(twin_ms))
            for code in comparison.get("limitation_codes") or ():
                text = str(code).strip()
                if text:
                    self._limitation_codes[text] += 1

    def mark_behavioural_regression(self, count: int = 1) -> None:
        with self._lock:
            self.behavioural_regressions += max(0, int(count))

    def mark_ownership_violation(self, count: int = 1) -> None:
        with self._lock:
            self.ownership_violations += max(0, int(count))

    def snapshot(self) -> StudyInsightsDualRunHealthSnapshot:
        with self._lock:
            requests = self.dual_run_requests
            legacy_ok = self.legacy_success_count
            twin_ok = self.twin_success_count
            divergences = self.divergence_count
            legacy_lat = list(self._legacy_latencies_ms)
            twin_lat = list(self._twin_latencies_ms)
            codes = tuple(self._limitation_codes.most_common())
            regressions = self.behavioural_regressions
            ownership = self.ownership_violations
            twin_unavailable = self.twin_unavailable_count
            twin_exception = self.twin_exception_count

        legacy_sorted = sorted(legacy_lat)
        twin_sorted = sorted(twin_lat)
        readiness = _assess_readiness(
            requests=requests,
            twin_ok=twin_ok,
            regressions=regressions,
            ownership=ownership,
        )
        return StudyInsightsDualRunHealthSnapshot(
            dual_run_requests=requests,
            legacy_success_count=legacy_ok,
            twin_success_count=twin_ok,
            twin_unavailable_count=twin_unavailable,
            twin_exception_count=twin_exception,
            divergence_count=divergences,
            behavioural_regressions=regressions,
            ownership_violations=ownership,
            legacy_success_rate=_rate(legacy_ok, requests),
            twin_success_rate=_rate(twin_ok, requests),
            divergence_rate=_rate(divergences, requests),
            average_legacy_latency_ms=_avg(legacy_lat),
            average_twin_latency_ms=_avg(twin_lat),
            p95_legacy_latency_ms=_percentile(legacy_sorted, 95.0),
            p95_twin_latency_ms=_percentile(twin_sorted, 95.0),
            limitation_code_frequency=codes,
            overall_dual_run_readiness=readiness,
        )


def _assess_readiness(
    *,
    requests: int,
    twin_ok: int,
    regressions: int,
    ownership: int,
) -> str:
    if regressions > 0 or ownership > 0:
        return "blocked"
    if requests <= 0:
        return "not_assessed"
    if twin_ok <= 0:
        return "observational_only"
    return "ready_for_ep002_5_planning"


_DEFAULT: StudyInsightsDualRunHealthMetrics | None = None


def get_study_insights_dual_run_health_metrics() -> StudyInsightsDualRunHealthMetrics:
    """Return the process-default dual-run health aggregator."""
    global _DEFAULT
    if _DEFAULT is None:
        _DEFAULT = StudyInsightsDualRunHealthMetrics()
    return _DEFAULT


def set_study_insights_dual_run_health_metrics(
    metrics: StudyInsightsDualRunHealthMetrics | None,
) -> StudyInsightsDualRunHealthMetrics | None:
    """Replace the process-default aggregator; return the previous value."""
    global _DEFAULT
    previous = _DEFAULT
    _DEFAULT = metrics
    return previous


def build_study_insights_dual_run_health_metrics() -> StudyInsightsDualRunHealthMetrics:
    """Construct a fresh dual-run health aggregator."""
    return StudyInsightsDualRunHealthMetrics()
