"""Pure read-side Decision Engine.

Selects the next learning action from Twin + ReadinessState + CurriculumContext
+ Goals + Constraints (+ optional history). Never mutates Twin, never recomputes
readiness, never scores, never packages recommendations or missions.
"""

from __future__ import annotations

from datetime import datetime

from app.domain.decision.action_types import ActionFamily, ActionIntent, SelectedAction
from app.domain.decision.candidate import (
    CandidateAction,
    CandidateStatus,
    FeasibilityEnvelope,
)
from app.domain.decision.constraints import ConstraintClass, Constraints
from app.domain.decision.decision import (
    ConstraintAcknowledgement,
    Decision,
    DecisionLineage,
    DecisionScope,
    DecisionWarrantPosture,
)
from app.domain.decision.history import DecisionHistory
from app.domain.decision.nomination import (
    TWIN_DOMAIN_BEHAVIOUR,
    TWIN_DOMAIN_CURRICULUM,
    TWIN_DOMAIN_GOALS,
    TWIN_DOMAIN_KNOWLEDGE,
    TWIN_DOMAIN_MEMORY,
    TWIN_DOMAIN_PERFORMANCE,
    evidence_ids_from_twin,
    has_confidence_shaped_input,
    highest_weight_topic_id,
    nominate_candidates,
)
from app.domain.decision.reason_codes import ENGINE_VERSION, ReasonCodeId, ReasonCodeRef
from app.domain.readiness.curriculum_context import CurriculumContext
from app.domain.readiness.factors import (
    FactorId,
    FactorPosture,
    OverallPosture,
    WarrantPosture,
)
from app.domain.readiness.readiness_state import ReadinessState
from app.domain.twin.digital_twin import DigitalTwin

# Intensive families that may be demoted under protect / scarce time.
_INTENSIVE_FAMILIES = frozenset(
    {
        ActionFamily.ASSESS,
        ActionFamily.STUDY,
        ActionFamily.REVISE,
    }
)


class DecisionEngine:
    """Pure evaluate API for structural Decision Engine.

    Observational only: reads Twin + ReadinessState + CurriculumContext;
    never calls Update Strategies or mutates inputs.
    """

    @staticmethod
    def evaluate(
        twin: DigitalTwin,
        readiness: ReadinessState,
        curriculum: CurriculumContext,
        constraints: Constraints,
        *,
        decision_history: DecisionHistory | None = None,
        as_of: datetime | None = None,
        evaluation_id: str | None = None,
    ) -> Decision:
        """Evaluate a frozen ``Decision`` from educational context inputs.

        Args:
            twin: Digital Twin snapshot (read-only; never mutated).
            readiness: ReadinessState context only (not recomputed here).
            curriculum: Framework-free syllabus identities / weights / order.
            constraints: Session feasibility envelope.
            decision_history: Optional anti-thrash context (dismiss ≠ mastery).
            as_of: Optional evaluation timestamp (omit for deterministic equality).
            evaluation_id: Optional audit identity.

        Returns:
            Immutable Decision with selected action, candidates, reasons, lineage.
        """
        history = decision_history or DecisionHistory.create()
        scope = _build_scope(twin, curriculum, readiness)
        _validate_scope_coherence(twin, curriculum, readiness)

        raw_candidates = nominate_candidates(
            twin, readiness, curriculum, constraints
        )
        ordered, acknowledgements = _apply_constraints_and_order(
            raw_candidates, constraints, readiness, curriculum, history
        )
        selected_candidate = _select_candidate(ordered, readiness, constraints)
        final_candidates = _mark_selected(ordered, selected_candidate)

        selected = SelectedAction.create(
            selected_candidate.family,
            curriculum_entity_id=selected_candidate.curriculum_entity_id,
            intent=selected_candidate.intent,
        )
        reason_codes = _author_reason_codes(
            twin=twin,
            readiness=readiness,
            curriculum=curriculum,
            constraints=constraints,
            history=history,
            selected=selected_candidate,
            acknowledgements=acknowledgements,
        )
        lineage = _build_lineage(
            twin=twin,
            readiness=readiness,
            curriculum=curriculum,
            selected=selected_candidate,
            candidates=final_candidates,
        )
        warrant_posture = _inherit_warrant_posture(readiness)

        return Decision.create(
            scope=scope,
            selected=selected,
            candidates=final_candidates,
            reason_codes=reason_codes,
            lineage=lineage,
            constraint_acknowledgements=acknowledgements,
            warrant_posture=warrant_posture,
            curriculum_format=curriculum.format,
            readiness_overall_posture=readiness.overall_posture,
            readiness_overall_warrant=readiness.overall_warrant,
            engine_version=ENGINE_VERSION,
            evaluation_id=evaluation_id,
            evaluated_at=as_of,
        )


