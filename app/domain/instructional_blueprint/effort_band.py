"""Relative instructional effort band for blueprint planning.

Effort is not wall-clock time alone and never encodes mastery or pass
probability. Bands inform structural sequencing only.
"""

from __future__ import annotations

from enum import StrEnum


class EffortBand(StrEnum):
    """Relative instructional effort band (structure only)."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTENSIVE = "extensive"


_EFFORT_RANK: dict[EffortBand, int] = {
    EffortBand.LOW: 1,
    EffortBand.MEDIUM: 2,
    EffortBand.HIGH: 3,
    EffortBand.EXTENSIVE: 4,
}

# Deterministic relative effort units by band (not minutes of study content).
_EFFORT_UNITS: dict[EffortBand, int] = {
    EffortBand.LOW: 2,
    EffortBand.MEDIUM: 4,
    EffortBand.HIGH: 6,
    EffortBand.EXTENSIVE: 9,
}


def effort_rank(band: EffortBand) -> int:
    """Return a stable ordinal for comparison (1=LOW … 4=EXTENSIVE)."""
    return _EFFORT_RANK[band]


def effort_units_for(band: EffortBand) -> int:
    """Return deterministic relative effort units for a band."""
    return _EFFORT_UNITS[band]


def effort_at_least(left: EffortBand, right: EffortBand) -> bool:
    """True when ``left`` is at least as demanding as ``right``."""
    return effort_rank(left) >= effort_rank(right)


def resolve_effort_band(value: EffortBand | str) -> EffortBand:
    """Resolve an effort token to an ``EffortBand``."""
    if isinstance(value, EffortBand):
        return value
    token = (value or "").strip().lower().replace("-", "_").replace(" ", "_")
    if not token:
        return EffortBand.MEDIUM
    try:
        return EffortBand(token)
    except ValueError:
        upper = token.upper()
        if upper in EffortBand.__members__:
            return EffortBand[upper]
        return EffortBand.MEDIUM
