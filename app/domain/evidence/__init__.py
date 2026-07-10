"""Evidence domain package: extraction and validation stages.

Pure conceptual objects that convert Learning Events into Evidence Candidates
and structurally validate those candidates before transformation. See README.md.
"""

from __future__ import annotations

from app.domain.evidence.evidence_candidate import EvidenceCandidate
from app.domain.evidence.evidence_category import (
    EvidenceCategory,
    EvidenceConfidenceLevel,
)
from app.domain.evidence.evidence_extractor import EvidenceExtractor
from app.domain.evidence.extractors import BaseExtractor
from app.domain.evidence.validation_message import ValidationMessage
from app.domain.evidence.validation_result import ValidationResult
from app.domain.evidence.validation_severity import ValidationSeverity
from app.domain.evidence.validators import BaseValidator, EvidenceValidator

__all__ = [
    "BaseExtractor",
    "BaseValidator",
    "EvidenceCandidate",
    "EvidenceCategory",
    "EvidenceConfidenceLevel",
    "EvidenceExtractor",
    "EvidenceValidator",
    "ValidationMessage",
    "ValidationResult",
    "ValidationSeverity",
]
