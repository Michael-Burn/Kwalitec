"""Learner confidence inference — reproducible from observations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum


class ConfidenceBand(StrEnum):
    """Qualitative confidence band for Twin diagnostics."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    VERY_LOW = "very_low"
    UNKNOWN = "unknown"


def confidence_band_from_score(score: float) -> ConfidenceBand:
    value = max(0.0, min(1.0, float(score)))
    if value >= 0.85:
        return ConfidenceBand.HIGH
    if value >= 0.65:
        return ConfidenceBand.MEDIUM
    if value >= 0.45:
        return ConfidenceBand.LOW
    if value > 0.0:
        return ConfidenceBand.VERY_LOW
    return ConfidenceBand.UNKNOWN


@dataclass(frozen=True)
class ConfidenceState:
    """Aggregate confidence across recent educational outcomes."""

    score: float = 0.0
    band: ConfidenceBand = ConfidenceBand.UNKNOWN
    evidence_count: int = 0
    reason: str = ""
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        score = _clamp(self.score)
        object.__setattr__(self, "score", score)
        band = (
            self.band
            if isinstance(self.band, ConfidenceBand)
            else ConfidenceBand(str(self.band))
        )
        if band is ConfidenceBand.UNKNOWN and score > 0:
            band = confidence_band_from_score(score)
        object.__setattr__(self, "band", band)
        when = self.updated_at
        if when is not None and when.tzinfo is not None:
            object.__setattr__(
                self, "updated_at", when.astimezone(UTC).replace(tzinfo=None)
            )

    @classmethod
    def empty(cls) -> ConfidenceState:
        return cls()


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))
