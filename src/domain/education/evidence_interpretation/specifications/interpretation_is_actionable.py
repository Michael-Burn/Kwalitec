"""Specification: Interpretation is educationally actionable for downstream use.

Architecture Source
    EDUCATIONAL_EVIDENCE_MODEL.md /
    CAPABILITY_4_8_2_EDUCATIONAL_EVIDENCE_ANALYSIS.md
Concept
    InterpretationIsActionableSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.evidence_interpretation.enums import InterpretationStatus
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation

if TYPE_CHECKING:
    from domain.education.evidence_interpretation.aggregates.interpretation import (
        Interpretation,
    )


class InterpretationIsActionableSpecification:
    """True when an Interpretation is structurally ready as pattern output.

    Actionability means the interpretation is ACTIVE or REVISED, references
    evidence, identifies patterns and educational scope, and possesses at least
    LOW confidence. It does **not** mean the interpretation is a diagnosis,
    recommendation, or priority ranking.
    """

    def is_satisfied_by(self, interpretation: Interpretation) -> bool:
        if interpretation.status not in {
            InterpretationStatus.ACTIVE,
            InterpretationStatus.REVISED,
        }:
            return False
        if not interpretation.clusters:
            return False
        if not interpretation.patterns:
            return False
        if interpretation.confidence is None:
            return False
        if not interpretation.confidence.is_at_least(ConfidenceLevel.LOW):
            return False
        if interpretation.context is None:
            return False
        if not interpretation.context.educational_scope:
            return False
        if not interpretation.student_id:
            return False
        if not interpretation.referenced_evidence_ids():
            return False
        return True

    def assert_satisfied_by(self, interpretation: Interpretation) -> None:
        if not self.is_satisfied_by(interpretation):
            raise EducationalInvariantViolation(
                "interpretation is not educationally actionable",
                invariant="InterpretationIsActionableSpecification.unsatisfied",
            )
