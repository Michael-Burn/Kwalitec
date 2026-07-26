"""Strategy planners (MS-005 S1).

Pure read-only planners that transform StrategyContext into advice components.
No planner may mutate its inputs or re-rank Adaptive recommendations.
"""

from __future__ import annotations

from collections.abc import Mapping

from app.infrastructure.adapters.strategy_engine.contracts import (
    AVAILABILITY_AVAILABLE,
    KIND_BREAK,
    KIND_CONFIDENCE_INTERVENTION,
    KIND_FATIGUE_MANAGEMENT,
    KIND_RECOVERY_PLAN,
    KIND_REVISION_PLAN,
    KIND_SESSION_PLAN,
    KIND_STUDY_PLAN,
    ConfidenceIntervention,
    FatigueIntervention,
    InterventionSequencing,
    InterventionStep,
    RecoveryPlanAdvice,
    RevisionPlanAdvice,
    RevisionWindow,
    SessionPlanAdvice,
    StrategyContext,
    StudyPlanAdvice,
)

PRINCIPLE_NIGHTLY_TOPIC = "ep.director.nightly_topic"
PRINCIPLE_COMPLETABLE_SHELL = "ep.session.completable_shell"
PRINCIPLE_HONESTY = "ep.honesty.completion_neq_mastery"
PRINCIPLE_RECOVERY = "ep.recovery.restart_that_counts"
PRINCIPLE_FATIGUE = "ep.fatigue.diminishing_returns"
PRINCIPLE_CONFIDENCE = "ep.confidence.calibrate_to_evidence"

DEFAULT_SESSION_MINUTES = 45


class StudyPlanner:
    """Advise multi-horizon study structure without owning StudyPlan SQL."""

    PLANNER_ID = "study_planner"

    def plan(self, context: StrategyContext) -> StudyPlanAdvice:
        focus = _adaptive_focus_topics(context)
        limitations: list[str] = []
        if context.adaptive_availability != AVAILABILITY_AVAILABLE:
            limitations.append("adaptive_unavailable")
        if context.runtime_a_availability != AVAILABILITY_AVAILABLE:
            limitations.append("runtime_a_unavailable")
        if not focus and "adaptive_unavailable" not in limitations:
            limitations.append("sparse_evidence")

        goals = dict(context.runtime_a.get("student_goals") or {})
        minutes = goals.get("daily_minutes") or goals.get("minutes_per_day")
        daily_band = ""
        if isinstance(minutes, int | float) and minutes > 0:
            daily_band = f"{int(minutes)}m"
        elif focus:
            daily_band = f"{DEFAULT_SESSION_MINUTES}m"

        twin_factors = _twin_factors_used(context, ("learning_rhythm", "consistency"))
        stage = (context.lifecycle_stage or "").strip() or "Learning"
        available = (
            bool(focus) or context.runtime_a_availability == AVAILABILITY_AVAILABLE
        )
        return StudyPlanAdvice(
            horizon_sessions=3 if focus else None,
            focus_topics=tuple(focus),
            daily_minutes_band=daily_band,
            stage_policy=stage,
            twin_factors_used=tuple(twin_factors),
            limitations=tuple(limitations),
            available=available and bool(focus),
        )


