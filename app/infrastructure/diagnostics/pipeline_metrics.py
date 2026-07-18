"""Pipeline metrics — operational counters for orchestration / adapters."""

from __future__ import annotations

from typing import Any


class PipelineMetrics:
    """Operational pipeline metrics only (no mastery / ROI / readiness)."""

    ALLOWED_COUNTERS = frozenset(
        {
            "pipeline_started",
            "pipeline_completed",
            "pipeline_failed",
            "stage_started",
            "stage_completed",
            "stage_failed",
            "adapter_invoked",
            "adapter_failed",
            "event_published",
            "transaction_committed",
            "transaction_rolled_back",
            "optimistic_lock_conflict",
        }
    )

    def __init__(self) -> None:
        self._counters: dict[str, int] = {k: 0 for k in self.ALLOWED_COUNTERS}
        self._labels: dict[str, dict[str, int]] = {}

    def incr(self, name: str, *, amount: int = 1, **labels: str) -> None:
        """Increment an allowed operational counter."""
        if name not in self.ALLOWED_COUNTERS:
            raise ValueError(f"educational or unknown metric refused: {name}")
        self._counters[name] = self._counters.get(name, 0) + amount
        if labels:
            key = name + "|" + ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
            bucket = self._labels.setdefault(name, {})
            bucket[key] = bucket.get(key, 0) + amount

    def get(self, name: str) -> int:
        """Return a counter value."""
        return self._counters.get(name, 0)

    def snapshot(self) -> dict[str, Any]:
        """Return an opaque operational metrics snapshot."""
        return {
            "counters": dict(self._counters),
            "labeled": {k: dict(v) for k, v in self._labels.items()},
        }

    def clear(self) -> None:
        """Reset all counters."""
        self._counters = {k: 0 for k in self.ALLOWED_COUNTERS}
        self._labels.clear()
