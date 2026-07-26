"""Operational metrics for analytics infrastructure (EP-002 WS2).

Infrastructure counters only — never educational scores, mastery, or readiness.
Process-local; suitable for CLI snapshots and log-based monitoring until a
central metrics backend is composed.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class AnalyticsOperationalMetrics:
    """Thread-safe operational counters for the analytics pipeline.

    Attributes track infrastructure health only (PRD-001 / EP-002). Educational
    outcome metrics must never be recorded here.
    """

    events_received: int = 0
    events_dispatched: int = 0
    events_failed: int = 0
    events_rejected: int = 0
    events_duplicate: int = 0
    events_disabled: int = 0
    dispatch_latency_ms_total: float = 0.0
    dispatch_latency_samples: int = 0
    queue_depth: int = 0
    replay_count: int = 0
    duplicate_count: int = 0
    dead_letter_count: int = 0
    purge_deleted: int = 0
    user_deletions: int = 0
    exports_completed: int = 0
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def record_dispatch(
        self,
        *,
        status: str,
        elapsed_ms: float = 0.0,
    ) -> None:
        """Record one dispatcher outcome."""
        with self._lock:
            self.events_received += 1
            if elapsed_ms > 0:
                self.dispatch_latency_ms_total += elapsed_ms
                self.dispatch_latency_samples += 1
            if status == "enqueued":
                self.events_dispatched += 1
            elif status == "failed":
                self.events_failed += 1
            elif status == "rejected":
                self.events_rejected += 1
            elif status == "duplicate":
                self.events_duplicate += 1
                self.duplicate_count += 1
            elif status == "disabled":
                self.events_disabled += 1

    def set_queue_depth(self, depth: int) -> None:
        """Update current outbox pending (+ failed retryable) depth."""
        with self._lock:
            self.queue_depth = max(0, int(depth))

    def record_worker_success(self) -> None:
        """Record one successful outbox → event-store drain."""
        with self._lock:
            self.events_dispatched += 1

    def record_worker_failure(self) -> None:
        """Record one worker processing failure."""
        with self._lock:
            self.events_failed += 1

    def record_dead_letter(self) -> None:
        """Record one dead-letter transition."""
        with self._lock:
            self.dead_letter_count += 1

    def record_duplicate_suppressed(self) -> None:
        """Record idempotent duplicate suppression during drain/append."""
        with self._lock:
            self.duplicate_count += 1

    def record_replay(self, count: int = 1) -> None:
        """Record dead-letter / failed requeue operations."""
        with self._lock:
            self.replay_count += max(0, int(count))

    def record_purge(self, deleted: int) -> None:
        """Record retention purge deletions."""
        with self._lock:
            self.purge_deleted += max(0, int(deleted))

    def record_user_deletion(self) -> None:
        """Record one user analytics cascade deletion."""
        with self._lock:
            self.user_deletions += 1

    def record_export(self) -> None:
        """Record one privacy export fulfilment."""
        with self._lock:
            self.exports_completed += 1

    @property
    def dispatch_latency_ms_avg(self) -> float:
        """Average dispatch latency in milliseconds (0 if no samples)."""
        with self._lock:
            if self.dispatch_latency_samples == 0:
                return 0.0
            return self.dispatch_latency_ms_total / self.dispatch_latency_samples

    def snapshot(self) -> dict[str, Any]:
        """Return a plain dict snapshot for monitoring / CLI."""
        with self._lock:
            avg = (
                self.dispatch_latency_ms_total / self.dispatch_latency_samples
                if self.dispatch_latency_samples
                else 0.0
            )
            return {
                "events_received": self.events_received,
                "events_dispatched": self.events_dispatched,
                "events_failed": self.events_failed,
                "events_rejected": self.events_rejected,
                "events_duplicate": self.events_duplicate,
                "events_disabled": self.events_disabled,
                "dispatch_latency_ms_avg": round(avg, 4),
                "dispatch_latency_samples": self.dispatch_latency_samples,
                "queue_depth": self.queue_depth,
                "replay_count": self.replay_count,
                "duplicate_count": self.duplicate_count,
                "dead_letter_count": self.dead_letter_count,
                "purge_deleted": self.purge_deleted,
                "user_deletions": self.user_deletions,
                "exports_completed": self.exports_completed,
                "observed_at": time.time(),
            }

    def reset(self) -> None:
        """Reset all counters (tests only)."""
        with self._lock:
            self.events_received = 0
            self.events_dispatched = 0
            self.events_failed = 0
            self.events_rejected = 0
            self.events_duplicate = 0
            self.events_disabled = 0
            self.dispatch_latency_ms_total = 0.0
            self.dispatch_latency_samples = 0
            self.queue_depth = 0
            self.replay_count = 0
            self.duplicate_count = 0
            self.dead_letter_count = 0
            self.purge_deleted = 0
            self.user_deletions = 0
            self.exports_completed = 0


# Process-scoped default registry (tests may construct isolated instances).
ANALYTICS_METRICS = AnalyticsOperationalMetrics()
