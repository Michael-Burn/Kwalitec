"""Specification: EducationalHypothesis remains revisable.

Architecture Source
    EDUCATIONAL_HYPOTHESIS_MODEL.md
Concept
    HypothesisIsRevisableSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.hypothesis.enums import HypothesisStatus

if TYPE_CHECKING:
    from domain.education.hypothesis.aggregates.educational_hypothesis import (
        EducationalHypothesis,
    )


class HypothesisIsRevisableSpecification:
    """True when a hypothesis may still be revised, strengthened, or weakened.

    Discarded hypotheses are terminal and are not revisable. Active, revised,
    and suspended hypotheses remain revisable — refusal to revise is
    educational malpractice.
    """

    def is_satisfied_by(self, hypothesis: EducationalHypothesis) -> bool:
        if hypothesis.status is HypothesisStatus.DISCARDED:
            return False
        return hypothesis.status in {
            HypothesisStatus.ACTIVE,
            HypothesisStatus.REVISED,
            HypothesisStatus.SUSPENDED,
        }

    def assert_satisfied_by(self, hypothesis: EducationalHypothesis) -> None:
        if not self.is_satisfied_by(hypothesis):
            raise EducationalInvariantViolation(
                "hypothesis is not revisable",
                invariant="HypothesisIsRevisableSpecification.unsatisfied",
            )
