"""Specification: evidence is internally consistent.

Architecture Source
    STUDENT_DIGITAL_TWIN.md (Learning Evidence Model)
Concept
    EvidenceIsConsistentSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.educational_evidence.policies.evidence_validation_policy import (
    EvidenceValidationPolicy,
)
from domain.education.foundation.errors import EducationalInvariantViolation

if TYPE_CHECKING:
    from domain.education.educational_evidence.aggregates.educational_evidence import (
        EducationalEvidence,
    )


class EvidenceIsConsistentSpecification:
    """True when evidence context and metadata cohere with its type.

    Consistency here means structural/outcome coherence — for example a
    ``QUESTION_ANSWERED`` record can never carry ``is_correct=False``. It is
    not a judgement about educational correctness.
    """

    def is_satisfied_by(self, evidence: EducationalEvidence) -> bool:
        try:
            EvidenceValidationPolicy.assert_context_matches_type(
                evidence.evidence_type, evidence.context
            )
            EvidenceValidationPolicy.assert_metadata_matches_type(
                evidence.evidence_type, evidence.metadata
            )
        except EducationalInvariantViolation:
            return False
        return True

    def assert_satisfied_by(self, evidence: EducationalEvidence) -> None:
        if not self.is_satisfied_by(evidence):
            raise EducationalInvariantViolation(
                "evidence is not internally consistent",
                invariant="EvidenceIsConsistentSpecification.unsatisfied",
            )
