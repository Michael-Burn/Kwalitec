"""Educational Evidence Update — CapturedEvidence → EvidenceRecord storage.

Transforms captured study-session evidence into Educational Operating System
evidence records and updates the learner's educational evidence state.

Allowed: validation, deterministic transformation, transactional persistence
through repository ports, Twin evidence-history append, auditable summaries.

Forbidden: diagnosis, recommendations, prioritisation, study planning, mission
generation, AI, Flask, SQLAlchemy, educational content generation.
"""

from __future__ import annotations

from application.evidence_update.evidence_transformer import (
    EvidenceTransformer,
    EvidenceTransformError,
)
from application.evidence_update.evidence_update_request import (
    EvidenceUpdateRequest,
)
from application.evidence_update.evidence_update_result import (
    EvidenceUpdateAuditEntry,
    EvidenceUpdateOutcome,
    EvidenceUpdateResult,
)
from application.evidence_update.evidence_update_service import (
    EvidenceUpdateError,
    EvidenceUpdateService,
)

__all__ = [
    "EvidenceTransformError",
    "EvidenceTransformer",
    "EvidenceUpdateAuditEntry",
    "EvidenceUpdateError",
    "EvidenceUpdateOutcome",
    "EvidenceUpdateRequest",
    "EvidenceUpdateResult",
    "EvidenceUpdateService",
]
