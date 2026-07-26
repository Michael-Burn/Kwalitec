"""Evidence factual query — public read-model for Experience Feedback (P2-MS008).

Builds immutable EvidenceFactualSummary values from previously observed
EvidenceRecords. Counts delivery/event facts only — no scores, predictions,
mastery, recommendations, or educational interpretation.
"""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from datetime import date, datetime, timedelta
from typing import Any

from app.infrastructure.adapters.evidence_platform.contracts import (
    AUTHORITY_EVIDENCE_PLATFORM,
    AVAILABILITY_AVAILABLE,
    EvidenceFactualSummary,
    EvidenceRecord,
    serialize_canonical,
)

# Experience Observation event types that map to factual counters.
EVENT_SESSION_COMPLETED = "session_completed"
EVENT_REFLECTION_COMPLETED = "reflection_completed"
EVENT_MISSION_STARTED = "mission_started"

SOURCE_DESCRIPTION = "Based on your recorded study activity."
SOURCE_SERVICE = "evidence_factual_query"

REPORTING_PERIOD_THIS_WEEK = "this_week"
REPORTING_PERIOD_ALL = "all"

_WEEK_DAYS = 7


def deterministic_factual_summary_id(
    *,
    student_id: str,
    reporting_period: str,
    generated_at: str | None,
    evidence_refs: Sequence[str],
) -> str:
    """Derive summary_id from material factual fields (no wall-clock invent)."""
    material = {
        "evidence_refs": list(evidence_refs),
        "generated_at": generated_at,
        "reporting_period": reporting_period,
        "student_id": student_id,
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()
    return f"evfact-{digest[:32]}"


def build_factual_summary(
    student_id: str,
    records: Sequence[EvidenceRecord],
    *,
    reporting_period: str = REPORTING_PERIOD_THIS_WEEK,
    as_of: str | None = None,
) -> EvidenceFactualSummary:
    """Project EvidenceRecords into an immutable EvidenceFactualSummary.

    Counting rules (factual event tallies only):
    - completed_missions ← ``session_completed`` in reporting window
      (Daily Mission closes when the guided session completes)
    - study_sessions ← ``session_completed`` in reporting window
    - completed_reflections ← ``reflection_completed`` in reporting window
    - active_streak ← consecutive calendar days (ending at as_of / latest
      observed day) with ≥1 ``session_completed`` (uses all retained records,
      not only the reporting window)

    Does not invent timestamps — ``generated_at`` is ``as_of`` when provided,
    otherwise the latest ``observed_at`` / ``ingested_at`` among inputs.
    """
    sid = (student_id or "").strip()
    if not sid:
        raise ValueError("student_id must be a non-empty string")
    period = (reporting_period or REPORTING_PERIOD_THIS_WEEK).strip().lower()
    if not period:
        period = REPORTING_PERIOD_THIS_WEEK

    scoped = [
        record
        for record in records
        if isinstance(record, EvidenceRecord) and record.student_id == sid
    ]
    anchor = _resolve_anchor_date(as_of=as_of, records=scoped)
    windowed = _filter_reporting_window(
        scoped, period=period, anchor=anchor
    )

    event_counts: dict[str, int] = {}
    for record in windowed:
        key = (record.event_type or "").strip().lower()
        if not key:
            continue
        event_counts[key] = event_counts.get(key, 0) + 1

    completed_missions = event_counts.get(EVENT_SESSION_COMPLETED, 0)
    study_sessions = event_counts.get(EVENT_SESSION_COMPLETED, 0)
    completed_reflections = event_counts.get(EVENT_REFLECTION_COMPLETED, 0)
    active_streak = _active_streak(scoped, anchor=anchor)

    evidence_refs = tuple(
        sorted(
            {
                record.evidence_id
                for record in windowed
                if (record.evidence_id or "").strip()
            }
        )
    )
    generated_at = (as_of or "").strip() or _latest_timestamp(scoped) or None
    summary_id = deterministic_factual_summary_id(
        student_id=sid,
        reporting_period=period,
        generated_at=generated_at,
        evidence_refs=evidence_refs,
    )
    provenance: dict[str, Any] = {
        "authority": AUTHORITY_EVIDENCE_PLATFORM,
        "source_service": SOURCE_SERVICE,
        "reporting_period": period,
        "record_count": len(windowed),
        "anchor_date": anchor.isoformat() if anchor is not None else "",
        "counting_rules": {
            "completed_missions": EVENT_SESSION_COMPLETED,
            "study_sessions": EVENT_SESSION_COMPLETED,
            "completed_reflections": EVENT_REFLECTION_COMPLETED,
            "active_streak": f"consecutive_days_with_{EVENT_SESSION_COMPLETED}",
        },
    }
    return EvidenceFactualSummary(
        summary_id=summary_id,
        student_id=sid,
        reporting_period=period,
        completed_missions=completed_missions,
        completed_reflections=completed_reflections,
        study_sessions=study_sessions,
        active_streak=active_streak,
        generated_at=generated_at,
        evidence_refs=evidence_refs,
        event_counts=event_counts,
        provenance=provenance,
        source_description=SOURCE_DESCRIPTION,
        authority=AUTHORITY_EVIDENCE_PLATFORM,
        availability=AVAILABILITY_AVAILABLE,
    )


def _filter_reporting_window(
    records: Sequence[EvidenceRecord],
    *,
    period: str,
    anchor: date | None,
) -> list[EvidenceRecord]:
    if period == REPORTING_PERIOD_ALL or anchor is None:
        return list(records)
    if period != REPORTING_PERIOD_THIS_WEEK:
        # Unknown periods fall back to all retained records (still factual).
        return list(records)
    start = anchor - timedelta(days=_WEEK_DAYS - 1)
    filtered: list[EvidenceRecord] = []
    for record in records:
        observed = _record_date(record)
        if observed is None:
            continue
        if start <= observed <= anchor:
            filtered.append(record)
    return filtered


def _active_streak(
    records: Sequence[EvidenceRecord],
    *,
    anchor: date | None,
) -> int:
    """Count consecutive days with session_completed ending at anchor."""
    days = {
        _record_date(record)
        for record in records
        if (record.event_type or "").strip().lower() == EVENT_SESSION_COMPLETED
    }
    days.discard(None)
    if not days or anchor is None:
        return 0
    typed_days = {d for d in days if isinstance(d, date)}
    streak = 0
    cursor = anchor
    while cursor in typed_days:
        streak += 1
        cursor = cursor - timedelta(days=1)
    return streak


def _resolve_anchor_date(
    *,
    as_of: str | None,
    records: Sequence[EvidenceRecord],
) -> date | None:
    if as_of:
        parsed = _parse_date(as_of)
        if parsed is not None:
            return parsed
    latest: date | None = None
    for record in records:
        observed = _record_date(record)
        if observed is None:
            continue
        if latest is None or observed > latest:
            latest = observed
    return latest


def _record_date(record: EvidenceRecord) -> date | None:
    for raw in (record.observed_at, record.as_of, record.ingested_at):
        parsed = _parse_date(raw)
        if parsed is not None:
            return parsed
    return None


def _latest_timestamp(records: Sequence[EvidenceRecord]) -> str:
    best = ""
    for record in records:
        for raw in (record.observed_at, record.as_of, record.ingested_at):
            value = (raw or "").strip()
            if value and value > best:
                best = value
    return best


def _parse_date(value: str | None) -> date | None:
    raw = (value or "").strip()
    if not raw:
        return None
    # Accept YYYY-MM-DD or ISO datetime prefixes.
    day_part = raw[:10]
    try:
        return date.fromisoformat(day_part)
    except ValueError:
        pass
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).date()
    except ValueError:
        return None


__all__ = [
    "EVENT_MISSION_STARTED",
    "EVENT_REFLECTION_COMPLETED",
    "EVENT_SESSION_COMPLETED",
    "REPORTING_PERIOD_ALL",
    "REPORTING_PERIOD_THIS_WEEK",
    "SOURCE_DESCRIPTION",
    "build_factual_summary",
    "deterministic_factual_summary_id",
]
