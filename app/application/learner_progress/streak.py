"""Streak calculation over qualifying study days (plain, non-punitive naming)."""

from __future__ import annotations

from datetime import date, timedelta


def current_streak_days(study_days: set[date], *, as_of: date) -> int:
    """Consecutive qualifying days ending on ``as_of`` or the prior day."""
    if not study_days:
        return 0
    cursor = as_of
    if cursor not in study_days:
        cursor = as_of - timedelta(days=1)
        if cursor not in study_days:
            return 0
    streak = 0
    while cursor in study_days:
        streak += 1
        cursor -= timedelta(days=1)
        if streak > 3660:
            break
    return streak


def longest_streak_days(study_days: set[date]) -> int:
    """Longest run of consecutive qualifying days in ``study_days``."""
    if not study_days:
        return 0
    ordered = sorted(study_days)
    longest = 1
    current = 1
    for index in range(1, len(ordered)):
        if ordered[index] == ordered[index - 1] + timedelta(days=1):
            current += 1
            longest = max(longest, current)
        else:
            current = 1
    return longest


def monotonic_longest_streak_days(
    *,
    study_days: set[date],
    stored_longest: int,
) -> int:
    """Preserve historical peak; never decrease ``stored_longest``."""
    computed = longest_streak_days(study_days)
    return max(int(stored_longest or 0), computed)


def dates_in_range(
    study_days: set[date],
    *,
    start_date: date,
    end_date: date,
) -> tuple[date, ...]:
    """Distinct qualifying dates within ``[start_date, end_date]`` inclusive."""
    if start_date > end_date:
        return ()
    return tuple(
        sorted(d for d in study_days if start_date <= d <= end_date)
    )
