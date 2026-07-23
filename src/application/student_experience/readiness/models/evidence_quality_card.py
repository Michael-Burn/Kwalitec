"""EvidenceQualityCard — evidence quality / quantity projection."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.readiness.enums import (
    EvidenceQualityBand,
    EvidenceQuantityBand,
)
from application.student_experience.readiness.errors import (
    ReadinessInvariantViolation,
)


@dataclass(frozen=True, slots=True)
class EvidenceQualityCard:
    """Immutable evidence quality card — why the readiness picture is trustworthy."""

    available: bool
    quality: EvidenceQualityBand
    quality_label: str
    quantity: EvidenceQuantityBand
    quantity_label: str
    evidence_count: int
    message: str

    def __post_init__(self) -> None:
        if not isinstance(self.quality, EvidenceQualityBand):
            raise ReadinessInvariantViolation(
                "quality must be an EvidenceQualityBand",
                invariant="EvidenceQualityCard.quality.type",
            )
        if not isinstance(self.quantity, EvidenceQuantityBand):
            raise ReadinessInvariantViolation(
                "quantity must be an EvidenceQuantityBand",
                invariant="EvidenceQualityCard.quantity.type",
            )
        if isinstance(self.evidence_count, bool) or not isinstance(
            self.evidence_count, int
        ):
            raise ReadinessInvariantViolation(
                "evidence_count must be an integer",
                invariant="EvidenceQualityCard.evidence_count.type",
            )
        if self.evidence_count < 0:
            raise ReadinessInvariantViolation(
                "evidence_count must be >= 0",
                invariant="EvidenceQualityCard.evidence_count.range",
            )
        for name in ("quality_label", "quantity_label", "message"):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise ReadinessInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"EvidenceQualityCard.{name}.required",
                )
            object.__setattr__(self, name, value)
