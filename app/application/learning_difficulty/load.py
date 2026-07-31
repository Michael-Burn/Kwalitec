"""Cognitive / educational load estimation (KWP-009).

Estimates educational load from repeated mistakes, reflection density,
session frequency, partial completion, recovery, study duration, and
repeated reinforcement. Never uses psychological labels.
"""

from __future__ import annotations

from app.application.learning_difficulty.complexity import (
    objective_complexity,
    observed_difficulty,
)
from app.application.learning_difficulty.dto import (
    DifficultyEvidenceInput,
    LearningEffort,
    ObservedDifficulty,
    RevisionPressure,
    SessionIntensity,
)


def estimate_load_points(evidence: DifficultyEvidenceInput) -> int:
    """Deterministic 0–100 educational load points from sitting evidence."""
    points = 0
    incorrect = evidence.practice_incorrect
    correct = evidence.practice_correct
    attempted = evidence.practice_attempted

    # Repeated mistakes
    if incorrect >= 3:
        points += 28
    elif incorrect == 2:
        points += 18
    elif incorrect == 1:
        points += 8

    if attempted > 0 and incorrect > correct:
        points += 10

    # Reflection density — reflection present with weak practice signals load
    if evidence.has_reflection or evidence.reflection_count > 0:
        if incorrect > 0 or evidence.weak_topic:
            points += 8
        elif evidence.reflection_count >= 2:
            points += 6

    # Session frequency
    recent = evidence.recent_session_count
    if recent is not None:
        if recent >= 5:
            points += 14
        elif recent >= 3:
            points += 8

    # Partial completion / abandoned
    if evidence.partial_completion or evidence.finish_verdict == "partially":
        points += 12
    if evidence.abandoned:
        points += 16
    if evidence.consecutive_partial_finishes >= 2:
        points += 10

    # Study duration
    duration = evidence.session_duration_minutes
    if duration is not None:
        if duration >= 75:
            points += 18
        elif duration >= 50:
            points += 10
        elif duration >= 35:
            points += 4

    # Repeated reinforcement
    reinforcement = evidence.reinforcement_session_count
    if reinforcement >= 3:
        points += 20
    elif reinforcement == 2:
        points += 12
    elif reinforcement == 1:
        points += 6

    if evidence.topic_attempt_count >= 4:
        points += 8

    # Retention / weak topic
    if evidence.retention_risk:
        points += 8
    if evidence.weak_topic:
        points += 10

    # Recovery reduces load slightly (learner is absorbing the demand)
    if evidence.recovered_after_misses or evidence.recovered_after_difficult:
        points = max(0, points - 8)

    # Strong clean sitting
    if correct > 0 and incorrect == 0 and not evidence.partial_completion:
        points = max(0, points - 6)

    return max(0, min(100, points))


def learning_effort_for(
    evidence: DifficultyEvidenceInput,
    *,
    load_points: int | None = None,
) -> LearningEffort:
    """Map load + observed difficulty into LearningEffort."""
    points = estimate_load_points(evidence) if load_points is None else load_points
    observed = observed_difficulty(evidence)

    if points >= 70 or observed is ObservedDifficulty.VERY_DEMANDING:
        return LearningEffort.VERY_HIGH
    if points >= 45 or observed is ObservedDifficulty.DEMANDING:
        return LearningEffort.HIGH
    if points >= 20 or observed is ObservedDifficulty.MODERATE:
        return LearningEffort.STEADY
    if points > 0 or observed is ObservedDifficulty.LIGHT:
        return LearningEffort.LOW
    return LearningEffort.LOW


def session_intensity_for(
    evidence: DifficultyEvidenceInput,
    *,
    load_points: int | None = None,
) -> SessionIntensity:
    """Estimate session intensity from duration + load + cadence."""
    points = estimate_load_points(evidence) if load_points is None else load_points
    duration = evidence.session_duration_minutes
    recent = evidence.recent_session_count

    if points >= 70 or (duration is not None and duration >= 75 and points >= 40):
        return SessionIntensity.OVERLOADED
    if (
        points >= 45
        or (duration is not None and duration >= 50)
        or (recent is not None and recent >= 5 and points >= 30)
    ):
        return SessionIntensity.HEAVY
    if points >= 20 or (duration is not None and duration >= 25):
        return SessionIntensity.STANDARD
    return SessionIntensity.LIGHT


def revision_pressure_for(
    evidence: DifficultyEvidenceInput,
    *,
    load_points: int | None = None,
) -> RevisionPressure:
    """Pressure to reinforce / revise rather than advance."""
    points = estimate_load_points(evidence) if load_points is None else load_points
    observed = observed_difficulty(evidence)
    incorrect = evidence.practice_incorrect
    reinforcement = evidence.reinforcement_session_count

    if (
        observed is ObservedDifficulty.VERY_DEMANDING
        or (evidence.retention_risk and incorrect > 0)
        or (reinforcement >= 3 and incorrect > 0)
    ):
        return RevisionPressure.URGENT
    if (
        observed is ObservedDifficulty.DEMANDING
        or incorrect >= 2
        or reinforcement >= 2
        or points >= 50
    ):
        return RevisionPressure.ELEVATED
    if incorrect > 0 or reinforcement == 1 or evidence.partial_completion:
        return RevisionPressure.LIGHT
    return RevisionPressure.NONE


def profile_signals(evidence: DifficultyEvidenceInput) -> tuple[str, ...]:
    """Evidence codes explaining the load estimate (founder / audit)."""
    codes: list[str] = []
    if evidence.practice_incorrect >= 2:
        codes.append("repeated_mistakes")
    elif evidence.practice_incorrect == 1:
        codes.append("practice_miss")
    if evidence.has_reflection or evidence.reflection_count > 0:
        codes.append("reflection_present")
    if evidence.recent_session_count is not None and evidence.recent_session_count >= 3:
        codes.append("high_session_frequency")
    if evidence.partial_completion or evidence.finish_verdict == "partially":
        codes.append("partial_completion")
    if evidence.abandoned:
        codes.append("abandoned")
    if evidence.recovered_after_misses or evidence.recovered_after_difficult:
        codes.append("recovery")
    if evidence.session_duration_minutes is not None and (
        evidence.session_duration_minutes >= 50
    ):
        codes.append("long_duration")
    if evidence.reinforcement_session_count >= 1:
        codes.append("repeated_reinforcement")
    if evidence.weak_topic:
        codes.append("weak_topic")
    if evidence.retention_risk:
        codes.append("retention_risk")
    obj = objective_complexity(evidence)
    observed = observed_difficulty(evidence)
    codes.append(f"objective_{obj.value}")
    codes.append(f"observed_{observed.value}")
    return tuple(codes)
