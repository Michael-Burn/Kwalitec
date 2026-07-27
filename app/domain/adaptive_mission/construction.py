"""Construct an AdaptiveMission from a prioritised educational candidate.

Pure construction — no I/O, no LLM, no educational reasoning.
"""

from __future__ import annotations

import hashlib
from datetime import UTC, date, datetime

from app.domain.adaptive_mission.adaptive_mission import AdaptiveMission
from app.domain.adaptive_mission.mission import Mission, MissionStatus
from app.domain.adaptive_mission.mission_objective import MissionObjective
from app.domain.adaptive_mission.mission_outcome import MissionOutcome
from app.domain.adaptive_mission.mission_plan import MissionPlan
from app.domain.adaptive_mission.mission_progress import MissionProgress
from app.domain.adaptive_mission.mission_reason import MissionReason
from app.domain.adaptive_mission.mission_schedule import MissionSchedule
from app.domain.adaptive_mission.mission_step import (
    ActivityType,
    MissionActivity,
    MissionStep,
)
from app.domain.adaptive_mission.prioritisation import MissionCandidate


def construct_mission(
    *,
    twin_id: str,
    student_id: str,
    mission_date: date,
    candidate: MissionCandidate,
    mission_id: str | None = None,
    reasoning_run_id: str = "",
    created_at: datetime | None = None,
    available_minutes: int = 45,
) -> AdaptiveMission:
    """Build one daily AdaptiveMission from a prioritised candidate."""
    when = created_at or datetime.now(UTC).replace(tzinfo=None)
    mid = mission_id or _mission_id(twin_id, mission_date, candidate.concept_id)
    concept_id = candidate.concept_id
    title = candidate.concept_title or concept_id

    recovery_ids = (
        tuple(candidate.recovery_path.concept_ids)
        if candidate.recovery_path is not None
        else ()
    )
    prereq_ids = tuple(c for c in recovery_ids if c != concept_id)

    steps = _build_steps(
        mission_id=mid,
        concept_id=concept_id,
        concept_title=title,
        prereq_ids=prereq_ids,
        evidence_ids=candidate.evidence_ids,
        available_minutes=available_minutes,
        needs_recovery=candidate.gap is not None,
    )
    duration = sum(s.activity.estimated_minutes for s in steps)
    concepts = tuple(dict.fromkeys([*prereq_ids, concept_id]))

    objective = MissionObjective(
        objective_id=f"obj-{mid}",
        statement=_objective_statement(candidate, title),
        primary_concept_id=concept_id,
        supporting_concept_ids=prereq_ids,
        source_recommendation_id=(
            candidate.recommendation.recommendation_id
            if candidate.recommendation
            else ""
        ),
        source_gap_id=candidate.gap.gap_id if candidate.gap else "",
    )
    plan = MissionPlan(
        plan_id=f"plan-{mid}",
        objective=objective,
        steps=steps,
        concepts_covered=concepts,
        estimated_duration_minutes=duration,
    )
    reflection_minutes = min(5, max(3, duration // 10))
    schedule = MissionSchedule(
        total_minutes=duration,
        focus_block_minutes=max(1, duration - reflection_minutes),
        reflection_minutes=reflection_minutes,
        allocation_note=(
            "Abstract time budget for today's session — no clock scheduling."
        ),
    )
    reason = MissionReason(
        summary=_reason_summary(candidate, title),
        educational_explanation=candidate.priority_score.explanation,
        decision_references=tuple(
            filter(
                None,
                (
                    candidate.recommendation.recommendation_id
                    if candidate.recommendation
                    else "",
                    candidate.gap.gap_id if candidate.gap else "",
                ),
            )
        ),
        recommendation_ids=(
            (candidate.recommendation.recommendation_id,)
            if candidate.recommendation
            else ()
        ),
        gap_ids=((candidate.gap.gap_id,) if candidate.gap else ()),
        recovery_path_concept_ids=recovery_ids,
        evidence_ids=candidate.evidence_ids,
        graph_influence=(
            candidate.recovery_path.reason
            if candidate.recovery_path is not None
            else "No Learning Graph recovery path attached."
        ),
    )
    outcome = MissionOutcome(
        outcome_id=f"out-{mid}",
        statement=(
            f"Improve understanding of {title} through focused "
            f"{'recovery and practice' if candidate.gap else 'practice'}."
        ),
        target_concept_id=concept_id,
        expected_mastery_delta=0.05 if candidate.gap else 0.03,
        success_signals=(
            "Complete all mission steps",
            "Answer reflection prompt honestly",
            "Demonstrate reduced uncertainty on the primary concept",
        ),
    )
    success_criteria = (
        f"Complete prerequisite recovery for {title}"
        if prereq_ids
        else f"Engage primary concept {title}",
        "Finish the focus practice or recovery activity",
        "Complete the reflection step",
    )
    progress = MissionProgress.from_steps(
        progress_id=f"prog-{mid}",
        mission_id=mid,
        steps_total=len(steps),
        steps_completed=0,
        updated_at=when,
    )
    goal = f"Today: strengthen {title}"
    identity = Mission(
        mission_id=mid,
        twin_id=twin_id,
        student_id=student_id,
        mission_date=mission_date,
        status=MissionStatus.DRAFT,
        goal=goal,
    )
    return AdaptiveMission(
        identity=identity,
        objective=objective,
        plan=plan,
        schedule=schedule,
        reason=reason,
        expected_outcome=outcome,
        priority=candidate.priority,
        success_criteria=success_criteria,
        reflection_prompt=(
            f"What felt clearer about {title} after today's session, "
            "and what still needs another pass?"
        ),
        progress=progress,
        evidence_references=candidate.evidence_ids,
        concepts_covered=concepts,
        estimated_duration_minutes=duration,
        source_recommendation_ids=reason.recommendation_ids,
        source_gap_ids=reason.gap_ids,
        reasoning_run_id=reasoning_run_id or "",
        validation_passed=False,
        validation_summary="",
        created_at=when,
        updated_at=when,
        version=1,
    )


def _build_steps(
    *,
    mission_id: str,
    concept_id: str,
    concept_title: str,
    prereq_ids: tuple[str, ...],
    evidence_ids: tuple[str, ...],
    available_minutes: int,
    needs_recovery: bool,
) -> tuple[MissionStep, ...]:
    steps: list[MissionStep] = []
    order = 1
    budget = max(20, int(available_minutes))

    # Cap prerequisite reviews so one day stays focused.
    for prereq in prereq_ids[:2]:
        minutes = min(10, max(5, budget // 6))
        steps.append(
            MissionStep(
                step_id=f"{mission_id}-s{order}",
                order=order,
                activity=MissionActivity(
                    activity_type=ActivityType.PREREQUISITE_REVIEW,
                    concept_id=prereq,
                    title=f"Prerequisite review: {prereq}",
                    estimated_minutes=minutes,
                    reason="Learning Graph recovery path requires this foundation.",
                    evidence_references=evidence_ids,
                ),
                success_criterion=f"Recall key ideas of {prereq}",
            )
        )
        order += 1
        budget -= minutes

    if needs_recovery:
        primary_type = ActivityType.CONCEPT_RECOVERY
        primary_title = f"Concept recovery: {concept_title}"
        primary_reason = "Twin knowledge gap decision selected this concept."
    else:
        primary_type = ActivityType.PRACTICE
        primary_title = f"Practice: {concept_title}"
        primary_reason = "Twin recommendation decision selected this concept."

    primary_minutes = min(25, max(12, budget - 8))
    steps.append(
        MissionStep(
            step_id=f"{mission_id}-s{order}",
            order=order,
            activity=MissionActivity(
                activity_type=primary_type,
                concept_id=concept_id,
                title=primary_title,
                estimated_minutes=primary_minutes,
                reason=primary_reason,
                evidence_references=evidence_ids,
            ),
            success_criterion=f"Complete focused work on {concept_title}",
        )
    )
    order += 1
    budget -= primary_minutes

    if budget >= 8:
        steps.append(
            MissionStep(
                step_id=f"{mission_id}-s{order}",
                order=order,
                activity=MissionActivity(
                    activity_type=ActivityType.MIXED_QUESTIONS,
                    concept_id=concept_id,
                    title=f"Mixed questions: {concept_title}",
                    estimated_minutes=min(12, budget - 5),
                    reason="Consolidate today's concept with varied practice.",
                    evidence_references=evidence_ids,
                ),
                success_criterion=(
                    "Attempt mixed questions without looking up answers first"
                ),
            )
        )
        order += 1

    steps.append(
        MissionStep(
            step_id=f"{mission_id}-s{order}",
            order=order,
            activity=MissionActivity(
                activity_type=ActivityType.REFLECTION,
                concept_id=concept_id,
                title=f"Reflection: {concept_title}",
                estimated_minutes=5,
                reason="Capture what improved and what remains uncertain.",
                evidence_references=(),
            ),
            success_criterion="Answer the reflection prompt",
        )
    )
    return tuple(steps)


def _objective_statement(candidate: MissionCandidate, title: str) -> str:
    if candidate.gap is not None:
        return (
            f"Recover understanding of {title} by repairing prerequisite "
            "weaknesses and practising the target concept."
        )
    return (
        f"Advance mastery of {title} through focused practice aligned to "
        "today's educational recommendation."
    )


def _reason_summary(candidate: MissionCandidate, title: str) -> str:
    if candidate.recommendation is not None:
        return (
            f"Today's highest-impact session targets {title} based on "
            f"recommendation {candidate.recommendation.recommendation_id}."
        )
    if candidate.gap is not None:
        return (
            f"Today's highest-impact session targets {title} based on "
            f"knowledge gap {candidate.gap.gap_id}."
        )
    return f"Today's highest-impact session targets {title}."


def _mission_id(twin_id: str, mission_date: date, concept_id: str) -> str:
    digest = hashlib.sha256(
        f"{twin_id}|{mission_date.isoformat()}|{concept_id}".encode()
    ).hexdigest()[:16]
    return f"ame-{digest}"
