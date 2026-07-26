"""Strategy Explainability (MS-005 S2).

Produces deterministic StrategyExplanationBundle values from immutable
LearningIntervention artefacts. No shadow validation, Experience authority
cutover, Runtime A / Twin / Adaptive mutation, persistence, or UI changes.
"""

from __future__ import annotations

from collections.abc import Mapping

from app.infrastructure.adapters.strategy_engine.contracts import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    STRATEGY_VERSION_S2,
    AdaptiveConsumedExplanation,
    AlternativeInterventionItem,
    EducationalPrincipleApplied,
    LearningIntervention,
    MissionNoteExplanation,
    PlannerContribution,
    RuntimeAEvidenceRef,
    StrategyAlternativesExplanation,
    StrategyConfidenceExplanation,
    StrategyExplanationBundle,
    StrategyLimitationsExplanation,
    StrategyWhyExplanation,
    TwinFactorConsidered,
    TwinFactorsExplanation,
)
from app.infrastructure.adapters.strategy_engine.planners import (
    PRINCIPLE_COMPLETABLE_SHELL,
    PRINCIPLE_CONFIDENCE,
    PRINCIPLE_FATIGUE,
    PRINCIPLE_HONESTY,
    PRINCIPLE_NIGHTLY_TOPIC,
    PRINCIPLE_RECOVERY,
)
from app.infrastructure.adapters.strategy_engine.validation import (
    StrategyValidationError,
)

# Explainability construction version (rules for explanation text / refs).
EXPLAINABILITY_VERSION = STRATEGY_VERSION_S2
PRINCIPLE_VERSION = STRATEGY_VERSION_S2
PRINCIPLE_INSPECTABILITY = "ep.inspectability.why_tonight"
PRINCIPLE_REVISION = "ep.revision.spacing_structure"
PRINCIPLE_STUDY = "ep.study.horizon_structure"

# Registered principle catalogue (STRATEGY_EXPLAINABILITY.md §7).
PRINCIPLE_CATALOGUE: Mapping[str, str] = {
    PRINCIPLE_NIGHTLY_TOPIC: "Defensible tonight direction",
    PRINCIPLE_COMPLETABLE_SHELL: "Reduce evening planning load",
    PRINCIPLE_HONESTY: "Coverage is not understanding",
    PRINCIPLE_RECOVERY: "Restart without pep-talk theatre",
    PRINCIPLE_FATIGUE: "Protect load / stop advice",
    PRINCIPLE_CONFIDENCE: "Confidence vs performance evidence",
    PRINCIPLE_INSPECTABILITY: "Student-verifiable rationale",
    PRINCIPLE_REVISION: "Structure Adaptive revision advice",
    PRINCIPLE_STUDY: "Multi-day structure without plan ownership",
}

PRIMARY_DRIVER_FACETS: Mapping[str, str] = {
    "cognitive_load": "FATIGUE_MANAGEMENT",
    "cognitive_load_indicators": "FATIGUE_MANAGEMENT",
    "confidence_trend": "CONFIDENCE_INTERVENTION",
    "persistence": "RECOVERY_PLAN",
    "revision_behaviour": "REVISION_PLAN",
}


class StrategyExplainabilityValidationError(StrategyValidationError):
    """Raised when Strategy explainability inputs violate contracts."""


def _parse_evidence_token(token: str) -> RuntimeAEvidenceRef:
    raw = (token or "").strip()
    if not raw:
        return RuntimeAEvidenceRef()
    if ":" in raw:
        kind, _, rest = raw.partition(":")
        kind_norm = kind.strip().lower()
        if kind_norm == "topic_progress":
            kind_norm = "topic_progress"
        elif kind_norm == "topic":
            kind_norm = "topic"
        try:
            return RuntimeAEvidenceRef(
                kind=kind_norm if kind_norm else "opaque",
                id=rest.strip(),
            )
        except ValueError:
            return RuntimeAEvidenceRef(kind="opaque", id=raw)
    return RuntimeAEvidenceRef(kind="opaque", id=raw)


