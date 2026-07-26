"""Strategy Engine core orchestration (MS-005 S1).

Transforms StrategyContext into one immutable LearningIntervention by
coordinating all educational planning responsibilities. No Experience
projection, no Runtime A / Twin / Adaptive mutation, no persistence.
"""

from __future__ import annotations

import hashlib

from app.infrastructure.adapters.strategy_engine.contracts import (
    AUTHORITY_STRATEGY_ENGINE,
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    STRATEGY_VERSION_S1,
    InterventionStep,
    LearningIntervention,
    StrategyContext,
    StrategyExplanationPlaceholder,
    StrategyProvenancePlaceholder,
)
from app.infrastructure.adapters.strategy_engine.planners import (
    PRINCIPLE_NIGHTLY_TOPIC,
    ConfidenceManager,
    FatigueManager,
    InterventionPlanner,
    RecoveryPlanner,
    RevisionPlanner,
    SessionPlanner,
    StudyPlanner,
)
from app.infrastructure.adapters.strategy_engine.validation import (
    assert_adaptive_topic_order_preserved,
    validate_learning_intervention,
    validate_strategy_context,
)


class StrategyEngine:
    """Core Learning Strategy Engine — deterministic intervention orchestration.

    Identical StrategyContext → identical LearningIntervention every execution.
    """

    ENGINE_ID = "strategy_engine"
    ENGINE_VERSION = STRATEGY_VERSION_S1

    def __init__(
        self,
        *,
        study_planner: StudyPlanner | None = None,
        session_planner: SessionPlanner | None = None,
        revision_planner: RevisionPlanner | None = None,
        recovery_planner: RecoveryPlanner | None = None,
        fatigue_manager: FatigueManager | None = None,
        confidence_manager: ConfidenceManager | None = None,
        intervention_planner: InterventionPlanner | None = None,
        enabled: bool = True,
    ) -> None:
        self._enabled = bool(enabled)
        self._study = study_planner or StudyPlanner()
        self._session = session_planner or SessionPlanner()
        self._revision = revision_planner or RevisionPlanner()
        self._recovery = recovery_planner or RecoveryPlanner()
        self._fatigue = fatigue_manager or FatigueManager()
        self._confidence = confidence_manager or ConfidenceManager()
        self._sequencer = intervention_planner or InterventionPlanner()

    @property
    def engine_id(self) -> str:
        return self.ENGINE_ID

    @property
    def engine_version(self) -> str:
        return self.ENGINE_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    def evaluate(self, context: StrategyContext) -> LearningIntervention:
        """Orchestrate all planners into one immutable LearningIntervention."""
        validate_strategy_context(context)

        study = self._study.plan(context)
        session = self._session.plan(context)
        revision = self._revision.plan(context)
        recovery = self._recovery.plan(context)
        fatigue = self._fatigue.plan(context)
        confidence = self._confidence.plan(context)
        sequencing = self._sequencer.compose(
            context,
            study=study,
            session=session,
            revision=revision,
            recovery=recovery,
            fatigue=fatigue,
            confidence=confidence,
        )

        assert_adaptive_topic_order_preserved(
            adaptive_focus_topics=study.focus_topics,
            study_focus_topics=study.focus_topics,
        )

        limitations = _merge_limitations(
            study.limitations,
            session.limitations,
            revision.limitations,
            recovery.limitations,
            fatigue.limitations,
            confidence.limitations,
            _context_limitations(context),
        )
        principles = _merge_principles(
            session.educational_principle_ids,
            recovery.educational_principle_ids,
            fatigue.educational_principle_ids,
            confidence.educational_principle_ids,
        )
        if not principles and sequencing.primary_kind:
            principles = (PRINCIPLE_NIGHTLY_TOPIC,)

        topic_refs = _topic_refs(session=session, study=study, revision=revision)
        steps = _primary_steps(
            sequencing.primary_kind,
            session=session,
            recovery=recovery,
        )
        runtime_a_refs = _runtime_a_refs(context, recovery=recovery, session=session)
        minutes = session.total_minutes
        if (
            fatigue.available
            and fatigue.minutes_adjustment is not None
            and minutes is not None
        ):
            minutes = max(15, minutes + fatigue.minutes_adjustment)

        objective = _educational_objective(sequencing.primary_kind, session=session)
        intervention = LearningIntervention(
            intervention_id=_deterministic_intervention_id(context),
            strategy_version=STRATEGY_VERSION_S1,
            adaptive_recommendation_ref=context.adaptive_recommendation_ref,
            twin_ref=context.twin_ref,
            runtime_a_evidence_ref=context.runtime_a_evidence_ref,
            educational_objective=objective,
            explanation=StrategyExplanationPlaceholder(
                why_summary=_why_summary(sequencing.composition_rule),
                educational_principle_ids=principles,
                limitations_codes=limitations,
                limitations_summary=_limitations_summary(limitations),
                input_summary=(
                    f"student_id={context.student_id};"
                    f"runtime_a={context.runtime_a_availability};"
                    f"twin={context.twin_availability};"
                    f"adaptive={context.adaptive_availability}"
                ),
            ),
            provenance=StrategyProvenancePlaceholder(
                source_service="strategy_engine",
                source_entity="LearningIntervention",
                collected_at=context.as_of,
                availability=(
                    AVAILABILITY_AVAILABLE
                    if sequencing.primary_kind
                    else AVAILABILITY_UNAVAILABLE
                ),
                unavailable_reason=(
                    "" if sequencing.primary_kind else "empty_authentic"
                ),
                kind="strategy_derived",
            ),
            kind=sequencing.primary_kind,
            steps=steps,
            topic_refs=topic_refs,
            educational_principle_ids=principles,
            runtime_a_refs=runtime_a_refs,
            minutes_budget=minutes,
            authority=AUTHORITY_STRATEGY_ENGINE,
            limitations=limitations,
            study=study,
            session=session,
            revision=revision,
            recovery=recovery,
            fatigue=fatigue,
            confidence=confidence,
            sequencing=sequencing,
        )
        return validate_learning_intervention(intervention)


