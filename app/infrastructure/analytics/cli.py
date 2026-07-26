"""Flask CLI commands for analytics operational readiness (EP-002).

All commands are fail-safe for educational UX: they never modify Twin,
Educational State, Learning Evidence, or missions. Feature flag remains
operator-controlled via environment (default OFF).
"""

from __future__ import annotations

import json
import logging
import sys

import click

from app.infrastructure.analytics.cleanup import (
    AnalyticsCleanupJob,
    AnalyticsRetentionEnforcer,
)
from app.infrastructure.analytics.feature_flag import resolve_analytics_feature_flag
from app.infrastructure.analytics.metrics import ANALYTICS_METRICS
from app.infrastructure.analytics.privacy import AnalyticsPrivacyService
from app.infrastructure.analytics.purge import AnalyticsPurgeJob
from app.infrastructure.analytics.replay import AnalyticsReplayService
from app.infrastructure.analytics.sqlalchemy_store import (
    SqlAnalyticsAuditLog,
    SqlAnalyticsEventStore,
    SqlOutboxSink,
)
from app.infrastructure.analytics.worker import AnalyticsOutboxWorker

logger = logging.getLogger(__name__)


def _compose_sql() -> tuple[
    SqlOutboxSink,
    SqlAnalyticsEventStore,
    SqlAnalyticsAuditLog,
]:
    return SqlOutboxSink(), SqlAnalyticsEventStore(), SqlAnalyticsAuditLog()


@click.command("analytics-worker-once")
@click.option("--batch-size", default=100, show_default=True, type=int)
@click.option("--max-attempts", default=5, show_default=True, type=int)
def analytics_worker_once_command(batch_size: int, max_attempts: int) -> None:
    """Drain one outbox batch into the durable event store."""
    outbox, store, _audit = _compose_sql()
    worker = AnalyticsOutboxWorker(
        outbox=outbox,
        store=store,
        max_attempts=max_attempts,
        batch_size=batch_size,
        metrics=ANALYTICS_METRICS,
    )
    result = worker.run_once()
    click.echo(
        json.dumps(
            {
                "claimed": result.claimed,
                "processed": result.processed,
                "duplicates": result.duplicates,
                "failed": result.failed,
                "dead_lettered": result.dead_lettered,
                "errors": list(result.errors),
            },
            sort_keys=True,
        )
    )


@click.command("analytics-replay")
@click.option("--limit", default=100, show_default=True, type=int)
@click.option("--drain/--no-drain", default=True, show_default=True)
@click.option("--reset-attempts/--keep-attempts", default=True, show_default=True)
@click.option("--outbox-id", multiple=True, help="Specific outbox_id to replay")
def analytics_replay_command(
    limit: int,
    drain: bool,
    reset_attempts: bool,
    outbox_id: tuple[str, ...],
) -> None:
    """Requeue dead-letter / failed outbox rows (optionally drain)."""
    outbox, store, _audit = _compose_sql()
    worker = AnalyticsOutboxWorker(
        outbox=outbox, store=store, metrics=ANALYTICS_METRICS
    )
    replay = AnalyticsReplayService(
        outbox=outbox, worker=worker, metrics=ANALYTICS_METRICS
    )
    ids = outbox_id if outbox_id else None
    if drain:
        result = replay.replay_and_drain(
            limit=limit,
            reset_attempts=reset_attempts,
            outbox_ids=ids,
        )
    else:
        result = replay.requeue_dead_letters(
            limit=limit,
            reset_attempts=reset_attempts,
            outbox_ids=ids,
        )
    click.echo(
        json.dumps(
            {
                "requeued": result.requeued,
                "skipped": result.skipped,
                "processed": result.processed,
                "duplicates": result.duplicates,
                "failed": result.failed,
                "dead_lettered": result.dead_lettered,
                "outbox_ids": list(result.outbox_ids),
            },
            sort_keys=True,
        )
    )


@click.command("analytics-retention")
@click.option("--dry-run/--execute", default=True, show_default=True)
def analytics_retention_command(dry_run: bool) -> None:
    """Enforce raw-event retention + outbox processed cleanup (PRD §7.1)."""
    outbox, store, audit = _compose_sql()
    purge = AnalyticsPurgeJob(store=store)
    cleanup = AnalyticsCleanupJob(outbox=outbox, audit=audit, metrics=ANALYTICS_METRICS)
    enforcer = AnalyticsRetentionEnforcer(
        purge_job=purge,
        cleanup_job=cleanup,
        audit=audit,
        metrics=ANALYTICS_METRICS,
    )
    result = enforcer.run(dry_run=dry_run)
    click.echo(
        json.dumps(
            {
                "dry_run": dry_run,
                "purge_scanned": result.purge.scanned,
                "purge_deleted": result.purge.deleted,
                "outbox_deleted": result.outbox_cleanup.deleted,
                "audit_id": result.audit_id,
            },
            sort_keys=True,
        )
    )


