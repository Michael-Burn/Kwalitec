"""DurationRules — deterministic duration and workload estimation."""

from __future__ import annotations

from application.education.mission_generation.enums import (
    LearningPace,
    MissionRecurrenceBand,
    MissionType,
)
from application.education.mission_generation.models.mission_estimate import (
    MissionEstimate,
)

# Fixed base minutes per mission type (deterministic catalogue).
_BASE_MINUTES: dict[MissionType, int] = {
    MissionType.PRACTICE_QUESTIONS: 20,
    MissionType.REVIEW_CONCEPT: 15,
    MissionType.STRENGTHEN_FOUNDATION: 25,
    MissionType.REVISE_PREREQUISITE: 20,
    MissionType.CONSOLIDATE_KNOWLEDGE: 18,
    MissionType.CHECKPOINT_PREPARATION: 30,
    MissionType.REVISION_SESSION: 15,
    MissionType.MIXED_PRACTICE: 25,
    MissionType.CONFIDENCE_RECOVERY: 15,
    MissionType.MAINTENANCE_REVIEW: 10,
}

_PACE_MULTIPLIER: dict[LearningPace, float] = {
    LearningPace.SLOW: 1.25,
    LearningPace.NORMAL: 1.0,
    LearningPace.FAST: 0.80,
}

# Increase/reduce revision frequency adjusts recurrence, not mission size.
# INCREASED keeps size slightly leaner; REDUCED preserves coverage (size).
_RECURRENCE_SIZE_MULTIPLIER: dict[MissionRecurrenceBand, float] = {
    MissionRecurrenceBand.INCREASED: 0.85,
    MissionRecurrenceBand.NORMAL: 1.0,
    MissionRecurrenceBand.REDUCED: 1.0,
}

_RECURRENCE_SESSIONS_PER_WEEK: dict[MissionRecurrenceBand, int] = {
    MissionRecurrenceBand.INCREASED: 4,
    MissionRecurrenceBand.NORMAL: 2,
    MissionRecurrenceBand.REDUCED: 1,
}


class DurationRules:
    """Deterministically estimates mission duration from type and pace."""

    @staticmethod
    def base_minutes(mission_type: MissionType) -> int:
        return _BASE_MINUTES[mission_type]

    @staticmethod
    def sessions_per_week(recurrence: MissionRecurrenceBand) -> int:
        return _RECURRENCE_SESSIONS_PER_WEEK[recurrence]

    @staticmethod
    def estimate(
        mission_type: MissionType,
        *,
        learning_pace: LearningPace = LearningPace.NORMAL,
        recurrence: MissionRecurrenceBand = MissionRecurrenceBand.NORMAL,
        coverage_weight: float = 1.0,
        source_count: int = 1,
    ) -> MissionEstimate:
        """Estimate duration for one mission.

        IncreaseRevisionFrequency increases recurrence (sessions/week) and
        slightly reduces size. ReduceRevisionFrequency / MaintainMastery
        decrease recurrence while preserving coverage size.
        """
        base = float(DurationRules.base_minutes(mission_type))
        pace = _PACE_MULTIPLIER.get(learning_pace, 1.0)
        recurrence_factor = _RECURRENCE_SIZE_MULTIPLIER.get(recurrence, 1.0)
        # Merged sources add bounded incremental load, not linear growth.
        merge_factor = 1.0 + 0.15 * max(0, source_count - 1)
        coverage = max(0.1, min(1.0, coverage_weight))
        minutes = int(round(base * pace * recurrence_factor * merge_factor * coverage))
        minutes = max(5, minutes)
        workload = round(
            (minutes / 30.0)
            * DurationRules.sessions_per_week(recurrence)
            / 2.0,
            4,
        )
        return MissionEstimate(
            duration_minutes=minutes,
            workload_units=max(0.1, workload),
        )
