"""Pure index document merge for qualifying study days."""

from __future__ import annotations

from datetime import date
from typing import Any

from app.application.learner_progress.streak import monotonic_longest_streak_days


def parse_qualifying_dates(document: dict[str, Any] | None) -> set[date]:
    """Load ISO date strings from a persisted index document."""
    if not isinstance(document, dict):
        return set()
    result: set[date] = set()
    for raw in document.get("qualifying_dates") or ():
        if isinstance(raw, str):
            try:
                result.add(date.fromisoformat(raw))
            except ValueError:
                continue
    return result


def merge_qualifying_date(
    document: dict[str, Any] | None,
    *,
    learner_id: str,
    study_date: date,
) -> dict[str, Any]:
    """Return updated index document with ``study_date`` included."""
    dates = parse_qualifying_dates(document)
    dates.add(study_date)
    stored_longest = int((document or {}).get("longest_streak_days") or 0)
    longest = monotonic_longest_streak_days(
        study_days=dates,
        stored_longest=stored_longest,
    )
    return {
        "learner_id": learner_id.strip(),
        "qualifying_dates": [d.isoformat() for d in sorted(dates)],
        "longest_streak_days": longest,
    }
