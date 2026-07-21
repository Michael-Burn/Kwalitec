"""Learning Evidence Capture — record completed study-session outcomes.

Captures observational facts from a guided study session as immutable
educational evidence. Never diagnoses, recommends, prioritises, plans study,
persists, orchestrates learning engines, or invokes AI.

Allowed: deterministic mapping of presentation / runtime inputs into
``LearningSessionOutcome`` and ``CapturedEvidence``.

Forbidden: mastery, diagnosis, prioritisation, strategy selection,
persistence, Flask/SQLAlchemy, educational content generation.
"""

from __future__ import annotations

from application.evidence_capture.captured_evidence import CapturedEvidence
from application.evidence_capture.evidence_capture_service import (
    EvidenceCaptureError,
    EvidenceCaptureService,
)
from application.evidence_capture.evidence_mapper import EvidenceMapper
from application.evidence_capture.learning_session_outcome import (
    CompletionStatus,
    LearningSessionOutcome,
)

__all__ = [
    "CapturedEvidence",
    "CompletionStatus",
    "EvidenceCaptureError",
    "EvidenceCaptureService",
    "EvidenceMapper",
    "LearningSessionOutcome",
]
