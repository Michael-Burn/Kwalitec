"""Estimated episode duration (KWP-015).

Derives minutes from curriculum effort, difficulty band, student pace,
and previous evidence — without mutating Learning Difficulty or Evidence.
"""

from __future__ import annotations

_DIFFICULTY_FACTOR: dict[str, float] = {
    "foundational": 0.9,
    "foundation": 0.9,
    "introductory": 0.9,
    "light": 0.85,
    "intermediate": 1.0,
    "moderate": 1.0,
    "advanced": 1.15,
    "demanding": 1.2,
    "capstone": 1.25,
    "intensive": 1.3,
    "very_demanding": 1.3,
}


def estimate_duration_minutes(
    *,
    base_effort_minutes: int = 0,
    difficulty_band: str = "",
    student_pace_factor: float = 1.0,
    previous_evidence_minutes: int = 0,
    weak_topic: bool = False,
    activity_count: int = 4,
) -> int:
    """Deterministic duration estimate for one Learning Episode."""
    base = int(base_effort_minutes or 0)
    if base <= 0:
        base = 45 if activity_count >= 4 else 30

    band = (difficulty_band or "").strip().lower().replace(" ", "_")
    diff = _DIFFICULTY_FACTOR.get(band, 1.0)
    pace = student_pace_factor if student_pace_factor > 0 else 1.0
    pace = max(0.75, min(1.4, pace))

    minutes = base * diff * pace
    if weak_topic:
        minutes *= 1.1
    if previous_evidence_minutes > 0:
        prior = min(previous_evidence_minutes, base)
        minutes *= max(0.85, 1.0 - (prior / max(base * 4, 1)))

    return max(15, int(round(minutes / 5.0) * 5))


def split_activity_minutes(
    total_minutes: int,
    *,
    activity_count: int,
) -> tuple[int, ...]:
    """Distribute episode minutes across activities (deterministic)."""
    n = max(1, int(activity_count or 1))
    total = max(n * 3, int(total_minutes or 0))
    base = total // n
    rem = total % n
    parts = [base] * n
    for i in range(rem):
        parts[i] += 1
    return tuple(parts)
