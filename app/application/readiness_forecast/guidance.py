"""Student-facing readiness forecast guidance (KWP-012).

Natural language only — no pass probabilities, no fabricated certainty.
"""

from __future__ import annotations

from app.application.readiness_forecast.dto import (
    TARGET_READINESS_STAGE,
    ForecastLabel,
    ForecastSignals,
    StudyTrajectory,
)

_FORBIDDEN = (
    "digital twin",
    "evidence authority",
    "pass probability",
    "guaranteed",
    "certain you will",
    "will definitely",
    "cognitive load",
    "overloaded",
    "badge",
    "leaderboard",
)


def guidance_for(
    label: ForecastLabel,
    *,
    signals: ForecastSignals,
    trajectory: StudyTrajectory,
) -> str:
    """Primary student guidance line."""
    stage = (
        trajectory.projected_readiness_stage
        or TARGET_READINESS_STAGE
    )
    sitting = "scheduled sitting" if signals.days_to_exam is not None else (
        "exam preparation"
    )

    if label == ForecastLabel.INSUFFICIENT_EVIDENCE:
        return (
            "Complete a few more study sittings and a clearer readiness "
            "trajectory will appear here."
        )
    if label == ForecastLabel.ON_TRACK:
        return (
            "If your recent study pattern continues, you are likely to reach "
            f"{stage} before your {sitting}."
        )
    if label == ForecastLabel.AHEAD_OF_SCHEDULE:
        return (
            "Current progress suggests you are ahead of the pace needed to "
            f"reach {TARGET_READINESS_STAGE} before your {sitting}."
        )
    if label == ForecastLabel.BUILDING_MOMENTUM:
        return (
            "Your recent sittings show building momentum. Keep the pattern "
            "steady and readiness should continue to strengthen."
        )
    if label == ForecastLabel.NEEDS_GREATER_CONSISTENCY:
        return (
            "Current progress suggests additional study consistency will be "
            "needed to stay on a healthy readiness trajectory."
        )
    if label == ForecastLabel.RECOVERY_REQUIRED:
        return (
            "Evidence points to recovery work first. Rebuild understanding "
            "before expecting readiness to climb."
        )
    if label == ForecastLabel.BELOW_TARGET_PACE:
        return (
            "At the current pace, readiness may land below "
            f"{TARGET_READINESS_STAGE} by your {sitting}. A steadier or "
            "slightly denser study rhythm would help."
        )
    return scrub(
        "Continue studying steadily: trajectory updates as evidence grows."
    )


def explanation_for(
    label: ForecastLabel,
    *,
    signals: ForecastSignals,
    trajectory: StudyTrajectory,
) -> str:
    """Supporting explanation with trend + honesty about confidence."""
    trend = trajectory.current_trend_title or "Not yet clear"
    confidence = trajectory.confidence_title or "Limited evidence"
    factors = ", ".join(trajectory.influential_factors[:3]) or "recent sittings"
    current = trajectory.current_readiness_stage or "Building"
    projected = trajectory.projected_readiness_stage or "still forming"

    base = (
        f"Current trend: {trend}. Today looks like {current}; "
        f"if the pattern continues, projection points toward {projected}. "
        f"Most influential factors: {factors}. "
        f"Confidence: {confidence}. This is a directional estimate, "
        "not a guarantee."
    )
    if label == ForecastLabel.INSUFFICIENT_EVIDENCE:
        return (
            "Not enough sittings yet to project readiness confidently. "
            "Trajectory builds from repeated, honest study evidence."
        )
    if signals.days_to_exam is not None:
        base += f" Days to exam considered: {signals.days_to_exam}."
    return scrub(base)


def scrub(text: str) -> str:
    """Strip forbidden internal vocabulary if it ever leaks."""
    out = text
    lowered = out.lower()
    for fragment in _FORBIDDEN:
        if fragment in lowered:
            # Soft scrub — replace whole sentence fragments conservatively.
            out = out.replace(fragment, "").replace(fragment.title(), "")
            lowered = out.lower()
    return " ".join(out.split()).strip()
