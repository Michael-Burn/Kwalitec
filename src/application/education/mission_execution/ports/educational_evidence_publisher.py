"""EducationalEvidencePublisher — publish evidence produced by execution."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from domain.education.educational_evidence.aggregates.educational_evidence import (
    EducationalEvidence,
)


class EducationalEvidencePublisher(ABC):
    """Outbound port for publishing EducationalEvidence from execution.

    Implementations live in infrastructure. This port never estimates
    mastery or updates StudentEducationalState — it only emits evidence.
    """

    @abstractmethod
    def publish_evidence(self, evidence: EducationalEvidence) -> None:
        """Publish a single evidence record."""

    @abstractmethod
    def publish_evidence_batch(
        self, evidence: Sequence[EducationalEvidence]
    ) -> None:
        """Publish a batch of evidence records."""