# ---------------------------------------------------------------------------
# Assemble / validate
# ---------------------------------------------------------------------------


def _build_scope(
    twin: DigitalTwin,
    curriculum: CurriculumContext,
    readiness: ReadinessState,
) -> DecisionScope:
    curriculum_id = (
        readiness.scope.curriculum_id
        or twin.identity.curriculum_id
        or curriculum.curriculum_id
    )
    return DecisionScope.create(
        twin.identity.student_id,
        curriculum_id=curriculum_id,
        sitting_date=(
            readiness.scope.sitting_date or twin.identity.target_sitting
        ),
        exam_label=readiness.scope.exam_label or twin.identity.current_exam,
    )


def _validate_scope_coherence(
    twin: DigitalTwin,
    curriculum: CurriculumContext,
    readiness: ReadinessState,
) -> None:
    twin_curriculum = twin.identity.curriculum_id
    if (
        twin_curriculum
        and twin_curriculum != curriculum.curriculum_id
        and readiness.scope.curriculum_id
        and readiness.scope.curriculum_id != curriculum.curriculum_id
    ):
        # Soft awareness only — do not invent Mid readiness; proceed with
        # CurriculumContext as syllabus authority for nomination.
        return


# ---------------------------------------------------------------------------
# Constraint handling + educational priority ordering (structural, not scores)
# ---------------------------------------------------------------------------


def _apply_constraints_and_order(
    candidates: list[CandidateAction],
    constraints: Constraints,
    readiness: ReadinessState,
    curriculum: CurriculumContext,
    history: DecisionHistory,
) -> tuple[list[CandidateAction], tuple[ConstraintAcknowledgement, ...]]:
    working = list(candidates)
    acknowledgements: list[ConstraintAcknowledgement] = []
    demoted_ids: list[str] = []

    if constraints.protect_intensity:
        for i, candidate in enumerate(working):
            if candidate.family in _INTENSIVE_FAMILIES:
                working[i] = candidate.with_status(
                    CandidateStatus.DEMOTED_BY_CONSTRAINT
                ).with_feasibility(FeasibilityEnvelope.PROTECT)
                demoted_ids.append(candidate.candidate_id)
        if demoted_ids:
            acknowledgements.append(
                ConstraintAcknowledgement.create(
                    ConstraintClass.BEHAVIOUR_SUSTAINABILITY
                    if constraints.burnout_risk
                    else ConstraintClass.INTENSITY,
                    demoted_candidate_ids=demoted_ids,
                    note_tags=("protect_intensity", "educational_need_visible"),
                )
            )

    if constraints.scarce_time:
        scarce_demoted: list[str] = []
        high_weight = highest_weight_topic_id(curriculum)
        for i, candidate in enumerate(working):
            if candidate.status == CandidateStatus.DEMOTED_BY_CONSTRAINT:
                continue
            # Demote low-weight polish under scarcity; keep high-weight need.
            if (
                "low_weight_polish" in candidate.note_tags
                or (
                    candidate.curriculum_entity_id is not None
                    and high_weight is not None
                    and candidate.curriculum_entity_id != high_weight
                    and candidate.family == ActionFamily.STUDY
                    and "coverage_gap" in candidate.note_tags
                    and candidate.curriculum_entity_id
                    not in curriculum.high_weight_topic_ids(
                        threshold=_median_weight(curriculum)
                    )
                )
            ):
                working[i] = candidate.with_status(
                    CandidateStatus.DEMOTED_BY_CONSTRAINT
                ).with_feasibility(FeasibilityEnvelope.TIGHT)
                scarce_demoted.append(candidate.candidate_id)
        if scarce_demoted:
            acknowledgements.append(
                ConstraintAcknowledgement.create(
                    ConstraintClass.SESSION_TIME,
                    demoted_candidate_ids=scarce_demoted,
                    note_tags=("scarce_time", "prefer_high_weight"),
                )
            )

    # History anti-thrash: demote recently dismissed identical actions (≠ mastery).
    dismissed = history.dismissed_keys()
    if dismissed:
        history_demoted: list[str] = []
        for i, candidate in enumerate(working):
            key = (candidate.family, candidate.curriculum_entity_id)
            if (
                key in dismissed
                and candidate.status != CandidateStatus.DEMOTED_BY_CONSTRAINT
            ):
                working[i] = candidate.with_status(
                    CandidateStatus.DEMOTED_BY_CONSTRAINT
                )
                history_demoted.append(candidate.candidate_id)
        if history_demoted:
            acknowledgements.append(
                ConstraintAcknowledgement.create(
                    ConstraintClass.GOAL_CAPACITY,
                    demoted_candidate_ids=history_demoted,
                    note_tags=("prior_dismiss_respected", "dismiss_not_mastery"),
                )
            )

    ordered = sorted(
        working,
        key=lambda c: _priority_key(c, readiness, curriculum, constraints),
    )
    return ordered, tuple(acknowledgements)


