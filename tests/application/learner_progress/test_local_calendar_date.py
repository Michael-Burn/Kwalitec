"""Learner-local calendar date for streak study-day derivation."""

from __future__ import annotations

from datetime import UTC, date, datetime

from app.application.learner_progress.local_calendar import (
    DEFAULT_LEARNER_TIMEZONE,
    local_calendar_date,
    normalize_iana_timezone,
    timezone_for_learner,
)
from app.application.learner_progress.qualifying_package import (
    study_date_from_package,
)


def test_harare_midnight_boundary_from_utc() -> None:
    """Africa/Harare is UTC+2 with no DST. Local midnight is 22:00 UTC."""
    just_before = datetime(2026, 9, 6, 21, 59, 59, tzinfo=UTC)
    just_after = datetime(2026, 9, 6, 22, 0, 0, tzinfo=UTC)
    assert local_calendar_date(just_before, "Africa/Harare") == date(2026, 9, 6)
    assert local_calendar_date(just_after, "Africa/Harare") == date(2026, 9, 7)


def test_london_dst_midnight_boundary_from_utc() -> None:
    """Europe/London is on BST (UTC+1) in September. Local midnight is 23:00 UTC.

    The same UTC instants resolve to a different Harare date, proving the
    helper is timezone-aware and not accidentally correct only for Zimbabwe.
    """
    just_before = datetime(2026, 9, 6, 22, 59, 59, tzinfo=UTC)
    just_after = datetime(2026, 9, 6, 23, 0, 0, tzinfo=UTC)
    assert local_calendar_date(just_before, "Europe/London") == date(2026, 9, 6)
    assert local_calendar_date(just_after, "Europe/London") == date(2026, 9, 7)
    assert local_calendar_date(just_before, "Africa/Harare") == date(2026, 9, 7)
    assert local_calendar_date(just_after, "Africa/Harare") == date(2026, 9, 7)


def test_london_winter_gmt_differs_from_harare() -> None:
    """Europe/London is GMT (UTC+0) in January; Harare remains UTC+2."""
    just_before = datetime(2026, 1, 15, 23, 59, 59, tzinfo=UTC)
    just_after = datetime(2026, 1, 16, 0, 0, 0, tzinfo=UTC)
    assert local_calendar_date(just_before, "Europe/London") == date(2026, 1, 15)
    assert local_calendar_date(just_after, "Europe/London") == date(2026, 1, 16)
    assert local_calendar_date(just_before, "Africa/Harare") == date(2026, 1, 16)
    assert local_calendar_date(just_after, "Africa/Harare") == date(2026, 1, 16)


def test_naive_datetime_is_treated_as_utc() -> None:
    naive = datetime(2026, 9, 6, 22, 0, 0)
    assert local_calendar_date(naive, "Africa/Harare") == date(2026, 9, 7)


def test_unknown_timezone_falls_back_to_harare() -> None:
    assert normalize_iana_timezone("Not/A_Zone") == DEFAULT_LEARNER_TIMEZONE
    just_after = datetime(2026, 9, 6, 22, 0, 0, tzinfo=UTC)
    assert local_calendar_date(just_after, "Not/A_Zone") == date(2026, 9, 7)


def test_study_date_from_package_uses_learner_timezone() -> None:
    just_after_harare_midnight = datetime(2026, 9, 6, 22, 0, 0, tzinfo=UTC)
    package = {
        "student_id": "42",
        "created_at": just_after_harare_midnight.isoformat(),
        "validation": {"may_update_twin": True},
    }
    assert study_date_from_package(
        package, timezone_name="Africa/Harare"
    ) == date(2026, 9, 7)
    assert study_date_from_package(
        package, timezone_name="Europe/London"
    ) == date(2026, 9, 6)


def test_user_timezone_defaults_to_harare(ctx, user) -> None:
    assert user.timezone == "Africa/Harare"
    assert timezone_for_learner(user.id) == "Africa/Harare"


def test_timezone_for_learner_reads_profile_setting(ctx, user) -> None:
    user.timezone = "Europe/London"
    assert timezone_for_learner(user.id) == "Europe/London"
