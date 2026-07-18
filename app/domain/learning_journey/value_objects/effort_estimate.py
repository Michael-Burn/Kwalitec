"""Educational effort estimate for journey and session planning.

Effort is not time alone. Bands express relative educational load without
claiming mastery outcomes or pass probability.
"""

from __future__ import annotations

from enum import StrEnum


class EffortEstimate(StrEnum):
    """Relative educational effort band.

    Informs planning and capacity realism. Does not auto-complete journeys
    or sessions. Does not encode mastery.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTENSIVE = "extensive"


# Ordinal ranks for deterministic comparisons (not scoring weights).
_EFFORT_RANK: dict[EffortEstimate, int] = {
    EffortEstimate.LOW: 1,
    EffortEstimate.MEDIUM: 2,
    EffortEstimate.HIGH: 3,
    EffortEstimate.EXTENSIVE: 4,
}


def effort_rank(estimate: EffortEstimate) -> int:
    """Return a stable ordinal for comparison (1=LOW … 4=EXTENSIVE)."""
    return _EFFORT_RANK[estimate]


def effort_at_least(left: EffortEstimate, right: EffortEstimate) -> bool:
    """True when ``left`` is at least as demanding as ``right``."""
    return effort_rank(left) >= effort_rank(right)
