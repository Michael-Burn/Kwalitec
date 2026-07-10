"""Evidence Extraction Engine domain package.

Pure conceptual objects that convert Learning Events into Evidence Candidates.
See README.md.
"""

from __future__ import annotations

from app.domain.evidence.evidence_candidate import EvidenceCandidate
from app.domain.evidence.evidence_category import (
    EvidenceCategory,
    EvidenceConfidenceLevel,
)
from app.domain.evidence.evidence_extractor import EvidenceExtractor
from app.domain.evidence.extractors import BaseExtractor

__all__ = [
    "BaseExtractor",
    "EvidenceCandidate",
    "EvidenceCategory",
    "EvidenceConfidenceLevel",
    "EvidenceExtractor",
]
