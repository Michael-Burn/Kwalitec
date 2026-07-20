"""Specification: EducationalHypothesis is educationally supported.

Architecture Source
    EDUCATIONAL_HYPOTHESIS_MODEL.md
Concept
    HypothesisIsSupportedSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.hypothesis.enums import HypothesisStatus

if TYPE_CHECKING:
    from domain.education.hypothesis.aggregates.educational_hypothesis import (
        EducationalHypothesis,
    )


class HypothesisIsSupportedSpecification:
    """True when a hypothesis has lawful diagnostic and evidential warrant.

    Support means the hypothesis references at least one Diagnosis, possesses
    plausibility and explanatory strength, cites supporting reasons, and is
    not DISCARDED. Support does **not** mean the hypothesis is a fact, a
    teaching strategy, or a priority ranking.
    """

    def is_satisfied_by(self, hypothesis: EducationalHypothesis) -> bool:
        if hypothesis.status is HypothesisStatus.DISCARDED:
            return False
        if not hypothesis.diagnosis_references:
            return False
        if hypothesis.plausibility is None:
            return False
        if hypothesis.explanatory_strength is None:
            return False
        if not hypothesis.reasons:
            return False
        if not hypothesis.explanation.strip():
            return False
        if hypothesis.scope is None:
            return False
        return True

    def assert_satisfied_by(self, hypothesis: EducationalHypothesis) -> None:
        if not self.is_satisfied_by(hypothesis):
            raise EducationalInvariantViolation(
                "hypothesis is not educationally supported",
                invariant="HypothesisIsSupportedSpecification.unsatisfied",
            )
