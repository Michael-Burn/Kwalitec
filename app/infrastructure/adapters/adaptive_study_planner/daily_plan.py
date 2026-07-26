"""Assemble Adaptive daily study plan from Canonical planner inputs (EP-001.2).

Planner-owned scheduling outputs. Uses Twin signals for prioritisation and
workload guardrails — never invents learner state.

EP-003.3: readiness-informed workload guardrails (via Twin consistency /
missed-session signals), recommendation-aware slot ordering (P-001.3 ladder
aligned: review → recovery/weak → progression), balanced minute allocation,
and adaptive recovery after missed sessions. Does not call ReadinessService
or RecommendationService — those remain sibling authorities consumed only
from PlanningService quality packaging.
"""

from __future__ import annotations

from datetime import date

from app.infrastructure.adapters.adaptive_study_planner.contracts import (
    PLANNER_CONSUMER_VERSION,
    AdaptivePlannerInputs,
    DailyStudyPlanProjection,
    MissionSlot,
    RecommendedWorkload,
    RevisionPriority,
    TopicPlanRow,
)
from app.infrastructure.adapters.digital_twin.contracts import (
    AUTHORITY_RUNTIME_A,
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
)

# Consistency / persistence labels that warrant a lighter load (deterministic).
_LIGHT_LOAD_LABELS = frozenset(
    {
        "irregular",
        "inconsistent",
        "fragile",
        "low",
        "struggling",
        "interrupted",
        "sparse",
    }
)

_WEAK_MASTERY_THRESHOLD = 60.0

# Slot weights for balanced daily workload (sum = 100).
_SLOT_WEIGHTS = {
    "review": 35,
    "recovery": 35,
    "weak": 35,
    "progression": 30,
}


def _is_due_for_review(row: TopicPlanRow, plan_date: date) -> bool:
    if not row.next_review_date:
        return False
    try:
        due = date.fromisoformat(str(row.next_review_date)[:10])
    except ValueError:
        return False
    return due <= plan_date


def _revision_priorities(
    topics: tuple[TopicPlanRow, ...],
) -> tuple[RevisionPriority, ...]:
    candidates = [
        row
        for row in topics
        if row.completed
        and row.mastery_score is not None
        and row.mastery_score < 70.0
    ]
    candidates.sort(
        key=lambda r: (
            r.mastery_score if r.mastery_score is not None else 999.0,
            r.topic_id,
        )
    )
    if not candidates:
        # Fall back: lowest mastery among completed topics.
        completed = [row for row in topics if row.completed]
        completed.sort(
            key=lambda r: (
                r.mastery_score if r.mastery_score is not None else 999.0,
                r.topic_id,
            )
        )
        candidates = completed[:3]
    priorities: list[RevisionPriority] = []
    for rank, row in enumerate(candidates[:5], start=1):
        score = row.mastery_score
        reason = (
            f"Completed topic with mastery {score:.0f}% — revision priority"
            if score is not None
            else "Completed topic — revision priority from Canonical progress"
        )
        priorities.append(
            RevisionPriority(
                topic_id=row.topic_id,
                topic_name=row.topic_name,
                mastery_score=score,
                reason=reason,
                rank=rank,
            )
        )
    return tuple(priorities)


def _recovery_active(inputs: AdaptivePlannerInputs) -> bool:
    return int(inputs.mission_missed_count or 0) > 0


