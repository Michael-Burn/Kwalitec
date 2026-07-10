"""Abstract extractor interface for Evidence Candidates.

Specialised extractors (QuestionAttempt, StudySession, Mission, …) inherit
from this base. This module defines the contract only — no specialised
implementations live here.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.evidence.evidence_candidate import EvidenceCandidate
from app.domain.learning_events.learning_event import LearningEvent


class BaseExtractor(ABC):
    """Strategy interface: Learning Event → zero or more Evidence Candidates.

    Implementations must remain pure domain logic: no persistence, scoring,
    Twin updates, or framework imports.
    """

    @abstractmethod
    def supports(self, event: LearningEvent) -> bool:
        """Return True if this extractor can interpret ``event``.

        Args:
            event: Learning Event under consideration.

        Returns:
            Whether ``extract`` should be invoked for this event.
        """

    @abstractmethod
    def extract(self, event: LearningEvent) -> list[EvidenceCandidate]:
        """Extract Evidence Candidates from a supported Learning Event.

        Args:
            event: Learning Event previously accepted by ``supports``.

        Returns:
            Zero or more immutable EvidenceCandidate objects. Never scores,
            persists, or mutates Twin state.
        """
