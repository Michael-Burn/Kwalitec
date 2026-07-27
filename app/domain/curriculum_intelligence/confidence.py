"""Confidence scoring contracts for Curriculum Intelligence (CIP-002).

Confidence is deterministic and explainable: score, reason, and factors.
Low-confidence entities remain usable but flagged for Founder review.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ConfidenceBand(StrEnum):
    """Qualitative band derived from numeric confidence."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    VERY_LOW = "very_low"


def confidence_band_from_score(score: float) -> ConfidenceBand:
    """Map 0.0–1.0 confidence into a Founder-facing band."""
    value = max(0.0, min(1.0, float(score)))
    if value >= 0.85:
        return ConfidenceBand.HIGH
    if value >= 0.65:
        return ConfidenceBand.MEDIUM
    if value >= 0.45:
        return ConfidenceBand.LOW
    return ConfidenceBand.VERY_LOW


@dataclass(frozen=True)
class ConfidenceFactor:
    """One named contribution to a confidence score."""

    code: str
    label: str
    weight: float
    contribution: float
    detail: str = ""


@dataclass(frozen=True)
class ConfidenceRecord:
    """Explainable confidence attached to an entity or relation."""

    confidence_id: str
    subject_kind: str
    subject_id: str
    score: float
    band: ConfidenceBand
    reason: str
    factors: tuple[ConfidenceFactor, ...]
    needs_review: bool
    review_threshold: float
    provenance_id: str | None = None
