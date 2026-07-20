"""Specification: Interpretation is educationally consistent.

Architecture Source
    EDUCATIONAL_EVIDENCE_MODEL.md /
    CAPABILITY_4_8_2_EDUCATIONAL_EVIDENCE_ANALYSIS.md
Concept
    InterpretationIsConsistentSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.evidence_interpretation.enums import InterpretationStatus
from domain.education.evidence_interpretation.policies.clustering_policy import (
    ClusteringPolicy,
)
from domain.education.foundation.errors import EducationalInvariantViolation

if TYPE_CHECKING:
    from domain.education.evidence_interpretation.aggregates.interpretation import (
        Interpretation,
    )


class InterpretationIsConsistentSpecification:
    """True when clusters, patterns, and confidence align educationally."""

    def is_satisfied_by(self, interpretation: Interpretation) -> bool:
        if interpretation.status is InterpretationStatus.INVALIDATED:
            return False
        try:
            ClusteringPolicy.assert_consistent(
                interpretation.clusters,
                interpretation.patterns,
                interpretation.confidence,
            )
        except EducationalInvariantViolation:
            return False
        return True

    def assert_satisfied_by(self, interpretation: Interpretation) -> None:
        if not self.is_satisfied_by(interpretation):
            raise EducationalInvariantViolation(
                "interpretation is not educationally consistent",
                invariant="InterpretationIsConsistentSpecification.unsatisfied",
            )