def _median_weight(curriculum: CurriculumContext) -> float:
    weights = [ref.weight for ref in curriculum.topics if ref.weight is not None]
    if not weights:
        return 0.0
    weights_sorted = sorted(weights)
    mid = len(weights_sorted) // 2
    if len(weights_sorted) % 2 == 0:
        return (weights_sorted[mid - 1] + weights_sorted[mid]) / 2.0
    return weights_sorted[mid]


def _priority_key(
    candidate: CandidateAction,
    readiness: ReadinessState,
    curriculum: CurriculumContext,
    constraints: Constraints,
) -> tuple[int, int, int, str]:
    """Structural priority: lower tuple sorts earlier (selected preference).

    Not a numeric ranking score field — posture only.
    """
    # Demoted / blocked go last among selection eligibility.
    status_rank = {
        CandidateStatus.CONSIDERED: 0,
        CandidateStatus.SELECTED: 0,
        CandidateStatus.DEMOTED_BY_CONSTRAINT: 8,
        CandidateStatus.BLOCKED: 9,
    }[candidate.status]

    # True cold-start / not-yet-knowable — prefer evidence-creating.
    # Low warrant alone must not override known Twin disagreements.
    cold = readiness.cold_start or (
        readiness.overall_posture == OverallPosture.NOT_YET_KNOWABLE
    )
    knowledge_j = readiness.factor(FactorId.KNOWLEDGE_STRENGTH)
    memory_j = readiness.factor(FactorId.MEMORY_STABILITY)
    assessment_j = readiness.factor(FactorId.ASSESSMENT_PERFORMANCE)
    behaviour_j = readiness.factor(FactorId.BEHAVIOUR_RELIABILITY)
    disagreement = (
        knowledge_j.posture == FactorPosture.SUPPORTIVE
        and memory_j.posture == FactorPosture.RISK_ELEVATING
    )
    thin_perf = assessment_j.sparse or assessment_j.posture in {
        FactorPosture.UNKNOWN,
        FactorPosture.LOW_WARRANT,
        FactorPosture.RISK_ELEVATING,
    }
    behaviour_strong_perf_thin = (
        behaviour_j.posture == FactorPosture.SUPPORTIVE and thin_perf
    )

    family_rank = 5
    # Feasibility protection outranks other postures when active.
    if constraints.protect_intensity and candidate.family == (
        ActionFamily.REST_PROTECT_INTENSITY
    ):
        family_rank = 0
    elif disagreement and candidate.family == ActionFamily.REVISE:
        family_rank = 0
    elif cold and candidate.family == ActionFamily.DIAGNOSTIC:
        family_rank = 1
    elif behaviour_strong_perf_thin and candidate.family in {
        ActionFamily.ASSESS,
        ActionFamily.DIAGNOSTIC,
    }:
        family_rank = 1 if candidate.family == ActionFamily.ASSESS else 2
    elif (
        thin_perf
        and not cold
        and not disagreement
        and candidate.family in {ActionFamily.ASSESS, ActionFamily.DIAGNOSTIC}
    ):
        family_rank = 2 if candidate.family == ActionFamily.ASSESS else 3
    elif candidate.family == ActionFamily.STUDY and "low_weight_polish" not in (
        candidate.note_tags
    ):
        family_rank = 3
    elif candidate.family == ActionFamily.REVISE:
        family_rank = 3
    elif candidate.family == ActionFamily.DIAGNOSTIC:
        family_rank = 4
    elif candidate.family == ActionFamily.ASSESS:
        family_rank = 4
    elif "low_weight_polish" in candidate.note_tags:
        family_rank = 6
    elif candidate.family == ActionFamily.REST_PROTECT_INTENSITY:
        family_rank = 5

    # Prefer high-weight curriculum entities under scarcity / cold start.
    weight_rank = 0
    high = highest_weight_topic_id(curriculum)
    if (
        candidate.curriculum_entity_id is not None
        and high is not None
        and candidate.curriculum_entity_id == high
    ):
        weight_rank = 0
    elif "low_weight_polish" in candidate.note_tags:
        weight_rank = 2
    else:
        weight_rank = 1

    return (status_rank, family_rank, weight_rank, candidate.candidate_id)


