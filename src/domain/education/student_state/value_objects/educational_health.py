"""Educational health — supplied overall educational posture.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
    EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md
Concept
    Educational Health
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.student_state.enums import EducationalHealthBand


@dataclass(frozen=True, slots=True)
class EducationalHealth(EducationalValueObject):
    """Immutable, supplied overall educational health posture.

    EducationalHealth stores a supplied band, optional ratio, and short
    explainability reason codes. It does not compute risk, diagnose
    burnout, or infer health from behaviour.
    """

    band: EducationalHealthBand
    ratio: float | None = None
    reasons: tuple[str, ...] = ()

    def _validate(self) -> None:
        if not isinstance(self.band, EducationalHealthBand):
            raise EducationalInvariantViolation(
                "band must be an EducationalHealthBand",
                invariant="EducationalHealth.band.type",
            )
        if self.ratio is not None:
            if isinstance(self.ratio, bool) or not isinstance(
                self.ratio, int | float
            ):
                raise EducationalInvariantViolation(
                    "ratio must be a real number when provided",
                    invariant="EducationalHealth.ratio.type",
                )
            if self.ratio < 0.0 or self.ratio > 1.0:
                raise EducationalInvariantViolation(
                    "ratio must be between 0.0 and 1.0 inclusive",
                    invariant="EducationalHealth.ratio.range",
                )
            object.__setattr__(self, "ratio", float(self.ratio))
        if not isinstance(self.reasons, tuple | list):
            raise EducationalInvariantViolation(
                "reasons must be a tuple or list of strings",
                invariant="EducationalHealth.reasons.type",
            )
        cleaned = tuple(
            require_non_empty_text(reason, "reason") for reason in self.reasons
        )
        object.__setattr__(self, "reasons", cleaned)

    @classmethod
    def unknown(cls) -> EducationalHealth:
        return cls(band=EducationalHealthBand.UNKNOWN)
