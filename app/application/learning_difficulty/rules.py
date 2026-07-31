"""Educational pacing and load recommendation rules (KWP-009).

Priority-ordered deterministic rules. Same inputs → same recommendation.
Does not redesign Learning Strategy or Diagnostics — composes load posture.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.learning_difficulty.complexity import (
    complexity_gap,
    objective_complexity,
    observed_difficulty,
)
from app.application.learning_difficulty.dto import (
    DifficultyEvidenceInput,
    EducationalPacing,
    LearningEffort,
    LoadRecommendation,
    ObjectiveComplexity,
    ObservedDifficulty,
    RevisionPressure,
    SessionIntensity,
)
from app.application.learning_difficulty.load import (
    estimate_load_points,
    learning_effort_for,
    profile_signals,
    revision_pressure_for,
    session_intensity_for,
)


@dataclass(frozen=True)
class DifficultyDecision:
    """Internal decision before guidance packaging."""

    recommendation: LoadRecommendation
    rule_id: str
    objective_complexity: ObjectiveComplexity
    observed_difficulty: ObservedDifficulty
    learning_effort: LearningEffort
    educational_pacing: EducationalPacing
    session_intensity: SessionIntensity
    revision_pressure: RevisionPressure
    load_points: int
    evidence_codes: tuple[str, ...]


def select_load_recommendation(
    evidence: DifficultyEvidenceInput,
) -> DifficultyDecision:
    """Return a deterministic load / pacing recommendation."""
    objective = objective_complexity(evidence)
    observed = observed_difficulty(evidence)
    points = estimate_load_points(evidence)
    effort = learning_effort_for(evidence, load_points=points)
    intensity = session_intensity_for(evidence, load_points=points)
    pressure = revision_pressure_for(evidence, load_points=points)
    gap = complexity_gap(objective, observed)
    codes = profile_signals(evidence)

    # 1. Topic needs splitting — very demanding + heavy reinforcement
    # (more specific than generic session-length reduction)
    if (
        observed is ObservedDifficulty.VERY_DEMANDING
        and (
            evidence.reinforcement_session_count >= 2
            or evidence.topic_attempt_count >= 3
        )
        and evidence.practice_incorrect >= 2
    ):
        return DifficultyDecision(
            recommendation=LoadRecommendation.SPLIT_TOPIC,
            rule_id="split_very_demanding",
            objective_complexity=objective,
            observed_difficulty=observed,
            learning_effort=effort,
            educational_pacing=EducationalPacing.HOLD,
            session_intensity=intensity,
            revision_pressure=pressure,
            load_points=points,
            evidence_codes=codes + ("split_candidate",),
        )

    # 2. Overloaded sitting → reduce session length
    if intensity is SessionIntensity.OVERLOADED or (
        evidence.session_duration_minutes is not None
        and evidence.session_duration_minutes >= 75
        and points >= 45
    ):
        return DifficultyDecision(
            recommendation=LoadRecommendation.REDUCE_SESSION_LENGTH,
            rule_id="overloaded_reduce_length",
            objective_complexity=objective,
            observed_difficulty=observed,
            learning_effort=effort,
            educational_pacing=EducationalPacing.SLOW,
            session_intensity=intensity,
            revision_pressure=pressure,
            load_points=points,
            evidence_codes=codes + ("overloaded",),
        )

    # 3. Consolidation when observed >> objective or elevated revision pressure
    if (
        gap >= 2
        or pressure is RevisionPressure.URGENT
        or (
            observed
            in {
                ObservedDifficulty.DEMANDING,
                ObservedDifficulty.VERY_DEMANDING,
            }
            and evidence.practice_incorrect >= 2
        )
    ):
        return DifficultyDecision(
            recommendation=LoadRecommendation.TAKE_CONSOLIDATION_SESSION,
            rule_id="consolidation_high_load",
            objective_complexity=objective,
            observed_difficulty=observed,
            learning_effort=effort,
            educational_pacing=EducationalPacing.SLOW,
            session_intensity=intensity,
            revision_pressure=pressure,
            load_points=points,
            evidence_codes=codes + ("gap_or_pressure",),
        )

    # 4. Decrease spacing — closer returns (elevated pressure / retention)
    if pressure in {RevisionPressure.ELEVATED, RevisionPressure.LIGHT} and (
        observed is ObservedDifficulty.DEMANDING
        or evidence.retention_risk
        or evidence.practice_incorrect >= 1
    ):
        return DifficultyDecision(
            recommendation=LoadRecommendation.DECREASE_SPACING,
            rule_id="decrease_spacing_elevated",
            objective_complexity=objective,
            observed_difficulty=observed,
            learning_effort=effort,
            educational_pacing=EducationalPacing.SLOW,
            session_intensity=intensity,
            revision_pressure=pressure,
            load_points=points,
            evidence_codes=codes + ("closer_returns",),
        )

    # 5. Heavy intensity without crash → reduce length
    if intensity is SessionIntensity.HEAVY and effort in {
        LearningEffort.HIGH,
        LearningEffort.VERY_HIGH,
    }:
        return DifficultyDecision(
            recommendation=LoadRecommendation.REDUCE_SESSION_LENGTH,
            rule_id="heavy_intensity_shorten",
            objective_complexity=objective,
            observed_difficulty=observed,
            learning_effort=effort,
            educational_pacing=EducationalPacing.SLOW,
            session_intensity=intensity,
            revision_pressure=pressure,
            load_points=points,
            evidence_codes=codes + ("heavy_shorten",),
        )

    # 6. Increase challenge — light observed + strong outcomes
    if (
        observed is ObservedDifficulty.LIGHT
        and evidence.practice_correct > 0
        and evidence.practice_incorrect == 0
        and (
            evidence.progress_advanced
            or evidence.consecutive_strong_sittings >= 2
            or evidence.finish_verdict == "yes"
        )
        and gap <= 0
    ):
        return DifficultyDecision(
            recommendation=LoadRecommendation.INCREASE_CHALLENGE,
            rule_id="increase_challenge_stable",
            objective_complexity=objective,
            observed_difficulty=observed,
            learning_effort=effort,
            educational_pacing=EducationalPacing.ACCELERATE,
            session_intensity=intensity,
            revision_pressure=pressure,
            load_points=points,
            evidence_codes=codes + ("ready_for_harder",),
        )

    # 7. Increase spacing — stable light topic, no revision pressure
    if (
        observed is ObservedDifficulty.LIGHT
        and pressure is RevisionPressure.NONE
        and evidence.practice_incorrect == 0
        and evidence.practice_correct > 0
        and not evidence.retention_risk
    ):
        return DifficultyDecision(
            recommendation=LoadRecommendation.INCREASE_SPACING,
            rule_id="increase_spacing_stable",
            objective_complexity=objective,
            observed_difficulty=observed,
            learning_effort=effort,
            educational_pacing=EducationalPacing.MAINTAIN,
            session_intensity=intensity,
            revision_pressure=pressure,
            load_points=points,
            evidence_codes=codes + ("widen_spacing",),
        )

    # 8. Continue — recovery / improving after earlier difficulty
    if evidence.recovered_after_difficult or (
        evidence.recovered_after_misses and evidence.practice_correct > 0
    ):
        return DifficultyDecision(
            recommendation=LoadRecommendation.CONTINUE,
            rule_id="continue_after_recovery",
            objective_complexity=objective,
            observed_difficulty=observed,
            learning_effort=effort,
            educational_pacing=EducationalPacing.MAINTAIN,
            session_intensity=intensity,
            revision_pressure=pressure,
            load_points=points,
            evidence_codes=codes + ("recovering",),
        )

    # 9. Maintain pace — default steady path
    if observed in {
        ObservedDifficulty.LIGHT,
        ObservedDifficulty.MODERATE,
        ObservedDifficulty.UNKNOWN,
    }:
        return DifficultyDecision(
            recommendation=LoadRecommendation.MAINTAIN_PACE,
            rule_id="maintain_pace_default",
            objective_complexity=objective,
            observed_difficulty=observed,
            learning_effort=effort,
            educational_pacing=EducationalPacing.MAINTAIN,
            session_intensity=intensity,
            revision_pressure=pressure,
            load_points=points,
            evidence_codes=codes + ("steady",),
        )

    # 10. Fallback continue
    return DifficultyDecision(
        recommendation=LoadRecommendation.CONTINUE,
        rule_id="continue_fallback",
        objective_complexity=objective,
        observed_difficulty=observed,
        learning_effort=effort,
        educational_pacing=EducationalPacing.MAINTAIN,
        session_intensity=intensity,
        revision_pressure=pressure,
        load_points=points,
        evidence_codes=codes + ("fallback",),
    )
