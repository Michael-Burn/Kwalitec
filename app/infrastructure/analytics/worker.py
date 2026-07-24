"""Outbox drain worker — durable dispatch to event store (EP-002 WS1).

Never runs on the educational request path. Failures never roll back
learning outcomes. Feature flag does not need to be on for drain of
already-enqueued rows (ops recovery); enqueue remains flag-gated.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from app.infrastructure.analytics.metrics import (
    ANALYTICS_METRICS,
    AnalyticsOperationalMetrics,
)
from app.infrastructure.analytics.outbox import DurableOutboxPort, OutboxRecord
from app.infrastructure.analytics.repository import AnalyticsEventRepository
from app.infrastructure.analytics.serialization import AnalyticsEventSerializer
from app.infrastructure.analytics.status import (
    DEFAULT_MAX_ATTEMPTS,
    DEFAULT_WORKER_BATCH_SIZE,
    OUTBOX_DEAD_LETTER,
    OUTBOX_FAILED,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class WorkerBatchResult:
    """Outcome of one worker drain pass."""

    claimed: int = 0
    processed: int = 0
    duplicates: int = 0
    failed: int = 0
    dead_lettered: int = 0
    errors: tuple[str, ...] = ()


class AnalyticsOutboxWorker:
    """Process claimed outbox rows into the append-only event store."""

    def __init__(
        self,
        *,
        outbox: DurableOutboxPort,
        store: AnalyticsEventRepository,
        serializer: AnalyticsEventSerializer | None = None,
        metrics: AnalyticsOperationalMetrics | None = None,
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
        batch_size: int = DEFAULT_WORKER_BATCH_SIZE,
    ) -> None:
        self._outbox = outbox
        self._store = store
        self._serializer = serializer or AnalyticsEventSerializer()
        self._metrics = metrics if metrics is not None else ANALYTICS_METRICS
        self._max_attempts = max_attempts
        self._batch_size = batch_size

    def run_once(self) -> WorkerBatchResult:
        """Claim and process one batch. Safe under interruption (at-least-once)."""
        claimed = self._outbox.claim_batch(
            limit=self._batch_size,
            max_attempts=self._max_attempts,
        )
        processed = 0
        duplicates = 0
        failed = 0
        dead_lettered = 0
        errors: list[str] = []

        for record in claimed:
            try:
                outcome = self._process_one(record)
                if outcome == "processed":
                    processed += 1
                    self._metrics.record_worker_success()
                elif outcome == "duplicate":
                    duplicates += 1
                    processed += 1
                    self._metrics.record_duplicate_suppressed()
                    self._metrics.record_worker_success()
                elif outcome == "dead_letter":
                    dead_lettered += 1
                    self._metrics.record_dead_letter()
                    self._metrics.record_worker_failure()
                else:
                    failed += 1
                    self._metrics.record_worker_failure()
            except Exception as exc:  # noqa: BLE001 — never crash the worker loop
                msg = f"{record.outbox_id}:{exc.__class__.__name__}"
                errors.append(msg)
                logger.exception(
                    "analytics.worker_unexpected outbox_id=%s", record.outbox_id
                )
                self._fail_or_dead_letter(record, error=str(exc)[:512])
                if self._is_dead_letter(record.outbox_id):
                    dead_lettered += 1
                    self._metrics.record_dead_letter()
                else:
                    failed += 1
                self._metrics.record_worker_failure()

        depth = self._queue_depth()
        self._metrics.set_queue_depth(depth)
        return WorkerBatchResult(
            claimed=len(claimed),
            processed=processed,
            duplicates=duplicates,
            failed=failed,
            dead_lettered=dead_lettered,
            errors=tuple(errors),
        )

    def drain(self, *, max_batches: int = 100) -> WorkerBatchResult:
        """Run until empty or ``max_batches`` reached."""
        total = WorkerBatchResult()
        for _ in range(max_batches):
            batch = self.run_once()
            total = WorkerBatchResult(
                claimed=total.claimed + batch.claimed,
                processed=total.processed + batch.processed,
                duplicates=total.duplicates + batch.duplicates,
                failed=total.failed + batch.failed,
                dead_lettered=total.dead_lettered + batch.dead_lettered,
                errors=total.errors + batch.errors,
            )
            if batch.claimed == 0:
                break
        return total

    def _process_one(self, record: OutboxRecord) -> str:
        event = self._serializer.from_json(record.payload_json)
        inserted = self._store.append(event, payload_json=record.payload_json)
        self._outbox.mark_processed(record.outbox_id)
        return "processed" if inserted else "duplicate"

    def _fail_or_dead_letter(self, record: OutboxRecord, *, error: str) -> None:
        next_attempts = record.attempts + 1
        if next_attempts >= self._max_attempts:
            self._outbox.mark_dead_letter(record.outbox_id, error=error)
        else:
            self._outbox.mark_failed(record.outbox_id, error=error)

    def _is_dead_letter(self, outbox_id: str) -> bool:
        current = self._outbox.get(outbox_id)
        return current is not None and current.status == OUTBOX_DEAD_LETTER

    def _queue_depth(self) -> int:
        counts = self._outbox.count_by_status()
        return int(counts.get("pending", 0)) + int(counts.get(OUTBOX_FAILED, 0))
