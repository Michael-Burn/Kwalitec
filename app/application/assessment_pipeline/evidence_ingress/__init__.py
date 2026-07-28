"""AP-001 evidence ingress package (AP-002D1).

Single integration point between Assessment EvidenceBundle export and
StudentReasoningService. No educational behaviour changes beyond wiring.
"""

from __future__ import annotations

from app.application.assessment_pipeline.evidence_ingress.dto import (
    EvidenceIngressMapping,
    EvidenceIngressRequest,
    EvidenceIngressResult,
    EvidenceIngressTraceability,
    MappedEvidenceObservation,
)
from app.application.assessment_pipeline.evidence_ingress.errors import (
    DuplicateEvidenceSubmission,
    EvidenceIngressError,
    IncompleteEvidenceBundle,
    InvalidEvidenceBundle,
    MissingObservationReference,
    UnsupportedEvidenceVersion,
)
from app.application.assessment_pipeline.evidence_ingress.mapper import (
    map_evidence_bundle,
)
from app.application.assessment_pipeline.evidence_ingress.repository import (
    EvidenceSubmissionRecord,
    EvidenceSubmissionRepository,
    InMemoryEvidenceSubmissionRepository,
)
from app.application.assessment_pipeline.evidence_ingress.service import (
    EvidenceIngressService,
)
from app.application.assessment_pipeline.evidence_ingress.validator import (
    validate_evidence_bundle,
)
from app.application.assessment_pipeline.evidence_ingress.versions import (
    INGRESS_CONTRACT_VERSION,
    INGRESS_TRIGGERED_BY,
    SUPPORTED_PACKAGING_VERSIONS,
)

__all__ = [
    "INGRESS_CONTRACT_VERSION",
    "INGRESS_TRIGGERED_BY",
    "SUPPORTED_PACKAGING_VERSIONS",
    "DuplicateEvidenceSubmission",
    "EvidenceIngressError",
    "EvidenceIngressMapping",
    "EvidenceIngressRequest",
    "EvidenceIngressResult",
    "EvidenceIngressService",
    "EvidenceIngressTraceability",
    "EvidenceSubmissionRecord",
    "EvidenceSubmissionRepository",
    "InMemoryEvidenceSubmissionRepository",
    "IncompleteEvidenceBundle",
    "InvalidEvidenceBundle",
    "MappedEvidenceObservation",
    "MissingObservationReference",
    "UnsupportedEvidenceVersion",
    "map_evidence_bundle",
    "validate_evidence_bundle",
]
