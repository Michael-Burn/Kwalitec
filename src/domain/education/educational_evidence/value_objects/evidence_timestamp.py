"""Evidence timestamp — when an educational observation occurred.

Architecture Source
    STUDENT_DIGITAL_TWIN.md (Learning Evidence Model, Evidence rules)
Concept
    Evidence Timestamp
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class EvidenceTimestamp(EducationalValueObject):
    """Immutable educational observation time.

    Timestamps are always supplied by the caller — this value object never
    reads the wall clock. Naive datetimes are rejected; educational
    evidence time must be timezone-aware.
    """

    occurred_at: datetime

    def _validate(self) -> None:
        if not isinstance(self.occurred_at, datetime):
            raise EducationalInvariantViolation(
                "occurred_at must be a datetime",
                invariant="EvidenceTimestamp.occurred_at.type",
            )
        if self.occurred_at.tzinfo is None:
            raise EducationalInvariantViolation(
                "occurred_at must be timezone-aware",
                invariant="EvidenceTimestamp.occurred_at.timezone_aware",
            )

    @classmethod
    def of(cls, occurred_at: datetime) -> EvidenceTimestamp:
        """Build a timestamp from a timezone-aware datetime."""
        return cls(occurred_at=occurred_at)

    def is_before(self, other: EvidenceTimestamp) -> bool:
        if not isinstance(other, EvidenceTimestamp):
            raise EducationalInvariantViolation(
                "other must be an EvidenceTimestamp",
                invariant="EvidenceTimestamp.is_before.type",
            )
        return self.occurred_at < other.occurred_at

    def is_after(self, other: EvidenceTimestamp) -> bool:
        if not isinstance(other, EvidenceTimestamp):
            raise EducationalInvariantViolation(
                "other must be an EvidenceTimestamp",
                invariant="EvidenceTimestamp.is_after.type",
            )
        return self.occurred_at > other.occurred_at

    def __str__(self) -> str:
        return self.occurred_at.isoformat()
