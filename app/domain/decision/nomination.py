"""Pure nomination helpers for Decision Engine candidates.

Structural presence / tension / warrant visibility — no ranking formulas.
Curriculum identities come only from CurriculumContext.
"""

from __future__ import annotations

from app.domain.decision.action_types import ActionFamily, ActionIntent
from app.domain.decision.candidate import (
    CandidateAction,
    CandidateStatus,
    FeasibilityEnvelope,
)
from app.domain.decision.constraints import Constraints
from app.domain.readiness.curriculum_context import CurriculumContext
from app.domain.readiness.factors import (
    FactorId,
    FactorPosture,
    OverallPosture,
    WarrantPosture,
)
from app.domain.readiness.readiness_state import ReadinessState
from app.domain.twin.digital_twin import DigitalTwin
from app.domain.twin.knowledge_state import KnowledgeState
from app.domain.twin.memory_state import MemoryState
from app.domain.twin.performance_state import PerformanceState

# Structural risk tags mirrored from readiness (not scoring).
_RISK_SUMMARY_TAGS = frozenset(
    {
        "weak",
        "risk",
        "risk_elevating",
        "concerning",
        "incorrect",
        "fail",
        "failed",
        "low",
    }
)

TWIN_DOMAIN_KNOWLEDGE = "knowledge"
TWIN_DOMAIN_MEMORY = "memory"
TWIN_DOMAIN_BEHAVIOUR = "behaviour"
TWIN_DOMAIN_PERFORMANCE = "performance"
TWIN_DOMAIN_GOALS = "goals"
TWIN_DOMAIN_CURRICULUM = "curriculum"


def highest_weight_topic_id(curriculum: CurriculumContext) -> str | None:
    """Return the highest-weight curriculum topic id, or first topic, or None.

    Deterministic: ties broken by curriculum topic order (first wins).
    """
    if not curriculum.topics:
        return None
    best_id: str | None = None
    best_weight: float | None = None
    for ref in curriculum.topics:
        if ref.weight is None:
            if best_id is None:
                best_id = ref.topic_id
            continue
        if best_weight is None or ref.weight > best_weight:
            best_weight = ref.weight
            best_id = ref.topic_id
    return best_id


def knowledge_gap_topic_ids(
    twin: DigitalTwin,
    curriculum: CurriculumContext,
) -> tuple[str, ...]:
    """Curriculum topics with weak/absent mastery beliefs (structural)."""
    belief_by_id = {
        record.topic_id: record.mastery_belief
        for record in twin.knowledge.topic_mastery
    }
    gaps: list[str] = []
    for ref in curriculum.topics:
        belief = belief_by_id.get(ref.topic_id)
        if belief is None or belief < 0.5:
            gaps.append(ref.topic_id)
    return tuple(gaps)


def stale_memory_topic_ids(twin: DigitalTwin) -> tuple[str, ...]:
    """Topics with retention slots lacking reinforcement or low retention."""
    stale: list[str] = []
    for record in twin.memory.retention:
        if record.last_reinforced is None:
            stale.append(record.topic_id)
        elif (
            record.retention_belief is not None and record.retention_belief < 0.5
        ):
            stale.append(record.topic_id)
    return tuple(stale)


def performance_risk_topic_ids(twin: DigitalTwin) -> tuple[str, ...]:
    """Scopes with risk-elevating performance summary tags."""
    risky: list[str] = []
    for summary in twin.performance.performance_summaries:
        if _summary_has_risk(summary.summary):
            risky.append(summary.scope_id)
    return tuple(risky)


def _summary_has_risk(summary: dict) -> bool:
    for key, value in summary.items():
        if str(key).strip().lower() in _RISK_SUMMARY_TAGS:
            return True
        if isinstance(value, str) and value.strip().lower() in _RISK_SUMMARY_TAGS:
            return True
    return False


def has_confidence_shaped_input(twin: DigitalTwin) -> bool:
    """Detect confidence-shaped bags used only for risk framing — never mastery."""
    metrics = twin.behaviour.consistency_metrics
    for key in metrics:
        if "confidence" in str(key).strip().lower():
            return True
    return False


def evidence_ids_from_twin(twin: DigitalTwin) -> tuple[str, ...]:
    """Collect evidence lineage hooks exposed by Twin domains (deterministic)."""
    ids: list[str] = []
    seen: set[str] = set()
    for collection in (
        twin.knowledge.evidence_ids,
        twin.memory.revision_ids,
        twin.behaviour.evidence_ids,
        twin.performance.evidence_ids,
    ):
        for evidence_id in collection:
            if evidence_id not in seen:
                seen.add(evidence_id)
                ids.append(evidence_id)
    return tuple(ids)


