"""Objective topic complexity and observed learner difficulty (KWP-009).

Differentiates authored / curriculum complexity from how demanding the
topic has been for *this* learner. Deterministic — no AI.
"""

from __future__ import annotations

from app.application.learning_difficulty.dto import (
    DifficultyEvidenceInput,
    ObjectiveComplexity,
    ObservedDifficulty,
    map_authored_difficulty,
)


def objective_complexity(
    evidence: DifficultyEvidenceInput,
) -> ObjectiveComplexity:
    """Derive objective topic complexity from authored signals or heuristics.

    Prefer authored / CKG difficulty when present. Otherwise estimate from
    learning-objective count and practice volume — never invent a band when
    evidence is empty.
    """
    authored = map_authored_difficulty(evidence.authored_difficulty)
    if authored is not ObjectiveComplexity.UNKNOWN:
        return authored

    lo_count = len(evidence.learning_objectives)
    attempted = evidence.practice_attempted
    if lo_count == 0 and attempted == 0 and not evidence.topic_title:
        return ObjectiveComplexity.UNKNOWN

    # Heuristic when authored difficulty is absent: denser objectives /
    # larger practice sets imply more demanding topics.
    if lo_count >= 4 or attempted >= 6:
        return ObjectiveComplexity.DEMANDING
    if lo_count >= 2 or attempted >= 3:
        return ObjectiveComplexity.MODERATE
    if lo_count >= 1 or attempted >= 1 or evidence.topic_title:
        return ObjectiveComplexity.LIGHT
    return ObjectiveComplexity.UNKNOWN


def observed_difficulty(
    evidence: DifficultyEvidenceInput,
) -> ObservedDifficulty:
    """How difficult this topic has been for the learner from outcomes."""
    correct = evidence.practice_correct
    incorrect = evidence.practice_incorrect
    attempted = evidence.practice_attempted
    reinforcement = evidence.reinforcement_session_count
    topic_attempts = evidence.topic_attempt_count

    if attempted == 0 and not evidence.weak_topic and reinforcement == 0:
        if evidence.abandoned or evidence.partial_completion:
            return ObservedDifficulty.MODERATE
        return ObservedDifficulty.UNKNOWN

    error_rate = (incorrect / attempted) if attempted > 0 else 0.0
    heavy_reinforcement = reinforcement >= 2 or topic_attempts >= 3
    recovering = evidence.recovered_after_misses or evidence.recovered_after_difficult

    if (
        error_rate >= 0.75
        or (incorrect >= 3 and correct == 0)
        or (evidence.weak_topic and incorrect >= 2 and heavy_reinforcement)
    ):
        band = ObservedDifficulty.VERY_DEMANDING
    elif (
        error_rate >= 0.5
        or incorrect >= 2
        or evidence.weak_topic
        or heavy_reinforcement
        or (evidence.partial_completion and incorrect > 0)
    ):
        band = ObservedDifficulty.DEMANDING
    elif error_rate > 0 or evidence.partial_completion or reinforcement == 1:
        band = ObservedDifficulty.MODERATE
    elif correct > 0 and incorrect == 0:
        band = ObservedDifficulty.LIGHT
    else:
        band = ObservedDifficulty.UNKNOWN

    # Recovery after misses softens very-demanding → demanding.
    if band is ObservedDifficulty.VERY_DEMANDING and recovering and correct > 0:
        return ObservedDifficulty.DEMANDING
    return band


def complexity_gap(
    objective: ObjectiveComplexity,
    observed: ObservedDifficulty,
) -> int:
    """Signed gap: positive when learner finds topic harder than objective.

    Used by rules to recommend different pacing when observed >> objective.
    """
    obj_rank = {
        ObjectiveComplexity.UNKNOWN: 1,
        ObjectiveComplexity.LIGHT: 0,
        ObjectiveComplexity.MODERATE: 1,
        ObjectiveComplexity.DEMANDING: 2,
        ObjectiveComplexity.INTENSIVE: 3,
    }
    obs_rank = {
        ObservedDifficulty.UNKNOWN: 1,
        ObservedDifficulty.LIGHT: 0,
        ObservedDifficulty.MODERATE: 1,
        ObservedDifficulty.DEMANDING: 2,
        ObservedDifficulty.VERY_DEMANDING: 3,
    }
    return obs_rank[observed] - obj_rank[objective]
