"""Educational quality rules for automatically generated learning artefacts (EQ-001)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any

EXPLANATION_SCHEMA_VERSION = "eq001/p001.2/v1"
EXPLANATION_LEVEL_MISSION = "level_1"
EXPLANATION_LEVEL_JOURNEY = "level_2"

CONFIDENCE_HIGH = "High confidence"
CONFIDENCE_MODERATE = "Moderate confidence"
CONFIDENCE_LOW = "Low confidence / Suggested"

COMPLETION_DEFINITION_TEMPLATE = (
    "Complete all listed mission tasks for {topic_code} on this study day. "
    "Mission completion records study progress for the topic; "
    "it does not certify mastery or Exam Ready status."
)

REVISION_RATIO_DEFAULT = 0.20
REVISION_FLOOR_MINUTES_DEFAULT = 60
WEEKDAY_MINUTES_DEFAULT = 90
WEEKEND_MINUTES_DEFAULT = 120

FORBIDDEN_JARGON = (
    "twin",
    "adaptive engine",
    "warrant",
    "pipeline",
    "entity_id",
    "runtime c",
    "pi-001",
)


@dataclass(frozen=True)
class QualityIssue:
    rule_id: str
    severity: str
    message: str
    artefact_id: str = ""


@dataclass(frozen=True)
class QualityCheckResult:
    rule_id: str
    passed: bool
    message: str
    artefact_id: str = ""


@dataclass(frozen=True)
class EducationalQualityReport:
    curriculum_identity: str
    passed: bool
    checks: tuple[QualityCheckResult, ...] = field(default_factory=tuple)
    issues: tuple[QualityIssue, ...] = field(default_factory=tuple)

    @property
    def failed_rule_ids(self) -> tuple[str, ...]:
        return tuple(check.rule_id for check in self.checks if not check.passed)


def build_mission_completion_definition(*, topic_code: str) -> str:
    return COMPLETION_DEFINITION_TEMPLATE.format(topic_code=topic_code)


def build_mission_educational_rationale(
    *,
    topic_code: str,
    topic_title: str,
    objective_codes: tuple[str, ...],
    prerequisite_ids: tuple[str, ...],
) -> str:
    objective_clause = (
        f" It advances learning objective(s) {', '.join(objective_codes)}."
        if objective_codes
        else ""
    )
    prereq_clause = (
        " Prerequisites from the published syllabus are satisfied before this topic."
        if prerequisite_ids
        else " This topic is an entry point in the published syllabus order."
    )
    return (
        f"Today focuses on {topic_code} — {topic_title} because it is the next "
        f"incomplete topic in syllabus order.{objective_clause}{prereq_clause}"
    )


def build_mission_explanation(
    *,
    topic_id: str,
    topic_code: str,
    topic_title: str,
    objective_ids: tuple[str, ...],
    objective_codes: tuple[str, ...],
    estimated_duration_minutes: int,
    educational_rationale: str,
    prerequisites_satisfied: bool,
) -> dict[str, Any]:
    confidence = (
        CONFIDENCE_HIGH if prerequisites_satisfied else CONFIDENCE_LOW
    )
    evidence = [
        f"Published topic {topic_code} ({topic_id})",
        f"Estimated duration {estimated_duration_minutes} minutes",
    ]
    if objective_codes:
        evidence.append(
            "Learning objectives: " + ", ".join(objective_codes)
        )
    elif objective_ids:
        evidence.append(
            "Learning objective ids: " + ", ".join(objective_ids)
        )
    evidence.append(
        "Prerequisites satisfied"
        if prerequisites_satisfied
        else "Prerequisites not yet satisfied"
    )
    return {
        "judgement": f"Study {topic_code} — {topic_title}",
        "why_this_mission": educational_rationale,
        "why_this_plan": educational_rationale,
        "supporting_evidence": evidence,
        "confidence_level": confidence,
        "expected_benefit": (
            f"First-pass syllabus coverage progress on {topic_code}. "
            "Mission completion is study progress only, not mastery."
        ),
        "suggested_next_action": (
            f"Complete today's mission tasks for {topic_code}."
        ),
        "review_point": "After mission completion or the next study day",
        "plan_drivers": [
            "syllabus_order",
            "learning_objectives",
            "prerequisites",
            "estimated_duration",
        ],
        "explanation_schema_version": EXPLANATION_SCHEMA_VERSION,
        "explanation_level": EXPLANATION_LEVEL_MISSION,
        "explanation_schema_complete": True,
    }


def build_prerequisite_validation(
    *,
    required_ids: tuple[str, ...],
    completed_topic_ids: tuple[str, ...] | set[str],
) -> dict[str, Any]:
    completed = set(completed_topic_ids)
    satisfied = tuple(pid for pid in required_ids if pid in completed)
    missing = tuple(pid for pid in required_ids if pid not in completed)
    return {
        "required_ids": list(required_ids),
        "satisfied_ids": list(satisfied),
        "missing_ids": list(missing),
        "all_satisfied": len(missing) == 0,
    }


def build_journey_explanation(
    *,
    current_topic_id: str | None,
    current_topic_code: str | None,
    current_topic_title: str | None,
    previous_topic_id: str | None,
    previous_topic_code: str | None,
    next_topic_id: str | None,
    next_topic_code: str | None,
    next_topic_title: str | None,
    coverage_ratio: float,
    journey_stage: str,
    syllabus_complete: bool,
    completed_count: int,
    total_count: int,
) -> dict[str, Any]:
    if syllabus_complete or current_topic_id is None:
        why_today = (
            "First-pass syllabus coverage is complete for this published subject."
        )
        unlocks_next = (
            "Revision and readiness review become the lawful next posture; "
            "mission completion alone does not certify mastery."
        )
    else:
        code = current_topic_code or current_topic_id
        title = current_topic_title or code
        why_today = (
            f"Today's topic is {code} — {title} because it is the next incomplete "
            "topic in published syllabus order with satisfied prerequisites."
        )
        if next_topic_id:
            ncode = next_topic_code or next_topic_id
            ntitle = next_topic_title or ncode
            unlocks_next = (
                f"Completing today's mission unlocks {ncode} — {ntitle}."
            )
        else:
            unlocks_next = (
                "Completing today's mission completes first-pass syllabus coverage."
            )

    if previous_topic_id:
        pcode = previous_topic_code or previous_topic_id
        why_previous = (
            f"Topic {pcode} is complete because its curriculum-bound mission "
            "was completed and recorded as study progress."
        )
    else:
        why_previous = (
            "No previous topic is complete yet; this is the start of the journey."
        )

    return {
        "why_today": why_today,
        "why_previous_complete": why_previous,
        "unlocks_next": unlocks_next,
        "supporting_evidence": [
            f"Journey stage: {journey_stage}",
            f"Coverage: {completed_count} of {total_count} topics "
            f"({coverage_ratio:.0%})",
            f"Syllabus complete: {syllabus_complete}",
        ],
        "explanation_schema_version": EXPLANATION_SCHEMA_VERSION,
        "explanation_level": EXPLANATION_LEVEL_JOURNEY,
        "explanation_schema_complete": True,
    }


def project_study_plan_pacing(
    *,
    topic_templates: tuple[dict[str, Any], ...],
    exam_date: date | None,
    as_of: date,
    weekday_minutes: int = WEEKDAY_MINUTES_DEFAULT,
    weekend_minutes: int = WEEKEND_MINUTES_DEFAULT,
    revision_ratio: float = REVISION_RATIO_DEFAULT,
    revision_floor_minutes: int = REVISION_FLOOR_MINUTES_DEFAULT,
) -> dict[str, Any]:
    first_pass = sum(
        max(0, int(t.get("recommended_minutes") or 0)) for t in topic_templates
    )
    revision_minutes = max(
        revision_floor_minutes,
        int(round(first_pass * revision_ratio)),
    )
    total_required = first_pass + revision_minutes

    if exam_date is None:
        return {
            "exam_date": None,
            "exam_date_aware": False,
            "as_of": as_of.isoformat(),
            "first_pass_minutes": first_pass,
            "revision_minutes": revision_minutes,
            "revision_ratio": revision_ratio,
            "total_required_minutes": total_required,
            "available_study_minutes": None,
            "study_days_remaining": None,
            "required_average_minutes_per_study_day": None,
            "feasible": None,
            "shortfall_minutes": None,
            "weekday_minutes": weekday_minutes,
            "weekend_minutes": weekend_minutes,
            "notes": (
                "No exam date set; revision allocation is still reserved in the "
                "projection but feasibility cannot be assessed against a deadline."
            ),
        }

    if exam_date < as_of:
        return {
            "exam_date": exam_date.isoformat(),
            "exam_date_aware": True,
            "as_of": as_of.isoformat(),
            "first_pass_minutes": first_pass,
            "revision_minutes": revision_minutes,
            "revision_ratio": revision_ratio,
            "total_required_minutes": total_required,
            "available_study_minutes": 0,
            "study_days_remaining": 0,
            "required_average_minutes_per_study_day": None,
            "feasible": False,
            "shortfall_minutes": total_required,
            "weekday_minutes": weekday_minutes,
            "weekend_minutes": weekend_minutes,
            "notes": "Exam date is before the projection as-of date.",
        }

    available = 0
    study_days = 0
    cursor = as_of
    while cursor <= exam_date:
        budget = weekend_minutes if cursor.weekday() >= 5 else weekday_minutes
        if budget > 0:
            available += budget
            study_days += 1
        cursor = date.fromordinal(cursor.toordinal() + 1)

    average = (
        int(round(total_required / study_days)) if study_days > 0 else None
    )
    feasible = available >= total_required
    shortfall = 0 if feasible else total_required - available
    return {
        "exam_date": exam_date.isoformat(),
        "exam_date_aware": True,
        "as_of": as_of.isoformat(),
        "first_pass_minutes": first_pass,
        "revision_minutes": revision_minutes,
        "revision_ratio": revision_ratio,
        "total_required_minutes": total_required,
        "available_study_minutes": available,
        "study_days_remaining": study_days,
        "required_average_minutes_per_study_day": average,
        "feasible": feasible,
        "shortfall_minutes": shortfall,
        "weekday_minutes": weekday_minutes,
        "weekend_minutes": weekend_minutes,
        "notes": (
            "Pacing is feasible within the stated daily budgets."
            if feasible
            else (
                f"Honest shortfall of {shortfall} minutes against exam date; "
                "load was not silently compressed."
            )
        ),
    }


def contains_forbidden_jargon(text: str) -> bool:
    lowered = (text or "").lower()
    return any(token in lowered for token in FORBIDDEN_JARGON)
