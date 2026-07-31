"""Classify readiness forecast labels from trajectory (KWP-012)."""

from __future__ import annotations

from app.application.readiness_forecast.dto import (
    TARGET_READINESS_RATIO,
    ForecastLabel,
    ForecastSignals,
    StudyTrajectory,
    TrendDirection,
)
from app.application.readiness_forecast.projection import reaches_target_by_exam


def classify_forecast(
    signals: ForecastSignals,
    trajectory: StudyTrajectory,
) -> tuple[ForecastLabel, str]:
    """Return (label, rule_id) — deterministic, evidence-gated."""
    if signals.sitting_count < 2:
        return ForecastLabel.INSUFFICIENT_EVIDENCE, "RF-01-thin-history"

    if (
        signals.recovery_pressure >= 0.45
        or (
            signals.retention_risk_rate >= 0.4
            and trajectory.current_trend
            in {TrendDirection.DECLINING, TrendDirection.RECOVERING}
        )
    ) and signals.recent_strong_ratio < 0.55:
        return ForecastLabel.RECOVERY_REQUIRED, "RF-02-recovery-required"

    if signals.consistency_score < 0.35 or (
        signals.sittings_per_week < 1.0 and signals.sitting_count >= 3
    ):
        return (
            ForecastLabel.NEEDS_GREATER_CONSISTENCY,
            "RF-03-needs-consistency",
        )

    on_target = reaches_target_by_exam(trajectory)
    projected = trajectory.projected_readiness_ratio
    current = signals.current_readiness_ratio

    if (
        signals.days_to_exam is not None
        and projected is not None
        and current is not None
        and projected >= TARGET_READINESS_RATIO
        and current >= 0.55
        and signals.days_to_exam > 21
        and trajectory.current_trend
        in {TrendDirection.IMPROVING, TrendDirection.STABLE}
    ):
        # Comfortably clears Ready for Revision with time to spare.
        surplus_weeks = max(0.0, (projected - TARGET_READINESS_RATIO) / 0.04)
        if surplus_weeks >= 2.0 or (
            current >= TARGET_READINESS_RATIO and signals.consistency_score >= 0.55
        ):
            return ForecastLabel.AHEAD_OF_SCHEDULE, "RF-04-ahead"

    if on_target is False and signals.days_to_exam is not None:
        return ForecastLabel.BELOW_TARGET_PACE, "RF-05-below-pace"

    if on_target is True and trajectory.current_trend in {
        TrendDirection.IMPROVING,
        TrendDirection.STABLE,
        TrendDirection.RECOVERING,
    }:
        return ForecastLabel.ON_TRACK, "RF-06-on-track"

    if trajectory.current_trend == TrendDirection.IMPROVING or (
        signals.memory_improving and signals.recent_strong_ratio >= 0.4
    ):
        return ForecastLabel.BUILDING_MOMENTUM, "RF-07-building"

    if on_target is True:
        return ForecastLabel.ON_TRACK, "RF-06-on-track-stable"

    if signals.days_to_exam is None and projected is not None:
        if projected >= TARGET_READINESS_RATIO:
            return ForecastLabel.ON_TRACK, "RF-06-on-track-no-exam"
        if projected >= 0.55:
            return ForecastLabel.BUILDING_MOMENTUM, "RF-07-building-no-exam"
        return ForecastLabel.BELOW_TARGET_PACE, "RF-05-below-no-exam"

    return ForecastLabel.BUILDING_MOMENTUM, "RF-07-building-default"
