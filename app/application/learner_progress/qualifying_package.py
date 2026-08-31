"""Qualifying study day rules derived from Accepted Evidence Packages.

A qualifying study day is a calendar day on which at least one Educational+
observation with ``may_update_twin=True`` was accepted for a learner. This
mirrors the Twin admissibility gate without requiring Twin consumption.
"""

from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any


def package_qualifies_for_study_day(package: dict[str, Any]) -> bool:
    """True when an opaque package authorises a qualifying study day."""
    validation = package.get("validation")
    if not isinstance(validation, dict):
        return False
    return bool(validation.get("may_update_twin"))


def study_date_from_package(package: dict[str, Any]) -> date | None:
    """Calendar date (UTC) for the sitting represented by the package."""
    raw = package.get("created_at")
    if isinstance(raw, str):
        try:
            created = datetime.fromisoformat(raw)
        except ValueError:
            return None
    elif isinstance(raw, datetime):
        created = raw
    else:
        return None
    if created.tzinfo is None:
        created = created.replace(tzinfo=UTC)
    return created.astimezone(UTC).date()


def learner_id_from_package(package: dict[str, Any]) -> str | None:
    """Normalised learner id string from package attribution."""
    sid = str(package.get("student_id") or "").strip()
    return sid or None
