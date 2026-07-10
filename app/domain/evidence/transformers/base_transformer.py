"""Abstract transformer interface for Learning Evidence.

Specialised transformers (Knowledge, Behaviour, Confidence, Revision,
Planning, Time, …) inherit from this base. This module defines the contract
only — no specialised implementations live here.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.evidence.evidence_candidate import EvidenceCandidate
from app.domain.evidence.learning_evidence import LearningEvidence


class BaseTransformer(ABC):
    """Strategy interface: validated Evidence Candidate → Learning Evidence.

    Implementations must remain pure domain logic: normalization only — no
    persistence, scoring, Twin updates, recommendations, or framework imports.
    """

    @abstractmethod
    def supports(self, candidate: EvidenceCandidate) -> bool:
        """Return True if this transformer can normalize ``candidate``.

        Args:
            candidate: Validated Evidence Candidate under consideration.

        Returns:
            Whether ``transform`` should be invoked for this candidate.
        """

    @abstractmethod
    def transform(self, candidate: EvidenceCandidate) -> LearningEvidence:
        """Normalize a supported Evidence Candidate into Learning Evidence.

        Args:
            candidate: Validated Evidence Candidate previously accepted by
                ``supports``. Must not be mutated.

        Returns:
            One immutable LearningEvidence object. Never scores, persists,
            recommends, or mutates Twin state.
        """
