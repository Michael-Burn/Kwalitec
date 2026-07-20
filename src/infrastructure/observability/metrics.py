"""Pipeline success / failure and timing metrics (operational only)."""

from __future__ import annotations

from typing import Any


class PipelineMetrics:
    """Counters and timing aggregates for Educational Pipeline runs.

    Forbidden: mastery, readiness, ROI, or other educational scores.
    """

    ALLOWED_COUNTERS = frozenset(
        {
            "pipeline_started",
            "pipeline_succeeded",
            "pipeline_failed",
            "ai_enrichment_started",
            "ai_enrichment_succeeded",
            "ai_enrichment_failed",
            "ai_enrichment_fallback",
            "ai_provider_retry",
            "ai_provider_timeout",
        }
    )

    def __init__(self) -> None:
        self._counters: dict[str, int] = {name: 0 for name in self.ALLOWED_COUNTERS}
        self._timings_ms: dict[str, list[float]] = {}

    def incr(self, name: str, *, amount: int = 1) -> None:
        if name not in self.ALLOWED_COUNTERS:
            raise ValueError(f"unknown or educational metric refused: {name}")
        self._counters[name] = self._counters.get(name, 0) + amount

    def record_timing(self, name: str, duration_ms: float) -> None:
        if duration_ms < 0:
            raise ValueError("duration_ms must be >= 0")
        self._timings_ms.setdefault(name, []).append(float(duration_ms))

    def get(self, name: str) -> int:
        return self._counters.get(name, 0)

    def timing_summary(self) -> dict[str, dict[str, float]]:
        summary: dict[str, dict[str, float]] = {}
        for name, samples in self._timings_ms.items():
            if not samples:
                continue
            summary[name] = {
                "count": float(len(samples)),
                "total_ms": sum(samples),
                "max_ms": max(samples),
                "last_ms": samples[-1],
            }
        return summary

    def snapshot(self) -> dict[str, Any]:
        return {
            "counters": dict(self._counters),
            "timings_ms": self.timing_summary(),
        }

    def clear(self) -> None:
        self._counters = {name: 0 for name in self.ALLOWED_COUNTERS}
        self._timings_ms.clear()
