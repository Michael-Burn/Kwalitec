"""Founder-facing serializers for CIP-002 / CIP-003 intelligence surfaces."""

from __future__ import annotations

from app.domain.curriculum_intelligence.audit import AuditEvent
from app.domain.curriculum_intelligence.provenance import ProvenanceRecord
from app.domain.curriculum_intelligence.validation_report import ValidationReport
from app.domain.curriculum_retrieval.result import RankedEvidence, RetrievalResult


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


def ranked_evidence_public(item: RankedEvidence) -> dict:
    """Educational ranked evidence — no vector ids or model internals."""
    return {
        "entity_id": item.entity_id,
        "kind": item.kind,
        "title": item.title,
        "body": item.body,
        "document_id": item.document_id,
        "version_label": item.version_label,
        "confidence": item.confidence,
        "confidence_band": item.confidence_band,
        "verified": item.verified,
        "provenance_id": item.provenance_id,
        "rank_score": item.rank_score,
        "ranking": item.ranking.as_dict(),
        "graph_distance": item.graph_distance,
        "source_pages": list(item.source_pages),
        "prerequisites": list(item.prerequisites),
        "related_concepts": list(item.related_concepts),
        "supporting_formulae": list(item.supporting_formulae),
        "worked_examples": list(item.worked_examples),
        "practice_questions": list(item.practice_questions),
        "learning_objectives": list(item.learning_objectives),
        "evidence": [
            {
                "evidence_id": e.evidence_id,
                "role": e.role,
                "excerpt": e.excerpt,
                "page_number": e.page_number,
                "provenance_id": e.provenance_id,
            }
            for e in item.evidence
        ],
    }


def retrieval_result_public(result: RetrievalResult) -> dict:
    """Full retrieval response for Founder Evidence Explorer / APIs."""
    payload: dict = {
        "query_text": result.query_text,
        "intent": result.intent.value,
        "profile": result.profile.value,
        "results": [ranked_evidence_public(r) for r in result.results],
        "concept_ids": list(result.concept_ids),
        "learning_objective_ids": list(result.learning_objective_ids),
        "definition_ids": list(result.definition_ids),
        "formula_ids": list(result.formula_ids),
        "example_ids": list(result.example_ids),
        "practice_question_ids": list(result.practice_question_ids),
        "prerequisite_ids": list(result.prerequisite_ids),
        "related_concept_ids": list(result.related_concept_ids),
        "retrieval_log_id": result.retrieval_log_id,
    }
    if result.diagnostics is not None:
        d = result.diagnostics
        payload["diagnostics"] = {
            "intent": d.intent.value,
            "profile": d.profile.value,
            "candidate_count": d.candidate_count,
            "graph_expanded_count": d.graph_expanded_count,
            "metadata_filtered_count": d.metadata_filtered_count,
            "vector_hit_count": d.vector_hit_count,
            "ranked_count": d.ranked_count,
            "seed_entity_ids": list(d.seed_entity_ids),
            "notes": list(d.notes),
        }
    return payload
