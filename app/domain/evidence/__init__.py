"""Evidence domain package: extraction, validation, and transformation.

Pure conceptual objects that convert Learning Events into Evidence Candidates,
structurally validate those candidates, and normalize accepted candidates into
canonical Learning Evidence. See README.md.
"""

from __future__ import annotations

from app.domain.evidence.evidence_candidate import EvidenceCandidate
from app.domain.evidence.evidence_category import (
    EvidenceCategory,
    EvidenceConfidenceLevel,
)
from app.domain.evidence.evidence_extractor import EvidenceExtractor
from app.domain.evidence.evidence_transformer import (
    EvidenceTransformer,
    TransformationError,
)
from app.domain.evidence.evidence_type import EvidenceType
from app.domain.evidence.extractors import BaseExtractor
from app.domain.evidence.learning_evidence import LearningEvidence
from app.domain.evidence.transformers import BaseTransformer
from app.domain.evidence.validation_message import ValidationMessage
from app.domain.evidence.validation_result import ValidationResult
from app.domain.evidence.validation_severity import ValidationSeverity
from app.domain.evidence.validators import BaseValidator, EvidenceValidator

__all__ = [
    "BaseExtractor",
    "BaseTransformer",
    "BaseValidator",
    "EvidenceCandidate",
    "EvidenceCategory",
    "EvidenceConfidenceLevel",
    "EvidenceExtractor",
    "EvidenceTransformer",
    "EvidenceType",
    "EvidenceValidator",
    "LearningEvidence",
    "TransformationError",
    "ValidationMessage",
    "ValidationResult",
    "ValidationSeverity",
]
