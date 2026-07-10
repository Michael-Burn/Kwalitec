"""Abstract validator interface for Evidence Candidates.

Specialised structural (and future) validators inherit from this base.
This module defines the contract only — composition lives in
``EvidenceValidator``.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.evidence.evidence_candidate import EvidenceCandidate
from app.domain.evidence.validation_message import ValidationMessage


class BaseValidator(ABC):
    """Strategy interface: Evidence Candidate → zero or more messages.

    Implementations must remain pure domain logic: no persistence, scoring,
    Twin updates, mutation of the candidate, or framework imports.
    """

    @abstractmethod
    def validate(self, candidate: EvidenceCandidate) -> list[ValidationMessage]:
        """Inspect ``candidate`` and return structural findings.

        Args:
            candidate: Immutable Evidence Candidate under review. Must not be
                mutated.

        Returns:
            Zero or more ValidationMessage objects. An empty list means this
            validator found no issues. Never transforms, scores, or persists.
        """
