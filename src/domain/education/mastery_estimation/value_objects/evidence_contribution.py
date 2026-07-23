"""Evidence contribution — how one piece of evidence shaped an estimate.

Architecture Source
    STUDENT_DIGITAL_TWIN.md (Learning Evidence Model)
Concept
    Evidence Contribution

This value object legitimately references ``educational_evidence`` types.
Unlike its sibling bounded contexts, Mastery Estimation exists to reason
across ``educational_evidence``, ``student_state``, and ``knowledge_graph``
— it does not stay isolated from them.
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.educational_evidence.enums import EvidenceType
from domain.education.educational_evidence.ids import EvidenceId
from domain.education.educational_evidence.value_objects.evidence_timestamp import (
    EvidenceTimestamp,
)
from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class EvidenceContribution(EducationalValueObject):
    """Immutable record of one evidence item's signed influence.

    ``contribution`` is a signed strength in ``[-1.0, 1.0]``: positive
    values support mastery, negative values weigh against it, and ``0.0``
    denotes evidence that was considered but is educationally neutral (for
    example an engagement signal with no correctness outcome). ``weight``
    is the evidentiary magnitude the estimator assigned when deriving
    ``contribution`` from the underlying evidence.
    """

    evidence_id: EvidenceId
    evidence_type: EvidenceType
    contribution: float
    weight: float
    occurred_at: EvidenceTimestamp

    def _validate(self) -> None:
        if not isinstance(self.evidence_id, EvidenceId):
            raise EducationalInvariantViolation(
                "evidence_id must be an EvidenceId",
                invariant="EvidenceContribution.evidence_id.type",
            )
        if not isinstance(self.evidence_type, EvidenceType):
            raise EducationalInvariantViolation(
                "evidence_type must be an EvidenceType",
                invariant="EvidenceContribution.evidence_type.type",
            )
        if isinstance(self.contribution, bool) or not isinstance(
            self.contribution, int | float
        ):
            raise EducationalInvariantViolation(
                "contribution must be a real number",
                invariant="EvidenceContribution.contribution.type",
            )
        if self.contribution < -1.0 or self.contribution > 1.0:
            raise EducationalInvariantViolation(
                "contribution must be between -1.0 and 1.0 inclusive",
                invariant="EvidenceContribution.contribution.range",
            )
        object.__setattr__(
            self, "contribution", round(float(self.contribution), 4)
        )
        if isinstance(self.weight, bool) or not isinstance(
            self.weight, int | float
        ):
            raise EducationalInvariantViolation(
                "weight must be a real number",
                invariant="EvidenceContribution.weight.type",
            )
        if self.weight < 0.0 or self.weight > 1.0:
            raise EducationalInvariantViolation(
                "weight must be between 0.0 and 1.0 inclusive",
                invariant="EvidenceContribution.weight.range",
            )
        object.__setattr__(self, "weight", round(float(self.weight), 4))
        if not isinstance(self.occurred_at, EvidenceTimestamp):
            raise EducationalInvariantViolation(
                "occurred_at must be an EvidenceTimestamp",
                invariant="EvidenceContribution.occurred_at.type",
            )

    def is_positive(self) -> bool:
        return self.contribution > 0.0

    def is_negative(self) -> bool:
        return self.contribution < 0.0

    def is_neutral(self) -> bool:
        return self.contribution == 0.0

    def weighted_magnitude(self) -> float:
        """Absolute weighted strength of this contribution."""
        return round(abs(self.contribution) * self.weight, 4)

    def __str__(self) -> str:
        return f"{self.evidence_id.value}:{self.contribution:+.4f}"
