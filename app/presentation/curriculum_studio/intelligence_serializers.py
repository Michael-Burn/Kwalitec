"""Founder-facing serializers for CIP-002 intelligence surfaces."""

from __future__ import annotations

from app.domain.curriculum_intelligence.audit import AuditEvent
from app.domain.curriculum_intelligence.provenance import ProvenanceRecord
from app.domain.curriculum_intelligence.validation_report import ValidationReport


def provenance_public(prov: ProvenanceRecord) -> dict:
    """Educational provenance only — no storage keys or implementation paths."""
    return {
        "provenance_id": prov.provenance_id,
        "subject_kind": prov.subject_kind.value,
        "subject_id": prov.subject_id,
        "source_document_id": prov.source_document_id,
        "source_version": prov.source_version_label,
        "source_pages": list(prov.source_pages),
        "source_paragraphs": list(prov.source_paragraphs),
        "parser_version": prov.parser_version,
        "pipeline_job_id": prov.pipeline_job_id,
        "chain_stage": prov.chain_stage.value,
        "evidence": [
            {
                "page": e.page_number,
                "paragraph": e.paragraph_index,
                "excerpt": e.excerpt,
                "role": e.evidence_role,
            }
            for e in prov.evidence
        ],
        "created_at": prov.created_at_iso,
    }


def validation_report_public(report: ValidationReport) -> dict:
    return {
        "report_id": report.report_id,
        "document_id": report.document_id,
        "passed": report.passed,
        "issue_count": report.issue_count,
        "error_count": report.error_count,
        "warning_count": report.warning_count,
        "created_at": report.created_at_iso,
        "issues": [
            {
                "issue_id": i.issue_id,
                "kind": i.kind.value,
                "severity": i.severity.value,
                "message": i.message,
                "subject_kind": i.subject_kind,
                "subject_id": i.subject_id,
                "related_ids": list(i.related_ids),
            }
            for i in report.issues
        ],
    }


def audit_event_public(event: AuditEvent) -> dict:
    return {
        "event_id": event.event_id,
        "action": event.action.value,
        "actor_id": event.actor_id,
        "subject_kind": event.subject_kind,
        "subject_id": event.subject_id,
        "document_id": event.document_id,
        "document_version": event.document_version,
        "message": event.message,
        "created_at": event.created_at_iso,
    }
