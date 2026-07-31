"""Learning momentum from existing evidence signals (KWP-007).

Tracks Recovery / Plateau / Acceleration / Consistency / Topic stability.
Does not invent persistence — reuses sitting, cadence, and Progress flags.
"""

from __future__ import annotations

from app.application.learning_strategy.calibration import performance_band
from app.application.learning_strategy.dto import (
    MomentumPosture,
    StrategyEvidenceInput,
)


def derive_momentum(
    evidence: StrategyEvidenceInput,
) -> tuple[MomentumPosture, str]:
    """Derive momentum posture and student-safe guidance."""
    topic = evidence.topic_title or "this topic"
    perf = performance_band(evidence)

    if evidence.abandoned or evidence.finish_verdict == "no":
        return (
            MomentumPosture.RECOVERY,
            "Today's Session points to a recovery step — restart gently "
            f"on {topic} when you return.",
        )

    if evidence.retention_risk or (
        evidence.days_since_topic_practice is not None
        and evidence.days_since_topic_practice >= 14
        and evidence.weak_topic
    ):
        return (
            MomentumPosture.RECOVERY,
            f"Prior work on {topic} needs recovery before new challenge.",
        )

    if (
        evidence.consecutive_partial_finishes >= 2
        or (
            evidence.finish_verdict == "partially"
            and perf in {"mixed", "weak"}
        )
    ):
        return (
            MomentumPosture.PLATEAU,
            f"Progress on {topic} looks steady but flat — deepen practice "
            "before speeding up.",
        )

    if (
        evidence.progress_advanced
        and perf == "strong"
        and (
            evidence.consecutive_strong_sittings >= 1
            or evidence.practice_incorrect == 0
        )
    ):
        return (
            MomentumPosture.ACCELERATION,
            f"Strong practice on {topic} supports moving forward with "
            "confidence.",
        )

    if perf == "strong" and evidence.practice_incorrect == 0:
        streak = evidence.streak_days
        if streak is not None and streak >= 3:
            return (
                MomentumPosture.CONSISTENCY,
                "Your recent study rhythm is consistent — that stability "
                f"helps {topic} stick.",
            )
        return (
            MomentumPosture.TOPIC_STABILITY,
            f"{topic} looks stable after today's accurate practice.",
        )

    if evidence.streak_days is not None and evidence.streak_days >= 2:
        return (
            MomentumPosture.CONSISTENCY,
            "Keeping a steady Session rhythm supports long-term retention.",
        )

    if evidence.recent_session_count is not None and evidence.recent_session_count >= 3:
        return (
            MomentumPosture.CONSISTENCY,
            "Recent Sessions show a usable study cadence — keep it light "
            "and regular.",
        )

    if evidence.practice_attempted <= 0 and not evidence.progress_advanced:
        return (
            MomentumPosture.QUIET,
            "Not enough practice signal yet to describe learning momentum.",
        )

    return (
        MomentumPosture.PLATEAU,
        f"Keep practising {topic} steadily — momentum builds from "
        "repeated honest sittings.",
    )
