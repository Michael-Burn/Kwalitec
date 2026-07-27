"""Curriculum Intelligence Pipeline (CIP) domain package.

Bounded context for transforming uploaded curriculum PDFs into structured
educational knowledge that powers the Student Digital Twin roadmap.

CIP-001: extraction → map → graph.
CIP-002: provenance, confidence, validation, Founder review, audit.
No LLM. No embeddings. No OCR. No student-facing recommendation logic.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "AuditAction",
    "AuditEvent",
    "BlockKind",
    "ConfidenceBand",
    "ConfidenceFactor",
    "ConfidenceRecord",
    "CurriculumEntityKind",
    "CurriculumKnowledgeEntity",
    "CurriculumMap",
    "ENTITY_CHILD_KINDS",
    "ExtractedBlock",
    "ExtractedDocument",
    "ExtractedPage",
    "FOUNDER_PIPELINE_MILESTONES",
    "FOUNDER_STAGE_LABELS",
    "GRAPH_BUILDER_VERSION",
    "KnowledgeGraph",
    "KnowledgeRelation",
    "KnowledgeRelationType",
    "MAPPER_VERSION",
    "PARSER_VERSION",
    "PIPELINE_ORDER",
    "PipelineQualityMetrics",
    "PipelineStage",
    "PipelineTransitionEvent",
    "ProvenanceChainStage",
    "ProvenanceRecord",
    "ProvenanceSubjectKind",
    "ReviewDecision",
    "ReviewRecord",
    "ReviewStatus",
    "StructuralDocument",
    "StructuralKind",
    "StructuralNode",
    "SupportingEvidence",
    "ValidationIssue",
    "ValidationIssueKind",
    "ValidationReport",
    "ValidationSeverity",
    "VerificationStatus",
    "confidence_band_from_score",
    "founder_label",
    "has_reached",
    "is_failure",
    "is_terminal",
    "next_pipeline_stage",
    "pipeline_index",
    "resolve_pipeline_stage",
    "resume_stage_after_failure",
]

_EXPORT_MODULES = {
    "BlockKind": "app.domain.curriculum_intelligence.extracted_document",
    "ExtractedBlock": "app.domain.curriculum_intelligence.extracted_document",
    "ExtractedDocument": "app.domain.curriculum_intelligence.extracted_document",
    "ExtractedPage": "app.domain.curriculum_intelligence.extracted_document",
    "StructuralKind": "app.domain.curriculum_intelligence.structural_document",
    "StructuralNode": "app.domain.curriculum_intelligence.structural_document",
    "StructuralDocument": "app.domain.curriculum_intelligence.structural_document",
    "CurriculumEntityKind": "app.domain.curriculum_intelligence.curriculum_entity",
    "CurriculumKnowledgeEntity": "app.domain.curriculum_intelligence.curriculum_entity",
    "CurriculumMap": "app.domain.curriculum_intelligence.curriculum_entity",
    "ENTITY_CHILD_KINDS": "app.domain.curriculum_intelligence.curriculum_entity",
    "KnowledgeRelationType": "app.domain.curriculum_intelligence.knowledge_graph",
    "KnowledgeRelation": "app.domain.curriculum_intelligence.knowledge_graph",
    "KnowledgeGraph": "app.domain.curriculum_intelligence.knowledge_graph",
    "PipelineStage": "app.domain.curriculum_intelligence.pipeline_stage",
    "PipelineTransitionEvent": "app.domain.curriculum_intelligence.pipeline_stage",
    "PIPELINE_ORDER": "app.domain.curriculum_intelligence.pipeline_stage",
    "FOUNDER_PIPELINE_MILESTONES": "app.domain.curriculum_intelligence.pipeline_stage",
    "FOUNDER_STAGE_LABELS": "app.domain.curriculum_intelligence.pipeline_stage",
    "founder_label": "app.domain.curriculum_intelligence.pipeline_stage",
    "has_reached": "app.domain.curriculum_intelligence.pipeline_stage",
    "is_failure": "app.domain.curriculum_intelligence.pipeline_stage",
    "is_terminal": "app.domain.curriculum_intelligence.pipeline_stage",
    "next_pipeline_stage": "app.domain.curriculum_intelligence.pipeline_stage",
    "pipeline_index": "app.domain.curriculum_intelligence.pipeline_stage",
    "resolve_pipeline_stage": "app.domain.curriculum_intelligence.pipeline_stage",
    "resume_stage_after_failure": "app.domain.curriculum_intelligence.pipeline_stage",
    "PARSER_VERSION": "app.domain.curriculum_intelligence.provenance",
    "MAPPER_VERSION": "app.domain.curriculum_intelligence.provenance",
    "GRAPH_BUILDER_VERSION": "app.domain.curriculum_intelligence.provenance",
    "ProvenanceSubjectKind": "app.domain.curriculum_intelligence.provenance",
    "ProvenanceChainStage": "app.domain.curriculum_intelligence.provenance",
    "SupportingEvidence": "app.domain.curriculum_intelligence.provenance",
    "ProvenanceRecord": "app.domain.curriculum_intelligence.provenance",
    "ConfidenceBand": "app.domain.curriculum_intelligence.confidence",
    "ConfidenceFactor": "app.domain.curriculum_intelligence.confidence",
    "ConfidenceRecord": "app.domain.curriculum_intelligence.confidence",
    "confidence_band_from_score": "app.domain.curriculum_intelligence.confidence",
    "ReviewStatus": "app.domain.curriculum_intelligence.review",
    "VerificationStatus": "app.domain.curriculum_intelligence.review",
    "ReviewDecision": "app.domain.curriculum_intelligence.review",
    "ReviewRecord": "app.domain.curriculum_intelligence.review",
    "AuditAction": "app.domain.curriculum_intelligence.audit",
    "AuditEvent": "app.domain.curriculum_intelligence.audit",
    "ValidationIssueKind": "app.domain.curriculum_intelligence.validation_report",
    "ValidationSeverity": "app.domain.curriculum_intelligence.validation_report",
    "ValidationIssue": "app.domain.curriculum_intelligence.validation_report",
    "ValidationReport": "app.domain.curriculum_intelligence.validation_report",
    "PipelineQualityMetrics": "app.domain.curriculum_intelligence.quality_metrics",
}


def __getattr__(name: str) -> Any:
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from importlib import import_module

    module = import_module(module_name)
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
