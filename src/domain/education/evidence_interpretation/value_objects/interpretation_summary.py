"""Interpretation summary — observational synopsis of interpreted patterns.

Architecture Source
    EDUCATIONAL_EVIDENCE_MODEL.md /
    CAPABILITY_4_8_2_EDUCATIONAL_EVIDENCE_ANALYSIS.md
Concept
    Interpretation Summary
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation

# Forbidden conclusion vocabulary — interpretation summarises patterns only.
_FORBIDDEN_CONCLUSION_TOKENS = frozenset(
    {
        "diagnose",
        "diagnosis",
        "recommend",
        "recommendation",
        "prioritise",
        "prioritize",
        "priority",
        "mastery",
        "mastered",
        "prescribe",
        "prescription",
    }
)


@dataclass(frozen=True, slots=True)
class InterpretationSummary(EducationalValueObject):
    """Immutable observational synopsis of an Interpretation.

    Summarises interpreted educational patterns. Must not encode diagnoses,
    recommendations, or priority rankings.
    """

    text: str
    pattern_count: int
    cluster_count: int

    def _validate(self) -> None:
        object.__setattr__(self, "text", require_non_empty_text(self.text, "text"))
        lowered = self.text.casefold()
        for token in _FORBIDDEN_CONCLUSION_TOKENS:
            if token in lowered:
                raise EducationalInvariantViolation(
                    f"interpretation summary must not contain conclusion "
                    f"language ({token})",
                    invariant="InterpretationSummary.text.no_conclusion",
                )
        if not isinstance(self.pattern_count, int) or isinstance(
            self.pattern_count, bool
        ):
            raise EducationalInvariantViolation(
                "pattern_count must be an integer",
                invariant="InterpretationSummary.pattern_count.type",
            )
        if self.pattern_count < 1:
            raise EducationalInvariantViolation(
                "pattern_count must be at least 1",
                invariant="InterpretationSummary.pattern_count.min",
            )
        if not isinstance(self.cluster_count, int) or isinstance(
            self.cluster_count, bool
        ):
            raise EducationalInvariantViolation(
                "cluster_count must be an integer",
                invariant="InterpretationSummary.cluster_count.type",
            )
        if self.cluster_count < 1:
            raise EducationalInvariantViolation(
                "cluster_count must be at least 1",
                invariant="InterpretationSummary.cluster_count.min",
            )

    @classmethod
    def of(
        cls,
        text: str,
        *,
        pattern_count: int,
        cluster_count: int,
    ) -> InterpretationSummary:
        return cls(
            text=text,
            pattern_count=pattern_count,
            cluster_count=cluster_count,
        )

    def __str__(self) -> str:
        return self.text
