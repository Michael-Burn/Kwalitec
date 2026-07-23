"""Student-facing presentation helpers — projection only, no educational reasoning.

Maps existing Education OS primitives into human-readable labels. Never
estimates mastery, generates recommendations, or invents missions.
"""

from __future__ import annotations

from application.student_experience.progress.enums import (
    StudyTimeBand,
    TrajectoryLabel,
    TrendDirection,
    WeekdayLabel,
)

_WEEKDAY_LABELS: tuple[WeekdayLabel, ...] = (
    WeekdayLabel.MONDAY,
    WeekdayLabel.TUESDAY,
    WeekdayLabel.WEDNESDAY,
    WeekdayLabel.THURSDAY,
    WeekdayLabel.FRIDAY,
    WeekdayLabel.SATURDAY,
    WeekdayLabel.SUNDAY,
)

_TREND_MESSAGES: dict[TrendDirection, str] = {
    TrendDirection.UNKNOWN: "Not enough history to show a trend yet.",
    TrendDirection.IMPROVING: "Your recent history shows improvement.",
    TrendDirection.STEADY: "Your recent history is holding steady.",
    TrendDirection.DECLINING: "Your recent history has softened — keep studying.",
}

_TRAJECTORY_MESSAGES: dict[TrajectoryLabel, str] = {
    TrajectoryLabel.UNKNOWN: "Your learning journey will appear as you study.",
    TrajectoryLabel.JUST_STARTING: "You're just getting started on your journey.",
    TrajectoryLabel.BUILDING: "You're building a steady study rhythm.",
    TrajectoryLabel.STEADY: "You're making consistent progress.",
    TrajectoryLabel.ACCELERATING: "Your learning momentum is picking up.",
}

_STUDY_TIME_MESSAGES: dict[StudyTimeBand, str] = {
    StudyTimeBand.UNKNOWN: "Preferred study time will appear as you complete sessions.",
    StudyTimeBand.MORNING: "You tend to study in the morning.",
    StudyTimeBand.AFTERNOON: "You tend to study in the afternoon.",
    StudyTimeBand.EVENING: "You tend to study in the evening.",
    StudyTimeBand.NIGHT: "You tend to study late at night.",
}


def humanise_identifier(value: str | None) -> str:
    """Turn kebab/snake identifiers into Title Case labels."""
    if value is None:
        return ""
    cleaned = value.strip().replace("_", " ").replace("-", " ")
    if not cleaned:
        return ""
    return " ".join(part.capitalize() for part in cleaned.split())


def weekday_label(weekday: int | None) -> WeekdayLabel:
    """Map Python weekday index (Monday=0) to a student-facing label."""
    if weekday is None or weekday < 0 or weekday > 6:
        return WeekdayLabel.UNKNOWN
    return _WEEKDAY_LABELS[weekday]


def weekday_message(label: WeekdayLabel) -> str:
    if label is WeekdayLabel.UNKNOWN:
        return "Most productive weekday will appear as you study."
    return f"Your most productive weekday is {label.value.capitalize()}."


def study_time_band(hour: int | None) -> StudyTimeBand:
    """Project an hour-of-day into a preferred study-time band."""
    if hour is None or hour < 0 or hour > 23:
        return StudyTimeBand.UNKNOWN
    if 5 <= hour < 12:
        return StudyTimeBand.MORNING
    if 12 <= hour < 17:
        return StudyTimeBand.AFTERNOON
    if 17 <= hour < 22:
        return StudyTimeBand.EVENING
    return StudyTimeBand.NIGHT


def study_time_message(band: StudyTimeBand) -> str:
    return _STUDY_TIME_MESSAGES[band]


def trend_message(direction: TrendDirection, *, subject: str) -> str:
    """Student-facing trend sentence for a named subject area."""
    if direction is TrendDirection.UNKNOWN:
        return f"{subject} trend will appear as you build more history."
    if direction is TrendDirection.IMPROVING:
        return f"Your {subject} trend is improving."
    if direction is TrendDirection.STEADY:
        return f"Your {subject} trend is steady."
    return f"Your {subject} trend has softened recently."


def trend_from_deltas(
    values: tuple[float, ...], *, epsilon: float = 0.02
) -> TrendDirection:
    """Deterministic historical trend from ordered scalar samples."""
    if len(values) < 2:
        return TrendDirection.UNKNOWN
    delta = values[-1] - values[0]
    if delta > epsilon:
        return TrendDirection.IMPROVING
    if delta < -epsilon:
        return TrendDirection.DECLINING
    return TrendDirection.STEADY


def trajectory_from_activity(
    *,
    completed_missions: int,
    current_streak: int,
    weekly_missions: int,
) -> TrajectoryLabel:
    """Project a trajectory label from historical activity counts."""
    if completed_missions <= 0 and weekly_missions <= 0:
        if current_streak <= 0:
            return TrajectoryLabel.UNKNOWN
        return TrajectoryLabel.JUST_STARTING
    if completed_missions < 3:
        return TrajectoryLabel.JUST_STARTING
    if weekly_missions >= 5 and current_streak >= 3:
        return TrajectoryLabel.ACCELERATING
    if current_streak >= 2 or weekly_missions >= 2:
        return TrajectoryLabel.STEADY
    return TrajectoryLabel.BUILDING


def trajectory_message(label: TrajectoryLabel) -> str:
    return _TRAJECTORY_MESSAGES[label]


def count_phrase(count: int, singular: str, plural: str | None = None) -> str:
    """Format a count into student-facing language."""
    noun = singular if count == 1 else (plural or f"{singular}s")
    return f"{count} {noun}"
