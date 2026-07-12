"""Pure execution-layer Mission Intelligence.

Operationalises Decision(s) into an attributable Mission. Never re-selects,
never invents ranking or filler, never mutates Twin, never recomputes readiness,
never calls DecisionEngine, never owns Recommendation packaging or WeekPlan.
"""

from __future__ import annotations

from collections.abc import Sequence

from app.domain.decision.decision import Decision
from app.domain.mission.attribution import DecisionAttribution, DecisionCitation
from app.domain.mission.context import MissionExecutionContext
from app.domain.mission.evidence_hooks import MissionEvidenceHooks
from app.domain.mission.feasibility import (
    FeasibilityAcknowledgement,
    FeasibilityEffect,
)
from app.domain.mission.load_shaping import (
    intensity_demotion_required,
    resolve_include_count,
)
from app.domain.mission.mission import (
    MISSION_INTELLIGENCE_VERSION,
    Mission,
    MissionRegenerationIdentity,
    MissionScope,
)
from app.domain.mission.sequencing import authorise_prefix, preserve_decision_order
from app.domain.mission.task import MissionTask, RecommendationLanguageHook
from app.domain.mission.warrant import (
    THIN_MISSION_WARRANT_POSTURES,
    aggregate_mission_warrant,
    inherit_mission_warrant,
)
from app.domain.recommendation.recommendation import Recommendation


class MissionIntelligence:
    """Pure compose API for structural Mission Intelligence.

    Observational / projection only: reads Decision(s) + execution context;
    never calls Update Strategies, never mutates inputs, never re-selects,
    never invents filler tasks.
    """

    @staticmethod
    def compose(
        decision_or_batch: Decision | Sequence[Decision],
        execution_context: MissionExecutionContext,
        recommendation_language: Recommendation | None = None,
    ) -> Mission:
        """Compose a frozen ``Mission`` from Decision authority + context.

        Args:
            decision_or_batch: One Decision or an ordered Decision batch
                (Decision-authored educational order).
            execution_context: Goals / Constraints / session capacity bounds.
            recommendation_language: Optional Decision-faithful packaging
                language — never selection or sequencing authority.

        Returns:
            Immutable Mission projecting authorised Decision action(s).

        Raises:
            ValueError: If Decision batch empty or preconditions fail.
        """
        decisions = _bind_decision_batch(decision_or_batch)
        _validate_preconditions(decisions)
        ordered = preserve_decision_order(decisions)

        include_count, feasibility_acks = resolve_include_count(
            ordered, execution_context
        )
        included, _omitted = authorise_prefix(ordered, include_count)

        intensity_demote = intensity_demotion_required(execution_context)
        language_hook = _optional_language_hook(recommendation_language, ordered)
        evidence_hooks = MissionEvidenceHooks.default_behaviour_hooks(
            journal_or_recording_refs=execution_context.journal_history_refs,
        )

        tasks = _operationalise_tasks(
            included,
            intensity_demote=intensity_demote,
            language_hook=language_hook,
            evidence_hooks=evidence_hooks,
            execution_context=execution_context,
        )

        # Aggregate feasibility: ensure empty remainder is explicit when no tasks.
        acks = list(feasibility_acks)
        if not tasks and not any(
            a.effect == FeasibilityEffect.EMPTY_CAPACITY_REMAINDER for a in acks
        ):
            acks.append(
                FeasibilityAcknowledgement.create(
                    FeasibilityEffect.EMPTY_CAPACITY_REMAINDER,
                    note_tags=(
                        "empty_capacity_remainder",
                        "no_filler_invented",
                    ),
                )
            )

        warrant = aggregate_mission_warrant(
            tuple(d.warrant_posture for d in ordered)
        )
        # Thin warrant must survive; never coerce Mid/High packing theatre.
        if warrant in THIN_MISSION_WARRANT_POSTURES:
            acks.append(
                FeasibilityAcknowledgement.create(
                    FeasibilityEffect.INCLUDED_AS_AUTHORISED,
                    note_tags=(
                        "thin_warrant_honesty_preserved",
                        "no_mid_high_preparedness_coercion",
                        "cold_start_or_low_warrant_execution",
                    ),
                )
            )

        primary = ordered[0]
        scope = MissionScope.from_decision_scope(
            primary.scope,
            session_window_id=execution_context.session_window_id,
            session_date=execution_context.session_date,
        )
        citations = tuple(
            DecisionCitation.from_decision(d, batch_index=i)
            for i, d in enumerate(ordered)
        )
        regeneration = MissionRegenerationIdentity.create(
            decision_evaluation_ids=tuple(
                d.evaluation_id for d in ordered if d.evaluation_id
            ),
            decision_engine_versions=tuple(
                dict.fromkeys(d.engine_version for d in ordered)
            ),
            twin_snapshot_ref=execution_context.twin_snapshot_ref,
            compose_version=MISSION_INTELLIGENCE_VERSION,
            session_window_id=execution_context.session_window_id,
        )

        return Mission.create(
            scope=scope,
            tasks=tasks,
            decision_citations=citations,
            warrant_posture=warrant,
            feasibility_acknowledgements=acks,
            regeneration_identity=regeneration,
            evidence_hooks=evidence_hooks,
            curriculum_format=primary.curriculum_format,
            mission_intelligence_version=MISSION_INTELLIGENCE_VERSION,
        )