def _today_missions(
    inputs: AdaptivePlannerInputs,
    *,
    plan_date: date,
    revision_priorities: tuple[RevisionPriority, ...],
) -> tuple[MissionSlot, ...]:
    """Build today's slots in recommendation-aware Decision Framework order.

    Order: review (routine revision / due) → recovery or weak → progression.
    After missed sessions, prefer recovery over new progression (adaptive
    recovery) so the day stays coherent and completable.
    """
    slots: list[MissionSlot] = []
    topics = inputs.topics
    used: set[str] = set()
    recovering = _recovery_active(inputs)
    missed = int(inputs.mission_missed_count or 0)

    # Review slot — spaced repetition from Canonical next_review_date.
    due = [row for row in topics if _is_due_for_review(row, plan_date)]
    due.sort(
        key=lambda r: (
            r.next_review_date or "",
            r.mastery_score if r.mastery_score is not None else 999.0,
            r.topic_id,
        )
    )
    if due:
        row = due[0]
        used.add(row.topic_id)
        slots.append(
            MissionSlot(
                slot="review",
                topic_id=row.topic_id,
                topic_name=row.topic_name,
                reason=f"Due for review (scheduled {row.next_review_date})",
                priority="high",
                expected_benefit=(
                    "Maintain spaced repetition and prevent knowledge decay."
                ),
            )
        )

    # Weak / recovery slot — from mastery payload (recommendation-aware weak focus).
    weak = [
        row
        for row in topics
        if row.topic_id not in used
        and row.mastery_score is not None
        and row.mastery_score < _WEAK_MASTERY_THRESHOLD
    ]
    weak.sort(key=lambda r: (r.mastery_score or 999.0, r.topic_id))
    if weak:
        row = weak[0]
        used.add(row.topic_id)
        if recovering:
            slots.append(
                MissionSlot(
                    slot="recovery",
                    topic_id=row.topic_id,
                    topic_name=row.topic_name,
                    reason=(
                        f"Recovery focus after {missed} missed session(s) — "
                        f"weak topic (mastery {row.mastery_score:.0f}%)"
                    ),
                    priority="high",
                    expected_benefit=(
                        "Rebuild study rhythm on the weakest area before "
                        "adding new syllabus progress."
                    ),
                )
            )
        else:
            slots.append(
                MissionSlot(
                    slot="weak",
                    topic_id=row.topic_id,
                    topic_name=row.topic_name,
                    reason=(
                        f"Weak topic (mastery {row.mastery_score:.0f}% "
                        f"— below {_WEAK_MASTERY_THRESHOLD:.0f}% threshold)"
                    ),
                    priority="high",
                    expected_benefit=(
                        "Improve weakest area for maximum readiness gain "
                        "per study hour."
                    ),
                )
            )
    elif revision_priorities:
        top = revision_priorities[0]
        if top.topic_id not in used:
            used.add(top.topic_id)
            slot_name = "recovery" if recovering else "weak"
            reason = (
                f"Recovery consolidation after {missed} missed session(s) — "
                f"{top.reason}"
                if recovering
                else top.reason
            )
            slots.append(
                MissionSlot(
                    slot=slot_name,
                    topic_id=top.topic_id,
                    topic_name=top.topic_name,
                    reason=reason,
                    priority="high" if recovering else "medium",
                    expected_benefit=(
                        "Rebuild confidence on a weaker completed topic."
                        if recovering
                        else (
                            "Consolidate a weaker completed topic from "
                            "Canonical state."
                        )
                    ),
                )
            )

    # Progression slot — Learning Mode only (first incomplete).
    # Adaptive recovery: when missed sessions and we already have review +
    # recovery/weak, skip progression to keep a balanced, completable day.
    stage = (inputs.lifecycle_stage or "").strip().lower()
    skip_progression = recovering and len(slots) >= 2
    if stage != "revision" and not skip_progression:
        for row in topics:
            if not row.completed and row.topic_id not in used:
                used.add(row.topic_id)
                slots.append(
                    MissionSlot(
                        slot="progression",
                        topic_id=row.topic_id,
                        topic_name=row.topic_name,
                        reason="Next incomplete topic from Canonical progress",
                        priority="medium",
                        expected_benefit=(
                            "Continue forward progress through the syllabus."
                        ),
                    )
                )
                break

    return tuple(slots)