def build_strategy_engine(*, enabled: bool) -> StrategyEngine | None:
    """DI helper — construct StrategyEngine only when the flag is on."""
    if not enabled:
        return None
    return StrategyEngine(enabled=True)


def _deterministic_intervention_id(context: StrategyContext) -> str:
    digest = hashlib.sha256(context.serialize().encode("utf-8")).hexdigest()[:16]
    return f"s1-{digest}"


def _merge_limitations(*groups: tuple[str, ...]) -> tuple[str, ...]:
    seen: set[str] = set()
    ordered: list[str] = []
    for group in groups:
        for item in group:
            code = str(item).strip()
            if not code or code in seen:
                continue
            seen.add(code)
            ordered.append(code)
    return tuple(ordered)


def _merge_principles(*groups: tuple[str, ...]) -> tuple[str, ...]:
    return _merge_limitations(*groups)


def _context_limitations(context: StrategyContext) -> tuple[str, ...]:
    codes: list[str] = []
    if context.runtime_a_availability != AVAILABILITY_AVAILABLE:
        codes.append("runtime_a_unavailable")
    if context.twin_availability != AVAILABILITY_AVAILABLE:
        codes.append("twin_unavailable")
    if context.adaptive_availability != AVAILABILITY_AVAILABLE:
        codes.append("adaptive_unavailable")
    return tuple(codes)


def _topic_refs(*, session, study, revision) -> tuple[str, ...]:
    ordered: list[str] = []
    seen: set[str] = set()
    for code in (
        session.primary_topic,
        session.advisory_topic,
        *study.focus_topics,
        revision.primary_revision_topic,
    ):
        value = str(code or "").strip()
        if not value or value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return tuple(ordered)


def _primary_steps(
    primary_kind: str, *, session, recovery
) -> tuple[InterventionStep, ...]:
    if primary_kind == "RECOVERY_PLAN":
        return recovery.steps
    if primary_kind in {"SESSION_PLAN", "FATIGUE_MANAGEMENT", "BREAK"}:
        return session.phases
    if primary_kind == "REVISION_PLAN" and session.phases:
        return session.phases
    return session.phases


def _runtime_a_refs(context: StrategyContext, *, recovery, session) -> tuple[str, ...]:
    refs: list[str] = []
    seen: set[str] = set()

    def _add(value: str) -> None:
        code = (value or "").strip()
        if not code or code in seen:
            return
        seen.add(code)
        refs.append(code)

    if context.runtime_a_evidence_ref:
        _add(context.runtime_a_evidence_ref)
    if context.mission_id:
        _add(f"mission:{context.mission_id}")
    for item in recovery.runtime_a_refs:
        _add(item)
    if session.primary_topic:
        _add(f"topic:{session.primary_topic}")
    return tuple(refs)


def _educational_objective(primary_kind: str, *, session) -> str:
    if primary_kind == "FATIGUE_MANAGEMENT":
        return "Protect educational value under load"
    if primary_kind == "RECOVERY_PLAN":
        return "Restart learning without mastery theatre"
    if primary_kind == "REVISION_PLAN":
        return "Structure revision from Adaptive priority"
    if primary_kind == "CONFIDENCE_INTERVENTION":
        return "Calibrate confidence to Runtime A evidence"
    if primary_kind == "STUDY_PLAN":
        return "Advise multi-session study structure"
    if primary_kind == "SESSION_PLAN" and session.primary_topic:
        return f"Complete tonight's session on {session.primary_topic}"
    if primary_kind == "SESSION_PLAN":
        return "Complete tonight's session shell"
    return ""


def _why_summary(composition_rule: str) -> str:
    mapping = {
        "fatigue_critical": "Fatigue is critical — load protection is primary.",
        "recovery_trigger": "Recovery trigger active — restart structure is primary.",
        "revision_lifecycle": (
            "Revision lifecycle — Adaptive revision structure is primary."
        ),
        "confidence_divergence": (
            "Confidence diverges from Runtime A performance evidence."
        ),
        "default_session": "Default learning night — session shell is primary.",
        "study_fallback": "Session topic unavailable — study structure advice only.",
        "empty_authentic": "Insufficient inputs for authentic intervention structure.",
    }
    return mapping.get(
        composition_rule,
        "Strategy orchestration composed from Runtime A, Twin, and Adaptive inputs.",
    )


def _limitations_summary(limitations: tuple[str, ...]) -> str:
    if not limitations:
        return ""
    return "Limitations: " + ", ".join(limitations)
