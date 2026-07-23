"""EvidenceProvider — load and record EducationalEvidence for orchestration."""

from __future__ import annotations

from abc import ABC, abstractmethod

from domain.education.educational_evidence.aggregates.educational_evidence import (
    EducationalEvidence,
)


class EvidenceProvider(ABC):
    """Outbound port for educational evidence retrieval and recording.

    Implementations live in infrastructure. This package defines the
    interface only — no SQLAlchemy, no repositories here.
    """

    @abstractmethod
    def list_evidence(self, student_id: str) -> tuple[EducationalEvidence, ...]:
        """Return recorded evidence for ``student_id`` (may be empty)."""

    @abstractmethod
    def record_evidence(self, evidence: EducationalEvidence) -> None:
        """Persist or acknowledge newly produced educational evidence.

        Raises:
            application.errors.ApplicationError: On coordination failure.
        """