def _reason_codes(intervention: LearningIntervention) -> tuple[str, ...]:
    codes: list[str] = []
    rule = (intervention.sequencing.composition_rule or "").strip()
    if rule:
        codes.append(f"composition:{rule}")
    if intervention.kind:
        codes.append(f"kind:{intervention.kind}")
    for code in intervention.limitations:
        if code and code not in codes:
            codes.append(code)
    if not codes:
        codes.append("empty_authentic")
    return tuple(codes)


def _runtime_a_refs(
    intervention: LearningIntervention,
) -> tuple[RuntimeAEvidenceRef, ...]:
    tokens: list[str] = []
    seen: set[str] = set()

    def _add(value: str) -> None:
        code = (value or "").strip()
        if not code or code in seen:
            return
        seen.add(code)
        tokens.append(code)

    _add(intervention.runtime_a_evidence_ref)
    for item in intervention.runtime_a_refs:
        _add(item)
    for item in intervention.recovery.runtime_a_refs:
        _add(item)
    for item in intervention.fatigue.runtime_a_activity_refs:
        _add(item)
    for item in intervention.confidence.runtime_a_performance_refs:
        _add(item)
    return tuple(_parse_evidence_token(token) for token in tokens)


def _twin_factor_role(facet_id: str, primary_kind: str) -> str:
    expected = PRIMARY_DRIVER_FACETS.get(facet_id, "")
    if expected and expected == primary_kind:
        return "primary_driver"
    if facet_id in {
        "learning_rhythm",
        "consistency",
        "session_habits",
        "revision_behaviour",
        "persistence",
        "confidence_trend",
        "cognitive_load",
        "cognitive_load_indicators",
    }:
        return "modulator"
    return "supporting"


def _twin_factors(intervention: LearningIntervention) -> TwinFactorsExplanation:
    factors: list[TwinFactorConsidered] = []
    seen: set[str] = set()
    twin_unavailable = "twin_unavailable" in intervention.limitations

    def _add(
        facet_id: str,
        *,
        availability: str,
        role: str,
        note: str = "",
    ) -> None:
        name = (facet_id or "").strip()
        if not name or name in seen:
            return
        seen.add(name)
        factors.append(
            TwinFactorConsidered(
                facet_id=name,
                availability=availability,
                role=role,
                note=note,
            )
        )

    for facet_id in intervention.study.twin_factors_used:
        _add(
            facet_id,
            availability=(
                AVAILABILITY_UNAVAILABLE if twin_unavailable else AVAILABILITY_AVAILABLE
            ),
            role=_twin_factor_role(facet_id, intervention.kind),
            note="study_structure_modulator",
        )
    for facet_id in intervention.session.twin_factors_used:
        _add(
            facet_id,
            availability=(
                AVAILABILITY_UNAVAILABLE if twin_unavailable else AVAILABILITY_AVAILABLE
            ),
            role=_twin_factor_role(facet_id, intervention.kind),
            note="session_structure_modulator",
        )
    if intervention.revision.twin_revision_behaviour_ref:
        _add(
            "revision_behaviour",
            availability=(
                AVAILABILITY_UNAVAILABLE if twin_unavailable else AVAILABILITY_AVAILABLE
            ),
            role=_twin_factor_role("revision_behaviour", intervention.kind),
            note=intervention.revision.twin_revision_behaviour_ref,
        )
    if intervention.recovery.twin_persistence_ref:
        _add(
            "persistence",
            availability=(
                AVAILABILITY_UNAVAILABLE if twin_unavailable else AVAILABILITY_AVAILABLE
            ),
            role=_twin_factor_role("persistence", intervention.kind),
            note=intervention.recovery.twin_persistence_ref,
        )
    if intervention.fatigue.twin_cognitive_load_ref:
        _add(
            "cognitive_load_indicators",
            availability=(
                AVAILABILITY_UNAVAILABLE if twin_unavailable else AVAILABILITY_AVAILABLE
            ),
            role=_twin_factor_role("cognitive_load_indicators", intervention.kind),
            note=intervention.fatigue.twin_cognitive_load_ref,
        )
    if intervention.confidence.twin_confidence_trend_ref:
        _add(
            "confidence_trend",
            availability=(
                AVAILABILITY_UNAVAILABLE if twin_unavailable else AVAILABILITY_AVAILABLE
            ),
            role=_twin_factor_role("confidence_trend", intervention.kind),
            note=intervention.confidence.twin_confidence_trend_ref,
        )

    if twin_unavailable and not factors:
        _add(
            "twin_snapshot",
            availability=AVAILABILITY_UNAVAILABLE,
            role="ignored_unavailable",
            note="twin_unavailable",
        )

    if twin_unavailable:
        summary = (
            "Twin unavailable — structure uses Runtime A / Adaptive only; "
            "no Twin estimates invented."
        )
    elif not factors:
        summary = "No Twin factors modulated this intervention structure."
    else:
        names = ",".join(item.facet_id for item in factors)
        summary = (
            f"Twin factors [{names}] modulated structure "
            f"(minutes/phases/fatigue/recovery tone); primary topic identity "
            f"remains mission/Adaptive-derived."
        )
    return TwinFactorsExplanation(
        snapshot_ref=intervention.twin_ref,
        factors_considered=tuple(factors),
        summary=summary,
    )


