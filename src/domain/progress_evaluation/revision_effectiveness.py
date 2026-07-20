"""RevisionEffectiveness — how well revision translates into retention.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
    SESSION_ASSEMBLY_MODEL.md
Concept
    Revision Effectiveness
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.progress_evaluation.enums import RevisionEffectivenessBand


@dataclass(frozen=True, slots=True)
class RevisionEffectiveness(EducationalValueObject):
    """Immutable revision-effectiveness judgement from plans and retention.

    Compares scheduled review effort against retention posture and retention
    probes. Does not invent scheduling or mastery claims.
    """

    band: RevisionEffectivenessBand
    review_session_count: int
    retention_probe_count: int
    score_millipoints: int
    explanation: str

    def _validate(self) -> None:
        if not isinstance(self.band, RevisionEffectivenessBand):
            raise EducationalInvariantViolation(
                "band must be a RevisionEffectivenessBand",
                invariant="RevisionEffectiveness.band.type",
            )
        for name, value in (
            ("review_session_count", self.review_session_count),
            ("retention_probe_count", self.retention_probe_count),
            ("score_millipoints", self.score_millipoints),
        ):
            if not isinstance(value, int) or isinstance(value, bool):
                raise EducationalInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"RevisionEffectiveness.{name}.type",
                )
        if self.review_session_count < 0:
            raise EducationalInvariantViolation(
                "review_session_count must be non-negative",
                invariant="RevisionEffectiveness.review_session_count.non_negative",
            )
        if self.retention_probe_count < 0:
            raise EducationalInvariantViolation(
                "retention_probe_count must be non-negative",
                invariant="RevisionEffectiveness.retention_probe_count.non_negative",
            )
        if self.score_millipoints < 0 or self.score_millipoints > 1000:
            raise EducationalInvariantViolation(
                "score_millipoints must be between 0 and 1000 inclusive",
                invariant="RevisionEffectiveness.score_millipoints.range",
            )
        object.__setattr__(
            self,
            "explanation",
            require_non_empty_text(self.explanation, "explanation"),
        )

    @property
    def is_effective(self) -> bool:
        return self.band is RevisionEffectivenessBand.EFFECTIVE