def _allocate_minutes(
    missions: tuple[MissionSlot, ...],
    *,
    recommended_minutes: int,
) -> tuple[MissionSlot, ...]:
    """Distribute recommended minutes across slots (balanced daily workload)."""
    if not missions:
        return missions
    total = max(0, int(recommended_minutes))
    if total <= 0:
        return tuple(
            MissionSlot(
                slot=m.slot,
                topic_id=m.topic_id,
                topic_name=m.topic_name,
                reason=m.reason,
                priority=m.priority,
                expected_benefit=m.expected_benefit,
                allocated_minutes=0,
            )
            for m in missions
        )

    weights = [_SLOT_WEIGHTS.get(m.slot, 30) for m in missions]
    weight_sum = sum(weights) or len(missions)
    allocated: list[int] = []
    remaining = total
    for index, weight in enumerate(weights):
        if index == len(weights) - 1:
            allocated.append(max(0, remaining))
        else:
            raw_share = int(round(total * weight / weight_sum))
            share = max(5, raw_share) if total >= 15 else max(0, raw_share)
            share = min(share, remaining)
            allocated.append(share)
            remaining -= share

    return tuple(
        MissionSlot(
            slot=m.slot,
            topic_id=m.topic_id,
            topic_name=m.topic_name,
            reason=m.reason,
            priority=m.priority,
            expected_benefit=m.expected_benefit,
            allocated_minutes=mins,
        )
        for m, mins in zip(missions, allocated, strict=True)
    )


def _topic_ordering(topics: tuple[TopicPlanRow, ...]) -> tuple[dict, ...]:
    """Ordered study sequence: incomplete syllabus leaves, then weak completed."""
    ordering: list[dict] = []
    for index, row in enumerate(topics, start=1):
        ordering.append(
            {
                "position": index,
                "topic_id": row.topic_id,
                "topic_name": row.topic_name,
                "completed": row.completed,
                "mastery_score": row.mastery_score,
                "current_stage": row.current_stage,
                "role": "progression" if not row.completed else "revision_pool",
            }
        )
    return tuple(ordering)


def _recommend_workload(
    inputs: AdaptivePlannerInputs,
    *,
    available_study_minutes: int,
) -> RecommendedWorkload:
    base = max(0, int(available_study_minutes))
    preferred = inputs.preferred_session_minutes
    recommended = base
    reasons: list[str] = [
        f"Plan capacity for today is {base} minutes (StudyPlan / TimeEngine)."
    ]

    if preferred is not None and preferred > 0:
        recommended = min(recommended, preferred) if recommended > 0 else preferred
        reasons.append(
            f"Canonical preferences prefer sessions of {preferred} minutes."
        )

    labels = " ".join(
        [
            inputs.consistency_label,
            *inputs.behaviour_labels.values(),
        ]
    ).lower()
    if any(token in labels for token in _LIGHT_LOAD_LABELS) and recommended > 20:
        reduced = max(20, int(recommended * 0.9))
        if reduced < recommended:
            reasons.append(
                "Consistency / behaviour signals suggest a slightly lighter load "
                f"({inputs.consistency_label or 'behaviour facet'})."
            )
            recommended = reduced

    # Adaptive recovery after missed sessions — protect completable days.
    missed = int(inputs.mission_missed_count or 0)
    if missed > 0 and recommended > 20:
        factor = max(0.75, 1.0 - 0.05 * min(missed, 4))
        reduced = max(20, int(recommended * factor))
        if reduced < recommended:
            reasons.append(
                f"Adaptive recovery after {missed} missed session(s) — "
                "slightly lighter load to rebuild consistency."
            )
            recommended = reduced

    streak = inputs.current_streak
    if streak is not None and streak >= 3 and recommended == base and missed == 0:
        reasons.append(
            f"Current streak of {streak} days supports sustaining planned capacity."
        )

    if recommended == 0 and base == 0:
        reasons.append("No available study minutes configured on the active plan.")

    return RecommendedWorkload(
        available_study_minutes=base,
        recommended_minutes=recommended,
        rationale=" ".join(reasons),
        authority=AUTHORITY_RUNTIME_A,
    )


