"""Audit event catalogue for curriculum publishing governance."""

from __future__ import annotations

from enum import StrEnum


class AuditEventType(StrEnum):
    """Append-only audit categories. Records must never be deleted."""

    EDITORIAL = "editorial"
    PUBLICATION = "publication"
    ARCHIVE = "archive"
    SUCCESSOR_PREPARE = "successor_prepare"
    SNAPSHOT = "snapshot"
