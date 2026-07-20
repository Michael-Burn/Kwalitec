"""Progress evaluation enumerations.

Vocabulary for deterministic ProgressReport projections. Trends, velocity,
revision effectiveness, and intervention urgency are educational progress
signals explained from evidence — not opaque scores or UI presentation.
"""

from __future__ import annotations

from enum import StrEnum


class TrendDirection(StrEnum):
    """Direction of an educational progress trend."""

    IMPROVING = "improving"
    STABLE = "stable"
    DECLINING = "declining"
    INSUFFICIENT_DATA = "insufficient_data"


class VelocityBand(StrEnum):
    """Qualitative band for LearningVelocity."""

    STALLED = "stalled"
    SLOW = "slow"
    MODERATE = "moderate"
    FAST = "fast"
    UNKNOWN = "unknown"


class StabilityBand(StrEnum):
    """Knowledge stability derived from retention memory and probes."""

    UNSTABLE = "unstable"
    FRAGILE = "fragile"
    STABLE = "stable"
    DURABLE = "durable"
    UNKNOWN = "unknown"


class RevisionEffectivenessBand(StrEnum):
    """How well scheduled revision is translating into retained knowledge."""

    INEFFECTIVE = "ineffective"
    MIXED = "mixed"
    EFFECTIVE = "effective"
    UNKNOWN = "unknown"
    INAPPLICABLE = "inapplicable"


class InterventionUrgency(StrEnum):
    """Urgency of an InterventionSignal derived from progress thresholds."""

    NONE = "none"
    ADVISORY = "advisory"
    ELEVATED = "elevated"
    CRITICAL = "critical"


class ProgressMetricCode(StrEnum):
    """Stable codes for ProgressMetric entries on a ProgressReport."""

    MASTERY_TREND = "mastery_trend"
    CONFIDENCE_TREND = "confidence_trend"
    LEARNING_VELOCITY = "learning_velocity"
    KNOWLEDGE_STABILITY = "knowledge_stability"
    REVISION_EFFECTIVENESS = "revision_effectiveness"
    CONFIDENCE_LEVEL = "confidence_level"
    INTERVENTION_REQUIRED = "intervention_required"
