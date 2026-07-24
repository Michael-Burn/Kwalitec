"""Replay tooling for dead-letter / failed outbox rows (EP-002 WS1)."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from app.infrastructure.analytics.metrics import (
    ANALYTICS_METRICS,
    AnalyticsOperationalMetrics,
)
from app.infrastructure.analytics.outbox import DurableOutboxPort
from app.infrastructure.analytics.status import OUTBOX_DEAD_LETTER, OUTBOX_FAILED
from app.infrastructure.analytics.worker import AnalyticsOutboxWorker, WorkerBatchResult

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ReplayResult:
    """Outcome of a replay operation."""

    requeued: int = 0
    skipped: int = 0
    processed: int = 0
    duplicates: int = 0
    failed: int = 0
    dead_lettered: int = 0
    outbox_ids: tuple[str, ...] = ()


class AnalyticsReplayService:
    """Requeue dead-letter / failed rows and optionally drain them."""

    def __init__(
        self,
        *,
        outbox: DurableOutboxPort,
        worker: AnalyticsOutboxWorker | None = None,
        metrics: AnalyticsOperationalMetrics | None = None,
    ) -> None:
        self._outbox = outbox
        self._worker = worker
        self._metrics = metrics if metrics is not None else ANALYTICS_METRICS

    def requeue_dead_letters(
        self,
        *,
        limit: int = 100,
        reset_attempts: bool = True,
        outbox_ids: tuple[str, ...] | None = None,
    ) -> ReplayResult:
        """Move dead-letter (or explicit ids) back to pending."""
        targets: list[str]
        if outbox_ids is not None:
            targets = list(outbox_ids)
        else:
            targets = [r.outbox_id for r in self._outbox.list_dead_letters(limit=limit)]

        requeued = 0
        skipped = 0
        ok_ids: list[str] = []
        for oid in targets:
            record = self._outbox.get(oid)
            if record is None:
                skipped += 1
                continue
            if record.status not in {OUTBOX_DEAD_LETTER, OUTBOX_FAILED}:
                skipped += 1
                continue
            if self._outbox.requeue(oid, reset_attempts=reset_attempts):
                requeued += 1
                ok_ids.append(oid)
            else:
                skipped += 1

        if requeued:
            self._metrics.record_replay(requeued)
            logger.info(
                "analytics.replay_requeued count=%s skipped=%s", requeued, skipped
            )
        return ReplayResult(
            requeued=requeued,
            skipped=skipped,
            outbox_ids=tuple(ok_ids),
        )

    def replay_and_drain(
        self,
        *,
        limit: int = 100,
        reset_attempts: bool = True,
        outbox_ids: tuple[str, ...] | None = None,
    ) -> ReplayResult:
        """Requeue then drain via the bound worker."""
        if self._worker is None:
            raise RuntimeError("worker is required for replay_and_drain")
        base = self.requeue_dead_letters(
            limit=limit,
            reset_attempts=reset_attempts,
            outbox_ids=outbox_ids,
        )
        drained: WorkerBatchResult = self._worker.drain(max_batches=max(1, limit))
        return ReplayResult(
            requeued=base.requeued,
            skipped=base.skipped,
            processed=drained.processed,
            duplicates=drained.duplicates,
            failed=drained.failed,
            dead_lettered=drained.dead_lettered,
            outbox_ids=base.outbox_ids,
        )
