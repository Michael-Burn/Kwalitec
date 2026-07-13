"""Educational KPI status — presentation semantics from known evidence only.

Capability 4.7: Dashboard status labels must be educationally honest.
This module is the single source of truth for schedule/pace status wording.

It derives labels only from evidence the platform currently owns:
- calendar (days remaining)
- study-plan hours vs remaining curriculum hours (TimeEngine)

It does NOT invent:
- predictive pass probability
- risk modelling
- burnout prediction
- preparedness bands
- a fictional “expected coverage by day N” curve

Future slots (readiness / risk / study_velocity / predicted_completion) are
reserved on the presentation artefact so later capabilities can populate them
without redesigning the dashboard surface. They remain None until those
algorithms exist.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class _HoursBalance(Protocol):
    """Minimal TimeSummary-shaped protocol for surplus/deficit."""

    hours_surplus_or_deficit: float
    remaining_hours: float
    available_study_hours: float


# Machine codes — stable for CSS / tests / future consumers
CODE_EXAM_PERIOD = "exam_period"
CODE_CURRICULUM_COMPLETE = "curriculum_complete"
CODE_COMFORTABLE_PACE = "comfortable_pace"
CODE_PACE_MATCHES_PLAN = "pace_matches_plan"
CODE_SCHEDULE_TIGHT = "schedule_tight"
CODE_HIGH_REMAINING_WORKLOAD = "high_remaining_workload"
CODE_LIMITED_TIME = "limited_time"
CODE_PLAN_ACTIVE = "plan_active"
CODE_UNKNOWN = "unknown"

# Presentation severity — styling cue only, not a risk claim
SEVERITY_NEUTRAL = "neutral"
SEVERITY_INFO = "info"
SEVERITY_ATTENTION = "attention"
SEVERITY_URGENT = "urgent"

# Text symbols (not colour-only) for accessibility
_SYMBOLS: dict[str, str] = {
    SEVERITY_NEUTRAL: "·",
    SEVERITY_INFO: "✓",
    SEVERITY_ATTENTION: "!",
    SEVERITY_URGENT: "‼",
}

# Surplus/deficit hour thresholds (planned available vs remaining curriculum work)
_COMFORTABLE_SURPLUS_HOURS = 20.0
_TIGHT_DEFICIT_HOURS = -20.0
_LIMITED_TIME_DAYS = 14


@dataclass(frozen=True)
class EducationalKpiStatus:
    """Immutable presentation status for a dashboard KPI.

    ``kind`` identifies which educational concept this status describes.
    Future capabilities may add parallel statuses (readiness, risk, …)
    without changing this shape — reserved fields stay None until then.
    """

    kind: str
    code: str
    label: str
    evidence_summary: str
    severity: str
    # Reserved for future algorithms — do not populate until evidence exists
    readiness: str | None = None
    risk: str | None = None
    study_velocity: str | None = None
    predicted_completion: str | None = None

    @property
    def symbol(self) -> str:
        """Non-colour cue for badges (light / dark / high contrast)."""
        return _SYMBOLS.get(self.severity, _SYMBOLS[SEVERITY_NEUTRAL])

    def to_dict(self) -> dict:
        """Plain dict for templates and ExamTimeline payloads."""
        return {
            "kind": self.kind,
            "code": self.code,
            "label": self.label,
            "evidence_summary": self.evidence_summary,
            "severity": self.severity,
            "symbol": self.symbol,
            "status": self.code,  # alias for legacy schedule_status consumers
            "readiness": self.readiness,
            "risk": self.risk,
            "study_velocity": self.study_velocity,
            "predicted_completion": self.predicted_completion,
        }


class EducationalKpiStatusService:
    """Derives educationally honest schedule/pace status from known evidence."""

    KIND_SCHEDULE_PACE = "schedule_pace"

    @staticmethod
    def from_time_balance(
        *,
        days_remaining: int,
        hours_surplus_or_deficit: float,
        remaining_hours: float | None = None,
        available_study_hours: float | None = None,
        coverage_pct: float | None = None,
    ) -> EducationalKpiStatus:
        """Status from calendar + planned hours vs remaining curriculum hours.

        Args:
            days_remaining: Calendar days until exam (may be negative).
            hours_surplus_or_deficit: Available planned hours minus remaining
                curriculum hours (positive = surplus).
            remaining_hours: Optional remaining workload for evidence text.
            available_study_hours: Optional available hours for evidence text.
            coverage_pct: Optional coverage for curriculum-complete shortcut.
        """
        if days_remaining <= 0:
            return EducationalKpiStatus(
                kind=EducationalKpiStatusService.KIND_SCHEDULE_PACE,
                code=CODE_EXAM_PERIOD,
                label="Exam Period",
                evidence_summary="Exam date has arrived or passed.",
                severity=SEVERITY_ATTENTION,
            )

        if coverage_pct is not None and coverage_pct >= 100:
            return EducationalKpiStatus(
                kind=EducationalKpiStatusService.KIND_SCHEDULE_PACE,
                code=CODE_CURRICULUM_COMPLETE,
                label="Curriculum Complete",
                evidence_summary=(
                    "All measured curriculum topics are complete; "
                    "focus on revision within remaining calendar time."
                ),
                severity=SEVERITY_INFO,
            )

        if days_remaining <= _LIMITED_TIME_DAYS and hours_surplus_or_deficit < 0:
            evidence = EducationalKpiStatusService._hours_evidence(
                hours_surplus_or_deficit,
                remaining_hours,
                available_study_hours,
                days_remaining,
            )
            return EducationalKpiStatus(
                kind=EducationalKpiStatusService.KIND_SCHEDULE_PACE,
                code=CODE_LIMITED_TIME,
                label="Limited Time Remaining",
                evidence_summary=evidence,
                severity=SEVERITY_URGENT,
            )

        if hours_surplus_or_deficit >= _COMFORTABLE_SURPLUS_HOURS:
            return EducationalKpiStatus(
                kind=EducationalKpiStatusService.KIND_SCHEDULE_PACE,
                code=CODE_COMFORTABLE_PACE,
                label="Comfortable Pace",
                evidence_summary=EducationalKpiStatusService._hours_evidence(
                    hours_surplus_or_deficit,
                    remaining_hours,
                    available_study_hours,
                    days_remaining,
                ),
                severity=SEVERITY_INFO,
            )

        if hours_surplus_or_deficit >= 0:
            return EducationalKpiStatus(
                kind=EducationalKpiStatusService.KIND_SCHEDULE_PACE,
                code=CODE_PACE_MATCHES_PLAN,
                label="Pace Matches Plan",
                evidence_summary=EducationalKpiStatusService._hours_evidence(
                    hours_surplus_or_deficit,
                    remaining_hours,
                    available_study_hours,
                    days_remaining,
                ),
                severity=SEVERITY_INFO,
            )

        if hours_surplus_or_deficit >= _TIGHT_DEFICIT_HOURS:
            return EducationalKpiStatus(
                kind=EducationalKpiStatusService.KIND_SCHEDULE_PACE,
                code=CODE_SCHEDULE_TIGHT,
                label="Schedule Tight",
                evidence_summary=EducationalKpiStatusService._hours_evidence(
                    hours_surplus_or_deficit,
                    remaining_hours,
                    available_study_hours,
                    days_remaining,
                ),
                severity=SEVERITY_ATTENTION,
            )

        return EducationalKpiStatus(
            kind=EducationalKpiStatusService.KIND_SCHEDULE_PACE,
            code=CODE_HIGH_REMAINING_WORKLOAD,
            label="High Remaining Workload",
            evidence_summary=EducationalKpiStatusService._hours_evidence(
                hours_surplus_or_deficit,
                remaining_hours,
                available_study_hours,
                days_remaining,
            ),
            severity=SEVERITY_URGENT,
        )

    @staticmethod
    def from_time_summary(
        time_summary: _HoursBalance,
        days_remaining: int,
        *,
        coverage_pct: float | None = None,
    ) -> EducationalKpiStatus:
        """Derive status from a TimeEngine ``TimeSummary`` and calendar days."""
        return EducationalKpiStatusService.from_time_balance(
            days_remaining=days_remaining,
            hours_surplus_or_deficit=time_summary.hours_surplus_or_deficit,
            remaining_hours=time_summary.remaining_hours,
            available_study_hours=time_summary.available_study_hours,
            coverage_pct=coverage_pct,
        )

    @staticmethod
    def from_days_remaining(days_remaining: int) -> EducationalKpiStatus:
        """Calendar-only fallback when hours balance is unavailable.

        Does not claim behind/ahead — only states time facts the system knows.
        """
        if days_remaining <= 0:
            return EducationalKpiStatus(
                kind=EducationalKpiStatusService.KIND_SCHEDULE_PACE,
                code=CODE_EXAM_PERIOD,
                label="Exam Period",
                evidence_summary="Exam date has arrived or passed.",
                severity=SEVERITY_ATTENTION,
            )

        if days_remaining <= _LIMITED_TIME_DAYS:
            return EducationalKpiStatus(
                kind=EducationalKpiStatusService.KIND_SCHEDULE_PACE,
                code=CODE_LIMITED_TIME,
                label="Limited Time Remaining",
                evidence_summary=(
                    f"{days_remaining} calendar day"
                    f"{'s' if days_remaining != 1 else ''} until the exam date."
                ),
                severity=SEVERITY_ATTENTION,
            )

        return EducationalKpiStatus(
            kind=EducationalKpiStatusService.KIND_SCHEDULE_PACE,
            code=CODE_PLAN_ACTIVE,
            label="Plan Active",
            evidence_summary=(
                f"{days_remaining} calendar days remaining until the exam date. "
                "Workload balance is not yet calculated."
            ),
            severity=SEVERITY_NEUTRAL,
        )

    @staticmethod
    def _hours_evidence(
        surplus: float,
        remaining_hours: float | None,
        available_study_hours: float | None,
        days_remaining: int,
    ) -> str:
        parts = [f"{days_remaining} days remaining"]
        if remaining_hours is not None and available_study_hours is not None:
            parts.append(
                f"{remaining_hours:.0f}h remaining curriculum work vs "
                f"{available_study_hours:.0f}h planned available"
            )
        if surplus >= 0:
            parts.append(f"{surplus:.0f}h surplus vs plan")
        else:
            parts.append(f"{abs(surplus):.0f}h deficit vs plan")
        return "; ".join(parts) + "."
