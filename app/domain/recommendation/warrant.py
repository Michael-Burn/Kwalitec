"""Recommendation Confidence / warrant posture vocabulary.

Inherits Decision warrant honesty. Distinct from self-report Confidence,
Mastery, and Readiness overall. Not a selection score.
"""

from __future__ import annotations

from enum import StrEnum

from app.domain.decision.decision import DecisionWarrantPosture


class RecommendationConfidencePosture(StrEnum):
    """Evidence-density honesty of the packaged suggestion.

    Low / cold_start / not_yet_knowable remain first-class. Never coerce into
    Mid or High preparedness theatre under thin warrant.
    """

    HONEST_LOW = "honest_low"
    COLD_START = "cold_start"
    NOT_YET_KNOWABLE = "not_yet_knowable"
    HONEST_MEDIUM = "honest_medium"
    HONEST_HIGH = "honest_high"


# Mapping Decision warrant → Recommendation Confidence honesty.
_WARRANT_TO_CONFIDENCE: dict[
    DecisionWarrantPosture, RecommendationConfidencePosture
] = {
    DecisionWarrantPosture.COLD_START: RecommendationConfidencePosture.COLD_START,
    DecisionWarrantPosture.NOT_YET_KNOWABLE: (
        RecommendationConfidencePosture.NOT_YET_KNOWABLE
    ),
    DecisionWarrantPosture.INHERITED_LOW: RecommendationConfidencePosture.HONEST_LOW,
    DecisionWarrantPosture.INHERITED_MEDIUM: (
        RecommendationConfidencePosture.HONEST_MEDIUM
    ),
    DecisionWarrantPosture.INHERITED_HIGH: RecommendationConfidencePosture.HONEST_HIGH,
}


# Postures that must never be narrated as Mid/High preparedness.
THIN_WARRANT_CONFIDENCE_POSTURES: frozenset[RecommendationConfidencePosture] = (
    frozenset(
        {
            RecommendationConfidencePosture.HONEST_LOW,
            RecommendationConfidencePosture.COLD_START,
            RecommendationConfidencePosture.NOT_YET_KNOWABLE,
        }
    )
)


def inherit_confidence_posture(
    warrant: DecisionWarrantPosture | str,
) -> RecommendationConfidencePosture:
    """Propagate Decision warrant honesty into Recommendation Confidence.

    Args:
        warrant: Decision warrant posture (inherited from readiness).

    Returns:
        Matching Recommendation Confidence honesty posture.
    """
    posture = (
        warrant
        if isinstance(warrant, DecisionWarrantPosture)
        else DecisionWarrantPosture(warrant)
    )
    return _WARRANT_TO_CONFIDENCE[posture]
