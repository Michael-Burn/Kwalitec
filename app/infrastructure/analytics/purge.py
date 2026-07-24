"""Retention / purge job skeleton (PRD-001 §7.1).

Phase A delivers a callable skeleton with batch sizing and audit hooks.
Does not schedule itself and does not run in the request path.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Protocol

logger = logging.getLogger(__name__)

# PRD-001 §7.1 — raw events / snapshots: 18 months from occurred_at.
RAW_EVENT_RETENTION = timedelta(days=18 * 30)  # approx 18 months
# PRD-001 §10 — batch size.
DEFAULT_BATCH_SIZE = 1000


@dataclass(frozen=True)
class PurgeResult:
    """Outcome of one purge batch."""

    scanned: int = 0
    deleted: int = 0
    cutoff: datetime | None = None
    dry_run: bool = True
    notes: str = ""


class AnalyticsEventStorePort(Protocol):
    """Minimal store port for purge (implemented by repository adapters)."""

    def count_expired(self, *, cutoff: datetime) -> int:
        """Count raw event rows with occurred_at &lt; cutoff."""
        ...

    def delete_expired(self, *, cutoff: datetime, limit: int) -> int:
        """Delete up to ``limit`` expired rows; return deleted count."""
        ...


@dataclass
class AnalyticsPurgeJob:
    """Skeleton purge job — safe to call; no-op without a store binding."""

    store: AnalyticsEventStorePort | None = None
    retention: timedelta = RAW_EVENT_RETENTION
    batch_size: int = DEFAULT_BATCH_SIZE

    def run(
        self,
        *,
        now: datetime | None = None,
        dry_run: bool = True,
    ) -> PurgeResult:
        """Run one purge pass.

        Args:
            now: Reference time (defaults to UTC now).
            dry_run: When True, only count expired rows (default).
        """
        when = now if now is not None else datetime.now(tz=UTC)
        if when.tzinfo is None:
            when = when.replace(tzinfo=UTC)
        cutoff = when - self.retention

        if self.store is None:
            logger.info(
                "analytics.purge_skipped reason=no_store cutoff=%s dry_run=%s",
                cutoff.isoformat(),
                dry_run,
            )
            return PurgeResult(
                scanned=0,
                deleted=0,
                cutoff=cutoff,
                dry_run=dry_run,
                notes="no_store",
            )

        scanned = self.store.count_expired(cutoff=cutoff)
        deleted = 0
        if not dry_run and scanned > 0:
            deleted = self.store.delete_expired(
                cutoff=cutoff, limit=self.batch_size
            )
        logger.info(
            "analytics.purge_run scanned=%s deleted=%s cutoff=%s dry_run=%s",
            scanned,
            deleted,
            cutoff.isoformat(),
            dry_run,
        )
        return PurgeResult(
            scanned=scanned,
            deleted=deleted,
            cutoff=cutoff,
            dry_run=dry_run,
        )