class SessionPlanner:
    """Build tonight's completable session shell around mission authority."""

    PLANNER_ID = "session_planner"

    def plan(self, context: StrategyContext) -> SessionPlanAdvice:
        mission_topic = _mission_topic(context)
        adaptive_topic = _adaptive_primary_topic(context)
        limitations: list[str] = []

        if context.runtime_a_availability != AVAILABILITY_AVAILABLE:
            limitations.append("runtime_a_unavailable")
        if context.adaptive_availability != AVAILABILITY_AVAILABLE:
            limitations.append("adaptive_unavailable")

        if mission_topic:
            primary = mission_topic
            advisory = (
                adaptive_topic
                if adaptive_topic and adaptive_topic != mission_topic
                else ""
            )
            mission_aligned = not advisory
        else:
            primary = adaptive_topic
            advisory = ""
            mission_aligned = False
            if not primary:
                limitations.append("no_session_topic")

        goals = dict(context.runtime_a.get("student_goals") or {})
        minutes_raw = goals.get("daily_minutes") or goals.get("minutes_per_day")
        total = (
            int(minutes_raw)
            if isinstance(minutes_raw, int | float) and minutes_raw > 0
            else DEFAULT_SESSION_MINUTES
        )
        # Mild fatigue shortening is expressed via FatigueManager; session keeps
        # goal minutes and lets sequencing / fatigue guidance advise adjustment.

        phases = ()
        if primary:
            orient = max(5, total // 9)
            close = max(5, total // 6)
            study = max(10, total - orient - close - 5)
            phases = (
                InterventionStep(
                    order=1,
                    action_code="orient",
                    summary=f"Confirm tonight's topic ({primary})",
                    minutes=orient,
                    intent="orient",
                ),
                InterventionStep(
                    order=2,
                    action_code="study_materials",
                    summary="Study external materials for the topic",
                    minutes=study,
                    intent="study_materials",
                ),
                InterventionStep(
                    order=3,
                    action_code="practice_close",
                    summary="Close with an honest performance check",
                    minutes=close,
                    intent="practice_close",
                ),
                InterventionStep(
                    order=4,
                    action_code="log_outcome",
                    summary="Record outcome via Runtime A completion path",
                    minutes=5,
                    intent="log_outcome",
                ),
            )

        twin_factors = _twin_factors_used(
            context, ("session_habits", "learning_rhythm")
        )
        return SessionPlanAdvice(
            primary_topic=primary,
            advisory_topic=advisory,
            phases=phases,
            total_minutes=total if primary else None,
            close_ritual="practice_outcome_honesty",
            materials_note="bring_your_own_materials",
            twin_factors_used=tuple(twin_factors),
            adaptive_decision_ref=context.adaptive_recommendation_ref,
            educational_principle_ids=(
                PRINCIPLE_NIGHTLY_TOPIC,
                PRINCIPLE_COMPLETABLE_SHELL,
            ),
            mission_aligned=mission_aligned,
            limitations=tuple(limitations),
            available=bool(primary),
        )


class RevisionPlanner:
    """Structure Adaptive revision priority without inventing topic rankings."""

    PLANNER_ID = "revision_planner"

    def plan(self, context: StrategyContext) -> RevisionPlanAdvice:
        limitations: list[str] = []
        if context.adaptive_availability != AVAILABILITY_AVAILABLE:
            limitations.append("adaptive_unavailable")
            return RevisionPlanAdvice(
                limitations=tuple(limitations),
                available=False,
            )

        topics = _adaptive_focus_topics(context)
        if not topics:
            limitations.append("sparse_evidence")
            return RevisionPlanAdvice(
                adaptive_decision_ref=context.adaptive_recommendation_ref,
                limitations=tuple(limitations),
                available=False,
            )

        # Preserve Adaptive order: primary window first, remainder as next window.
        primary = topics[0]
        remainder = topics[1:4]
        windows = [
            RevisionWindow(
                window_id="rev-1",
                due_band="near",
                topics=(primary,),
                suggested_minutes=25,
                rationale_codes=("adaptive_revision_priority",),
            )
        ]
        if remainder:
            windows.append(
                RevisionWindow(
                    window_id="rev-2",
                    due_band="next",
                    topics=tuple(remainder),
                    suggested_minutes=20,
                    rationale_codes=("adaptive_alternatives_order_preserved",),
                )
            )

        twin_ref = ""
        profile = dict(context.twin.get("profile") or {})
        revision_facet = dict(profile.get("revision_behaviour") or {})
        if revision_facet.get("availability") == AVAILABILITY_AVAILABLE:
            twin_ref = "twin.profile.revision_behaviour"
        elif context.twin_availability != AVAILABILITY_AVAILABLE:
            limitations.append("twin_unavailable")

        stage = (context.lifecycle_stage or "").strip().lower()
        available = stage == "revision" or bool(topics)
        return RevisionPlanAdvice(
            windows=tuple(windows),
            primary_revision_topic=primary,
            spacing_note=str(
                context.adaptive.get("revision_spacing")
                or context.adaptive.get("spacing_note")
                or ""
            ),
            twin_revision_behaviour_ref=twin_ref,
            adaptive_decision_ref=context.adaptive_recommendation_ref,
            limitations=tuple(limitations),
            available=available,
        )


class RecoveryPlanner:
    """Build restart structure after abandonment / failure / gap signals."""

    PLANNER_ID = "recovery_planner"

    def plan(self, context: StrategyContext) -> RecoveryPlanAdvice:
        trigger, refs = _detect_recovery_trigger(context)
        limitations: list[str] = []
        if context.runtime_a_availability != AVAILABILITY_AVAILABLE:
            limitations.append("runtime_a_unavailable")
        if not trigger:
            return RecoveryPlanAdvice(
                limitations=tuple(limitations),
                available=False,
            )

        restart = _mission_topic(context) or _adaptive_primary_topic(context)
        if not restart:
            limitations.append("no_restart_topic")

        twin_ref = ""
        profile = dict(context.twin.get("profile") or {})
        persistence = dict(profile.get("persistence") or {})
        if persistence.get("availability") == AVAILABILITY_AVAILABLE:
            twin_ref = "twin.profile.persistence"
        elif context.twin_availability != AVAILABILITY_AVAILABLE:
            limitations.append("twin_unavailable")

        steps = (
            InterventionStep(
                order=1,
                action_code="acknowledge_state",
                summary="Acknowledge what Runtime A already recorded",
                intent="honesty",
            ),
            InterventionStep(
                order=2,
                action_code="restart_topic",
                summary=(
                    f"Restart on {restart}" if restart else "Await topic authority"
                ),
                intent="restart",
            ),
            InterventionStep(
                order=3,
                action_code="short_session",
                summary="Use a short completable session shell",
                minutes=25,
                intent="session",
            ),
        )
        return RecoveryPlanAdvice(
            trigger_kind=trigger,
            runtime_a_refs=tuple(refs),
            restart_topic=restart,
            steps=steps,
            what_still_counts="Prior recorded attempts and progress remain facts",
            what_does_not_count="Incomplete sessions do not equal mastery",
            twin_persistence_ref=twin_ref,
            educational_principle_ids=(PRINCIPLE_RECOVERY, PRINCIPLE_HONESTY),
            limitations=tuple(limitations),
            available=bool(restart),
        )


class FatigueManager:
    """Derive fatigue guidance from Twin load + Runtime A activity density."""

    PLANNER_ID = "fatigue_manager"

    def plan(self, context: StrategyContext) -> FatigueIntervention:
        limitations: list[str] = []
        twin_available = context.twin_availability == AVAILABILITY_AVAILABLE
        runtime_available = context.runtime_a_availability == AVAILABILITY_AVAILABLE
        if not twin_available:
            limitations.append("twin_unavailable")
        if not runtime_available:
            limitations.append("runtime_a_unavailable")

        load_label, twin_ref = _twin_cognitive_load(context)
        attempt_count, activity_refs = _recent_activity(context)

        severity = _fatigue_severity(load_label=load_label, attempt_count=attempt_count)
        if not severity:
            return FatigueIntervention(
                limitations=tuple(limitations),
                available=False,
            )

        action = {
            "low": "reduce_intensity",
            "medium": "shorten_session",
            "high": "insert_break",
            "critical": "stop_for_tonight",
        }.get(severity, "")
        adjustment = {
            "low": -5,
            "medium": -10,
            "high": -15,
            "critical": None,
        }.get(severity)

        return FatigueIntervention(
            severity_band=severity,
            recommended_action=action,
            minutes_adjustment=adjustment,
            twin_cognitive_load_ref=twin_ref,
            runtime_a_activity_refs=tuple(activity_refs),
            educational_principle_ids=(PRINCIPLE_FATIGUE,),
            limitations=tuple(limitations),
            available=True,
        )


class ConfidenceManager:
    """Calibrate confidence interventions to Runtime A performance evidence."""

    PLANNER_ID = "confidence_manager"

    def plan(self, context: StrategyContext) -> ConfidenceIntervention:
        limitations: list[str] = []
        if context.twin_availability != AVAILABILITY_AVAILABLE:
            limitations.append("twin_unavailable")
        if context.runtime_a_availability != AVAILABILITY_AVAILABLE:
            limitations.append("runtime_a_unavailable")
            return ConfidenceIntervention(
                limitations=tuple(limitations),
                available=False,
            )

        trend_label, twin_ref = _twin_confidence_trend(context)
        performance_band, perf_refs = _runtime_performance_band(context)
        divergence = _confidence_divergence(
            twin_label=trend_label,
            performance_band=performance_band,
        )
        if divergence in ("", "none") and not twin_ref:
            return ConfidenceIntervention(
                divergence_band="none" if performance_band else "",
                limitations=tuple(limitations),
                available=False,
            )

        action = {
            "none": "affirm_cautious",
            "mild": "request_practice_close",
            "material": "reduce_certainty_copy",
            "severe": "assess_structure",
        }.get(divergence, "")

        return ConfidenceIntervention(
            divergence_band=divergence or "none",
            twin_confidence_trend_ref=twin_ref,
            runtime_a_performance_refs=tuple(perf_refs),
            recommended_action=action,
            honesty_guard_copy_codes=(
                ("completion_neq_mastery",)
                if divergence in ("material", "severe")
                else ()
            ),
            educational_principle_ids=(PRINCIPLE_CONFIDENCE, PRINCIPLE_HONESTY),
            limitations=tuple(limitations),
            available=divergence not in ("", "none") or bool(perf_refs),
        )


class InterventionPlanner:
    """Compose planner outputs into primary + supporting sequencing."""

    PLANNER_ID = "intervention_planner"

    def compose(
        self,
        context: StrategyContext,
        *,
        study: StudyPlanAdvice,
        session: SessionPlanAdvice,
        revision: RevisionPlanAdvice,
        recovery: RecoveryPlanAdvice,
        fatigue: FatigueIntervention,
        confidence: ConfidenceIntervention,
    ) -> InterventionSequencing:
        """Select primary intervention kind per INTERVENTION_MODEL composition rules."""
        _ = context
        if fatigue.available and fatigue.severity_band == "critical":
            return InterventionSequencing(
                primary_kind=KIND_FATIGUE_MANAGEMENT,
                supporting_kinds=_supporting(
                    [
                        KIND_BREAK,
                        KIND_SESSION_PLAN if session.available else "",
                        KIND_STUDY_PLAN if study.available else "",
                    ]
                ),
                priority_band="critical",
                composition_rule="fatigue_critical",
            )

        if recovery.available and recovery.trigger_kind:
            return InterventionSequencing(
                primary_kind=KIND_RECOVERY_PLAN,
                supporting_kinds=_supporting(
                    [
                        KIND_SESSION_PLAN if session.available else "",
                        KIND_FATIGUE_MANAGEMENT if fatigue.available else "",
                        KIND_CONFIDENCE_INTERVENTION if confidence.available else "",
                    ]
                ),
                priority_band="high",
                composition_rule="recovery_trigger",
            )

        stage = (context.lifecycle_stage or "").strip().lower()
        if stage == "revision" and revision.available:
            return InterventionSequencing(
                primary_kind=KIND_REVISION_PLAN,
                supporting_kinds=_supporting(
                    [
                        KIND_STUDY_PLAN if study.available else "",
                        KIND_CONFIDENCE_INTERVENTION if confidence.available else "",
                        KIND_FATIGUE_MANAGEMENT if fatigue.available else "",
                    ]
                ),
                priority_band="high",
                composition_rule="revision_lifecycle",
            )

        if (
            confidence.available
            and confidence.divergence_band in ("material", "severe")
            and not session.available
        ):
            return InterventionSequencing(
                primary_kind=KIND_CONFIDENCE_INTERVENTION,
                supporting_kinds=_supporting(
                    [
                        KIND_STUDY_PLAN if study.available else "",
                        KIND_FATIGUE_MANAGEMENT if fatigue.available else "",
                    ]
                ),
                priority_band="medium",
                composition_rule="confidence_divergence",
            )

        supporting = _supporting(
            [
                KIND_STUDY_PLAN if study.available else "",
                KIND_REVISION_PLAN
                if revision.available and stage != "revision"
                else "",
                KIND_FATIGUE_MANAGEMENT if fatigue.available else "",
                KIND_CONFIDENCE_INTERVENTION
                if confidence.available
                and confidence.divergence_band in ("mild", "material", "severe")
                else "",
                KIND_RECOVERY_PLAN if recovery.available else "",
            ]
        )
        if session.available:
            return InterventionSequencing(
                primary_kind=KIND_SESSION_PLAN,
                supporting_kinds=supporting,
                priority_band="medium",
                composition_rule="default_session",
            )
        if study.available:
            return InterventionSequencing(
                primary_kind=KIND_STUDY_PLAN,
                supporting_kinds=supporting,
                priority_band="low",
                composition_rule="study_fallback",
            )
        return InterventionSequencing(
            primary_kind="",
            supporting_kinds=(),
            priority_band="",
            composition_rule="empty_authentic",
        )


def _supporting(kinds: list[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    ordered: list[str] = []
    for kind in kinds:
        value = (kind or "").strip().upper()
        if not value or value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return tuple(ordered)


def _adaptive_primary_topic(context: StrategyContext) -> str:
    adaptive = dict(context.adaptive or {})
    recommendation = dict(adaptive.get("recommendation") or {})
    topic = str(
        recommendation.get("topic_code")
        or adaptive.get("topic_code")
        or ""
    ).strip()
    return topic


def _adaptive_focus_topics(context: StrategyContext) -> list[str]:
    """Preserve Adaptive ranking order (primary then alternatives)."""
    topics: list[str] = []
    seen: set[str] = set()

    def _add(code: str) -> None:
        value = (code or "").strip()
        if not value or value in seen:
            return
        seen.add(value)
        topics.append(value)

    _add(_adaptive_primary_topic(context))

    adaptive = dict(context.adaptive or {})
    explanation = dict(adaptive.get("explanation") or {})
    for ref in explanation.get("topic_refs") or ():
        if isinstance(ref, Mapping):
            _add(str(ref.get("topic_code") or ""))
        else:
            _add(str(ref))

    for alt in adaptive.get("alternatives") or ():
        if isinstance(alt, Mapping):
            _add(str(alt.get("topic_code") or ""))
        else:
            _add(str(alt))

    # Explicit revision_priority list when Adaptive exposes it — order preserved.
    for item in adaptive.get("revision_priority") or ():
        if isinstance(item, Mapping):
            _add(str(item.get("topic_code") or ""))
        else:
            _add(str(item))

    return topics


def _mission_topic(context: StrategyContext) -> str:
    mission = dict(context.runtime_a.get("mission") or {})
    return str(
        mission.get("topic_code")
        or mission.get("topic_id")
        or mission.get("topic")
        or ""
    ).strip()


def _twin_factors_used(
    context: StrategyContext,
    facet_names: tuple[str, ...],
) -> list[str]:
    if context.twin_availability != AVAILABILITY_AVAILABLE:
        return []
    profile = dict(context.twin.get("profile") or {})
    used: list[str] = []
    for name in facet_names:
        facet = dict(profile.get(name) or {})
        if facet.get("availability") == AVAILABILITY_AVAILABLE:
            used.append(name)
    return used


def _twin_cognitive_load(context: StrategyContext) -> tuple[str, str]:
    if context.twin_availability != AVAILABILITY_AVAILABLE:
        return "", ""
    profile = dict(context.twin.get("profile") or {})
    facet = dict(profile.get("cognitive_load_indicators") or {})
    if facet.get("availability") != AVAILABILITY_AVAILABLE:
        return "", ""
    label = str(facet.get("label") or facet.get("load_note") or "").strip().lower()
    return label, "twin.profile.cognitive_load_indicators"


def _twin_confidence_trend(context: StrategyContext) -> tuple[str, str]:
    if context.twin_availability != AVAILABILITY_AVAILABLE:
        return "", ""
    profile = dict(context.twin.get("profile") or {})
    facet = dict(profile.get("confidence_trend") or {})
    if facet.get("availability") != AVAILABILITY_AVAILABLE:
        return "", ""
    label = str(facet.get("label") or facet.get("trend_note") or "").strip().lower()
    return label, "twin.profile.confidence_trend"


def _recent_activity(context: StrategyContext) -> tuple[int, list[str]]:
    attempts = list(context.runtime_a.get("study_attempts") or ())
    evidence = dict(context.runtime_a.get("evidence") or {})
    evidence_attempts = list(evidence.get("attempts") or ())
    rows = attempts or evidence_attempts
    refs: list[str] = []
    for row in rows[:10]:
        if not isinstance(row, Mapping):
            continue
        attempt_id = str(row.get("id") or row.get("attempt_id") or "").strip()
        if attempt_id:
            refs.append(f"attempt:{attempt_id}")
    return len(rows), refs


def _fatigue_severity(*, load_label: str, attempt_count: int) -> str:
    text = (load_label or "").lower()
    if "critical" in text or "exhausted" in text:
        return "critical"
    if "high" in text or "overload" in text or attempt_count >= 8:
        return "high"
    if "medium" in text or "moderate" in text or attempt_count >= 5:
        return "medium"
    if "low" in text or attempt_count >= 3:
        return "low"
    return ""


def _runtime_performance_band(context: StrategyContext) -> tuple[str, list[str]]:
    refs: list[str] = []
    scores: list[float] = []
    for row in context.runtime_a.get("topic_progress") or ():
        if not isinstance(row, Mapping):
            continue
        topic_id = str(row.get("topic_id") or "").strip()
        if topic_id:
            refs.append(f"topic_progress:{topic_id}")
        if row.get("mastery_score") is not None:
            try:
                scores.append(float(row.get("mastery_score")))
            except (TypeError, ValueError):
                continue
    for row in context.runtime_a.get("study_attempts") or ():
        if not isinstance(row, Mapping):
            continue
        attempt_id = str(row.get("id") or row.get("attempt_id") or "").strip()
        if attempt_id:
            refs.append(f"attempt:{attempt_id}")
        if row.get("score") is not None:
            try:
                scores.append(float(row.get("score")))
            except (TypeError, ValueError):
                continue
    if not scores:
        return "", refs[:8]
    mean = sum(scores) / len(scores)
    if mean >= 0.75:
        return "strong", refs[:8]
    if mean >= 0.45:
        return "mixed", refs[:8]
    return "weak", refs[:8]


def _confidence_divergence(*, twin_label: str, performance_band: str) -> str:
    text = (twin_label or "").lower()
    high_confidence = any(
        token in text for token in ("high", "rising", "confident", "overconfident")
    )
    low_confidence = any(
        token in text for token in ("low", "falling", "uncertain", "cautious")
    )
    if not performance_band:
        if high_confidence:
            return "mild"
        return "none" if text else ""
    if high_confidence and performance_band == "weak":
        return "severe"
    if high_confidence and performance_band == "mixed":
        return "material"
    if low_confidence and performance_band == "strong":
        return "mild"
    if high_confidence and performance_band == "strong":
        return "none"
    return "none"


def _detect_recovery_trigger(
    context: StrategyContext,
) -> tuple[str, list[str]]:
    mission = dict(context.runtime_a.get("mission") or {})
    status = str(mission.get("status") or "").strip().lower()
    mission_id = str(mission.get("mission_id") or mission.get("id") or "").strip()
    if status in {"abandoned", "cancelled", "interrupted"}:
        refs = [f"mission:{mission_id}"] if mission_id else []
        kind = (
            "interrupted_session" if status == "interrupted" else "abandoned_mission"
        )
        return kind, refs

    failed_refs: list[str] = []
    for row in context.runtime_a.get("study_attempts") or ():
        if not isinstance(row, Mapping):
            continue
        outcome = str(row.get("outcome") or row.get("result") or "").strip().lower()
        if outcome in {"failed", "fail", "incorrect"}:
            attempt_id = str(row.get("id") or row.get("attempt_id") or "").strip()
            if attempt_id:
                failed_refs.append(f"attempt:{attempt_id}")
    if failed_refs:
        return "failed_attempt", failed_refs[:5]

    gap_days = context.runtime_a.get("days_since_last_activity")
    if isinstance(gap_days, int | float) and gap_days >= 7:
        return "long_gap", ["runtime_a:days_since_last_activity"]
    return "", []
