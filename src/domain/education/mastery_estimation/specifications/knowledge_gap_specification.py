"""Specification: a KnowledgeGap is internally well-formed and non-trivial.

Architecture Source
    KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md
    KNOWLEDGE_DEPENDENCY_MODEL.md
Concept
    Knowledge Gap Specification
"""

from __future__ import annotations

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.mastery_estimation.enums import KnowledgeGapKind
from domain.education.mastery_estimation.value_objects.knowledge_gap import (
    KnowledgeGap,
)

# A gap's own mastery_score must fall below this magnitude — a gap can
# never be attached to a competency that is already comfortably secure.
_GAP_MAGNITUDE_CEILING = 0.60


class KnowledgeGapSpecification:
    """A KnowledgeGap must describe a genuine, evidenced weakness.

    Beyond the shape invariants ``KnowledgeGap`` already enforces at
    construction (``WEAK_PREREQUISITE`` gaps always carry
    ``related_competency_id`` and ``dependency_strength``), this
    specification additionally requires that the gap's own
    ``mastery_score`` actually has supporting evidence and sits below the
    secure threshold — a gap is never raised over an unassessed
    competency (absence of evidence is not itself a weakness) or over one
    that already demonstrates secure mastery.
    """

    @staticmethod
    def is_satisfied_by(gap: KnowledgeGap) -> bool:
        if not gap.mastery_score.has_evidence():
            return False
        if gap.mastery_score.magnitude >= _GAP_MAGNITUDE_CEILING:
            return False
        if gap.kind is KnowledgeGapKind.WEAK_PREREQUISITE:
            return (
                gap.related_competency_id is not None
                and gap.dependency_strength is not None
                and gap.related_competency_id != gap.competency_id
            )
        return gap.related_competency_id is None and gap.dependency_strength is None

    @staticmethod
    def assert_satisfied_by(gap: KnowledgeGap) -> None:
        if not KnowledgeGapSpecification.is_satisfied_by(gap):
            raise EducationalInvariantViolation(
                "a knowledge gap must be evidenced, below the secure "
                "threshold, and carry exactly the fields its kind requires",
                invariant="KnowledgeGapSpecification.well_formed",
            )