def default_feasibility(constraints: Constraints) -> FeasibilityEnvelope:
    """Map Constraints to a structural feasibility envelope."""
    if constraints.protect_intensity:
        return FeasibilityEnvelope.PROTECT
    if constraints.scarce_time:
        return FeasibilityEnvelope.TIGHT
    if constraints.intensity.value in {"limited"}:
        return FeasibilityEnvelope.TIGHT
    if constraints.available_minutes is None:
        return FeasibilityEnvelope.UNKNOWN
    return FeasibilityEnvelope.AMPLE


def nominate_candidates(
    twin: DigitalTwin,
    readiness: ReadinessState,
    curriculum: CurriculumContext,
    constraints: Constraints,
) -> list[CandidateAction]:
    """Nominate structural candidates from Twin + Readiness + Curriculum.

    Always returns at least one diagnostic / evidence-creating candidate.
    Does not invent syllabus identities outside CurriculumContext.
    """
    high_weight = highest_weight_topic_id(curriculum)
    gaps = knowledge_gap_topic_ids(twin, curriculum)
    stale = stale_memory_topic_ids(twin)
    perf_risk = performance_risk_topic_ids(twin)
    feas = default_feasibility(constraints)
    cold = _is_cold_or_low_warrant(readiness)
    candidates: list[CandidateAction] = []
    seq = 0

    def _next_id(family: ActionFamily) -> str:
        nonlocal seq
        seq += 1
        return f"{family.value}-{seq}"

    # Diagnostic / evidence-creating — always available for cold start honesty.
    diag_entity = high_weight
    candidates.append(
        CandidateAction.create(
            _next_id(ActionFamily.DIAGNOSTIC),
            ActionFamily.DIAGNOSTIC,
            curriculum_entity_id=diag_entity,
            intent=ActionIntent.EVIDENCE_CREATING,
            status=CandidateStatus.CONSIDERED,
            feasibility=feas,
            twin_domains=(TWIN_DOMAIN_CURRICULUM,),
            readiness_factor_ids=(FactorId.EVIDENCE_WARRANT.value,),
            note_tags=(
                "evidence_creating",
                "cold_start_fallback" if cold else "baseline",
            ),
        )
    )

    # Study / coverage on highest-weight gap (curriculum-bound).
    study_entity = _prefer_high_weight(gaps, curriculum, fallback=high_weight)
    if study_entity is not None or gaps:
        entity = study_entity or high_weight
        candidates.append(
            CandidateAction.create(
                _next_id(ActionFamily.STUDY),
                ActionFamily.STUDY,
                curriculum_entity_id=entity,
                intent=ActionIntent.COVERAGE_GAP,
                status=CandidateStatus.CONSIDERED,
                feasibility=feas,
                twin_domains=(TWIN_DOMAIN_KNOWLEDGE, TWIN_DOMAIN_CURRICULUM),
                readiness_factor_ids=(
                    FactorId.KNOWLEDGE_STRENGTH.value,
                    FactorId.CURRICULUM_COVERAGE.value,
                ),
                note_tags=("coverage_gap",),
            )
        )

    # Revise when Memory risk or Knowledge/Memory disagreement.
    knowledge_j = readiness.factor(FactorId.KNOWLEDGE_STRENGTH)
    memory_j = readiness.factor(FactorId.MEMORY_STABILITY)
    disagreement = (
        knowledge_j.posture == FactorPosture.SUPPORTIVE
        and memory_j.posture == FactorPosture.RISK_ELEVATING
    )
    revise_entity = _prefer_high_weight(stale, curriculum, fallback=None)
    if revise_entity is None and disagreement and high_weight is not None:
        revise_entity = high_weight
    if revise_entity is not None or disagreement or stale:
        entity = revise_entity or high_weight
        intent = (
            ActionIntent.FACTOR_DISAGREEMENT
            if disagreement
            else ActionIntent.RETENTION_RISK
        )
        tags = ["retention_risk"]
        if disagreement:
            tags.append("knows_now_may_not_retain")
        candidates.append(
            CandidateAction.create(
                _next_id(ActionFamily.REVISE),
                ActionFamily.REVISE,
                curriculum_entity_id=entity,
                intent=intent,
                status=CandidateStatus.CONSIDERED,
                feasibility=feas,
                twin_domains=(TWIN_DOMAIN_MEMORY, TWIN_DOMAIN_KNOWLEDGE),
                readiness_factor_ids=(
                    FactorId.MEMORY_STABILITY.value,
                    FactorId.KNOWLEDGE_STRENGTH.value,
                ),
                note_tags=tuple(tags),
            )
        )

    # Assess when Performance thin / risk or Behaviour strong + Performance thin.
    assessment_j = readiness.factor(FactorId.ASSESSMENT_PERFORMANCE)
    behaviour_j = readiness.factor(FactorId.BEHAVIOUR_RELIABILITY)
    thin_perf = (
        assessment_j.sparse
        or assessment_j.posture
        in {
            FactorPosture.UNKNOWN,
            FactorPosture.LOW_WARRANT,
            FactorPosture.RISK_ELEVATING,
        }
        or bool(perf_risk)
    )
    behaviour_strong_perf_thin = (
        behaviour_j.posture == FactorPosture.SUPPORTIVE and thin_perf
    )
    if thin_perf or behaviour_strong_perf_thin:
        assess_entity = (
            _prefer_high_weight(perf_risk, curriculum, fallback=high_weight)
            or high_weight
        )
        tags = ["assessment_warrant"]
        if behaviour_strong_perf_thin:
            tags.append("behaviour_strong_performance_thin")
        candidates.append(
            CandidateAction.create(
                _next_id(ActionFamily.ASSESS),
                ActionFamily.ASSESS,
                curriculum_entity_id=assess_entity,
                intent=ActionIntent.ASSESSMENT_WARRANT,
                status=CandidateStatus.CONSIDERED,
                feasibility=feas,
                twin_domains=(TWIN_DOMAIN_PERFORMANCE, TWIN_DOMAIN_BEHAVIOUR),
                readiness_factor_ids=(
                    FactorId.ASSESSMENT_PERFORMANCE.value,
                    FactorId.BEHAVIOUR_RELIABILITY.value,
                ),
                note_tags=tuple(tags),
            )
        )

    # Rest / protect intensity when sustainability risk dominates.
    if constraints.protect_intensity:
        candidates.append(
            CandidateAction.create(
                _next_id(ActionFamily.REST_PROTECT_INTENSITY),
                ActionFamily.REST_PROTECT_INTENSITY,
                curriculum_entity_id=None,
                intent=ActionIntent.FEASIBILITY_PROTECTION,
                status=CandidateStatus.CONSIDERED,
                feasibility=FeasibilityEnvelope.PROTECT,
                twin_domains=(TWIN_DOMAIN_BEHAVIOUR, TWIN_DOMAIN_GOALS),
                readiness_factor_ids=(FactorId.BEHAVIOUR_RELIABILITY.value,),
                note_tags=("protect_intensity", "need_remains_visible"),
            )
        )

    # Low-weight polish candidate (often demoted under scarcity) for explainability.
    low_weight = _lowest_weight_topic_id(curriculum)
    if (
        low_weight is not None
        and high_weight is not None
        and low_weight != high_weight
        and not cold
    ):
        candidates.append(
            CandidateAction.create(
                _next_id(ActionFamily.STUDY),
                ActionFamily.STUDY,
                curriculum_entity_id=low_weight,
                intent=ActionIntent.COVERAGE_GAP,
                status=CandidateStatus.CONSIDERED,
                feasibility=feas,
                twin_domains=(TWIN_DOMAIN_CURRICULUM,),
                readiness_factor_ids=(FactorId.CURRICULUM_COVERAGE.value,),
                note_tags=("low_weight_polish",),
            )
        )

    return candidates


