"""Health metrics for Twin & Authority soak (EP-002.3).

Aggregates observational rates only. Never influences student UX.
"""

from __future__ import annotations

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


@dataclass(frozen=True)
class TwinAuthoritySoakHealthSnapshot:
    """Immutable ops-facing soak health projection."""

    executions: int = 0
    success_count: int = 0
    unavailable_count: int = 0
    limitation_count: int = 0
    failure_count: int = 0
    exception_count: int = 0
    foundation_assemble_count: int = 0
    share_hit_count: int = 0
    latency_ms_sum: float = 0.0
    latency_ms_count: int = 0
    average_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    share_hit_rate: float = 0.0
    failure_rate: float = 0.0
    rollback_ok: bool = False
    matrix_cells_ok: int = 0
    matrix_cells_total: int = 0

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "average_latency_ms": self.average_latency_ms,
            "exception_count": self.exception_count,
            "executions": self.executions,
            "failure_count": self.failure_count,
            "failure_rate": self.failure_rate,
            "foundation_assemble_count": self.foundation_assemble_count,
            "limitation_count": self.limitation_count,
            "matrix_cells_ok": self.matrix_cells_ok,
            "matrix_cells_total": self.matrix_cells_total,
            "p95_latency_ms": self.p95_latency_ms,
            "rollback_ok": self.rollback_ok,
            "share_hit_count": self.share_hit_count,
            "share_hit_rate": self.share_hit_rate,
            "success_count": self.success_count,
            "unavailable_count": self.unavailable_count,
        }


@dataclass
class TwinAuthoritySoakHealthMetrics:
    """Mutable in-process soak health aggregator (observational)."""

    _lock: Lock = field(default_factory=Lock, repr=False)
    executions: int = 0
    success_count: int = 0
    unavailable_count: int = 0
    limitation_count: int = 0
    failure_count: int = 0
    exception_count: int = 0
    foundation_assemble_count: int = 0
    share_hit_count: int = 0
    latency_ms_sum: float = 0.0
    latency_ms_count: int = 0
    _latencies_ms: list[float] = field(default_factory=list, repr=False)
    rollback_ok: bool = False
    matrix_cells_ok: int = 0
    matrix_cells_total: int = 0
    limitation_code_counts: dict[str, int] = field(default_factory=dict)

    def record_execution(
        self,
        *,
        outcome: str,
        latency_ms: float | None = None,
        limitation_codes: tuple[str, ...] | list[str] | None = None,
        exception: bool = False,
    ) -> None:
        with self._lock:
            self.executions += 1
            if exception or outcome == "exception":
                self.exception_count += 1
                self.failure_count += 1
            elif outcome == "unavailable":
                self.unavailable_count += 1
            elif outcome == "limitation":
                self.limitation_count += 1
            elif outcome == "success":
                self.success_count += 1
            else:
                self.failure_count += 1

            for code in limitation_codes or ():
                key = str(code)
                self.limitation_code_counts[key] = (
                    self.limitation_code_counts.get(key, 0) + 1
                )

            if latency_ms is not None:
                ms = float(latency_ms)
                self.latency_ms_sum += ms
                self.latency_ms_count += 1
                self._latencies_ms.append(ms)

    def record_foundation(
        self, *, assembled: bool, share_hit: bool = False
    ) -> None:
        with self._lock:
            if assembled:
                self.foundation_assemble_count += 1
            if share_hit:
                self.share_hit_count += 1

    def record_rollback(self, *, ok: bool) -> None:
        with self._lock:
            self.rollback_ok = bool(ok)

    def record_matrix(self, *, ok: bool) -> None:
        with self._lock:
            self.matrix_cells_total += 1
            if ok:
                self.matrix_cells_ok += 1

    def snapshot(self) -> TwinAuthoritySoakHealthSnapshot:
        with self._lock:
            avg = (
                round(self.latency_ms_sum / self.latency_ms_count, 3)
                if self.latency_ms_count
                else 0.0
            )
            sorted_lat = sorted(self._latencies_ms)
            assemble_total = (
                self.foundation_assemble_count + self.share_hit_count
            )
            return TwinAuthoritySoakHealthSnapshot(
                executions=self.executions,
                success_count=self.success_count,
                unavailable_count=self.unavailable_count,
                limitation_count=self.limitation_count,
                failure_count=self.failure_count,
                exception_count=self.exception_count,
                foundation_assemble_count=self.foundation_assemble_count,
                share_hit_count=self.share_hit_count,
                latency_ms_sum=round(self.latency_ms_sum, 3),
                latency_ms_count=self.latency_ms_count,
                average_latency_ms=avg,
                p95_latency_ms=_percentile(sorted_lat, 95.0),
                share_hit_rate=_rate(self.share_hit_count, assemble_total),
                failure_rate=_rate(
                    self.failure_count + self.exception_count, self.executions
                ),
                rollback_ok=self.rollback_ok,
                matrix_cells_ok=self.matrix_cells_ok,
                matrix_cells_total=self.matrix_cells_total,
            )

    def clear(self) -> None:
        with self._lock:
            self.executions = 0
            self.success_count = 0
            self.unavailable_count = 0
            self.limitation_count = 0
            self.failure_count = 0
            self.exception_count = 0
            self.foundation_assemble_count = 0
            self.share_hit_count = 0
            self.latency_ms_sum = 0.0
            self.latency_ms_count = 0
            self._latencies_ms.clear()
            self.rollback_ok = False
            self.matrix_cells_ok = 0
            self.matrix_cells_total = 0
            self.limitation_code_counts.clear()


def build_twin_authority_soak_health_metrics() -> TwinAuthoritySoakHealthMetrics:
    """DI helper for soak health metrics."""
    return TwinAuthoritySoakHealthMetrics()


__all__ = [
    "TwinAuthoritySoakHealthMetrics",
    "TwinAuthoritySoakHealthSnapshot",
    "build_twin_authority_soak_health_metrics",
]