def _adaptive_consumed(
    intervention: LearningIntervention,
) -> AdaptiveConsumedExplanation:
    decision_id = (
        intervention.adaptive_recommendation_ref
        or intervention.session.adaptive_decision_ref
        or intervention.revision.adaptive_decision_ref
    ).strip()
    adaptive_unavailable = "adaptive_unavailable" in intervention.limitations
    availability = (
        AVAILABILITY_UNAVAILABLE
        if adaptive_unavailable or not decision_id
        else AVAILABILITY_AVAILABLE
    )
    primary = (
        intervention.session.advisory_topic
        or intervention.session.primary_topic
        or (intervention.topic_refs[0] if intervention.topic_refs else "")
        or intervention.revision.primary_revision_topic
    )
    alternatives: list[str] = []
    for topic in intervention.study.focus_topics:
        if topic and topic != primary and topic not in alternatives:
            alternatives.append(topic)
    for topic in intervention.topic_refs:
        if topic and topic != primary and topic not in alternatives:
            alternatives.append(topic)
    if availability == AVAILABILITY_UNAVAILABLE:
        return AdaptiveConsumedExplanation(
            decision_id=decision_id,
            primary_topic=primary,
            recommendation_summary="",
            alternatives_preserved=tuple(alternatives),
            availability=AVAILABILITY_UNAVAILABLE,
            unavailable_reason=(
                "adaptive_unavailable"
                if adaptive_unavailable
                else "adaptive_decision_ref_missing"
            ),
        )
    summary = f"Consumed Adaptive decision {decision_id}"
    if primary:
        summary = f"{summary}; primary_topic={primary}"
    return AdaptiveConsumedExplanation(
        decision_id=decision_id,
        primary_topic=primary,
        recommendation_summary=summary,
        alternatives_preserved=tuple(alternatives),
        availability=AVAILABILITY_AVAILABLE,
        unavailable_reason="",
    )


def _how_applied(principle_id: str, intervention: LearningIntervention) -> str:
    mapping = {
        PRINCIPLE_NIGHTLY_TOPIC: (
            f"Primary kind {intervention.kind or 'EMPTY'} directs tonight's focus"
        ),
        PRINCIPLE_COMPLETABLE_SHELL: (
            f"Session phases={len(intervention.session.phases)}; "
            f"minutes={intervention.minutes_budget}"
        ),
        PRINCIPLE_HONESTY: "Close ritual / recovery copy avoids mastery theatre",
        PRINCIPLE_RECOVERY: (
            f"Recovery trigger={intervention.recovery.trigger_kind or 'none'}"
        ),
        PRINCIPLE_FATIGUE: (
            f"Fatigue action={intervention.fatigue.recommended_action or 'none'}"
        ),
        PRINCIPLE_CONFIDENCE: (
            f"Confidence action="
            f"{intervention.confidence.recommended_action or 'none'}"
        ),
        PRINCIPLE_INSPECTABILITY: "Why summary + evidence refs exposed for UX",
        PRINCIPLE_REVISION: (
            f"Revision windows={len(intervention.revision.windows)}"
        ),
        PRINCIPLE_STUDY: (
            f"Study horizon_sessions={intervention.study.horizon_sessions}"
        ),
    }
    return mapping.get(principle_id, f"Applied to {intervention.kind or 'EMPTY'}")


