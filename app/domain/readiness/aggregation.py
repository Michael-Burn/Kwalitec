"""Pure read-side Readiness Aggregation.

Derives a factorable ``ReadinessState`` from a Twin snapshot, CurriculumContext,
and Goals (via Twin). Never mutates Twin domains, never writes evidence, never
selects actions, never computes readiness percentages or pass probability.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.domain.readiness.curriculum_context import CurriculumContext
from app.domain.readiness.factors import (
    CRITICAL_SITTING_FACTORS,
    FACTOR_CATALOGUE,
    TWIN_DOMAIN_BEHAVIOUR,
    TWIN_DOMAIN_CURRICULUM,
    TWIN_DOMAIN_GOALS,
    TWIN_DOMAIN_IDENTITY,
    TWIN_DOMAIN_KNOWLEDGE,
    TWIN_DOMAIN_MEMORY,
    TWIN_DOMAIN_PERFORMANCE,
    FactorId,
    FactorPosture,
    OverallPosture,
    WarrantPosture,
)
from app.domain.readiness.readiness_state import (
    FactorAttribution,
    FactorJudgement,
    ReadinessScope,
    ReadinessState,
)
from app.domain.twin.behaviour_state import BehaviourState
from app.domain.twin.digital_twin import DigitalTwin
from app.domain.twin.goal_state import GoalState
from app.domain.twin.identity_state import IdentityState
from app.domain.twin.knowledge_state import KnowledgeState
from app.domain.twin.memory_state import MemoryState
from app.domain.twin.performance_state import PerformanceState

# Structural summary tags that elevate assessment risk without scoring formulas.
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

_WARRANT_RANK = {
    WarrantPosture.LOW: 0,
    WarrantPosture.MEDIUM: 1,
    WarrantPosture.HIGH: 2,
}


class ReadinessAggregation:
    """Pure derive API for structural Readiness Aggregation.

    Observational only: reads Twin + CurriculumContext; never calls Update
    Strategies or mutates inputs.
    """

    @staticmethod
    def derive(
        twin: DigitalTwin,
        curriculum: CurriculumContext,
        *,
        as_of: datetime | None = None,
        derivation_id: str | None = None,
    ) -> ReadinessState:
        """Derive a frozen ``ReadinessState`` from Twin + Curriculum + Goals.

        Args:
            twin: Digital Twin snapshot (read-only; never mutated).
            curriculum: Framework-free syllabus denominator / weights.
            as_of: Optional derivation timestamp (omit for deterministic equality).
            derivation_id: Optional audit identity.

        Returns:
            Immutable factorable readiness judgement.
        """
        scope = _build_scope(twin, curriculum)
        goal_notes = _goal_constraint_notes(twin.goals, twin.identity.target_sitting)
        density = _DomainDensity.from_twin(twin)

        judgements: list[FactorJudgement] = []
        for factor_id in FACTOR_CATALOGUE:
            judgements.append(
                _judge_factor(
                    factor_id, twin=twin, curriculum=curriculum, density=density
                )
            )

        cold_start = density.is_cold_start()
        overall_warrant = _propagate_overall_warrant(judgements, curriculum, twin)
        overall_posture = _compose_overall_posture(
            judgements=judgements,
            cold_start=cold_start,
            overall_warrant=overall_warrant,
            density=density,
        )

        # Re-bind evidence_warrant factor to match overall honesty.
        judgements = _align_evidence_warrant_factor(
            judgements, overall_warrant, cold_start
        )

        return ReadinessState.create(
            scope=scope,
            overall_posture=overall_posture,
            overall_warrant=overall_warrant,
            factors=judgements,
            curriculum_format=curriculum.format,
            cold_start=cold_start,
            derivation_id=derivation_id,
            derived_at=as_of,
            goal_constraint_notes=goal_notes,
        )


# ---------------------------------------------------------------------------
# Domain density / cold start
# ---------------------------------------------------------------------------


class _DomainDensity:
    """Structural presence flags for Twin educational domains."""

    __slots__ = (
        "knowledge_slots",
        "knowledge_beliefs",
        "memory_slots",
        "memory_beliefs",
        "behaviour_lineage",
        "performance_lineage",
        "goals_present",
    )

    def __init__(
        self,
        *,
        knowledge_slots: bool,
        knowledge_beliefs: bool,
        memory_slots: bool,
        memory_beliefs: bool,
        behaviour_lineage: bool,
        performance_lineage: bool,
        goals_present: bool,
    ) -> None:
        self.knowledge_slots = knowledge_slots
        self.knowledge_beliefs = knowledge_beliefs
        self.memory_slots = memory_slots
        self.memory_beliefs = memory_beliefs
        self.behaviour_lineage = behaviour_lineage
        self.performance_lineage = performance_lineage
        self.goals_present = goals_present

    @classmethod
    def from_twin(cls, twin: DigitalTwin) -> _DomainDensity:
        knowledge = twin.knowledge
        memory = twin.memory
        behaviour = twin.behaviour
        performance = twin.performance
        goals = twin.goals
        return cls(
            knowledge_slots=bool(knowledge.topic_mastery),
            knowledge_beliefs=any(
                record.mastery_belief is not None for record in knowledge.topic_mastery
            ),
            memory_slots=bool(memory.retention),
            memory_beliefs=any(
                record.retention_belief is not None for record in memory.retention
            ),
            behaviour_lineage=_behaviour_has_lineage(behaviour),
            performance_lineage=_performance_has_lineage(performance),
            goals_present=_goals_present(goals),
        )

    def is_cold_start(self) -> bool:
        """True when educational domains lack meaningful Twin evidence."""
        educational_empty = not (
            self.knowledge_slots
            or self.memory_slots
            or self.behaviour_lineage
            or self.performance_lineage
        )
        if educational_empty:
            return True
        # Sparse: behaviour-only Twins remain cold for exam readiness.
        if (
            self.behaviour_lineage
            and not self.knowledge_slots
            and not self.memory_slots
            and not self.performance_lineage
        ):
            return True
        return False

    def educational_evidence_present(self) -> bool:
        return bool(
            self.knowledge_slots
            or self.memory_slots
            or self.behaviour_lineage
            or self.performance_lineage
        )


def _behaviour_has_lineage(behaviour: BehaviourState) -> bool:
    return bool(
        behaviour.evidence_ids
        or behaviour.session_history_ids
        or behaviour.study_pattern_ids
    )


def _performance_has_lineage(performance: PerformanceState) -> bool:
    return bool(
        performance.assessment_ids
        or performance.evidence_ids
        or performance.performance_summaries
    )


def _goals_present(goals: GoalState) -> bool:
    return (
        goals.target_pass_probability is not None
        or goals.target_completion_date is not None
        or goals.planned_study_hours_per_week is not None
    )


# ---------------------------------------------------------------------------
# Scope / goals
# ---------------------------------------------------------------------------


def _build_scope(twin: DigitalTwin, curriculum: CurriculumContext) -> ReadinessScope:
    identity = twin.identity
    sitting = twin.goals.target_completion_date or identity.target_sitting
    curriculum_id = identity.curriculum_id or curriculum.curriculum_id
    return ReadinessScope.create(
        identity.student_id,
        curriculum_id=curriculum_id,
        sitting_date=sitting,
        exam_label=identity.current_exam,
    )


def _goal_constraint_notes(
    goals: GoalState,
    identity_sitting: object | None,
) -> tuple[str, ...]:
    notes: list[str] = []
    if goals.target_completion_date is not None:
        notes.append("goal_completion_date")
    if identity_sitting is not None:
        notes.append("identity_sitting")
    if goals.planned_study_hours_per_week is not None:
        notes.append("planned_weekly_hours")
    if goals.target_pass_probability is not None:
        notes.append("pass_ambition")
    if not notes:
        notes.append("no_goal_constraints")
    return tuple(notes)


# ---------------------------------------------------------------------------
# Per-factor judgements
# ---------------------------------------------------------------------------


def _judge_factor(
    factor_id: FactorId,
    *,
    twin: DigitalTwin,
    curriculum: CurriculumContext,
    density: _DomainDensity,
) -> FactorJudgement:
    if factor_id == FactorId.CURRICULUM_COVERAGE:
        return _judge_curriculum_coverage(twin.knowledge, curriculum)
    if factor_id == FactorId.KNOWLEDGE_STRENGTH:
        return _judge_knowledge_strength(twin.knowledge, curriculum)
    if factor_id == FactorId.MEMORY_STABILITY:
        return _judge_memory_stability(twin.memory, twin.goals, twin.identity)
    if factor_id == FactorId.BEHAVIOUR_RELIABILITY:
        return _judge_behaviour_reliability(twin.behaviour, twin.goals)
    if factor_id == FactorId.ASSESSMENT_PERFORMANCE:
        return _judge_assessment_performance(twin.performance, curriculum)
    if factor_id == FactorId.TIME_GOAL_PRESSURE:
        return _judge_time_goal_pressure(twin, density)
    if factor_id == FactorId.EVIDENCE_WARRANT:
        return _judge_evidence_warrant_placeholder(density)
    raise ValueError(f"unknown factor_id: {factor_id}")


def _judge_curriculum_coverage(
    knowledge: KnowledgeState,
    curriculum: CurriculumContext,
) -> FactorJudgement:
    curriculum_ids = set(curriculum.topic_ids)
    present_ids = tuple(
        record.topic_id
        for record in knowledge.topic_mastery
        if not curriculum_ids or record.topic_id in curriculum_ids
    )
    evidence_ids = knowledge.evidence_ids
    attribution = FactorAttribution.create(
        twin_domains=(TWIN_DOMAIN_KNOWLEDGE, TWIN_DOMAIN_CURRICULUM),
        curriculum_entity_ids=present_ids or curriculum.topic_ids[:3],
        evidence_ids=evidence_ids,
        notes=("coverage_structural", f"format_{curriculum.format.value}"),
    )
    if not knowledge.topic_mastery:
        return FactorJudgement.create(
            FactorId.CURRICULUM_COVERAGE,
            posture=FactorPosture.UNKNOWN,
            warrant=WarrantPosture.LOW,
            attribution=attribution,
            sparse=True,
        )
    # Structural presence only — never claims mastery High.
    return FactorJudgement.create(
        FactorId.CURRICULUM_COVERAGE,
        posture=FactorPosture.LOW_WARRANT,
        warrant=(
            WarrantPosture.LOW
            if len(present_ids) < max(1, len(curriculum_ids) // 2)
            else WarrantPosture.MEDIUM
        ),
        attribution=FactorAttribution.create(
            twin_domains=attribution.twin_domains,
            curriculum_entity_ids=present_ids,
            evidence_ids=evidence_ids,
            notes=(*attribution.notes, "structural_presence"),
        ),
        sparse=(
            len(present_ids) == 0
            or len(present_ids) < max(1, len(curriculum_ids) // 2)
        ),
    )


def _judge_knowledge_strength(
    knowledge: KnowledgeState,
    curriculum: CurriculumContext,
) -> FactorJudgement:
    belief_topics = tuple(
        record.topic_id
        for record in knowledge.topic_mastery
        if record.mastery_belief is not None
    )
    evidence_ids = tuple(
        eid
        for record in knowledge.topic_mastery
        for eid in record.evidence_ids
    ) or knowledge.evidence_ids
    attribution = FactorAttribution.create(
        twin_domains=(TWIN_DOMAIN_KNOWLEDGE,),
        curriculum_entity_ids=belief_topics or tuple(
            r.topic_id for r in knowledge.topic_mastery
        ),
        evidence_ids=evidence_ids,
        notes=("knowledge_strength", f"format_{curriculum.format.value}"),
    )
    if not belief_topics:
        # Slots without beliefs remain unknown — never fabricate High mastery.
        notes = (*attribution.notes, "empty_mastery_beliefs")
        if knowledge.topic_mastery:
            notes = (*notes, "slots_without_beliefs")
        return FactorJudgement.create(
            FactorId.KNOWLEDGE_STRENGTH,
            posture=FactorPosture.UNKNOWN,
            warrant=WarrantPosture.LOW,
            attribution=FactorAttribution.create(
                twin_domains=attribution.twin_domains,
                curriculum_entity_ids=attribution.curriculum_entity_ids,
                evidence_ids=evidence_ids,
                notes=notes,
            ),
            sparse=True,
        )
    # Structural proxy only: presence of stored beliefs is supportive of the
    # Knowledge Strength *factor*, not an overall exam-ready claim.
    return FactorJudgement.create(
        FactorId.KNOWLEDGE_STRENGTH,
        posture=FactorPosture.SUPPORTIVE,
        warrant=WarrantPosture.MEDIUM,
        attribution=FactorAttribution.create(
            twin_domains=attribution.twin_domains,
            curriculum_entity_ids=belief_topics,
            evidence_ids=evidence_ids,
            notes=(*attribution.notes, "structural_proxy"),
        ),
        sparse=False,
    )


def _judge_memory_stability(
    memory: MemoryState,
    goals: GoalState,
    identity: IdentityState,
) -> FactorJudgement:
    evidence_ids = memory.revision_ids
    topic_ids = tuple(record.topic_id for record in memory.retention)
    sitting = goals.target_completion_date or identity.target_sitting
    attribution = FactorAttribution.create(
        twin_domains=(TWIN_DOMAIN_MEMORY, TWIN_DOMAIN_GOALS),
        curriculum_entity_ids=topic_ids,
        evidence_ids=evidence_ids,
        notes=("memory_stability",),
    )
    if not memory.retention:
        return FactorJudgement.create(
            FactorId.MEMORY_STABILITY,
            posture=FactorPosture.UNKNOWN,
            warrant=WarrantPosture.LOW,
            attribution=attribution,
            sparse=True,
        )

    belief_topics = tuple(
        record.topic_id
        for record in memory.retention
        if record.retention_belief is not None
    )
    reinforced = tuple(
        record.topic_id
        for record in memory.retention
        if record.last_reinforced is not None
    )

    if not belief_topics and not reinforced:
        # Slots without reinforcement clocks or beliefs.
        # Sitting date present → structural retention risk (not decay math).
        if sitting is not None:
            return FactorJudgement.create(
                FactorId.MEMORY_STABILITY,
                posture=FactorPosture.RISK_ELEVATING,
                warrant=WarrantPosture.LOW,
                attribution=FactorAttribution.create(
                    twin_domains=attribution.twin_domains,
                    curriculum_entity_ids=topic_ids,
                    evidence_ids=evidence_ids,
                    notes=(
                        *attribution.notes,
                        "empty_retention_beliefs",
                        "sitting_without_reinforcement",
                    ),
                ),
                sparse=True,
            )
        return FactorJudgement.create(
            FactorId.MEMORY_STABILITY,
            posture=FactorPosture.UNKNOWN,
            warrant=WarrantPosture.LOW,
            attribution=FactorAttribution.create(
                twin_domains=attribution.twin_domains,
                curriculum_entity_ids=topic_ids,
                evidence_ids=evidence_ids,
                notes=(*attribution.notes, "empty_retention_beliefs"),
            ),
            sparse=True,
        )

    # Sitting date without reinforcement → structural risk elevation (not decay math).
    if sitting is not None and not reinforced and not belief_topics:
        return FactorJudgement.create(
            FactorId.MEMORY_STABILITY,
            posture=FactorPosture.RISK_ELEVATING,
            warrant=WarrantPosture.LOW,
            attribution=FactorAttribution.create(
                twin_domains=attribution.twin_domains,
                curriculum_entity_ids=topic_ids,
                evidence_ids=evidence_ids,
                notes=(*attribution.notes, "sitting_without_reinforcement"),
            ),
            sparse=True,
        )

    if belief_topics or reinforced:
        # Unverified retention beside other strong factors surfaces as risk when
        # beliefs are absent but slots exist under sitting pressure.
        if not belief_topics and sitting is not None:
            return FactorJudgement.create(
                FactorId.MEMORY_STABILITY,
                posture=FactorPosture.RISK_ELEVATING,
                warrant=WarrantPosture.LOW,
                attribution=FactorAttribution.create(
                    twin_domains=attribution.twin_domains,
                    curriculum_entity_ids=topic_ids,
                    evidence_ids=evidence_ids,
                    notes=(*attribution.notes, "retention_unverified_at_sitting"),
                ),
                sparse=True,
            )
        return FactorJudgement.create(
            FactorId.MEMORY_STABILITY,
            posture=FactorPosture.LOW_WARRANT,
            warrant=WarrantPosture.LOW if not belief_topics else WarrantPosture.MEDIUM,
            attribution=FactorAttribution.create(
                twin_domains=attribution.twin_domains,
                curriculum_entity_ids=topic_ids,
                evidence_ids=evidence_ids,
                notes=(*attribution.notes, "structural_retention_presence"),
            ),
            sparse=not belief_topics,
        )

    return FactorJudgement.create(
        FactorId.MEMORY_STABILITY,
        posture=FactorPosture.UNKNOWN,
        warrant=WarrantPosture.LOW,
        attribution=attribution,
        sparse=True,
    )


def _judge_behaviour_reliability(
    behaviour: BehaviourState,
    goals: GoalState,
) -> FactorJudgement:
    evidence_ids = behaviour.evidence_ids
    attribution = FactorAttribution.create(
        twin_domains=(TWIN_DOMAIN_BEHAVIOUR, TWIN_DOMAIN_GOALS),
        curriculum_entity_ids=(),
        evidence_ids=evidence_ids,
        notes=("behaviour_reliability",),
    )
    if not _behaviour_has_lineage(behaviour):
        return FactorJudgement.create(
            FactorId.BEHAVIOUR_RELIABILITY,
            posture=FactorPosture.UNKNOWN,
            warrant=WarrantPosture.LOW,
            attribution=attribution,
            sparse=True,
        )
    notes = (*attribution.notes, "lineage_present", "not_exam_readiness")
    if goals.planned_study_hours_per_week is not None:
        notes = (*notes, "capacity_context")
    # Behaviour lineage is informative for pace — never grants exam readiness.
    return FactorJudgement.create(
        FactorId.BEHAVIOUR_RELIABILITY,
        posture=FactorPosture.SUPPORTIVE,
        warrant=WarrantPosture.MEDIUM,
        attribution=FactorAttribution.create(
            twin_domains=attribution.twin_domains,
            evidence_ids=evidence_ids,
            notes=notes,
        ),
        sparse=False,
    )


def _judge_assessment_performance(
    performance: PerformanceState,
    curriculum: CurriculumContext,
) -> FactorJudgement:
    evidence_ids = performance.evidence_ids or performance.assessment_ids
    scope_ids = tuple(s.scope_id for s in performance.performance_summaries)
    attribution = FactorAttribution.create(
        twin_domains=(TWIN_DOMAIN_PERFORMANCE, TWIN_DOMAIN_CURRICULUM),
        curriculum_entity_ids=scope_ids,
        evidence_ids=evidence_ids,
        notes=("assessment_performance", f"format_{curriculum.format.value}"),
    )
    if not _performance_has_lineage(performance):
        return FactorJudgement.create(
            FactorId.ASSESSMENT_PERFORMANCE,
            posture=FactorPosture.UNKNOWN,
            warrant=WarrantPosture.LOW,
            attribution=attribution,
            sparse=True,
        )

    high_weight = curriculum.high_weight_topic_ids()
    risk_scopes = tuple(
        summary.scope_id
        for summary in performance.performance_summaries
        if _summary_indicates_risk(summary.summary)
    )
    high_weight_risk = tuple(
        sid for sid in risk_scopes if not high_weight or sid in high_weight
    )

    if high_weight_risk or risk_scopes:
        return FactorJudgement.create(
            FactorId.ASSESSMENT_PERFORMANCE,
            posture=FactorPosture.RISK_ELEVATING,
            warrant=WarrantPosture.MEDIUM if evidence_ids else WarrantPosture.LOW,
            attribution=FactorAttribution.create(
                twin_domains=attribution.twin_domains,
                curriculum_entity_ids=high_weight_risk or risk_scopes,
                evidence_ids=evidence_ids,
                notes=(
                    *attribution.notes,
                    "structural_risk_signal",
                    "high_weight_emphasis" if high_weight_risk else "risk_scope",
                ),
            ),
            sparse=False,
        )

    # Presence of assessment lineage without risk tags — low-warrant signal only.
    return FactorJudgement.create(
        FactorId.ASSESSMENT_PERFORMANCE,
        posture=FactorPosture.LOW_WARRANT,
        warrant=WarrantPosture.LOW,
        attribution=FactorAttribution.create(
            twin_domains=attribution.twin_domains,
            curriculum_entity_ids=scope_ids,
            evidence_ids=evidence_ids,
            notes=(*attribution.notes, "lineage_present_no_strength_claim"),
        ),
        sparse=len(performance.performance_summaries) == 0,
    )


def _summary_indicates_risk(summary: dict[str, Any]) -> bool:
    """True when stored summary facts already carry structural risk tags."""
    for key, value in summary.items():
        key_l = str(key).lower()
        if key_l in _RISK_SUMMARY_TAGS:
            return True
        if isinstance(value, str) and value.strip().lower() in _RISK_SUMMARY_TAGS:
            return True
        if key_l in {"strength", "result", "outcome", "status"} and isinstance(
            value, str
        ):
            if value.strip().lower() in _RISK_SUMMARY_TAGS:
                return True
    return False


def _judge_time_goal_pressure(
    twin: DigitalTwin,
    density: _DomainDensity,
) -> FactorJudgement:
    goals = twin.goals
    sitting = goals.target_completion_date or twin.identity.target_sitting
    attribution = FactorAttribution.create(
        twin_domains=(TWIN_DOMAIN_GOALS, TWIN_DOMAIN_IDENTITY),
        notes=("time_goal_pressure",),
    )
    if not density.goals_present and sitting is None:
        return FactorJudgement.create(
            FactorId.TIME_GOAL_PRESSURE,
            posture=FactorPosture.NOT_APPLICABLE,
            warrant=WarrantPosture.LOW,
            attribution=FactorAttribution.create(
                twin_domains=attribution.twin_domains,
                notes=(*attribution.notes, "no_goals"),
            ),
            sparse=True,
        )

    notes = list(attribution.notes)
    if sitting is not None:
        notes.append("sitting_date_present")
    if goals.planned_study_hours_per_week is not None:
        notes.append("capacity_present")

    thin_twin = not (
        density.knowledge_beliefs
        or density.performance_lineage
        or density.memory_beliefs
    )
    if sitting is not None and thin_twin:
        # Calendar pressure reframes; does not invent Assessment Performance.
        return FactorJudgement.create(
            FactorId.TIME_GOAL_PRESSURE,
            posture=FactorPosture.RISK_ELEVATING,
            warrant=WarrantPosture.LOW,
            attribution=FactorAttribution.create(
                twin_domains=attribution.twin_domains,
                notes=(*notes, "calendar_pressure_thin_twin"),
            ),
            sparse=True,
        )

    return FactorJudgement.create(
        FactorId.TIME_GOAL_PRESSURE,
        posture=FactorPosture.LOW_WARRANT,
        warrant=WarrantPosture.LOW,
        attribution=FactorAttribution.create(
            twin_domains=attribution.twin_domains,
            notes=(*notes, "goal_context_only"),
        ),
        sparse=False,
    )


def _judge_evidence_warrant_placeholder(density: _DomainDensity) -> FactorJudgement:
    """Initial evidence-warrant factor; aligned to overall after propagation."""
    if density.is_cold_start():
        warrant = WarrantPosture.LOW
        posture = FactorPosture.LOW_WARRANT
        sparse = True
        notes = ("meta_warrant", "cold_start")
    elif density.performance_lineage and density.knowledge_beliefs:
        warrant = WarrantPosture.MEDIUM
        posture = FactorPosture.LOW_WARRANT
        sparse = False
        notes = ("meta_warrant", "partial_density")
    else:
        warrant = WarrantPosture.LOW
        posture = FactorPosture.LOW_WARRANT
        sparse = True
        notes = ("meta_warrant", "sparse_critical_inputs")
    return FactorJudgement.create(
        FactorId.EVIDENCE_WARRANT,
        posture=posture,
        warrant=warrant,
        attribution=FactorAttribution.create(
            twin_domains=(
                TWIN_DOMAIN_KNOWLEDGE,
                TWIN_DOMAIN_MEMORY,
                TWIN_DOMAIN_BEHAVIOUR,
                TWIN_DOMAIN_PERFORMANCE,
            ),
            notes=notes,
        ),
        sparse=sparse,
    )


# ---------------------------------------------------------------------------
# Warrant propagation + overall posture
# ---------------------------------------------------------------------------


def _propagate_overall_warrant(
    judgements: list[FactorJudgement],
    curriculum: CurriculumContext,
    twin: DigitalTwin,
) -> WarrantPosture:
    """Overall warrant never stronger than critical sitting-relevant factors allow."""
    by_id = {j.factor_id: j for j in judgements}
    critical_warrants = [
        by_id[fid].warrant for fid in CRITICAL_SITTING_FACTORS if fid in by_id
    ]
    if not critical_warrants:
        return WarrantPosture.LOW

    # Sparse / unknown Performance keeps exam-preparedness warrant low.
    assessment = by_id.get(FactorId.ASSESSMENT_PERFORMANCE)
    if assessment is not None and (
        assessment.sparse
        or assessment.posture == FactorPosture.UNKNOWN
        or assessment.warrant == WarrantPosture.LOW
    ):
        floor = WarrantPosture.LOW
    else:
        floor = min(critical_warrants, key=lambda w: _WARRANT_RANK[w])

    # Dense evidence only on low-weight topics must not inflate sitting warrant.
    if _low_weight_density_only(twin, curriculum):
        floor = WarrantPosture.LOW

    return floor


def _low_weight_density_only(
    twin: DigitalTwin,
    curriculum: CurriculumContext,
) -> bool:
    """True when Twin density concentrates on topics with no/low weight."""
    high_weight = curriculum.high_weight_topic_ids()
    if not high_weight:
        return False
    knowledge_ids = {r.topic_id for r in twin.knowledge.topic_mastery}
    performance_ids = {s.scope_id for s in twin.performance.performance_summaries}
    touched = knowledge_ids | performance_ids
    if not touched:
        return False
    return touched.isdisjoint(high_weight)


def _compose_overall_posture(
    *,
    judgements: list[FactorJudgement],
    cold_start: bool,
    overall_warrant: WarrantPosture,
    density: _DomainDensity,
) -> OverallPosture:
    if cold_start:
        return OverallPosture.NOT_YET_KNOWABLE

    if overall_warrant == WarrantPosture.LOW and not density.performance_lineage:
        # Behaviour alone never yields exam-ready overall.
        return OverallPosture.NOT_YET_KNOWABLE

    postures = {j.factor_id: j.posture for j in judgements}
    content_ids = [
        FactorId.KNOWLEDGE_STRENGTH,
        FactorId.MEMORY_STABILITY,
        FactorId.ASSESSMENT_PERFORMANCE,
        FactorId.CURRICULUM_COVERAGE,
    ]
    content = [postures[fid] for fid in content_ids if fid in postures]

    has_risk = FactorPosture.RISK_ELEVATING in content
    has_supportive = FactorPosture.SUPPORTIVE in content
    knowledge_unknown = (
        postures.get(FactorId.KNOWLEDGE_STRENGTH) == FactorPosture.UNKNOWN
    )
    assessment_unknown = (
        postures.get(FactorId.ASSESSMENT_PERFORMANCE) == FactorPosture.UNKNOWN
    )
    memory_unknown = (
        postures.get(FactorId.MEMORY_STABILITY) == FactorPosture.UNKNOWN
    )

    if knowledge_unknown and assessment_unknown and memory_unknown:
        return OverallPosture.NOT_YET_KNOWABLE

    if has_risk and has_supportive:
        return OverallPosture.MIXED

    if has_risk or overall_warrant == WarrantPosture.LOW:
        return OverallPosture.FRAGILE

    critical_unknownish = all(
        postures.get(fid)
        in (
            FactorPosture.UNKNOWN,
            FactorPosture.LOW_WARRANT,
            FactorPosture.NOT_APPLICABLE,
            None,
        )
        for fid in CRITICAL_SITTING_FACTORS
    )
    if critical_unknownish:
        return OverallPosture.UNKNOWN

    # Structural ship: never emit fabricated Mid/High overall readiness.
    return OverallPosture.FRAGILE


def _align_evidence_warrant_factor(
    judgements: list[FactorJudgement],
    overall_warrant: WarrantPosture,
    cold_start: bool,
) -> list[FactorJudgement]:
    aligned: list[FactorJudgement] = []
    for judgement in judgements:
        if judgement.factor_id != FactorId.EVIDENCE_WARRANT:
            aligned.append(judgement)
            continue
        notes = (
            *judgement.attribution.notes,
            f"overall_warrant_{overall_warrant.value}",
        )
        if cold_start:
            notes = (*notes, "insufficient_evidence")
        aligned.append(
            FactorJudgement.create(
                FactorId.EVIDENCE_WARRANT,
                posture=FactorPosture.LOW_WARRANT
                if overall_warrant == WarrantPosture.LOW
                else judgement.posture,
                warrant=overall_warrant,
                attribution=FactorAttribution.create(
                    twin_domains=judgement.attribution.twin_domains,
                    curriculum_entity_ids=judgement.attribution.curriculum_entity_ids,
                    evidence_ids=judgement.attribution.evidence_ids,
                    notes=notes,
                ),
                sparse=overall_warrant == WarrantPosture.LOW,
            )
        )
    return aligned
