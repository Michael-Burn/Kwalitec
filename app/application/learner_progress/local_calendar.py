"""Canonical learner-local calendar dates for streak study-day derivation.

Event timestamps stay stored in UTC. This module is the single place that
turns a UTC instant plus an IANA timezone into the learner's calendar date.
It does not decide whether an activity qualifies, and it does not decide
whether qualifying days are consecutive.
"""

from __future__ import annotations

from datetime import UTC, date, datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

DEFAULT_LEARNER_TIMEZONE = "Africa/Harare"


def local_calendar_date(when: datetime, timezone_name: str) -> date:
    """Return the learner-local calendar date for a UTC timestamp.

    Args:
        when: Event time. Naive values are treated as UTC.
        timezone_name: IANA timezone identifier (for example ``Africa/Harare``).

    Returns:
        The calendar date in the resolved timezone. Unknown or empty timezone
        names fall back to ``Africa/Harare``.
    """
    zone = ZoneInfo(normalize_iana_timezone(timezone_name))
    if when.tzinfo is None:
        instant = when.replace(tzinfo=UTC)
    else:
        instant = when.astimezone(UTC)
    return instant.astimezone(zone).date()


def normalize_iana_timezone(timezone_name: str | None) -> str:
    """Return a valid IANA name, defaulting to ``Africa/Harare``."""
    name = (timezone_name or "").strip()
    if not name:
        return DEFAULT_LEARNER_TIMEZONE
    try:
        ZoneInfo(name)
    except ZoneInfoNotFoundError:
        return DEFAULT_LEARNER_TIMEZONE
    return name


def timezone_for_learner(learner_id: str | int | None) -> str:
    """Return the learner's profile timezone, or the product default.

    Missing users, missing app context, and invalid stored values all resolve
    to ``Africa/Harare``. The profile setting is the sole authority; this
    helper does not inspect devices, travel, or history.
    """
    if learner_id is None:
        return DEFAULT_LEARNER_TIMEZONE
    try:
        uid = int(str(learner_id).strip())
    except (TypeError, ValueError):
        return DEFAULT_LEARNER_TIMEZONE
    try:
        from app.extensions import db
        from app.models.user import User

        user = db.session.get(User, uid)
    except Exception:  # noqa: BLE001 - fail open to the product default
        return DEFAULT_LEARNER_TIMEZONE
    if user is None:
        return DEFAULT_LEARNER_TIMEZONE
    return normalize_iana_timezone(getattr(user, "timezone", None))