def _select_candidate(
    ordered: list[CandidateAction],
    _readiness: ReadinessState,
    _constraints: Constraints,
) -> CandidateAction:
    for candidate in ordered:
        if candidate.status in {
            CandidateStatus.CONSIDERED,
            CandidateStatus.SELECTED,
        }:
            return candidate
    # All demoted — prefer rest if present, else first demoted diagnostic.
    for candidate in ordered:
        if candidate.family == ActionFamily.REST_PROTECT_INTENSITY:
            return candidate.with_status(CandidateStatus.CONSIDERED)
    if ordered:
        return ordered[0].with_status(CandidateStatus.CONSIDERED)
    # Absolute fallback (should not happen — nomination always emits diagnostic).
    return CandidateAction.create(
        "diagnostic-fallback",
        ActionFamily.DIAGNOSTIC,
        intent=ActionIntent.EVIDENCE_CREATING,
        status=CandidateStatus.CONSIDERED,
        note_tags=("empty_nomination_fallback",),
        readiness_factor_ids=(FactorId.EVIDENCE_WARRANT.value,),
    )


def _mark_selected(
    ordered: list[CandidateAction],
    selected: CandidateAction,
) -> tuple[CandidateAction, ...]:
    result: list[CandidateAction] = []
    found = False
    for candidate in ordered:
        if (
            not found
            and candidate.candidate_id == selected.candidate_id
            and candidate.family == selected.family
        ):
            result.append(candidate.with_status(CandidateStatus.SELECTED))
            found = True
        elif candidate.status == CandidateStatus.SELECTED:
            result.append(candidate.with_status(CandidateStatus.CONSIDERED))
        else:
            result.append(candidate)
    if not found:
        result.insert(0, selected.with_status(CandidateStatus.SELECTED))
    return tuple(result)


# ---------------------------------------------------------------------------
# Reason codes + lineage + warrant
# ---------------------------------------------------------------------------


