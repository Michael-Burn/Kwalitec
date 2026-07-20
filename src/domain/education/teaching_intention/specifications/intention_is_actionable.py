"""Specification: TeachingIntention is instructional-actionable.

Architecture Source
    TEACHING_INTENTION_MODEL.md
Concept
    IntentionIsActionableSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.teaching_intention.enums import IntentionStatus
from domain.education.teaching_intention.policies.intention_alignment_policy import (
    IntentionAlignmentPolicy,
)
from domain.education.teaching_intention.policies.intention_validation_policy import (
    IntentionValidationPolicy,
)

if TYPE_CHECKING:
    from domain.education.teaching_intention.aggregates.teaching_intention import (
        TeachingIntention,
    )


class IntentionIsActionableSpecification:
    """True when an intention is structurally ready to govern instruction.

    Actionability means the intention is ACTIVE or REVISED, references a
    Priority and Diagnosis, possesses goal/outcome/scope/strength, and does
    not contradict constraints or Priority alignment. It does **not** mean a
    teaching strategy or learning episode has been selected.
    """

    def is_satisfied_by(self, intention: TeachingIntention) -> bool:
        if intention.status not in {
            IntentionStatus.ACTIVE,
            IntentionStatus.REVISED,
        }:
            return False
        if not intention.priority_references:
            return False
        if not intention.diagnosis_references:
            return False
        if not intention.goal.statement:
            return False
        if not intention.expected_outcome.statement:
            return False
        if not intention.scope.statement:
            return False
        if not intention.student_id:
            return False
        try:
            IntentionValidationPolicy.assert_constraints_satisfied(
                intention.constraints,
                intention_type=intention.intention_type,
                strength=intention.strength,
                priority_references=intention.priority_references,
                diagnosis_references=intention.diagnosis_references,
                hypothesis_references=intention.hypothesis_references,
                expected_outcome=intention.expected_outcome,
            )
            IntentionAlignmentPolicy.assert_priority_not_contradicted(
                intention.priority_references,
                intention.diagnosis_references,
                intention.intention_type,
            )
        except EducationalInvariantViolation:
            return False
        return True

    def assert_satisfied_by(self, intention: TeachingIntention) -> None:
        if not self.is_satisfied_by(intention):
            raise EducationalInvariantViolation(
                "teaching intention is not instructional-actionable",
                invariant="IntentionIsActionableSpecification.unsatisfied",
            )
