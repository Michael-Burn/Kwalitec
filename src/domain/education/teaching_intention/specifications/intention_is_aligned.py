"""Specification: TeachingIntention is aligned with Priority and Diagnosis.

Architecture Source
    TEACHING_INTENTION_MODEL.md
Concept
    IntentionIsAlignedSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.teaching_intention.policies.intention_alignment_policy import (
    IntentionAlignmentPolicy,
)

if TYPE_CHECKING:
    from domain.education.teaching_intention.aggregates.teaching_intention import (
        TeachingIntention,
    )


class IntentionIsAlignedSpecification:
    """True when intention type does not contradict Priority / Diagnosis.

    Alignment is educational reasoning integrity: the named change must be a
    lawful response to the referenced diagnoses under Priority. It is not
    strategy fitness or episode readiness.
    """

    def is_satisfied_by(self, intention: TeachingIntention) -> bool:
        return IntentionAlignmentPolicy.is_aligned(
            intention.intention_type,
            intention.priority_references,
            intention.diagnosis_references,
        )

    def assert_satisfied_by(self, intention: TeachingIntention) -> None:
        if not self.is_satisfied_by(intention):
            raise EducationalInvariantViolation(
                "teaching intention is not aligned with Priority and Diagnosis",
                invariant="IntentionIsAlignedSpecification.unsatisfied",
            )