@click.command("analytics-delete-user")
@click.argument("user_id", type=int)
@click.option("--requested-by", default="support", show_default=True)
@click.option("--yes", is_flag=True, help="Confirm cascade deletion")
def analytics_delete_user_command(
    user_id: int, requested_by: str, yes: bool
) -> None:
    """Cascade-delete analytics rows for a user (PRD §7.2).

    Educational domain data is untouched.
    """
    if not yes:
        click.echo("Refusing to delete without --yes", err=True)
        sys.exit(2)
    outbox, store, audit = _compose_sql()
    privacy = AnalyticsPrivacyService(
        event_store=store,
        outbox=outbox,
        audit=audit,
        metrics=ANALYTICS_METRICS,
    )
    result = privacy.delete_user_analytics(user_id, requested_by=requested_by)
    click.echo(
        json.dumps(
            {
                "user_id": result.user_id,
                "events_deleted": result.events_deleted,
                "outbox_deleted": result.outbox_deleted,
                "audit_id": result.audit_id,
            },
            sort_keys=True,
        )
    )


@click.command("analytics-export-user")
@click.argument("user_id", type=int)
@click.option("--requested-by", default="support", show_default=True)
@click.option("--output", type=click.Path(dir_okay=False), default="-")
def analytics_export_user_command(
    user_id: int, requested_by: str, output: str
) -> None:
    """Export one student's analytics events as JSON (PRD §7.3)."""
    _outbox, store, audit = _compose_sql()
    privacy = AnalyticsPrivacyService(
        event_store=store,
        audit=audit,
        metrics=ANALYTICS_METRICS,
    )
    result = privacy.export_student(user_id, requested_by=requested_by)
    if output == "-":
        click.echo(result.payload)
    else:
        with open(output, "w", encoding="utf-8") as fh:
            fh.write(result.payload)
        click.echo(
            f"wrote {result.event_count} events to {output} "
            f"audit={result.audit_id}"
        )


@click.command("analytics-export-audit")
@click.option("--action", default=None)
@click.option("--user-id", type=int, default=None)
@click.option("--output", type=click.Path(dir_okay=False), default="-")
def analytics_export_audit_command(
    action: str | None, user_id: int | None, output: str
) -> None:
    """Export analytics audit log as JSON lines (PRD §7.3)."""
    _outbox, store, audit = _compose_sql()
    privacy = AnalyticsPrivacyService(
        event_store=store,
        audit=audit,
        metrics=ANALYTICS_METRICS,
    )
    result = privacy.export_audit(action=action, user_id=user_id)
    if output == "-":
        click.echo(result.payload)
    else:
        with open(output, "w", encoding="utf-8") as fh:
            fh.write(result.payload)
        click.echo(f"wrote audit export audit={result.audit_id}")


@click.command("analytics-metrics")
def analytics_metrics_command() -> None:
    """Print process-local operational metrics snapshot (+ SQL queue depth)."""
    outbox, _store, _audit = _compose_sql()
    try:
        counts = outbox.count_by_status()
        depth = int(counts.get("pending", 0)) + int(counts.get("failed", 0))
        ANALYTICS_METRICS.set_queue_depth(depth)
        snap = ANALYTICS_METRICS.snapshot()
        snap["outbox_counts"] = counts
    except Exception as exc:  # noqa: BLE001
        snap = ANALYTICS_METRICS.snapshot()
        snap["outbox_error"] = exc.__class__.__name__
    flag = resolve_analytics_feature_flag()
    snap["feature_flag_enabled"] = flag.enabled
    click.echo(json.dumps(snap, sort_keys=True))


@click.command("analytics-verify-consent")
@click.argument("user_id", type=int)
@click.option("--invite-only/--open-cohort", default=True, show_default=True)
@click.option("--privacy-notice/--no-privacy-notice", default=True, show_default=True)
@click.option("--marketing-use", is_flag=True, default=False)
def analytics_verify_consent_command(
    user_id: int,
    invite_only: bool,
    privacy_notice: bool,
    marketing_use: bool,
) -> None:
    """Verify PRD-001 §8 consent assumptions for a user id."""
    privacy = AnalyticsPrivacyService(event_store=SqlAnalyticsEventStore())
    verdict = privacy.verify_consent(
        user_id=user_id,
        invite_only_cohort=invite_only,
        privacy_notice_acknowledged=privacy_notice,
        marketing_use=marketing_use,
    )
    click.echo(
        json.dumps(
            {
                "user_id": user_id,
                "allowed": verdict.allowed,
                "basis": verdict.basis,
                "notes": verdict.notes,
            },
            sort_keys=True,
        )
    )
    if not verdict.allowed:
        sys.exit(1)