def _principles(
    intervention: LearningIntervention,
) -> tuple[EducationalPrincipleApplied, ...]:
    ids = list(intervention.educational_principle_ids)
    if PRINCIPLE_INSPECTABILITY not in ids and (
        intervention.kind or intervention.explanation.why_summary
    ):
        ids.append(PRINCIPLE_INSPECTABILITY)
    if intervention.study.available and PRINCIPLE_STUDY not in ids:
        ids.append(PRINCIPLE_STUDY)
    if intervention.revision.available and PRINCIPLE_REVISION not in ids:
        ids.append(PRINCIPLE_REVISION)
    ordered: list[EducationalPrincipleApplied] = []
    seen: set[str] = set()
    for principle_id in ids:
        pid = (principle_id or "").strip()
        if not pid or pid in seen:
            continue
        seen.add(pid)
        ordered.append(
            EducationalPrincipleApplied(
                principle_id=pid,
                version=PRINCIPLE_VERSION,
                description=PRINCIPLE_CATALOGUE.get(pid, pid),
                how_applied=_how_applied(pid, intervention),
            )
        )
    return tuple(ordered)


def _confidence(
    intervention: LearningIntervention,
) -> StrategyConfidenceExplanation:
    codes = set(intervention.limitations)
    sparse = bool(
        codes
        & {
            "sparse_evidence",
            "runtime_a_unavailable",
            "adaptive_unavailable",
            "twin_unavailable",
            "empty_authentic",
            "no_session_topic",
        }
    )
    if not intervention.kind:
        band = "low"
        score = 0.2
        rationale = "Empty authentic intervention — orchestration incomplete."
    elif sparse and (
        "runtime_a_unavailable" in codes or "adaptive_unavailable" in codes
    ):
        band = "low"
        score = 0.35
        rationale = (
            "Sparse or unavailable Runtime A / Adaptive inputs — "
            "organisational director tone only."
        )
    elif "twin_unavailable" in codes or "sparse_evidence" in codes:
        band = "medium"
        score = 0.55
        rationale = (
            "Partial Twin or mild evidence sparsity — balanced orchestration language."
        )
    else:
        band = "high"
        score = 0.85
        rationale = (
            "Runtime A + Adaptive + Twin available with mission-aligned structure."
        )
    return StrategyConfidenceExplanation(
        score=score,
        band=band,
        rationale=rationale,
    )


def _alternatives(
    intervention: LearningIntervention,
) -> StrategyAlternativesExplanation:
    items: list[AlternativeInterventionItem] = []
    for rank, kind in enumerate(intervention.sequencing.supporting_kinds, start=1):
        items.append(
            AlternativeInterventionItem(
                intervention_kind=kind,
                rank=rank,
                reason_codes=(f"supporting:{kind}",),
                why_not_selected=(
                    f"Supporting under composition_rule="
                    f"{intervention.sequencing.composition_rule}; "
                    f"primary={intervention.kind}"
                ),
            )
        )
    if not items:
        return StrategyAlternativesExplanation(
            items=(),
            rationale=(
                "No supporting intervention kinds sequenced for this composition."
            ),
        )
    return StrategyAlternativesExplanation(
        items=tuple(items),
        rationale=(
            f"Primary={intervention.kind}; supporting kinds preserved in "
            f"sequencing order without Adaptive re-rank."
        ),
    )


