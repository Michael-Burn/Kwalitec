"""Outbox cleanup + retention enforcement orchestration (EP-002 WS1/WS4)."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, Protocol

from app.infrastructure.analytics.metrics import (
    ANALYTICS_METRICS,
    AnalyticsOperationalMetrics,
)
from app.infrastructure.analytics.outbox import DurableOutboxPort
from app.infrastructure.analytics.purge import AnalyticsPurgeJob, PurgeResult
from app.infrastructure.analytics.status import (
    AUDIT_RETENTION_DAYS,
    DEFAULT_PROCESSED_RETENTION_DAYS,
)

logger = logging.getLogger(__name__)


class AuditAppendPort(Protocol):
    """Minimal audit append contract."""

    def append(
        self,
        *,
        action: str,
        user_id: int | None = None,
        detail: dict | None = None,
    ) -> str:
        ...


@dataclass(frozen=True)
class CleanupResult:
    """Outcome of outbox processed-row cleanup."""

    deleted: int = 0
    dry_run: bool = True
    cutoff: datetime | None = None


@dataclass(frozen=True)
class RetentionEnforcementResult:
    """Combined retention pass: raw events + outbox cleanup."""

    purge: PurgeResult
    outbox_cleanup: CleanupResult
    audit_id: str = ""


class AnalyticsCleanupJob:
    """Delete processed outbox rows past the operational retention window."""

    def __init__(
        self,
        *,
        outbox: DurableOutboxPort,
        retention_days: int = DEFAULT_PROCESSED_RETENTION_DAYS,
        metrics: AnalyticsOperationalMetrics | None = None,
        audit: AuditAppendPort | None = None,
    ) -> None:
        self._outbox = outbox
        self._retention_days = retention_days
        self._metrics = metrics if metrics is not None else ANALYTICS_METRICS
        self._audit = audit

    def run(
        self,
        *,
        now: datetime | None = None,
        dry_run: bool = True,
        limit: int = 1000,
    ) -> CleanupResult:
        when = now if now is not None else datetime.now(tz=UTC)
        if when.tzinfo is None:
            when = when.replace(tzinfo=UTC)
        cutoff = when - timedelta(days=self._retention_days)
        if dry_run:
            counts = self._outbox.count_by_status()
            # Dry-run cannot cheaply filter by age without a list API; report 0.
            _ = counts
            return CleanupResult(deleted=0, dry_run=True, cutoff=cutoff)

        deleted = self._outbox.delete_processed(older_than=cutoff, limit=limit)
        if deleted and self._audit is not None:
            self._audit.append(
                action="analytics.outbox_cleaned",
                detail={"deleted": deleted, "cutoff": cutoff.isoformat()},
            )
        logger.info(
            "analytics.outbox_cleanup deleted=%s cutoff=%s dry_run=%s",
            deleted,
            cutoff.isoformat(),
            dry_run,
        )
        return CleanupResult(deleted=deleted, dry_run=False, cutoff=cutoff)


class AnalyticsRetentionEnforcer:
    """Enforce PRD-001 §7.1 raw retention + outbox cleanup with audit."""

    def __init__(
        self,
        *,
        purge_job: AnalyticsPurgeJob,
        cleanup_job: AnalyticsCleanupJob,
        audit: AuditAppendPort | None = None,
        metrics: AnalyticsOperationalMetrics | None = None,
    ) -> None:
        self._purge = purge_job
        self._cleanup = cleanup_job
        self._audit = audit
        self._metrics = metrics if metrics is not None else ANALYTICS_METRICS

    def run(
        self,
        *,
        now: datetime | None = None,
        dry_run: bool = True,
    ) -> RetentionEnforcementResult:
        purge = self._purge.run(now=now, dry_run=dry_run)
        cleanup = self._cleanup.run(now=now, dry_run=dry_run)
        if not dry_run and purge.deleted:
            self._metrics.record_purge(purge.deleted)
        audit_id = ""
        if self._audit is not None:
            detail: dict[str, Any] = {
                "purge_scanned": purge.scanned,
                "purge_deleted": purge.deleted,
                "purge_dry_run": purge.dry_run,
                "outbox_deleted": cleanup.deleted,
                "outbox_dry_run": cleanup.dry_run,
                "audit_retention_days": AUDIT_RETENTION_DAYS,
            }
            if purge.cutoff is not None:
                detail["purge_cutoff"] = purge.cutoff.isoformat()
            audit_id = self._audit.append(
                action="analytics.purge_run",
                detail=detail,
            )
        return RetentionEnforcementResult(
            purge=purge,
            outbox_cleanup=cleanup,
            audit_id=audit_id,
        )
