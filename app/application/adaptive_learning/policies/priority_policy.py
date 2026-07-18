"""Stateless priority policy — deterministic revision urgency weights."""

from __future__ import annotations


class PriorityPolicy:
    """Educational priority weights for revision decisions.

    No randomness. Identical factor inputs → identical priority.
    """

    WEIGHT_RETENTION_RISK = 0.22
    WEIGHT_MASTERY_GAP = 0.18
    WEIGHT_PREREQUISITE = 0.14
    WEIGHT_CURRICULUM = 0.12
    WEIGHT_STRUGGLE = 0.12
    WEIGHT_CONFIDENCE_GAP = 0.08
    WEIGHT_VELOCITY = 0.06
    WEIGHT_EXAM = 0.08

    MIN_REVISION_PRIORITY = 0.20
    HIGH_PRIORITY_THRESHOLD = 0.65
    CRITICAL_PRIORITY_THRESHOLD = 0.85

    # Velocity: low recent progress elevates revision need slightly.
    LOW_VELOCITY_EVENTS_PER_DAY = 1.0
    HIGH_VELOCITY_EVENTS_PER_DAY = 6.0

    @classmethod
    def weights_sum(cls) -> float:
        """Return the sum of factor weights (must be 1.0)."""
        return round(
            cls.WEIGHT_RETENTION_RISK
            + cls.WEIGHT_MASTERY_GAP
            + cls.WEIGHT_PREREQUISITE
            + cls.WEIGHT_CURRICULUM
            + cls.WEIGHT_STRUGGLE
            + cls.WEIGHT_CONFIDENCE_GAP
            + cls.WEIGHT_VELOCITY
            + cls.WEIGHT_EXAM,
            6,
        )

    @staticmethod
    def velocity_factor(events_per_day: float, mastery_delta: float) -> float:
        """Map velocity signals to a [0, 1] revision-need factor.

        Low activity or declining mastery → higher factor.
        """
        epd = max(0.0, float(events_per_day))
        if epd <= PriorityPolicy.LOW_VELOCITY_EVENTS_PER_DAY:
            activity = 0.85
        elif epd >= PriorityPolicy.HIGH_VELOCITY_EVENTS_PER_DAY:
            activity = 0.25
        else:
            span = (
                PriorityPolicy.HIGH_VELOCITY_EVENTS_PER_DAY
                - PriorityPolicy.LOW_VELOCITY_EVENTS_PER_DAY
            )
            activity = 0.85 - 0.60 * (
                (epd - PriorityPolicy.LOW_VELOCITY_EVENTS_PER_DAY) / span
            )
        decline = max(0.0, -float(mastery_delta))
        return _clamp01(0.70 * activity + 0.30 * decline)

    @staticmethod
    def meets_revision_threshold(priority_score: float) -> bool:
        """True when priority is high enough to recommend revision."""
        return priority_score >= PriorityPolicy.MIN_REVISION_PRIORITY


def _clamp01(value: float) -> float:
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return float(value)