def _mission_note(
    intervention: LearningIntervention,
) -> MissionNoteExplanation | None:
    if intervention.kind not in {"SESSION_PLAN", "FATIGUE_MANAGEMENT", "BREAK", ""}:
        if not intervention.session.available:
            return None
    aligned = bool(intervention.session.mission_aligned)
    if aligned:
        summary = (
            f"Session primary topic {intervention.session.primary_topic} "
            f"is mission-aligned."
        )
    elif intervention.session.advisory_topic:
        summary = (
            f"Mission topic {intervention.session.primary_topic} retained; "
            f"Adaptive advisory={intervention.session.advisory_topic}."
        )
    elif intervention.session.primary_topic:
        summary = (
            f"Session topic {intervention.session.primary_topic} "
            f"derived without mission alignment."
        )
    else:
        summary = "No mission-aligned session topic available."
    return MissionNoteExplanation(mission_aligned=aligned, summary=summary)


def _planner_contributions(
    intervention: LearningIntervention,
) -> tuple[PlannerContribution, ...]:
    return (
        PlannerContribution(
            planner_id="study_planner",
            available=intervention.study.available,
            contribution_summary=(
                f"focus_topics={list(intervention.study.focus_topics)};"
                f"horizon={intervention.study.horizon_sessions}"
            ),
            twin_factors_used=intervention.study.twin_factors_used,
            principle_ids=(PRINCIPLE_STUDY,) if intervention.study.available else (),
        ),
        PlannerContribution(
            planner_id="session_planner",
            available=intervention.session.available,
            contribution_summary=(
                f"primary={intervention.session.primary_topic};"
                f"phases={len(intervention.session.phases)};"
                f"mission_aligned={intervention.session.mission_aligned}"
            ),
            twin_factors_used=intervention.session.twin_factors_used,
            principle_ids=intervention.session.educational_principle_ids,
        ),
        PlannerContribution(
            planner_id="revision_planner",
            available=intervention.revision.available,
            contribution_summary=(
                f"windows={len(intervention.revision.windows)};"
                f"primary={intervention.revision.primary_revision_topic}"
            ),
            twin_factors_used=(
                ("revision_behaviour",)
                if intervention.revision.twin_revision_behaviour_ref
                else ()
            ),
            principle_ids=(
                (PRINCIPLE_REVISION,) if intervention.revision.available else ()
            ),
        ),
        PlannerContribution(
            planner_id="recovery_planner",
            available=intervention.recovery.available,
            contribution_summary=(
                f"trigger={intervention.recovery.trigger_kind};"
                f"steps={len(intervention.recovery.steps)}"
            ),
            twin_factors_used=(
                ("persistence",) if intervention.recovery.twin_persistence_ref else ()
            ),
            principle_ids=intervention.recovery.educational_principle_ids,
        ),
        PlannerContribution(
            planner_id="fatigue_manager",
            available=intervention.fatigue.available,
            contribution_summary=(
                f"severity={intervention.fatigue.severity_band};"
                f"action={intervention.fatigue.recommended_action}"
            ),
            twin_factors_used=(
                ("cognitive_load_indicators",)
                if intervention.fatigue.twin_cognitive_load_ref
                else ()
            ),
            principle_ids=intervention.fatigue.educational_principle_ids,
        ),
        PlannerContribution(
            planner_id="confidence_manager",
            available=intervention.confidence.available,
            contribution_summary=(
                f"divergence={intervention.confidence.divergence_band};"
                f"action={intervention.confidence.recommended_action}"
            ),
            twin_factors_used=(
                ("confidence_trend",)
                if intervention.confidence.twin_confidence_trend_ref
                else ()
            ),
            principle_ids=intervention.confidence.educational_principle_ids,
        ),
        PlannerContribution(
            planner_id="intervention_planner",
            available=bool(intervention.sequencing.primary_kind),
            contribution_summary=(
                f"primary={intervention.sequencing.primary_kind};"
                f"rule={intervention.sequencing.composition_rule};"
                f"supporting={list(intervention.sequencing.supporting_kinds)}"
            ),
            twin_factors_used=(),
            principle_ids=(PRINCIPLE_NIGHTLY_TOPIC,)
            if intervention.sequencing.primary_kind
            else (),
        ),
    )


