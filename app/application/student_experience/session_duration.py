"""Single planned session-duration fact for student-facing surfaces.

EP-007.1 / REM-03: Home, Mission, Session, and bridge adapters must agree on
one duration per day. Prefer the student's preferred session length (plan
contract); fall back to day-type weekday/weekend minutes only when preferred
is absent. Does not invent educational timing or change PlanningService math.
"""

from __future__ import annotations

from datetime import date
from typing import Any


def resolve_planned_session_minutes(
    study_plan: Any | None,
    *,
    mission_date: date | None = None,
) -> int | None:
    """Return the canonical planned session length in minutes.

    Args:
        study_plan: Active study plan (ORM or duck-typed) or None.
        mission_date: Optional calendar day for weekday/weekend fallback.

    Returns:
        Non-negative minutes, or None when no plan / no usable values.
    """
    if study_plan is None:
        return None

    preferred = getattr(study_plan, "preferred_session_minutes", None)
    if preferred is not None:
        try:
            minutes = int(preferred)
        except (TypeError, ValueError):
            minutes = None
        else:
            if minutes >= 0:
                return minutes

    day = mission_date
    if day is not None and day.weekday() >= 5:
        raw = getattr(study_plan, "weekend_study_minutes", None)
    else:
        raw = getattr(study_plan, "weekday_study_minutes", None)
    if raw is None:
        return None
    try:
        minutes = int(raw)
    except (TypeError, ValueError):
        return None
    return minutes if minutes >= 0 else None
