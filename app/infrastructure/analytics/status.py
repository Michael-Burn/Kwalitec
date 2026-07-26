"""Outbox status constants and defaults (EP-002 durable outbox)."""

from __future__ import annotations

# Outbox lifecycle statuses.
OUTBOX_PENDING = "pending"
OUTBOX_PROCESSING = "processing"
OUTBOX_PROCESSED = "processed"
OUTBOX_FAILED = "failed"
OUTBOX_DEAD_LETTER = "dead_letter"
OUTBOX_SKIPPED = "skipped"

# Retry / retention defaults (operational; not educational).
DEFAULT_MAX_ATTEMPTS = 5
DEFAULT_WORKER_BATCH_SIZE = 100
# Processed outbox rows retained briefly for ops forensics, then cleaned.
DEFAULT_PROCESSED_RETENTION_DAYS = 7
# Audit log retention (PRD-001 §9) — 36 months approx.
AUDIT_RETENTION_DAYS = 36 * 30