def _plan_coherence_label(missions: tuple[MissionSlot, ...]) -> str:
    """Label whether slot mix follows recommendation-aware ladder order."""
    order = [m.slot for m in missions]
    if not order:
        return "empty"
    allowed = {"review", "recovery", "weak", "progression"}
    if any(slot not in allowed for slot in order):
        return "mixed"
    # Review before weak/recovery before progression is coherent.
    rank = {"review": 0, "recovery": 1, "weak": 1, "progression": 2}
    ranks = [rank[s] for s in order]
    if ranks == sorted(ranks):
        return "aligned"
    return "reordered"


class DailyStudyPlanAssembler:
    """Assemble DailyStudyPlanProjection from AdaptivePlannerInputs + capacity."""

    ASSEMBLER_ID = "daily_study_plan_assembler"
    ASSEMBLER_VERSION = PLANNER_CONSUMER_VERSION

    def assemble(
        self,
        inputs: AdaptivePlannerInputs,
        *,
        plan_date: date,
        available_study_minutes: int,
    ) -> DailyStudyPlanProjection:
        if not isinstance(inputs, AdaptivePlannerInputs):
            raise TypeError("inputs must be AdaptivePlannerInputs")

        if inputs.availability != AVAILABILITY_AVAILABLE:
            empty_workload = RecommendedWorkload(
                available_study_minutes=max(0, int(available_study_minutes)),
                recommended_minutes=0,
                rationale="Canonical Learner State unavailable — no adaptive plan.",
            )
            return DailyStudyPlanProjection(
                student_id=inputs.student_id,
                as_of=inputs.as_of,
                plan_date=plan_date.isoformat(),
                consumer_version=PLANNER_CONSUMER_VERSION,
                foundation_version=inputs.foundation_version,
                twin_id=inputs.twin_id,
                availability=AVAILABILITY_UNAVAILABLE,
                unavailable_reason=inputs.unavailable_reason,
                lifecycle_stage=inputs.lifecycle_stage,
                today_missions=(),
                revision_priorities=(),
                topic_ordering=(),
                recommended_workload=empty_workload,
                provenance_refs=inputs.provenance_refs,
                limitations_codes=inputs.limitations_codes,
                explainability={
                    "source": "canonical_learner_state",
                    "status": "unavailable",
                },
            )

        revision = _revision_priorities(inputs.topics)
        missions = _today_missions(
            inputs, plan_date=plan_date, revision_priorities=revision
        )
        ordering = _topic_ordering(inputs.topics)
        workload = _recommend_workload(
            inputs, available_study_minutes=available_study_minutes
        )
        missions = _allocate_minutes(
            missions, recommended_minutes=workload.recommended_minutes
        )
        recovering = _recovery_active(inputs)
        coherence = _plan_coherence_label(missions)

        return DailyStudyPlanProjection(
            student_id=inputs.student_id,
            as_of=inputs.as_of,
            plan_date=plan_date.isoformat(),
            consumer_version=PLANNER_CONSUMER_VERSION,
            foundation_version=inputs.foundation_version,
            twin_id=inputs.twin_id,
            availability=AVAILABILITY_AVAILABLE,
            unavailable_reason="",
            lifecycle_stage=inputs.lifecycle_stage,
            today_missions=missions,
            revision_priorities=revision,
            topic_ordering=ordering,
            recommended_workload=workload,
            provenance_refs=inputs.provenance_refs,
            limitations_codes=inputs.limitations_codes,
            explainability={
                "source": "canonical_learner_state",
                "evidence_attempt_count": inputs.evidence_attempt_count,
                "current_streak": inputs.current_streak,
                "consistency_label": inputs.consistency_label,
                "behaviour_labels": dict(inputs.behaviour_labels),
                "mission_slots": [m.slot for m in missions],
                "mission_missed_count": int(inputs.mission_missed_count or 0),
                "recovery_mode": recovering,
                "plan_coherence": coherence,
                "recommendation_aware_order": True,
                "quality_contract": "ep003.3-assembler",
            },
        )


def build_daily_study_plan_assembler() -> DailyStudyPlanAssembler:
    return DailyStudyPlanAssembler()


__all__ = [
    "DailyStudyPlanAssembler",
    "build_daily_study_plan_assembler",
]
