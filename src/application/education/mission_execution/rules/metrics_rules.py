"""Deterministic metrics computation for MissionExecution."""

from __future__ import annotations

from datetime import datetime

from application.education.mission_execution.enums import ConfidenceTrend
from application.education.mission_execution.models.confidence_record import (
    ConfidenceRecord,
)
from application.education.mission_execution.models.execution_metrics import (
    ExecutionMetrics,
)
from application.education.mission_execution.models.reflection_record import (
    ReflectionRecord,
)
from application.education.mission_generation.ids import MissionStepId
from application.education.mission_generation.models.mission import Mission
from domain.education.foundation.enums import ConfidenceLevel

_LEVEL_ORDER: dict[ConfidenceLevel, int] = {
    ConfidenceLevel.VERY_LOW: 1,
    ConfidenceLevel.LOW: 2,
    ConfidenceLevel.MEDIUM: 3,
    ConfidenceLevel.HIGH: 4,
    ConfidenceLevel.VERY_HIGH: 5,
}


class MetricsRules:
    """Pure functions producing ExecutionMetrics from execution state."""

    @staticmethod
    def build_metrics(
        *,
        mission: Mission,
        completed_step_ids: tuple[MissionStepId, ...],
        skipped_step_ids: tuple[MissionStepId, ...],
        elapsed_study_time_seconds: float,
        paused_duration_seconds: float,
        started_at: datetime | None,
        finished_at: datetime | None,
        confidence_history: tuple[ConfidenceRecord, ...],
        reflection_history: tuple[ReflectionRecord, ...],
    ) -> ExecutionMetrics:
        total = len(mission.steps)
        completed = len(completed_step_ids)
        skipped = len(skipped_step_ids)
        completion_percentage = (
            100.0 if total == 0 else round(100.0 * completed / total, 4)
        )
        step_completion_rate = (
            1.0 if total == 0 else round(completed / total, 4)
        )
        if started_at is None:
            mission_duration = 0.0
        elif finished_at is not None:
            mission_duration = max(
                0.0, (finished_at - started_at).total_seconds()
            )
        else:
            mission_duration = max(
                0.0,
                float(elapsed_study_time_seconds)
                + float(paused_duration_seconds),
            )
        return ExecutionMetrics(
            elapsed_study_time_seconds=float(elapsed_study_time_seconds),
            paused_duration_seconds=float(paused_duration_seconds),
            mission_duration_seconds=mission_duration,
            completion_percentage=completion_percentage,
            step_completion_rate=step_completion_rate,
            skipped_steps=skipped,
            reflection_count=len(reflection_history),
            confidence_count=len(confidence_history),
            confidence_trend=MetricsRules.confidence_trend(confidence_history),
        )

    @staticmethod
    def confidence_trend(
        history: tuple[ConfidenceRecord, ...],
    ) -> ConfidenceTrend:
        if not history:
            return ConfidenceTrend.NONE
        if len(history) == 1:
            return ConfidenceTrend.STABLE
        ranks = [_LEVEL_ORDER[record.level] for record in history]
        deltas = [ranks[i + 1] - ranks[i] for i in range(len(ranks) - 1)]
        rising = any(d > 0 for d in deltas)
        falling = any(d < 0 for d in deltas)
        if rising and falling:
            return ConfidenceTrend.MIXED
        if rising:
            return ConfidenceTrend.RISING
        if falling:
            return ConfidenceTrend.FALLING
        return ConfidenceTrend.STABLE

    @staticmethod
    def elapsed_delta_seconds(
        *,
        last_active_at: datetime | None,
        at: datetime,
    ) -> float:
        if last_active_at is None:
            return 0.0
        return max(0.0, (at - last_active_at).total_seconds())
