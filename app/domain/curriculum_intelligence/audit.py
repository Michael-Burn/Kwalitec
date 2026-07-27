"""Immutable audit events for Curriculum Intelligence (CIP-002)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class AuditAction(StrEnum):
    """Important CIP actions that must leave an audit trail."""

    ENTITY_CREATED = "entity_created"
    RELATION_CREATED = "relation_created"
    ENTITY_REVIEWED = "entity_reviewed"
    ENTITY_APPROVED = "entity_approved"
    ENTITY_REJECTED = "entity_rejected"
    ENTITY_REMAPPED = "entity_remapped"
    VERSION_ARCHIVED = "version_archived"
    DOCUMENT_SUPERSEDED = "document_superseded"
    GRAPH_REBUILT = "graph_rebuilt"
    GRAPH_VALIDATED = "graph_validated"
    PIPELINE_RETRIED = "pipeline_retried"
    PIPELINE_COMPLETED = "pipeline_completed"
    METRICS_RECORDED = "metrics_recorded"


@dataclass(frozen=True)
class AuditEvent:
    """Append-only audit event for CIP actions."""

    event_id: str
    action: AuditAction
    actor_id: str
    subject_kind: str
    subject_id: str
    document_id: int | None
    pipeline_job_id: str
    document_version: str
    workspace_id: str
    message: str
    created_at_iso: str
    attributes: tuple[tuple[str, str], ...] = ()
