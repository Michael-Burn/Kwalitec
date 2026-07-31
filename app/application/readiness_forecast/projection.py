"""Project study trajectory from forecast signals (KWP-012).

Pure projection — never writes Evidence, Progress, Memory, or Twin.
Reuses KWP-006 readiness stage vocabulary.
"""

from __future__ import annotations

from app.application.readiness_forecast.dto import (
    CONFIDENCE_TITLES,
    TARGET_READINESS_RATIO,
    TREND_TITLES,
    ForecastConfidence,
    ForecastSignals,
    StudyTrajectory,
    TrendDirection,
)

# Same thresholds as Exam Week Briefing (KWP-006) — single vocabulary, no
# presentation-layer import from application.
_READINESS_STAGES: tuple[tuple[float, str], ...] = (
    (0.20, "Building"),
    (0.40, "Developing"),
    (0.60, "Strengthening"),
    (0.80, "Ready for Revision"),
    (1.01, "Ready for Assessment"),
)


def readiness_stage_for_ratio(value: float | None) -> str:
    """Map a readiness ratio to calm stage language (KWP-006 vocabulary)."""
    if value is None:
        return "Building"
    ratio = float(value)
    if ratio > 1.0:
        ratio = ratio / 100.0
    ratio = max(0.0, min(ratio, 1.0))
    for threshold, label in _READINESS_STAGES:
        if ratio < threshold:
            return label
    return "Ready for Assessment"


def project_trajectory(signals: ForecastSignals) -> StudyTrajectory:
    """Project readiness trajectory and explain assumptions / factors."""
    confidence = _confidence(signals)
    trend = _trend(signals)
    current_ratio = signals.current_readiness_ratio
    current_stage = (
        readiness_stage_for_ratio(current_ratio)
        if current_ratio is not None
        else ""
    )

    projected = _project_ratio(signals, current_ratio=current_ratio)
    projected_stage = (
        readiness_stage_for_ratio(projected) if projected is not None else ""
    )

    assumptions = _assumptions(signals)
    factors = _influential_factors(signals, trend=trend)

    return StudyTrajectory(
        current_trend=trend,
        current_trend_title=TREND_TITLES[trend],
        current_readiness_stage=current_stage,
        projected_readiness_ratio=projected,
        projected_readiness_stage=projected_stage,
        days_to_exam=signals.days_to_exam,
        key_assumptions=assumptions,
        influential_factors=factors,
        confidence=confidence,
        confidence_title=CONFIDENCE_TITLES[confidence],
    )


def _confidence(signals: ForecastSignals) -> ForecastConfidence:
    n = signals.sitting_count
    if n < 2:
        return ForecastConfidence.LIMITED
    if n < 5 or signals.consistency_score < 0.35:
        return ForecastConfidence.EMERGING
    return ForecastConfidence.ESTABLISHED


def _trend(signals: ForecastSignals) -> TrendDirection:
    if signals.sitting_count < 2:
        return TrendDirection.UNKNOWN
    if signals.recovery_pressure >= 0.4 or (
        signals.retention_risk_rate >= 0.35
        and signals.recent_strong_ratio < signals.early_strong_ratio
    ):
        if signals.memory_recovery_success or signals.recent_strong_ratio > (
            signals.early_strong_ratio + 0.05
        ):
            return TrendDirection.RECOVERING
        return TrendDirection.DECLINING

    delta = signals.recent_strong_ratio - signals.early_strong_ratio
    if delta >= 0.15 or (
        signals.memory_improving and signals.recent_strong_ratio >= 0.5
    ):
        return TrendDirection.IMPROVING
    if delta <= -0.15:
        return TrendDirection.DECLINING
    if signals.recovery_pressure >= 0.25:
        return TrendDirection.RECOVERING
    return TrendDirection.STABLE


def _project_ratio(
    signals: ForecastSignals,
    *,
    current_ratio: float | None,
) -> float | None:
    if current_ratio is None:
        return None

    # Weekly readiness gain from current study pattern (clamped, honest).
    weekly_gain = (
        0.04 * signals.consistency_score
        + 0.03 * signals.recent_strong_ratio
        + 0.025 * signals.progress_advance_rate
        + 0.015 * signals.intervention_help_rate
        - 0.03 * signals.recovery_pressure
        - 0.02 * signals.confidence_mismatch_rate
        - 0.015 * max(0.0, 0.45 - signals.consistency_score)
    )
    if signals.memory_improving:
        weekly_gain += 0.01
    if signals.sittings_per_week < 1.0 and signals.sitting_count >= 2:
        weekly_gain *= 0.6
    weekly_gain = max(-0.04, min(0.08, weekly_gain))

    days = signals.days_to_exam
    if days is None:
        # Without an exam date, project ~4 weeks of continued pattern.
        weeks = 4.0
    else:
        weeks = max(0.0, days / 7.0)

    projected = current_ratio + weekly_gain * weeks
    return max(0.0, min(1.0, projected))


def _assumptions(signals: ForecastSignals) -> tuple[str, ...]:
    items: list[str] = [
        "Recent study pattern continues at a similar cadence.",
        "No major syllabus or exam-date change.",
    ]
    if signals.days_to_exam is not None:
        items.append(
            f"Projection horizon is the scheduled sitting "
            f"({signals.days_to_exam} day(s) remaining)."
        )
    else:
        items.append(
            "No exam date available — projection uses a short four-week horizon."
        )
    if signals.sitting_count < 5:
        items.append(
            "Evidence is still thin — treat this as directional, not certain."
        )
    return tuple(items[:5])


def _influential_factors(
    signals: ForecastSignals,
    *,
    trend: TrendDirection,
) -> tuple[str, ...]:
    scored: list[tuple[float, str]] = [
        (signals.consistency_score, "Study consistency"),
        (signals.recent_strong_ratio, "Recent sitting strength"),
        (signals.progress_advance_rate, "Coverage progress"),
        (signals.recovery_pressure, "Recovery pressure"),
        (signals.retention_risk_rate, "Retention risk"),
        (signals.intervention_help_rate, "Intervention effectiveness"),
        (signals.difficulty_demand_rate, "Difficulty demand"),
        (signals.confidence_mismatch_rate, "Confidence alignment"),
        (signals.reflection_rate, "Reflection"),
    ]
    if signals.memory_improving:
        scored.append((0.7, "Learning Memory growth patterns"))
    if signals.days_to_exam is not None:
        # Closer exams weigh calendar more.
        urgency = max(0.0, 1.0 - min(signals.days_to_exam, 90) / 90.0)
        scored.append((urgency, "Time to exam"))

    scored.sort(key=lambda item: item[0], reverse=True)
    factors = [label for _score, label in scored[:4]]
    if trend == TrendDirection.RECOVERING and "Recovery pressure" not in factors:
        factors = ["Recovery pressure", *factors][:4]
    return tuple(factors)


def reaches_target_by_exam(trajectory: StudyTrajectory) -> bool | None:
    """Whether projected readiness meets Ready-for-Revision by exam."""
    if trajectory.projected_readiness_ratio is None:
        return None
    if trajectory.days_to_exam is None:
        return trajectory.projected_readiness_ratio >= TARGET_READINESS_RATIO
    return trajectory.projected_readiness_ratio >= TARGET_READINESS_RATIO
