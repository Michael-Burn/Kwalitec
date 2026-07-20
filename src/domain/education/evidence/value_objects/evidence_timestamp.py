"""Evidence timestamp — when an educational observation occurred.

Architecture Source
    CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md (§2 Attribution)
Concept
    Evidence Timestamp
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class EvidenceTimestamp(EducationalValueObject):
    """Immutable educational observation time.

    Timestamps are educational attribution, not persistence or audit plumbing.
    Naive datetimes are rejected — educational time must be timezone-aware.
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

    @classmethod
    def from_utc_components(
        cls,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
    ) -> EvidenceTimestamp:
        """Build a UTC evidence timestamp from calendar components."""
        return cls(
            occurred_at=datetime(
                year, month, day, hour, minute, second, tzinfo=UTC
            )
        )

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
