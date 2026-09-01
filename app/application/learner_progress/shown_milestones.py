"""Append-only document helpers for milestones already announced to a student.

Records what was shown. Does not compute or influence milestone detection,
Twin state, or Study Progress.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass(frozen=True)
class ShownMilestoneRecord:
    """One milestone that was announced to the student."""

    milestone_id: str
    label: str
    shown_at: date


def parse_shown_records(
    document: dict[str, Any] | None,
) -> tuple[ShownMilestoneRecord, ...]:
    """Load shown milestone rows from a persisted document."""
    if not isinstance(document, dict):
        return ()
    records: list[ShownMilestoneRecord] = []
    for raw in document.get("shown") or ():
        if not isinstance(raw, dict):
            continue
        milestone_id = str(raw.get("milestone_id") or "").strip()
        if not milestone_id:
            continue
        label = str(raw.get("label") or "").strip()
        shown_raw = raw.get("shown_at")
        shown_at: date | None = None
        if isinstance(shown_raw, str):
            try:
                shown_at = date.fromisoformat(shown_raw)
            except ValueError:
                shown_at = None
        if shown_at is None:
            continue
        records.append(
            ShownMilestoneRecord(
                milestone_id=milestone_id,
                label=label or milestone_id,
                shown_at=shown_at,
            )
        )
    return tuple(records)


def shown_milestone_ids(document: dict[str, Any] | None) -> frozenset[str]:
    """Ids already recorded as shown (for detector previously_earned)."""
    return frozenset(r.milestone_id for r in parse_shown_records(document))


def append_shown_milestone(
    document: dict[str, Any] | None,
    *,
    learner_id: str,
    milestone_id: str,
    label: str,
    shown_at: date,
) -> dict[str, Any]:
    """Return document with ``milestone_id`` appended if not already present."""
    mid = (milestone_id or "").strip()
    if not mid:
        existing = deepcopy(document) if isinstance(document, dict) else {}
        existing.setdefault("learner_id", learner_id.strip())
        existing.setdefault("shown", list(existing.get("shown") or []))
        return existing

    records = list(parse_shown_records(document))
    existing_ids = {r.milestone_id for r in records}
    if mid not in existing_ids:
        records.append(
            ShownMilestoneRecord(
                milestone_id=mid,
                label=(label or "").strip() or mid,
                shown_at=shown_at,
            )
        )
    return {
        "learner_id": learner_id.strip(),
        "shown": [
            {
                "milestone_id": r.milestone_id,
                "label": r.label,
                "shown_at": r.shown_at.isoformat(),
            }
            for r in records
        ],
    }