def _is_cold_or_low_warrant(readiness: ReadinessState) -> bool:
    return (
        readiness.cold_start
        or readiness.overall_posture
        in {OverallPosture.NOT_YET_KNOWABLE, OverallPosture.UNKNOWN}
        or readiness.overall_warrant == WarrantPosture.LOW
    )


def _prefer_high_weight(
    topic_ids: tuple[str, ...] | list[str],
    curriculum: CurriculumContext,
    *,
    fallback: str | None,
) -> str | None:
    if not topic_ids:
        return fallback
    weight_map = {ref.topic_id: ref.weight for ref in curriculum.topics}
    best: str | None = None
    best_w: float | None = None
    for topic_id in topic_ids:
        w = weight_map.get(topic_id)
        if w is None:
            if best is None:
                best = topic_id
            continue
        if best_w is None or w > best_w:
            best_w = w
            best = topic_id
    return best if best is not None else fallback


def _lowest_weight_topic_id(curriculum: CurriculumContext) -> str | None:
    best_id: str | None = None
    best_weight: float | None = None
    for ref in curriculum.topics:
        if ref.weight is None:
            continue
        if best_weight is None or ref.weight < best_weight:
            best_weight = ref.weight
            best_id = ref.topic_id
    return best_id


def twin_domain_sparse(twin: DigitalTwin) -> bool:
    """True when educational Twin domains look structurally empty."""
    return (
        _knowledge_empty(twin.knowledge)
        and _memory_empty(twin.memory)
        and not twin.behaviour.evidence_ids
        and not twin.behaviour.session_history_ids
        and _performance_empty(twin.performance)
    )


def _knowledge_empty(knowledge: KnowledgeState) -> bool:
    if not knowledge.topic_mastery:
        return True
    return all(r.mastery_belief is None for r in knowledge.topic_mastery)


def _memory_empty(memory: MemoryState) -> bool:
    return not memory.retention


def _performance_empty(performance: PerformanceState) -> bool:
    return not performance.assessment_ids and not performance.performance_summaries
