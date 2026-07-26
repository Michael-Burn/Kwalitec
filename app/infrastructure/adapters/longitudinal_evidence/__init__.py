"""Longitudinal Learning Evidence Repository package (P4-MS002).

Durable repository for educational observations collected across study
sessions, missions, reflections, advisory activations, and educational
trials.

Feature flag ``KWALITEC_LONGITUDINAL_EVIDENCE`` / ``ENABLE_LONGITUDINAL_EVIDENCE``
defaults OFF.

Stores evidence only. Does not influence Runtime A. No analytical
behaviour. No Adaptive / Recovery / policy weighting mutation.
"""

from __future__ import annotations

from .contracts import (
    APPEND_ONLY_VIOLATION,
    APPROVED_ADVISORY_FIELD,
    APPROVED_ADVISORY_FIELDS,
    AUTHORITY_LONGITUDINAL_EVIDENCE,
    AUTHORITY_RUNTIME_A,
    EVENT_ADVISORY_ACTIVATION,
    EVENT_EDUCATIONAL_TRIAL,
    EVENT_MISSION,
    EVENT_REFLECTION,
    EVENT_STUDY_SESSION,
    INVALID_STATE,
    LONGITUDINAL_ERROR_CODES,
    LONGITUDINAL_EVENT_TYPES,
    LONGITUDINAL_EVIDENCE_SCHEMA_VERSION,
    LONGITUDINAL_SOURCE_COMPONENTS,
    SCHEMA_INCOMPATIBLE,
    SOURCE_ADVISORY_OUTCOME,
    SOURCE_CONTROLLED_ADVISORY,
    SOURCE_EDUCATIONAL_TRIAL,
    SOURCE_EVIDENCE_PLATFORM,
    SOURCE_RECOMMENDATION_POLICY,
    SOURCE_RUNTIME_A,
    SOURCE_STUDENT_EXPERIENCE,
    SOURCE_UNIFIED_JOURNEY,
    SUPPORTED_SCHEMA_VERSIONS,
    UNAVAILABLE,
    LearningEvidenceRecord,
    LongitudinalEvidenceProvenance,
    LongitudinalEvidenceRepository,
    LongitudinalEvidenceResult,
    build_provenance,
    is_schema_compatible,
    serialize_canonical,
    snapshot_mapping,
    validate_learning_evidence_record,
)
from .repository import (
    REPOSITORY_ID,
    REPOSITORY_VERSION,
    SOURCE_SERVICE,
    InMemoryLongitudinalEvidenceRepository,
    build_longitudinal_evidence_repository,
    deterministic_record_id,
    make_record,
    opaque_student_id_hash,
)

__all__ = [
    "APPEND_ONLY_VIOLATION",
    "APPROVED_ADVISORY_FIELD",
    "APPROVED_ADVISORY_FIELDS",
    "AUTHORITY_LONGITUDINAL_EVIDENCE",
    "AUTHORITY_RUNTIME_A",
    "EVENT_ADVISORY_ACTIVATION",
    "EVENT_EDUCATIONAL_TRIAL",
    "EVENT_MISSION",
    "EVENT_REFLECTION",
    "EVENT_STUDY_SESSION",
    "INVALID_STATE",
    "LONGITUDINAL_ERROR_CODES",
    "LONGITUDINAL_EVENT_TYPES",
    "LONGITUDINAL_EVIDENCE_SCHEMA_VERSION",
    "LONGITUDINAL_SOURCE_COMPONENTS",
    "REPOSITORY_ID",
    "REPOSITORY_VERSION",
    "SCHEMA_INCOMPATIBLE",
    "SOURCE_ADVISORY_OUTCOME",
    "SOURCE_CONTROLLED_ADVISORY",
    "SOURCE_EDUCATIONAL_TRIAL",
    "SOURCE_EVIDENCE_PLATFORM",
    "SOURCE_RECOMMENDATION_POLICY",
    "SOURCE_RUNTIME_A",
    "SOURCE_SERVICE",
    "SOURCE_STUDENT_EXPERIENCE",
    "SOURCE_UNIFIED_JOURNEY",
    "SUPPORTED_SCHEMA_VERSIONS",
    "UNAVAILABLE",
    "InMemoryLongitudinalEvidenceRepository",
    "LearningEvidenceRecord",
    "LongitudinalEvidenceProvenance",
    "LongitudinalEvidenceRepository",
    "LongitudinalEvidenceResult",
    "build_longitudinal_evidence_repository",
    "build_provenance",
    "deterministic_record_id",
    "is_schema_compatible",
    "make_record",
    "opaque_student_id_hash",
    "serialize_canonical",
    "snapshot_mapping",
    "validate_learning_evidence_record",
]
