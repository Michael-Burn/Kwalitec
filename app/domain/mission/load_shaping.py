"""Pure load-shaping helpers for Mission composition.

Demote volume / intensity under Constraints / sustainability. Never invent
filler tasks. Never re-order educational priority. Never promote rejected
Decision candidates.
"""

from __future__ import annotations

from app.domain.decision.constraints import ConstraintClass
from app.domain.decision.decision import Decision
from app.domain.mission.context import MissionExecutionContext
from app.domain.mission.feasibility import (
    FeasibilityAcknowledgement,
    FeasibilityEffect,
)

# Structural session-slot size used only to bound how many authorised Decisions
# fit — not a packing solver, not educational ranking, not minute optimisation.
_STRUCTURAL_SLOT_MINUTES = 25


def resolve_include_count(
    decisions: tuple[Decision, ...],
    context: MissionExecutionContext,
) -> tuple[int, tuple[FeasibilityAcknowledgement, ...]]:
    """How many Decision-authored actions fit under capacity honesty.

    Preserves Decision batch order: include a prefix; omit trailing unfit work
    with acknowledgement. Empty capacity is a valid remainder — not filler
    authority.

    Returns:
        (include_count, feasibility_acknowledgements)
    """
    acks: list[FeasibilityAcknowledgement] = []
    n = len(decisions)
    if n == 0:
        return 0, (
            FeasibilityAcknowledgement.create(
                FeasibilityEffect.EMPTY_CAPACITY_REMAINDER,
                note_tags=("no_decisions_to_operationalise",),
            ),
        )

    remaining = context.remaining_available_minutes
    if context.already_committed_minutes > 0:
        acks.append(
            FeasibilityAcknowledgement.create(
                FeasibilityEffect.ALREADY_COMMITTED_CAPACITY,
                constraint_class=ConstraintClass.GOAL_CAPACITY,
                note_tags=(
                    "already_committed_work_acknowledged",
                    f"committed_minutes={context.already_committed_minutes}",
                ),
            )
        )

    # Explicit max_tasks ceiling (structural — not a ranking score).
    ceiling = n
    if context.max_tasks is not None:
        ceiling = min(ceiling, context.max_tasks)

    # Zero remaining capacity → empty mission (honest remainder).
    if remaining is not None and remaining <= 0:
        acks.append(
            FeasibilityAcknowledgement.create(
                FeasibilityEffect.EMPTY_CAPACITY_REMAINDER,
                constraint_class=ConstraintClass.SESSION_TIME,
                omitted_task_refs=_decision_refs(decisions),
                note_tags=(
                    "empty_capacity_remainder",
                    "no_filler_invented",
                    "leftover_time_not_educational_authority",
                ),
            )
        )
        return 0, tuple(acks)

    # Derive structural slot count from remaining minutes when known.
    if remaining is not None:
        slot_budget = max(0, remaining // _STRUCTURAL_SLOT_MINUTES)
        if remaining > 0 and slot_budget == 0:
            # Scarce but non-zero time: allow at most one authorised task.
            slot_budget = 1
        ceiling = min(ceiling, slot_budget)

    include = min(n, ceiling)
    omitted = decisions[include:]
    if omitted:
        acks.append(
            FeasibilityAcknowledgement.create(
                FeasibilityEffect.OMITTED_TRAILING_CAPACITY,
                constraint_class=ConstraintClass.SESSION_TIME,
                omitted_task_refs=_decision_refs(omitted),
                note_tags=(
                    "trailing_omission_under_capacity",
                    "decision_order_preserved",
                    "omission_not_reselection",
                    "no_rejected_candidate_promotion",
                ),
            )
        )
        acks.append(
            FeasibilityAcknowledgement.create(
                FeasibilityEffect.VOLUME_DEMOTED,
                constraint_class=ConstraintClass.SESSION_TIME,
                note_tags=("volume_demoted_under_capacity",),
            )
        )
    elif remaining is None and context.max_tasks is None:
        acks.append(
            FeasibilityAcknowledgement.create(
                FeasibilityEffect.INCLUDED_AS_AUTHORISED,
                note_tags=("all_authorised_actions_included",),
            )
        )
    else:
        acks.append(
            FeasibilityAcknowledgement.create(
                FeasibilityEffect.INCLUDED_AS_AUTHORISED,
                note_tags=("authorised_actions_fit_capacity",),
            )
        )

    if context.protect_intensity:
        acks.append(
            FeasibilityAcknowledgement.create(
                FeasibilityEffect.SUSTAINABILITY_PROTECT,
                constraint_class=ConstraintClass.BEHAVIOUR_SUSTAINABILITY,
                note_tags=(
                    "sustainability_protect",
                    "intensity_may_demote",
                    "rest_protect_not_failure",
                ),
            )
        )

    # Honour upstream Decision constraint acknowledgements as visible tags.
    for decision in decisions[:include]:
        for ack in decision.constraint_acknowledgements:
            acks.append(
                FeasibilityAcknowledgement.create(
                    FeasibilityEffect.INTENSITY_DEMOTED
                    if ack.constraint_class
                    in (
                        ConstraintClass.INTENSITY,
                        ConstraintClass.BEHAVIOUR_SUSTAINABILITY,
                    )
                    else FeasibilityEffect.VOLUME_DEMOTED,
                    constraint_class=ack.constraint_class,
                    omitted_task_refs=ack.demoted_candidate_ids,
                    note_tags=("decision_constraint_honoured", *ack.note_tags),
                )
            )

    return include, tuple(acks)


def intensity_demotion_required(context: MissionExecutionContext) -> bool:
    """True when sustainability / protect posture demotes intensity only."""
    return context.protect_intensity


def _decision_refs(decisions: tuple[Decision, ...] | list[Decision]) -> tuple[str, ...]:
    refs: list[str] = []
    for i, decision in enumerate(decisions):
        eval_id = decision.evaluation_id or f"batch-{i}"
        family = decision.selected.family.value
        entity = decision.selected.curriculum_entity_id or "unscoped"
        refs.append(f"{eval_id}:{family}:{entity}")
    return tuple(refs)
