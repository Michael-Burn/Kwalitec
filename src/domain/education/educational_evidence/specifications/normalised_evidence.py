"""Specification: evidence is in canonical normalised form.

Architecture Source
    STUDENT_DIGITAL_TWIN.md (Learning Evidence Model)
Concept
    NormalisedEvidenceSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.foundation.errors import EducationalInvariantViolation

if TYPE_CHECKING:
    from domain.education.educational_evidence.aggregates.educational_evidence import (
        EducationalEvidence,
    )


class NormalisedEvidenceSpecification:
    """True when evidence already equals its own normalised form.

    Guards against evidence drifting from canonical shape — normalised
    evidence must always be internally consistent with itself.
    """

    def is_satisfied_by(self, evidence: EducationalEvidence) -> bool:
        return evidence.is_normalised()

    def assert_satisfied_by(self, evidence: EducationalEvidence) -> None:
        if not self.is_satisfied_by(evidence):
            raise EducationalInvariantViolation(
                "evidence is not in canonical normalised form",
                invariant="NormalisedEvidenceSpecification.unsatisfied",
            )
