"""Evidence weight — deterministic epistemic magnitude of an observation.

Architecture Source
    STUDENT_DIGITAL_TWIN.md (Learning Evidence Model)
Concept
    Evidence Weight
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.educational_evidence.enums import EvidenceWeightBand
from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation

# Fixed threshold table — magnitude -> band. Deterministic, never estimated.
_BAND_THRESHOLDS: tuple[tuple[float, EvidenceWeightBand], ...] = (
    (0.05, EvidenceWeightBand.NEGLIGIBLE),
    (0.30, EvidenceWeightBand.LOW),
    (0.60, EvidenceWeightBand.MODERATE),
    (0.85, EvidenceWeightBand.HIGH),
)


@dataclass(frozen=True, slots=True)
class EvidenceWeight(EducationalValueObject):
    """Immutable, deterministic epistemic weight of a piece of evidence.

    ``band`` is always derived from ``magnitude`` by a fixed threshold
    table — never supplied independently — so weight and band can never
    disagree. This value object does not estimate mastery or readiness; it
    only classifies how much observational warrant a piece of evidence
    carries.
    """

    magnitude: float

    def _validate(self) -> None:
        if isinstance(self.magnitude, bool) or not isinstance(
            self.magnitude, int | float
        ):
            raise EducationalInvariantViolation(
                "magnitude must be a real number",
                invariant="EvidenceWeight.magnitude.type",
            )
        if self.magnitude < 0.0 or self.magnitude > 1.0:
            raise EducationalInvariantViolation(
                "magnitude must be between 0.0 and 1.0 inclusive",
                invariant="EvidenceWeight.magnitude.range",
            )
        object.__setattr__(self, "magnitude", round(float(self.magnitude), 4))

    @property
    def band(self) -> EvidenceWeightBand:
        for threshold, band in _BAND_THRESHOLDS:
            if self.magnitude < threshold:
                return band
        return EvidenceWeightBand.DECISIVE

    @classmethod
    def of(cls, magnitude: float) -> EvidenceWeight:
        return cls(magnitude=magnitude)

    def is_at_least(self, other: EvidenceWeight) -> bool:
        if not isinstance(other, EvidenceWeight):
            raise EducationalInvariantViolation(
                "other must be an EvidenceWeight",
                invariant="EvidenceWeight.is_at_least.type",
            )
        return self.magnitude >= other.magnitude

    def __str__(self) -> str:
        return f"{self.magnitude:.4f}:{self.band.value}"
