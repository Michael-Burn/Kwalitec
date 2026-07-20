"""InterventionSignal — progress-threshold signal that intervention is needed.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
    EDUCATIONAL_PRIORITY_MODEL.md
Concept
    Intervention Signal
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.progress_evaluation.enums import InterventionUrgency


@dataclass(frozen=True, slots=True)
class InterventionSignal(EducationalValueObject):
    """Immutable intervention signal derived from progress thresholds.

    Signals need — they do not approve, select, or orchestrate interventions.
    """

    required: bool
    urgency: InterventionUrgency
    reasons: tuple[str, ...]
    explanation: str

    def _validate(self) -> None:
        if not isinstance(self.required, bool):
            raise EducationalInvariantViolation(
                "required must be a boolean",
                invariant="InterventionSignal.required.type",
            )
        if not isinstance(self.urgency, InterventionUrgency):
            raise EducationalInvariantViolation(
                "urgency must be an InterventionUrgency",
                invariant="InterventionSignal.urgency.type",
            )
        if self.required and self.urgency is InterventionUrgency.NONE:
            raise EducationalInvariantViolation(
                "required intervention cannot have urgency NONE",
                invariant="InterventionSignal.required.urgency",
            )
        if not self.required and self.urgency is not InterventionUrgency.NONE:
            raise EducationalInvariantViolation(
                "non-required intervention must have urgency NONE",
                invariant="InterventionSignal.not_required.urgency",
            )
        if not isinstance(self.reasons, tuple):
            raise EducationalInvariantViolation(
                "reasons must be a tuple",
                invariant="InterventionSignal.reasons.type",
            )
        if self.required and not self.reasons:
            raise EducationalInvariantViolation(
                "required intervention must declare at least one reason",
                invariant="InterventionSignal.reasons.min_one",
            )
        if not self.required and self.reasons:
            raise EducationalInvariantViolation(
                "non-required intervention must not declare reasons",
                invariant="InterventionSignal.reasons.empty",
            )
        cleaned: list[str] = []
        for reason in self.reasons:
            cleaned.append(require_non_empty_text(reason, "reason"))
        object.__setattr__(self, "reasons", tuple(cleaned))
        object.__setattr__(
            self,
            "explanation",
            require_non_empty_text(self.explanation, "explanation"),
        )
