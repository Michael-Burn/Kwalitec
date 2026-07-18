"""Intervention priority — deterministic educational urgency scores."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class PriorityBand(StrEnum):
    """Discrete priority bands for explainable ranking."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NEGLIGIBLE = "negligible"


# Inclusive lower bounds for numeric priority in [0, 1].
_BAND_THRESHOLDS: tuple[tuple[float, PriorityBand], ...] = (
    (0.85, PriorityBand.CRITICAL),
    (0.65, PriorityBand.HIGH),
    (0.40, PriorityBand.MEDIUM),
    (0.20, PriorityBand.LOW),
    (0.0, PriorityBand.NEGLIGIBLE),
)


@dataclass(frozen=True)
class InterventionPriority:
    """Deterministic priority score with an explicit band.

    Priority is never random. Identical inputs → identical priority.
    """

    score: float
    band: PriorityBand
    retention_risk: float = 0.0
    mastery_gap: float = 0.0
    prerequisite_criticality: float = 0.0
    curriculum_importance: float = 0.0
    historical_struggle: float = 0.0
    confidence_gap: float = 0.0
    velocity_factor: float = 0.0
    exam_proximity: float = 0.0

    @classmethod
    def create(
        cls,
        score: float,
        *,
        band: PriorityBand | str | None = None,
        retention_risk: float = 0.0,
        mastery_gap: float = 0.0,
        prerequisite_criticality: float = 0.0,
        curriculum_importance: float = 0.0,
        historical_struggle: float = 0.0,
        confidence_gap: float = 0.0,
        velocity_factor: float = 0.0,
        exam_proximity: float = 0.0,
    ) -> InterventionPriority:
        """Construct InterventionPriority with validated unit-interval fields."""
        numeric = _unit_interval(score, "score")
        resolved_band = (
            priority_band_from_score(numeric)
            if band is None
            else resolve_priority_band(band)
        )
        return cls(
            score=numeric,
            band=resolved_band,
            retention_risk=_unit_interval(retention_risk, "retention_risk"),
            mastery_gap=_unit_interval(mastery_gap, "mastery_gap"),
            prerequisite_criticality=_unit_interval(
                prerequisite_criticality, "prerequisite_criticality"
            ),
            curriculum_importance=_unit_interval(
                curriculum_importance, "curriculum_importance"
            ),
            historical_struggle=_unit_interval(
                historical_struggle, "historical_struggle"
            ),
            confidence_gap=_unit_interval(confidence_gap, "confidence_gap"),
            velocity_factor=_unit_interval(velocity_factor, "velocity_factor"),
            exam_proximity=_unit_interval(exam_proximity, "exam_proximity"),
        )

    @classmethod
    def negligible(cls) -> InterventionPriority:
        """Return a zero-priority placeholder."""
        return cls.create(0.0)


def priority_band_from_score(score: float) -> PriorityBand:
    """Map a numeric priority in [0, 1] to an explicit band."""
    value = _clamp01(score)
    for threshold, band in _BAND_THRESHOLDS:
        if value >= threshold:
            return band
    return PriorityBand.NEGLIGIBLE


def resolve_priority_band(value: PriorityBand | str) -> PriorityBand:
    """Resolve a string or enum to PriorityBand."""
    if isinstance(value, PriorityBand):
        return value
    token = (value or "").strip().lower()
    try:
        return PriorityBand(token)
    except ValueError as exc:
        raise ValueError(f"unknown priority band: {value!r}") from exc


def _clamp01(value: float) -> float:
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return float(value)


def _unit_interval(value: float, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"{field_name} must be a number in [0, 1]")
    numeric = float(value)
    if numeric < 0.0 or numeric > 1.0:
        raise ValueError(f"{field_name} must be in [0, 1]")
    return numeric
