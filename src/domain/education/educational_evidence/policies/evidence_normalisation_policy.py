"""Policy producing canonical, internally-consistent evidence detail.

Architecture Source
    STUDENT_DIGITAL_TWIN.md (Learning Evidence Model)
Concept
    Evidence Normalisation Policy
"""

from __future__ import annotations

from domain.education.educational_evidence.value_objects.evidence_metadata import (
    EvidenceMetadata,
)
from domain.education.educational_evidence.value_objects.evidence_weight import (
    EvidenceWeight,
)


class EvidenceNormalisationPolicy:
    """Derives the canonical form of evidence value objects.

    Construction of ``EvidenceMetadata`` and ``EvidenceWeight`` already
    enforces canonical form eagerly (sorted keys; rounded magnitude with a
    band derived from it). This policy exposes that canonicalisation
    explicitly so normalisation is a first-class, testable operation rather
    than an incidental side effect of ``__post_init__``.
    """

    @staticmethod
    def normalise_metadata(metadata: EvidenceMetadata) -> EvidenceMetadata:
        return EvidenceMetadata(entries=metadata.entries)

    @staticmethod
    def normalise_weight(weight: EvidenceWeight) -> EvidenceWeight:
        return EvidenceWeight(magnitude=weight.magnitude)

    @staticmethod
    def is_metadata_normalised(metadata: EvidenceMetadata) -> bool:
        return metadata == EvidenceNormalisationPolicy.normalise_metadata(metadata)

    @staticmethod
    def is_weight_normalised(weight: EvidenceWeight) -> bool:
        return weight == EvidenceNormalisationPolicy.normalise_weight(weight)
