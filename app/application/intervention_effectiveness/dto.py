"""Educational Intervention Effectiveness DTOs (KWP-010).

Evaluates whether a prior educational recommendation improved subsequent
learning outcomes. Consumes existing Strategy / Difficulty recommendations
and sitting evidence — never redesigns those authorities.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from app.application.learning_difficulty.dto import LoadRecommendation
from app.application.learning_strategy.dto import (
    StrategyAction,
    StrategyEvidenceInput,
)


class InterventionKind(StrEnum):
    """Normalised intervention family under evaluation."""

    CONSOLIDATION = "consolidation"
    REINFORCEMENT = "reinforcement"
    REDUCE_SESSION_LENGTH = "reduce_session_length"
    INCREASE_SPACING = "increase_spacing"
    DECREASE_SPACING = "decrease_spacing"
    INCREASE_CHALLENGE = "increase_challenge"
    RECOVERY = "recovery"
    SLOW_PROGRESSION = "slow_progression"
    ADVANCE = "advance"
    MAINTAIN = "maintain"
    OTHER = "other"


class EffectivenessVerdict(StrEnum):
    """Internal outcome labels — never shown as scores to students."""

    EFFECTIVE = "effective"
    PARTIALLY_EFFECTIVE = "partially_effective"
    INEFFECTIVE = "ineffective"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


# Founder / audit labels only.
EFFECTIVENESS_VERDICT_LABELS: dict[EffectivenessVerdict, str] = {
    EffectivenessVerdict.EFFECTIVE: "Recommendation effective",
    EffectivenessVerdict.PARTIALLY_EFFECTIVE: "Recommendation partially effective",
    EffectivenessVerdict.INEFFECTIVE: "Recommendation ineffective",
    EffectivenessVerdict.INSUFFICIENT_EVIDENCE: "Insufficient evidence",
}

INTERVENTION_KIND_LABELS: dict[InterventionKind, str] = {
    InterventionKind.CONSOLIDATION: "Consolidation",
    InterventionKind.REINFORCEMENT: "Reinforcement",
    InterventionKind.REDUCE_SESSION_LENGTH: "Reduce session length",
    InterventionKind.INCREASE_SPACING: "Increase spacing",
    InterventionKind.DECREASE_SPACING: "Decrease spacing",
    InterventionKind.INCREASE_CHALLENGE: "Increase challenge",
    InterventionKind.RECOVERY: "Recovery",
    InterventionKind.SLOW_PROGRESSION: "Slow progression",
    InterventionKind.ADVANCE: "Advance",
    InterventionKind.MAINTAIN: "Maintain pace",
    InterventionKind.OTHER: "Other",
}


# Map StrategyAction → InterventionKind.
_STRATEGY_KIND: dict[StrategyAction, InterventionKind] = {
    StrategyAction.CONSOLIDATE_UNDERSTANDING: InterventionKind.CONSOLIDATION,
    StrategyAction.IMMEDIATE_REINFORCEMENT: InterventionKind.REINFORCEMENT,
    StrategyAction.REPEAT_PRACTICE: InterventionKind.REINFORCEMENT,
    StrategyAction.PRACTICE_FOR_CERTAINTY: InterventionKind.REINFORCEMENT,
    StrategyAction.SCHEDULED_REVISION: InterventionKind.INCREASE_SPACING,
    StrategyAction.INCREASE_CHALLENGE: InterventionKind.INCREASE_CHALLENGE,
    StrategyAction.RECOVER_PRIOR_KNOWLEDGE: InterventionKind.RECOVERY,
    StrategyAction.SLOW_PROGRESSION: InterventionKind.SLOW_PROGRESSION,
    StrategyAction.ADVANCE_TOPIC: InterventionKind.ADVANCE,
    StrategyAction.MAINTAIN_CURRENT_PACE: InterventionKind.MAINTAIN,
}

# Map LoadRecommendation → InterventionKind (pacing interventions).
_LOAD_KIND: dict[LoadRecommendation, InterventionKind] = {
    LoadRecommendation.TAKE_CONSOLIDATION_SESSION: InterventionKind.CONSOLIDATION,
    LoadRecommendation.REDUCE_SESSION_LENGTH: InterventionKind.REDUCE_SESSION_LENGTH,
    LoadRecommendation.INCREASE_SPACING: InterventionKind.INCREASE_SPACING,
    LoadRecommendation.DECREASE_SPACING: InterventionKind.DECREASE_SPACING,
    LoadRecommendation.INCREASE_CHALLENGE: InterventionKind.INCREASE_CHALLENGE,
    LoadRecommendation.SPLIT_TOPIC: InterventionKind.CONSOLIDATION,
    LoadRecommendation.CONTINUE: InterventionKind.MAINTAIN,
    LoadRecommendation.MAINTAIN_PACE: InterventionKind.MAINTAIN,
}


@dataclass(frozen=True)
class PriorIntervention:
    """A recommendation issued on a prior sitting (inputs only)."""

    kind: InterventionKind = InterventionKind.OTHER
    strategy_action: str = ""
    load_recommendation: str = ""
    topic_title: str = ""
    # Baseline evidence at recommendation time (for delta comparison).
    baseline_correct: int = 0
    baseline_incorrect: int = 0
    baseline_attempted: int = 0
    baseline_duration_minutes: int | None = None
    baseline_finish_verdict: str = ""
    baseline_progress_advanced: bool = False
    source: str = ""  # strategy | difficulty | explicit | replayed

    @property
    def has_recommendation(self) -> bool:
        return bool(self.strategy_action or self.load_recommendation) or (
            self.kind is not InterventionKind.OTHER
        )

    @property
    def has_baseline_practice(self) -> bool:
        return self.baseline_attempted > 0 or (
            self.baseline_correct + self.baseline_incorrect > 0
        )


@dataclass(frozen=True)
class EffectivenessEvidenceInput:
    """Prior intervention + subsequent sitting evidence for evaluation."""

    prior: PriorIntervention = field(default_factory=PriorIntervention)
    # Subsequent sitting (current) outcomes.
    topic_title: str = ""
    practice_correct: int = 0
    practice_incorrect: int = 0
    practice_attempted: int = 0
    finish_verdict: str = ""
    progress_advanced: bool = False
    mission_completed: bool = False
    has_reflection: bool = False
    abandoned: bool = False
    reported_confidence: float | None = None
    retention_risk: bool = False
    weak_topic: bool = False
    session_duration_minutes: int | None = None
    days_since_topic_practice: int | None = None
    recovered_after_misses: bool = False
    consecutive_strong_sittings: int = 0
    consecutive_partial_finishes: int = 0

    @classmethod
    def from_opaque(
        cls,
        opaque: dict[str, Any] | None = None,
        *,
        metadata: dict[str, Any] | None = None,
        twin_signals: dict[str, Any] | None = None,
        cadence: dict[str, Any] | None = None,
        prior: PriorIntervention | None = None,
    ) -> EffectivenessEvidenceInput:
        """Build from subsequent sitting opaque + optional prior enrichment."""
        strategy = StrategyEvidenceInput.from_opaque(
            opaque,
            metadata=metadata,
            twin_signals=twin_signals,
            cadence=cadence,
        )
        raw = dict(opaque or {})
        cad = dict(cadence or {})
        twin = dict(twin_signals or {})
        meta = dict(metadata or {})

        resolved_prior = prior or prior_from_enrichment(
            opaque=raw, metadata=meta, cadence=cad, twin_signals=twin
        )
        duration = _optional_int(
            raw.get("session_duration_minutes")
            or raw.get("actual_duration_minutes")
            or cad.get("session_duration_minutes")
        )
        return cls(
            prior=resolved_prior,
            topic_title=strategy.topic_title
            or resolved_prior.topic_title
            or str(raw.get("topic_title") or "").strip(),
            practice_correct=strategy.practice_correct,
            practice_incorrect=strategy.practice_incorrect,
            practice_attempted=strategy.practice_attempted,
            finish_verdict=strategy.finish_verdict,
            progress_advanced=strategy.progress_advanced,
            mission_completed=strategy.mission_completed,
            has_reflection=strategy.has_reflection,
            abandoned=strategy.abandoned,
            reported_confidence=strategy.reported_confidence,
            retention_risk=strategy.retention_risk,
            weak_topic=strategy.weak_topic,
            session_duration_minutes=duration,
            days_since_topic_practice=strategy.days_since_topic_practice,
            recovered_after_misses=bool(
                raw.get("recovered_after_misses")
                or twin.get("recovered_after_misses")
                or cad.get("recovered_after_misses")
            ),
            consecutive_strong_sittings=strategy.consecutive_strong_sittings,
            consecutive_partial_finishes=strategy.consecutive_partial_finishes,
        )


@dataclass(frozen=True)
class InterventionEffectivenessReport:
    """Deterministic effectiveness evaluation with student-safe feedback."""

    verdict: EffectivenessVerdict
    intervention_kind: InterventionKind
    feedback: str
    explanation: str
    rule_id: str
    evidence_codes: tuple[str, ...] = ()
    topic_title: str = ""
    strategy_action: str = ""
    load_recommendation: str = ""
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    @property
    def has_student_feedback(self) -> bool:
        """True when natural feedback should surface (not insufficient)."""
        return (
            self.verdict is not EffectivenessVerdict.INSUFFICIENT_EVIDENCE
            and bool(self.feedback.strip())
        )

    def to_opaque(self) -> dict[str, Any]:
        return {
            "verdict": self.verdict.value,
            "verdict_label": EFFECTIVENESS_VERDICT_LABELS[self.verdict],
            "intervention_kind": self.intervention_kind.value,
            "feedback": self.feedback,
            "explanation": self.explanation,
            "rule_id": self.rule_id,
            "evidence_codes": list(self.evidence_codes),
            "topic_title": self.topic_title,
            "strategy_action": self.strategy_action,
            "load_recommendation": self.load_recommendation,
        }

    def student_projection(self) -> dict[str, str]:
        """Student-safe fields only — no verdict labels."""
        return {
            "feedback": self.feedback,
            "explanation": self.explanation,
        }


def kind_from_strategy(action: StrategyAction | str | None) -> InterventionKind:
    if action is None or action == "":
        return InterventionKind.OTHER
    if isinstance(action, StrategyAction):
        return _STRATEGY_KIND.get(action, InterventionKind.OTHER)
    try:
        return _STRATEGY_KIND.get(StrategyAction(str(action)), InterventionKind.OTHER)
    except ValueError:
        return InterventionKind.OTHER


def kind_from_load(recommendation: LoadRecommendation | str | None) -> InterventionKind:
    if recommendation is None or recommendation == "":
        return InterventionKind.OTHER
    if isinstance(recommendation, LoadRecommendation):
        return _LOAD_KIND.get(recommendation, InterventionKind.OTHER)
    try:
        return _LOAD_KIND.get(
            LoadRecommendation(str(recommendation)), InterventionKind.OTHER
        )
    except ValueError:
        return InterventionKind.OTHER


def resolve_kind(
    *,
    strategy_action: str = "",
    load_recommendation: str = "",
    preferred: InterventionKind | None = None,
) -> InterventionKind:
    """Prefer load pacing kinds when they are more specific than maintain."""
    if preferred is not None and preferred is not InterventionKind.OTHER:
        return preferred
    load_kind = kind_from_load(load_recommendation)
    strategy_kind = kind_from_strategy(strategy_action)
    # Prefer concrete pacing interventions over generic strategy maintain.
    if load_kind in {
        InterventionKind.REDUCE_SESSION_LENGTH,
        InterventionKind.INCREASE_SPACING,
        InterventionKind.DECREASE_SPACING,
        InterventionKind.CONSOLIDATION,
        InterventionKind.INCREASE_CHALLENGE,
    }:
        return load_kind
    if strategy_kind is not InterventionKind.OTHER:
        return strategy_kind
    return load_kind


def prior_from_enrichment(
    *,
    opaque: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
    cadence: dict[str, Any] | None = None,
    twin_signals: dict[str, Any] | None = None,
) -> PriorIntervention:
    """Extract prior intervention from optional enrichments (never invent)."""
    raw = dict(opaque or {})
    meta = dict(metadata or {})
    cad = dict(cadence or {})
    twin = dict(twin_signals or {})

    blob: dict[str, Any] = {}
    for source in (
        raw.get("prior_intervention"),
        meta.get("prior_intervention"),
        cad.get("prior_intervention"),
        twin.get("prior_intervention"),
    ):
        if isinstance(source, dict) and source:
            blob = dict(source)
            break

    # Flat keys also accepted for thin enrichments.
    strategy_action = str(
        blob.get("strategy_action")
        or raw.get("prior_strategy_action")
        or cad.get("prior_strategy_action")
        or meta.get("prior_strategy_action")
        or ""
    ).strip()
    load_recommendation = str(
        blob.get("load_recommendation")
        or raw.get("prior_load_recommendation")
        or cad.get("prior_load_recommendation")
        or meta.get("prior_load_recommendation")
        or ""
    ).strip()
    kind_raw = str(blob.get("kind") or blob.get("intervention_kind") or "").strip()
    preferred: InterventionKind | None = None
    if kind_raw:
        try:
            preferred = InterventionKind(kind_raw)
        except ValueError:
            preferred = None

    kind = resolve_kind(
        strategy_action=strategy_action,
        load_recommendation=load_recommendation,
        preferred=preferred,
    )
    if not strategy_action and not load_recommendation and preferred is None:
        return PriorIntervention()

    return PriorIntervention(
        kind=kind,
        strategy_action=strategy_action,
        load_recommendation=load_recommendation,
        topic_title=str(
            blob.get("topic_title")
            or raw.get("prior_topic_title")
            or ""
        ).strip(),
        baseline_correct=int(
            blob.get("baseline_correct")
            or blob.get("practice_correct")
            or 0
        ),
        baseline_incorrect=int(
            blob.get("baseline_incorrect")
            or blob.get("practice_incorrect")
            or 0
        ),
        baseline_attempted=int(
            blob.get("baseline_attempted")
            or blob.get("practice_attempted")
            or 0
        ),
        baseline_duration_minutes=_optional_int(
            blob.get("baseline_duration_minutes")
            or blob.get("session_duration_minutes")
        ),
        baseline_finish_verdict=str(
            blob.get("baseline_finish_verdict")
            or blob.get("finish_verdict")
            or ""
        )
        .strip()
        .lower(),
        baseline_progress_advanced=_truthy(
            blob.get("baseline_progress_advanced")
            or blob.get("progress_advanced")
        ),
        source=str(blob.get("source") or "explicit").strip() or "explicit",
    )


def prior_from_sitting(
    *,
    strategy_action: StrategyAction | str = "",
    load_recommendation: LoadRecommendation | str = "",
    topic_title: str = "",
    practice_correct: int = 0,
    practice_incorrect: int = 0,
    practice_attempted: int = 0,
    session_duration_minutes: int | None = None,
    finish_verdict: str = "",
    progress_advanced: bool = False,
    source: str = "replayed",
) -> PriorIntervention:
    """Build a PriorIntervention from a prior sitting's engine outputs."""
    action = (
        strategy_action.value
        if isinstance(strategy_action, StrategyAction)
        else str(strategy_action or "")
    )
    load = (
        load_recommendation.value
        if isinstance(load_recommendation, LoadRecommendation)
        else str(load_recommendation or "")
    )
    return PriorIntervention(
        kind=resolve_kind(strategy_action=action, load_recommendation=load),
        strategy_action=action,
        load_recommendation=load,
        topic_title=topic_title,
        baseline_correct=practice_correct,
        baseline_incorrect=practice_incorrect,
        baseline_attempted=practice_attempted
        or (practice_correct + practice_incorrect),
        baseline_duration_minutes=session_duration_minutes,
        baseline_finish_verdict=str(finish_verdict or "").strip().lower(),
        baseline_progress_advanced=progress_advanced,
        source=source,
    )


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}