def _author_reason_codes(
    *,
    twin: DigitalTwin,
    readiness: ReadinessState,
    curriculum: CurriculumContext,
    constraints: Constraints,
    history: DecisionHistory,
    selected: CandidateAction,
    acknowledgements: tuple[ConstraintAcknowledgement, ...],
) -> tuple[ReasonCodeRef, ...]:
    codes: list[ReasonCodeRef] = []
    high = highest_weight_topic_id(curriculum)
    entity = selected.curriculum_entity_id

    cold = (
        readiness.cold_start
        or readiness.overall_posture == OverallPosture.NOT_YET_KNOWABLE
        or readiness.overall_warrant == WarrantPosture.LOW
    )
    if cold:
        codes.append(
            ReasonCodeRef.create(
                ReasonCodeId.INSUFFICIENT_WARRANT,
                readiness_factor_ids=(FactorId.EVIDENCE_WARRANT.value,),
                note_tags=("warrant_honesty",),
            )
        )
        codes.append(
            ReasonCodeRef.create(
                ReasonCodeId.PREFER_EVIDENCE_CREATING,
                readiness_factor_ids=(FactorId.EVIDENCE_WARRANT.value,),
                curriculum_entity_ids=(entity,) if entity else (),
                note_tags=("cold_start_posture",),
            )
        )
        if readiness.overall_posture == OverallPosture.NOT_YET_KNOWABLE:
            codes.append(
                ReasonCodeRef.create(
                    ReasonCodeId.NOT_YET_KNOWABLE_CONTEXT,
                    readiness_factor_ids=(FactorId.EVIDENCE_WARRANT.value,),
                    note_tags=("no_mid_coercion",),
                )
            )

    knowledge_j = readiness.factor(FactorId.KNOWLEDGE_STRENGTH)
    memory_j = readiness.factor(FactorId.MEMORY_STABILITY)
    if (
        knowledge_j.posture == FactorPosture.SUPPORTIVE
        and memory_j.posture == FactorPosture.RISK_ELEVATING
    ):
        codes.append(
            ReasonCodeRef.create(
                ReasonCodeId.KNOWS_NOW_MAY_NOT_RETAIN,
                twin_domains=(TWIN_DOMAIN_KNOWLEDGE, TWIN_DOMAIN_MEMORY),
                readiness_factor_ids=(
                    FactorId.KNOWLEDGE_STRENGTH.value,
                    FactorId.MEMORY_STABILITY.value,
                ),
                curriculum_entity_ids=(entity,) if entity else (),
                note_tags=("factor_disagreement",),
            )
        )

    if selected.family == ActionFamily.REVISE or memory_j.posture == (
        FactorPosture.RISK_ELEVATING
    ):
        codes.append(
            ReasonCodeRef.create(
                ReasonCodeId.MEMORY_STALENESS,
                twin_domains=(TWIN_DOMAIN_MEMORY,),
                readiness_factor_ids=(FactorId.MEMORY_STABILITY.value,),
                curriculum_entity_ids=(entity,) if entity else (),
            )
        )

    if selected.family == ActionFamily.STUDY or knowledge_j.posture in {
        FactorPosture.UNKNOWN,
        FactorPosture.LOW_WARRANT,
        FactorPosture.RISK_ELEVATING,
    }:
        if selected.family == ActionFamily.STUDY:
            codes.append(
                ReasonCodeRef.create(
                    ReasonCodeId.WEAK_OR_ABSENT_MASTERY,
                    twin_domains=(TWIN_DOMAIN_KNOWLEDGE,),
                    readiness_factor_ids=(FactorId.KNOWLEDGE_STRENGTH.value,),
                    curriculum_entity_ids=(entity,) if entity else (),
                )
            )

    if entity is not None and high is not None and entity == high:
        codes.append(
            ReasonCodeRef.create(
                ReasonCodeId.HIGH_WEIGHT_COVERAGE,
                twin_domains=(TWIN_DOMAIN_CURRICULUM,),
                readiness_factor_ids=(FactorId.CURRICULUM_COVERAGE.value,),
                curriculum_entity_ids=(entity,),
                note_tags=("official_weight",),
            )
        )

    assessment_j = readiness.factor(FactorId.ASSESSMENT_PERFORMANCE)
    behaviour_j = readiness.factor(FactorId.BEHAVIOUR_RELIABILITY)
    if assessment_j.sparse or assessment_j.posture in {
        FactorPosture.UNKNOWN,
        FactorPosture.LOW_WARRANT,
        FactorPosture.RISK_ELEVATING,
    }:
        if selected.family in {ActionFamily.ASSESS, ActionFamily.DIAGNOSTIC}:
            codes.append(
                ReasonCodeRef.create(
                    ReasonCodeId.THIN_PERFORMANCE_WARRANT,
                    twin_domains=(TWIN_DOMAIN_PERFORMANCE,),
                    readiness_factor_ids=(FactorId.ASSESSMENT_PERFORMANCE.value,),
                    curriculum_entity_ids=(entity,) if entity else (),
                )
            )
    if (
        behaviour_j.posture == FactorPosture.SUPPORTIVE
        and (
            assessment_j.sparse
            or assessment_j.posture
            in {
                FactorPosture.UNKNOWN,
                FactorPosture.LOW_WARRANT,
                FactorPosture.RISK_ELEVATING,
            }
        )
    ):
        codes.append(
            ReasonCodeRef.create(
                ReasonCodeId.BEHAVIOUR_STRONG_PERFORMANCE_THIN,
                twin_domains=(TWIN_DOMAIN_BEHAVIOUR, TWIN_DOMAIN_PERFORMANCE),
                readiness_factor_ids=(
                    FactorId.BEHAVIOUR_RELIABILITY.value,
                    FactorId.ASSESSMENT_PERFORMANCE.value,
                ),
                note_tags=("streaks_not_value",),
            )
        )

    time_j = readiness.factor(FactorId.TIME_GOAL_PRESSURE)
    if time_j.posture == FactorPosture.RISK_ELEVATING or constraints.scarce_time:
        codes.append(
            ReasonCodeRef.create(
                ReasonCodeId.SITTING_TIME_PRESSURE,
                twin_domains=(TWIN_DOMAIN_GOALS,),
                readiness_factor_ids=(FactorId.TIME_GOAL_PRESSURE.value,),
                note_tags=tuple(readiness.goal_constraint_notes),
            )
        )

    for ack in acknowledgements:
        if ack.constraint_class == ConstraintClass.SESSION_TIME:
            codes.append(
                ReasonCodeRef.create(
                    ReasonCodeId.SESSION_TIME_DEMOTION,
                    note_tags=ack.note_tags,
                )
            )
        elif ack.constraint_class in {
            ConstraintClass.INTENSITY,
            ConstraintClass.BEHAVIOUR_SUSTAINABILITY,
        }:
            code = (
                ReasonCodeId.BEHAVIOUR_SUSTAINABILITY
                if ack.constraint_class == ConstraintClass.BEHAVIOUR_SUSTAINABILITY
                else ReasonCodeId.INTENSITY_PROTECTION
            )
            codes.append(
                ReasonCodeRef.create(
                    code,
                    twin_domains=(TWIN_DOMAIN_BEHAVIOUR,),
                    note_tags=ack.note_tags,
                )
            )
        elif "prior_dismiss_respected" in ack.note_tags:
            codes.append(
                ReasonCodeRef.create(
                    ReasonCodeId.PRIOR_DISMISS_RESPECTED,
                    note_tags=("dismiss_not_mastery",),
                )
            )

    if has_confidence_shaped_input(twin):
        codes.append(
            ReasonCodeRef.create(
                ReasonCodeId.CONFIDENCE_NOT_MASTERY,
                twin_domains=(TWIN_DOMAIN_BEHAVIOUR,),
                note_tags=("risk_framing_only",),
            )
        )

    # Deduplicate by code_id preserving order.
    seen: set[ReasonCodeId] = set()
    unique: list[ReasonCodeRef] = []
    for ref in codes:
        if ref.code_id not in seen:
            seen.add(ref.code_id)
            unique.append(ref)

    if not unique:
        unique.append(
            ReasonCodeRef.create(
                ReasonCodeId.PREFER_EVIDENCE_CREATING,
                note_tags=("fallback_reason",),
            )
        )
    return tuple(unique)