# Public alias matching DecisionEngine / RecommendationEngine naming.
MissionEngine = MissionIntelligence


# ---------------------------------------------------------------------------
# Pipeline helpers
# ---------------------------------------------------------------------------


def _bind_decision_batch(
    decision_or_batch: Decision | Sequence[Decision],
) -> tuple[Decision, ...]:
    """Bind Decision / Decision batch as sole selection authority."""
    if isinstance(decision_or_batch, Decision):
        return (decision_or_batch,)
    batch = tuple(decision_or_batch)
    if not batch:
        raise ValueError("decision_or_batch must contain at least one Decision")
    for item in batch:
        if not isinstance(item, Decision):
            raise TypeError("decision_or_batch items must be Decision instances")
    return batch


def _validate_preconditions(decisions: tuple[Decision, ...]) -> None:
    """Require selected action(s) + reason codes + warrant on the core path."""
    for decision in decisions:
        if decision.selected is None:  # pragma: no cover - typed non-optional
            raise ValueError("Decision.selected action is required for composition")
        if not decision.reason_codes:
            raise ValueError(
                "Decision.reason_codes must contain at least one code for composition"
            )
        if decision.warrant_posture is None:  # pragma: no cover
            raise ValueError("Decision.warrant_posture is required for composition")
        # Ensure selected is present in candidates (Decision contract).
        _ = decision.selected_candidate


def _optional_language_hook(
    recommendation: Recommendation | None,
    decisions: tuple[Decision, ...],
) -> RecommendationLanguageHook | None:
    """Attach Recommendation language when present and Decision-faithful.

    Priority / packaging never sequences MissionTasks.
    """
    if recommendation is None:
        return None
    primary = decisions[0]
    # Decision-faithful check: suggestion must match primary selected action.
    if recommendation.suggestion.family != primary.selected.family:
        raise ValueError(
            "recommendation_language suggestion family must match Decision selected"
        )
    if (
        recommendation.suggestion.curriculum_entity_id
        != primary.selected.curriculum_entity_id
    ):
        raise ValueError(
            "recommendation_language curriculum scope must match Decision selected"
        )
    return RecommendationLanguageHook.create(
        packaging_version=recommendation.packaging_version,
        presentation_tags=recommendation.suggestion.presentation_tags,
        communication_tags=recommendation.communication_tags,
        suggestion_family=recommendation.suggestion.family.value,
        suggestion_curriculum_entity_id=(
            recommendation.suggestion.curriculum_entity_id
        ),
    )


def _operationalise_tasks(
    included: tuple[Decision, ...],
    *,
    intensity_demote: bool,
    language_hook: RecommendationLanguageHook | None,
    evidence_hooks: MissionEvidenceHooks,
    execution_context: MissionExecutionContext,
) -> tuple[MissionTask, ...]:
    """Map authorised Decision actions to MissionTasks — no re-selection."""
    tasks: list[MissionTask] = []
    for index, decision in enumerate(included):
        attribution = DecisionAttribution.from_decision(decision, batch_index=index)
        warrant = inherit_mission_warrant(decision.warrant_posture)
        feasibility = _task_feasibility(decision, intensity_demote=intensity_demote)
        # Language attaches only to the primary (batch index 0) when present.
        hook = language_hook if index == 0 else None
        eval_id = decision.evaluation_id or f"batch-{index}"
        task_id = (
            f"task-{index}-{decision.selected.family.value}-"
            f"{decision.selected.curriculum_entity_id or 'unscoped'}-{eval_id}"
        )
        # Structural cold-start tag: diagnostic Decisions stay diagnostic-shaped.
        _ = execution_context  # capacity already applied via include prefix
        tasks.append(
            MissionTask.create(
                task_id=task_id,
                sequence_position=index,
                family=decision.selected.family,
                curriculum_entity_id=decision.selected.curriculum_entity_id,
                intent=decision.selected.intent,
                attribution=attribution,
                warrant_posture=warrant,
                feasibility=feasibility,
                evidence_hooks=evidence_hooks,
                recommendation_language=hook,
                intensity_demoted=intensity_demote,
            )
        )
    return tuple(tasks)


def _task_feasibility(
    decision: Decision,
    *,
    intensity_demote: bool,
) -> FeasibilityAcknowledgement:
    """Per-task feasibility acknowledgement (inclusion / intensity only)."""
    notes: list[str] = ["decision_authorised_inclusion"]
    if decision.constraint_acknowledgements:
        notes.append("upstream_decision_constraints_honoured")
    if intensity_demote:
        notes.extend(
            [
                "intensity_demoted_under_sustainability",
                "action_family_unchanged",
                "rest_protect_not_failure",
            ]
        )
        return FeasibilityAcknowledgement.create(
            FeasibilityEffect.INTENSITY_DEMOTED,
            note_tags=notes,
        )
    return FeasibilityAcknowledgement.create(
        FeasibilityEffect.INCLUDED_AS_AUTHORISED,
        note_tags=notes,
    )
