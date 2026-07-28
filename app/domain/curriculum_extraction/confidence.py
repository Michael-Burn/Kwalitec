"""Extraction confidence scoring (Founder review only — never student-facing)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ConfidenceBand(StrEnum):
    """Founder-facing confidence bands."""

    HIGHLY_RELIABLE = "highly_reliable"
    REVIEW_RECOMMENDED = "review_recommended"
    MANUAL_CONFIRMATION = "manual_confirmation"


def confidence_band(score: int) -> ConfidenceBand:
    """Map a 0–100 confidence score to a Founder review band."""
    if not isinstance(score, int) or isinstance(score, bool):
        raise ValueError("confidence score must be an int")
    if score < 0 or score > 100:
        raise ValueError("confidence score must be in 0..100")
    if score >= 99:
        return ConfidenceBand.HIGHLY_RELIABLE
    if score >= 90:
        return ConfidenceBand.REVIEW_RECOMMENDED
    return ConfidenceBand.MANUAL_CONFIRMATION


@dataclass(frozen=True)
class ExtractionConfidence:
    """Integer confidence score with derived Founder band."""

    score: int

    def __post_init__(self) -> None:
        confidence_band(self.score)

    @classmethod
    def of(cls, score: int) -> ExtractionConfidence:
        return cls(score=score)

    @property
    def band(self) -> ConfidenceBand:
        return confidence_band(self.score)

    def requires_manual_confirmation(self) -> bool:
        return self.band is ConfidenceBand.MANUAL_CONFIRMATION
