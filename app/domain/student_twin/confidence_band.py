"""Explicit confidence bands — uncertainty must never be hidden."""

from __future__ import annotations

from enum import StrEnum


class ConfidenceBand(StrEnum):
    """Discrete confidence band for Twin conclusions."""

    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


# Inclusive lower bounds for numeric confidence in [0, 1].
_BAND_THRESHOLDS: tuple[tuple[float, ConfidenceBand], ...] = (
    (0.85, ConfidenceBand.VERY_HIGH),
    (0.65, ConfidenceBand.HIGH),
    (0.40, ConfidenceBand.MEDIUM),
    (0.20, ConfidenceBand.LOW),
    (0.0, ConfidenceBand.VERY_LOW),
)

_BAND_MIDPOINTS: dict[ConfidenceBand, float] = {
    ConfidenceBand.VERY_LOW: 0.10,
    ConfidenceBand.LOW: 0.30,
    ConfidenceBand.MEDIUM: 0.525,
    ConfidenceBand.HIGH: 0.75,
    ConfidenceBand.VERY_HIGH: 0.925,
}


def confidence_band_from_score(score: float) -> ConfidenceBand:
    """Map a numeric confidence in [0, 1] to an explicit band."""
    value = _clamp01(score)
    for threshold, band in _BAND_THRESHOLDS:
        if value >= threshold:
            return band
    return ConfidenceBand.VERY_LOW


def confidence_score_from_band(band: ConfidenceBand | str) -> float:
    """Return the deterministic midpoint score for a band."""
    resolved = resolve_confidence_band(band)
    return _BAND_MIDPOINTS[resolved]


def resolve_confidence_band(value: ConfidenceBand | str) -> ConfidenceBand:
    """Resolve a string or enum to ConfidenceBand."""
    if isinstance(value, ConfidenceBand):
        return value
    token = (value or "").strip().lower()
    try:
        return ConfidenceBand(token)
    except ValueError as exc:
        raise ValueError(f"unknown confidence band: {value!r}") from exc


def _clamp01(value: float) -> float:
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return float(value)
