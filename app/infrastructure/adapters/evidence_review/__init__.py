"""Educational Evidence Review Workspace package (P4-MS003).

Read-only operational review layer over the Longitudinal Learning Evidence
Repository. Enables human inspection of accumulated educational evidence
without influencing Runtime A.

Feature flag ``KWALITEC_EVIDENCE_REVIEW`` / ``ENABLE_EVIDENCE_REVIEW``
defaults OFF.

Never modifies recommendations, policy, Adaptive, Recovery, or educational
behaviour. No analytical models in this milestone.
"""

from __future__ import annotations

from .contracts import (
    AUTHORITY_EVIDENCE_REVIEW,
    AUTHORITY_LONGITUDINAL_EVIDENCE,
    AUTHORITY_RUNTIME_A,
    CSV_COLUMNS,
    EVIDENCE_REVIEW_ERROR_CODES,
    EVIDENCE_REVIEW_SCHEMA_VERSION,
    EXPORT_FORMAT_CSV,
    EXPORT_FORMAT_JSON,
    EXPORT_FORMATS,
    INVALID_STATE,
    UNAVAILABLE,
    EvidenceEventGroup,
    EvidenceProvenanceSummary,
    EvidenceReviewExport,
    EvidenceReviewFilter,
    EvidenceReviewResult,
    EvidenceTimeline,
    EvidenceTimeWindow,
    serialize_canonical,
)
from .service import (
    SERVICE_ID,
    SERVICE_VERSION,
    SOURCE_SERVICE,
    EvidenceQueryService,
    build_evidence_query_service,
    content_digest,
    deterministic_export_id,
    deterministic_timeline_id,
)

__all__ = [
    "AUTHORITY_EVIDENCE_REVIEW",
    "AUTHORITY_LONGITUDINAL_EVIDENCE",
    "AUTHORITY_RUNTIME_A",
    "CSV_COLUMNS",
    "EVIDENCE_REVIEW_ERROR_CODES",
    "EVIDENCE_REVIEW_SCHEMA_VERSION",
    "EXPORT_FORMAT_CSV",
    "EXPORT_FORMAT_JSON",
    "EXPORT_FORMATS",
    "INVALID_STATE",
    "SERVICE_ID",
    "SERVICE_VERSION",
    "SOURCE_SERVICE",
    "UNAVAILABLE",
    "EvidenceEventGroup",
    "EvidenceProvenanceSummary",
    "EvidenceQueryService",
    "EvidenceReviewExport",
    "EvidenceReviewFilter",
    "EvidenceReviewResult",
    "EvidenceTimeWindow",
    "EvidenceTimeline",
    "build_evidence_query_service",
    "content_digest",
    "deterministic_export_id",
    "deterministic_timeline_id",
    "serialize_canonical",
]