def explanation_is_complete(bundle: StrategyExplanationBundle) -> bool:
    """Return True when mandatory UX explainability groups are present."""
    if not (bundle.why.summary or "").strip():
        return False
    if not bundle.educational_objective.strip() and not bundle.why.summary.strip():
        return False
    sparse = "sparse_evidence" in bundle.limitations.codes
    if not bundle.runtime_a_evidence_refs and not sparse:
        return False
    if bundle.twin_factors is None:  # pragma: no cover - typed always present
        return False
    if bundle.adaptive_consumed is None:  # pragma: no cover
        return False
    if not bundle.educational_principles:
        return False
    for principle in bundle.educational_principles:
        if not principle.principle_id.strip() or not principle.how_applied.strip():
            return False
    if not (bundle.confidence.band or "").strip():
        return False
    if not (bundle.confidence.rationale or "").strip():
        return False
    if not bundle.planner_contributions:
        return False
    return True


class StrategyExplainabilityService:
    """Produce deterministic Strategy explanations from LearningInterventions.

    Rules:
    - MAY document existing intervention / planner fields only
    - MUST NOT invent evidence, re-rank Adaptive, mutate Twin / Runtime A,
      persist interventions, or cut over Experience authority
    - Identical LearningIntervention material → identical explanations
    """

    SERVICE_ID = "strategy_explainability"
    SERVICE_VERSION = "1.0.0-s2"

    def __init__(self, *, enabled: bool = True) -> None:
        self._enabled = bool(enabled)

    @property
    def service_id(self) -> str:
        return self.SERVICE_ID

    @property
    def service_version(self) -> str:
        return self.SERVICE_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    def explain(
        self,
        intervention: LearningIntervention,
    ) -> StrategyExplanationBundle:
        """Explain one immutable LearningIntervention."""
        if not self._enabled:
            raise StrategyExplainabilityValidationError(
                "StrategyExplainabilityService is disabled (feature flag OFF)"
            )
        if not isinstance(intervention, LearningIntervention):
            raise StrategyExplainabilityValidationError(
                "intervention must be a LearningIntervention"
            )

        limitations = StrategyLimitationsExplanation(
            codes=tuple(intervention.limitations),
            summary=(
                intervention.explanation.limitations_summary
                or (
                    "Limitations: " + ", ".join(intervention.limitations)
                    if intervention.limitations
                    else ""
                )
            ),
        )
        why_summary = (
            intervention.explanation.why_summary
            or intervention.educational_objective
            or "Strategy orchestration produced an empty authentic intervention."
        )
        return StrategyExplanationBundle(
            intervention_id=intervention.intervention_id,
            explainability_version=EXPLAINABILITY_VERSION,
            educational_objective=intervention.educational_objective,
            why=StrategyWhyExplanation(
                summary=why_summary,
                reason_codes=_reason_codes(intervention),
            ),
            runtime_a_evidence_refs=_runtime_a_refs(intervention),
            twin_factors=_twin_factors(intervention),
            adaptive_consumed=_adaptive_consumed(intervention),
            educational_principles=_principles(intervention),
            confidence=_confidence(intervention),
            alternatives=_alternatives(intervention),
            limitations=limitations,
            mission_note=_mission_note(intervention),
            planner_contributions=_planner_contributions(intervention),
        )


def build_strategy_explainability_service(
    *,
    enabled: bool,
) -> StrategyExplainabilityService | None:
    """DI helper — construct StrategyExplainabilityService only when flag is on."""
    if not enabled:
        return None
    return StrategyExplainabilityService(enabled=True)


__all__ = [
    "EXPLAINABILITY_VERSION",
    "PRINCIPLE_CATALOGUE",
    "PRINCIPLE_VERSION",
    "StrategyExplainabilityService",
    "StrategyExplainabilityValidationError",
    "build_strategy_explainability_service",
    "explanation_is_complete",
]
