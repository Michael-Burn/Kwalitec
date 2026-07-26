"""EvidenceAdvisoryAssembler — Evidence read-model → EvidenceAdvisory (P2-MS009).

Aggregates factual observations into advisory-ready summaries for Runtime A.
Preserves provenance. Performs no educational interpretation, scoring,
prediction, recommendation, or mastery inference.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from datetime import date, datetime, timedelta
from typing import Any

from app.infrastructure.adapters.evidence_platform.contracts import (
    AUTHORITY_EVIDENCE_PLATFORM,
    AVAILABILITY_AVAILABLE,
    EVIDENCE_VERSION_ADVISORY,
    ConsistencySummary,
    EngagementSummary,
    EvidenceAdvisory,
    EvidenceFactualSummary,
    FactualConstraint,
    ObservedPattern,
    serialize_canonical,
)

SOURCE_SERVICE = "evidence_advisory_assembler"
DEFAULT_SOURCE_DESCRIPTION = "Derived from recorded study activity."

_MONTH_NAMES = (
    "",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)


def deterministic_advisory_id(
    *,
    student_id: str,
    reporting_period: str,
    generated_at: str | None,
    evidence_summary_id: str,
    evidence_refs: tuple[str, ...] | list[str],
) -> str:
    """Derive advisory_id from material factual fields (no wall-clock invent)."""
    material = {
        "evidence_refs": list(evidence_refs),
        "evidence_summary_id": evidence_summary_id,
        "generated_at": generated_at,
        "reporting_period": reporting_period,
        "student_id": student_id,
        "version": EVIDENCE_VERSION_ADVISORY,
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()
    return f"evadv-{digest[:32]}"


def format_period_source_description(
    *,
    reporting_period: str,
    anchor_date: date | None = None,
    window_days: int = 7,
) -> str:
    """Human-readable provenance for the reporting window.

    Example: "Derived from recorded study activity between 1–7 August."
    """
    period = (reporting_period or "").strip().lower()
    if period == "all":
        return "Derived from all recorded study activity."
    if anchor_date is None:
        return DEFAULT_SOURCE_DESCRIPTION
    if period != "this_week":
        return (
            f"Derived from recorded study activity "
            f"(period={period}, as of {_format_day(anchor_date)})."
        )
    start = anchor_date - timedelta(days=max(1, window_days) - 1)
    return (
        "Derived from recorded study activity between "
        f"{_format_day_range(start, anchor_date)}."
    )


class EvidenceAdvisoryAssembler:
    """Convert EvidenceFactualSummary into immutable EvidenceAdvisory.

    Responsibilities:
    - aggregate factual observations
    - preserve provenance
    - expose advisory-ready summaries

    Non-responsibilities: educational interpretation, scoring, predictions,
    recommendations, mastery inference, repository access, Runtime A writes.
    """

    ASSEMBLER_ID = "evidence_advisory_assembler"
    ASSEMBLER_VERSION = "1.0.0-p2.ms009"

    def __init__(self, *, enabled: bool = True) -> None:
        self._enabled = bool(enabled)

    @property
    def assembler_id(self) -> str:
        return self.ASSEMBLER_ID

    @property
    def assembler_version(self) -> str:
        return self.ASSEMBLER_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    def assemble(
        self,
        summary: EvidenceFactualSummary,
        *,
        generated_at: str | None = None,
        anchor_date: date | None = None,
    ) -> EvidenceAdvisory:
        """Project an Evidence factual summary into EvidenceAdvisory."""
        if not self._enabled:
            raise ValueError(
                "EvidenceAdvisoryAssembler is disabled (feature flag OFF)"
            )
        if not isinstance(summary, EvidenceFactualSummary):
            raise TypeError("summary must be an EvidenceFactualSummary")

        period = (summary.reporting_period or "this_week").strip().lower()
        as_of = (generated_at or summary.generated_at or "").strip() or None
        resolved_anchor = anchor_date or _parse_date(as_of)
        source = format_period_source_description(
            reporting_period=period,
            anchor_date=resolved_anchor,
        )
        evidence_refs = tuple(summary.evidence_refs)
        evidence_summary_id = (summary.summary_id or "").strip()

        patterns = _build_observed_patterns(
            summary,
            evidence_refs=evidence_refs,
            source_description=source,
        )
        engagement = EngagementSummary(
            completed_missions=summary.completed_missions,
            study_sessions=summary.study_sessions,
            completed_reflections=summary.completed_reflections,
            event_counts=dict(summary.event_counts),
            source_description=source,
        )
        consistency = ConsistencySummary(
            active_streak=summary.active_streak,
            source_description=source,
        )
        constraints = _build_factual_constraints(
            summary, source_description=source
        )
        advisory_id = deterministic_advisory_id(
            student_id=summary.student_id,
            reporting_period=period,
            generated_at=as_of,
            evidence_summary_id=evidence_summary_id,
            evidence_refs=evidence_refs,
        )
        provenance: dict[str, Any] = {
            "authority": AUTHORITY_EVIDENCE_PLATFORM,
            "source_service": SOURCE_SERVICE,
            "assembler_version": self.ASSEMBLER_VERSION,
            "reporting_period": period,
            "evidence_summary_id": evidence_summary_id,
            "evidence_refs": list(evidence_refs),
            "evidence_provenance": dict(summary.provenance),
            "anchor_date": (
                resolved_anchor.isoformat() if resolved_anchor is not None else ""
            ),
            "source_description": source,
            "field_provenance": {
                "observed_patterns": source,
                "engagement_summary": source,
                "consistency_summary": source,
                "factual_constraints": source,
            },
        }
        return EvidenceAdvisory(
            advisory_id=advisory_id,
            reporting_period=period,
            observed_patterns=patterns,
            engagement_summary=engagement,
            consistency_summary=consistency,
            factual_constraints=constraints,
            provenance=provenance,
            generated_at=as_of,
            student_id=summary.student_id,
            evidence_summary_id=evidence_summary_id,
            evidence_refs=evidence_refs,
            source_description=source,
            authority=AUTHORITY_EVIDENCE_PLATFORM,
            availability=AVAILABILITY_AVAILABLE,
            advisory_version=EVIDENCE_VERSION_ADVISORY,
        )


def build_evidence_advisory_assembler(
    *,
    enabled: bool,
) -> EvidenceAdvisoryAssembler | None:
    """DI helper — construct assembler only when ENABLE_EVIDENCE_ADVISORY is ON."""
    if not enabled:
        return None
    return EvidenceAdvisoryAssembler(enabled=True)


def _build_observed_patterns(
    summary: EvidenceFactualSummary,
    *,
    evidence_refs: tuple[str, ...],
    source_description: str,
) -> tuple[ObservedPattern, ...]:
    patterns: list[ObservedPattern] = []
    event_counts: Mapping[str, Any] = summary.event_counts
    for key in sorted(event_counts.keys(), key=str):
        raw = event_counts[key]
        count = int(raw) if isinstance(raw, int) else 0
        if count <= 0:
            continue
        event_key = str(key).strip().lower()
        patterns.append(
            ObservedPattern(
                pattern_key=event_key,
                observation=(
                    f"{event_key} observed {count} time"
                    f"{'' if count == 1 else 's'} in the reporting period"
                ),
                count=count,
                evidence_refs=evidence_refs,
                source_description=source_description,
            )
        )
    if not patterns and summary.study_sessions == 0:
        patterns.append(
            ObservedPattern(
                pattern_key="no_session_completed",
                observation=(
                    "No session_completed events observed in the reporting period"
                ),
                count=0,
                evidence_refs=evidence_refs,
                source_description=source_description,
            )
        )
    return tuple(patterns)


def _build_factual_constraints(
    summary: EvidenceFactualSummary,
    *,
    source_description: str,
) -> tuple[FactualConstraint, ...]:
    constraints: list[FactualConstraint] = []
    if summary.study_sessions == 0:
        constraints.append(
            FactualConstraint(
                constraint_key="no_study_sessions_in_period",
                statement=(
                    "No study sessions were recorded in the reporting period."
                ),
                source_description=source_description,
            )
        )
    if summary.completed_reflections == 0:
        constraints.append(
            FactualConstraint(
                constraint_key="no_reflections_in_period",
                statement=(
                    "No reflections were recorded in the reporting period."
                ),
                source_description=source_description,
            )
        )
    if not summary.evidence_refs:
        constraints.append(
            FactualConstraint(
                constraint_key="empty_evidence_refs",
                statement=(
                    "No evidence record identifiers were retained for this window."
                ),
                source_description=source_description,
            )
        )
    return tuple(constraints)


def _format_day(value: date) -> str:
    return f"{value.day} {_MONTH_NAMES[value.month]}"


def _format_day_range(start: date, end: date) -> str:
    if start.year == end.year and start.month == end.month:
        return f"{start.day}–{end.day} {_MONTH_NAMES[end.month]}"
    if start.year == end.year:
        return (
            f"{start.day} {_MONTH_NAMES[start.month]}–"
            f"{end.day} {_MONTH_NAMES[end.month]}"
        )
    return (
        f"{start.day} {_MONTH_NAMES[start.month]} {start.year}–"
        f"{end.day} {_MONTH_NAMES[end.month]} {end.year}"
    )


def _parse_date(value: str | None) -> date | None:
    raw = (value or "").strip()
    if not raw:
        return None
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
    "DEFAULT_SOURCE_DESCRIPTION",
    "EvidenceAdvisoryAssembler",
    "SOURCE_SERVICE",
    "build_evidence_advisory_assembler",
    "deterministic_advisory_id",
    "format_period_source_description",
]
