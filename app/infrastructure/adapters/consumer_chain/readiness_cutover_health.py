"""In-process health metrics for Readiness Intelligence HTTP cutover (EP-002.6).

Aggregates cutover / fallback / alignment rates. Never influences student UX.
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
class ReadinessCutoverHealthSnapshot:
    """Immutable ops-facing readiness cutover health projection."""

    eligible_requests: int = 0
    cutover_served_count: int = 0
    legacy_fallback_count: int = 0
    twin_success_count: int = 0
    aligned_count: int = 0
    mismatched_count: int = 0
    twin_unavailable_alignment_count: int = 0
    limitation_fallback_count: int = 0
    behavioural_regressions: int = 0
    ownership_violations: int = 0
    legacy_fallback_rate: float = 0.0
    twin_success_rate: float = 0.0
    alignment_rate: float = 0.0
    limitation_driven_fallback_rate: float = 0.0
    average_legacy_latency_ms: float = 0.0
    average_twin_latency_ms: float = 0.0
    p95_legacy_latency_ms: float = 0.0
    p95_twin_latency_ms: float = 0.0
    overall_cutover_readiness: str = "not_assessed"

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "aligned_count": self.aligned_count,
            "alignment_rate": self.alignment_rate,
            "average_legacy_latency_ms": self.average_legacy_latency_ms,
            "average_twin_latency_ms": self.average_twin_latency_ms,
            "behavioural_regressions": self.behavioural_regressions,
            "cutover_served_count": self.cutover_served_count,
            "eligible_requests": self.eligible_requests,
            "legacy_fallback_count": self.legacy_fallback_count,
            "legacy_fallback_rate": self.legacy_fallback_rate,
            "limitation_driven_fallback_rate": self.limitation_driven_fallback_rate,
            "limitation_fallback_count": self.limitation_fallback_count,
            "mismatched_count": self.mismatched_count,
            "overall_cutover_readiness": self.overall_cutover_readiness,
            "ownership_violations": self.ownership_violations,
            "p95_legacy_latency_ms": self.p95_legacy_latency_ms,
            "p95_twin_latency_ms": self.p95_twin_latency_ms,
            "twin_success_count": self.twin_success_count,
            "twin_success_rate": self.twin_success_rate,
            "twin_unavailable_alignment_count": self.twin_unavailable_alignment_count,
        }


@dataclass
class ReadinessCutoverHealthMetrics:
    """Mutable in-process readiness cutover aggregator."""

    _lock: Lock = field(default_factory=Lock, repr=False)
    eligible_requests: int = 0
    cutover_served_count: int = 0
    legacy_fallback_count: int = 0
    twin_success_count: int = 0
    aligned_count: int = 0
    mismatched_count: int = 0
    twin_unavailable_alignment_count: int = 0
    limitation_fallback_count: int = 0
    behavioural_regressions: int = 0
    ownership_violations: int = 0
    _legacy_latencies_ms: list[float] = field(default_factory=list, repr=False)
    _twin_latencies_ms: list[float] = field(default_factory=list, repr=False)
    _fallback_reasons: Counter[str] = field(default_factory=Counter, repr=False)

    def reset(self) -> None:
        with self._lock:
            self.eligible_requests = 0
            self.cutover_served_count = 0
            self.legacy_fallback_count = 0
            self.twin_success_count = 0
            self.aligned_count = 0
            self.mismatched_count = 0
            self.twin_unavailable_alignment_count = 0
            self.limitation_fallback_count = 0
            self.behavioural_regressions = 0
            self.ownership_violations = 0
            self._legacy_latencies_ms.clear()
            self._twin_latencies_ms.clear()
            self._fallback_reasons.clear()

    def record(self, event: dict[str, Any]) -> None:
        with self._lock:
            attempted = bool(event.get("cutover_attempted"))
            if not attempted:
                reason = str(event.get("fallback_reason") or "")
                if reason:
                    self._fallback_reasons[reason] += 1
                return

            self.eligible_requests += 1
            served = bool(event.get("cutover_served"))
            if served:
                self.cutover_served_count += 1
                self.twin_success_count += 1
            else:
                self.legacy_fallback_count += 1
                reason = str(event.get("fallback_reason") or "")
                if reason:
                    self._fallback_reasons[reason] += 1
                if reason in {"blocking_limitation", "projection_empty"}:
                    self.limitation_fallback_count += 1

            status = str(event.get("alignment_status") or "")
            if status == "aligned":
                self.aligned_count += 1
            elif status == "mismatched":
                self.mismatched_count += 1
            elif status == "twin_unavailable":
                self.twin_unavailable_alignment_count += 1
            elif status == "limitation_fallback":
                if str(event.get("fallback_reason") or "") not in {
                    "blocking_limitation",
                    "projection_empty",
                }:
                    self.limitation_fallback_count += 1

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

    def snapshot(self) -> ReadinessCutoverHealthSnapshot:
        with self._lock:
            eligible = self.eligible_requests
            legacy_sorted = sorted(self._legacy_latencies_ms)
            twin_sorted = sorted(self._twin_latencies_ms)
            alignment_denom = self.aligned_count + self.mismatched_count
            readiness = self._assess_unlocked()
            return ReadinessCutoverHealthSnapshot(
                eligible_requests=eligible,
                cutover_served_count=self.cutover_served_count,
                legacy_fallback_count=self.legacy_fallback_count,
                twin_success_count=self.twin_success_count,
                aligned_count=self.aligned_count,
                mismatched_count=self.mismatched_count,
                twin_unavailable_alignment_count=self.twin_unavailable_alignment_count,
                limitation_fallback_count=self.limitation_fallback_count,
                behavioural_regressions=self.behavioural_regressions,
                ownership_violations=self.ownership_violations,
                legacy_fallback_rate=_rate(self.legacy_fallback_count, eligible),
                twin_success_rate=_rate(self.twin_success_count, eligible),
                alignment_rate=_rate(self.aligned_count, alignment_denom),
                limitation_driven_fallback_rate=_rate(
                    self.limitation_fallback_count, eligible
                ),
                average_legacy_latency_ms=_avg(legacy_sorted),
                average_twin_latency_ms=_avg(twin_sorted),
                p95_legacy_latency_ms=_percentile(legacy_sorted, 95.0),
                p95_twin_latency_ms=_percentile(twin_sorted, 95.0),
                overall_cutover_readiness=readiness,
            )

    def _assess_unlocked(self) -> str:
        if self.behavioural_regressions > 0 or self.ownership_violations > 0:
            return "blocked"
        if self.eligible_requests <= 0:
            return "not_assessed"
        if self.cutover_served_count <= 0:
            return "observational_only"
        return "ready_for_ep002_7_planning"


_DEFAULT: ReadinessCutoverHealthMetrics | None = None


def get_readiness_cutover_health_metrics() -> ReadinessCutoverHealthMetrics:
    global _DEFAULT
    if _DEFAULT is None:
        _DEFAULT = ReadinessCutoverHealthMetrics()
    return _DEFAULT


def set_readiness_cutover_health_metrics(
    metrics: ReadinessCutoverHealthMetrics | None,
) -> ReadinessCutoverHealthMetrics | None:
    global _DEFAULT
    previous = _DEFAULT
    _DEFAULT = metrics
    return previous


def build_readiness_cutover_health_metrics() -> ReadinessCutoverHealthMetrics:
    return ReadinessCutoverHealthMetrics()