def _build_lineage(
    *,
    twin: DigitalTwin,
    readiness: ReadinessState,
    curriculum: CurriculumContext,
    selected: CandidateAction,
    candidates: tuple[CandidateAction, ...],
) -> DecisionLineage:
    twin_domains: list[str] = []
    readiness_ids: list[str] = []
    curriculum_ids: list[str] = []
    rationale: list[str] = []

    for candidate in candidates:
        for domain in candidate.twin_domains:
            if domain not in twin_domains:
                twin_domains.append(domain)
        for factor_id in candidate.readiness_factor_ids:
            if factor_id not in readiness_ids:
                readiness_ids.append(factor_id)
        if (
            candidate.curriculum_entity_id
            and candidate.curriculum_entity_id not in curriculum_ids
        ):
            curriculum_ids.append(candidate.curriculum_entity_id)
        for tag in candidate.note_tags:
            if tag not in rationale:
                rationale.append(tag)

    if selected.curriculum_entity_id and selected.curriculum_entity_id not in (
        curriculum_ids
    ):
        curriculum_ids.append(selected.curriculum_entity_id)

    # Always cite curriculum context identity.
    if curriculum.curriculum_id and TWIN_DOMAIN_CURRICULUM not in twin_domains:
        twin_domains.append(TWIN_DOMAIN_CURRICULUM)

    return DecisionLineage.create(
        twin_domains=twin_domains,
        readiness_factor_ids=readiness_ids,
        curriculum_entity_ids=curriculum_ids,
        evidence_ids=evidence_ids_from_twin(twin),
        value_rationale_tags=rationale,
    )


def _inherit_warrant_posture(readiness: ReadinessState) -> DecisionWarrantPosture:
    if readiness.cold_start:
        return DecisionWarrantPosture.COLD_START
    if readiness.overall_posture == OverallPosture.NOT_YET_KNOWABLE:
        return DecisionWarrantPosture.NOT_YET_KNOWABLE
    if readiness.overall_warrant == WarrantPosture.LOW:
        return DecisionWarrantPosture.INHERITED_LOW
    if readiness.overall_warrant == WarrantPosture.MEDIUM:
        return DecisionWarrantPosture.INHERITED_MEDIUM
    return DecisionWarrantPosture.INHERITED_HIGH
