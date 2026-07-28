"""Observation categories — educational meaning without inference.

These categories describe what was observed in assessment evidence.
They are not mastery conclusions, risk labels, or recommendations.
"""

from __future__ import annotations

from enum import StrEnum


class ObservationCategory(StrEnum):
    """Canonical educational observation categories (AP-002D Design Pack)."""

    OBSERVED_CORRECTNESS = "observed_correctness"
    OBSERVED_CONFIDENCE = "observed_confidence"
    OBSERVED_MISCONCEPTION_INDICATORS = "observed_misconception_indicators"
    OBSERVED_RESPONSE_PERSISTENCE = "observed_response_persistence"
    OBSERVED_HINT_DEPENDENCY = "observed_hint_dependency"
    OBSERVED_TIMING_PROFILE = "observed_timing_profile"
    OBSERVED_COVERAGE = "observed_coverage"
    OBSERVED_CONSISTENCY = "observed_consistency"


KNOWN_OBSERVATION_CATEGORIES: frozenset[str] = frozenset(
    category.value for category in ObservationCategory
)


def parse_observation_category(value: str | ObservationCategory) -> ObservationCategory:
    """Parse a category or raise for unknown values (never invent)."""
    if isinstance(value, ObservationCategory):
        return value
    normalised = (value or "").strip()
    if normalised not in KNOWN_OBSERVATION_CATEGORIES:
        from app.domain.reasoning.interpretation.errors import (
            UnknownObservationCategory,
        )

        raise UnknownObservationCategory(
            f"unknown observation category: {value!r}"
        )
    return ObservationCategory(normalised)
