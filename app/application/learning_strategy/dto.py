"""Learning Strategy Engine DTOs (KWP-007).

Educational recommendations — not scores. Consumes existing evidence /
Progress / Twin signals; never evaluates evidence or advances Journey.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class StrategyAction(StrEnum):
    """Student-facing educational strategy vocabulary (titles, not scores)."""

    ADVANCE_TOPIC = "advance_topic"
    CONSOLIDATE_UNDERSTANDING = "consolidate_understanding"
    IMMEDIATE_REINFORCEMENT = "immediate_reinforcement"
    SCHEDULED_REVISION = "scheduled_revision"
    INCREASE_CHALLENGE = "increase_challenge"
    RECOVER_PRIOR_KNOWLEDGE = "recover_prior_knowledge"
    MAINTAIN_CURRENT_PACE = "maintain_current_pace"
    SLOW_PROGRESSION = "slow_progression"
    REPEAT_PRACTICE = "repeat_practice"
    PRACTICE_FOR_CERTAINTY = "practice_for_certainty"


class SpacingDecision(StrEnum):
    """When to revisit — derived from educational evidence, not fixed dates."""

    IMMEDIATE = "immediate"
    TOMORROW = "tomorrow"
    THIS_WEEK = "this_week"
    LATER = "later"
    NO_REVIEW = "no_review"


class MomentumPosture(StrEnum):
    """Learning momentum derived from existing sitting / cadence signals."""

    RECOVERY = "recovery"
    PLATEAU = "plateau"
    ACCELERATION = "acceleration"
    CONSISTENCY = "consistency"
    TOPIC_STABILITY = "topic_stability"
    QUIET = "quiet"


class ConfidenceCalibration(StrEnum):
    """Internal calibration only — never render these labels to students."""

    HEALTHY = "healthy"
    OVER_CONFIDENT = "over_confident"
    UNDER_CONFIDENT = "under_confident"
    UNKNOWN = "unknown"


# Student-safe titles for StrategyAction (product language).
STRATEGY_TITLES: dict[StrategyAction, str] = {
    StrategyAction.ADVANCE_TOPIC: "Advance Topic",
    StrategyAction.CONSOLIDATE_UNDERSTANDING: "Consolidate Understanding",
    StrategyAction.IMMEDIATE_REINFORCEMENT: "Immediate Reinforcement",
    StrategyAction.SCHEDULED_REVISION: "Scheduled Revision",
    StrategyAction.INCREASE_CHALLENGE: "Increase Challenge",
    StrategyAction.RECOVER_PRIOR_KNOWLEDGE: "Recover Prior Knowledge",
    StrategyAction.MAINTAIN_CURRENT_PACE: "Maintain Current Pace",
    StrategyAction.SLOW_PROGRESSION: "Slow Progression",
    StrategyAction.REPEAT_PRACTICE: "Repeat Practice",
    StrategyAction.PRACTICE_FOR_CERTAINTY: "Practice to Build Certainty",
}


@dataclass(frozen=True)
class StrategyEvidenceInput:
    """Opaque educational facts the engine may consume.

    All fields are optional / defaulted so thin sittings remain lawful.
    The engine never invents missing evidence.
    """

    topic_title: str = ""
    learning_objectives: tuple[str, ...] = ()
    practice_correct: int = 0
    practice_incorrect: int = 0
    practice_attempted: int = 0
    practice_unscored: int = 0
    finish_verdict: str = ""
    progress_advanced: bool = False
    mission_completed: bool = False
    evidence_disposition: str = ""
    has_reflection: bool = False
    abandoned: bool = False
    reported_confidence: float | None = None
    twin_confidence_band: str = ""
    days_since_topic_practice: int | None = None
    retention_risk: bool = False
    weak_topic: bool = False
    recent_session_count: int | None = None
    streak_days: int | None = None
    consecutive_partial_finishes: int = 0
    consecutive_strong_sittings: int = 0
    next_topic_title: str = ""

    @classmethod
    def from_opaque(
        cls,
        opaque: dict[str, Any] | None = None,
        *,
        metadata: dict[str, Any] | None = None,
        twin_signals: dict[str, Any] | None = None,
        cadence: dict[str, Any] | None = None,
    ) -> StrategyEvidenceInput:
        """Build inputs from sitting opaque summary + optional enrichments."""
        raw = dict(opaque or {})
        meta = dict(metadata or {})
        twin = dict(twin_signals or {})
        cad = dict(cadence or {})

        counts = _practice_counts(raw)
        finish = _finish_verdict(raw, meta)
        confidence = _reported_confidence(raw, twin)
        topic = str(
            raw.get("topic_title")
            or meta.get("topic_title")
            or ""
        ).strip()
        objectives = _string_tuple(
            raw.get("learning_objectives") or raw.get("objectives")
        )
        type_ids = _type_ids(raw)

        return cls(
            topic_title=topic,
            learning_objectives=objectives,
            practice_correct=counts["correct"],
            practice_incorrect=counts["incorrect"],
            practice_attempted=counts["attempted"],
            practice_unscored=counts["unscored"],
            finish_verdict=finish,
            progress_advanced=_truthy(
                meta.get("progress_advanced")
            )
            or bool(raw.get("progress_advanced")),
            mission_completed=_truthy(meta.get("mission_completed"))
            or bool(raw.get("mission_completed")),
            evidence_disposition=str(
                meta.get("evidence_disposition")
                or raw.get("evidence_disposition")
                or ""
            )
            .strip()
            .lower(),
            has_reflection="EV-RT-10" in type_ids
            or bool(raw.get("has_reflection")),
            abandoned="EV-RT-29" in type_ids
            or bool(raw.get("abandoned"))
            or str(raw.get("lifecycle_state") or "").lower()
            in {"abandoned", "interrupted"},
            reported_confidence=confidence,
            twin_confidence_band=str(
                twin.get("confidence_band")
                or twin.get("overall_band")
                or raw.get("twin_confidence_band")
                or ""
            )
            .strip()
            .lower(),
            days_since_topic_practice=_optional_int(
                twin.get("days_since_topic_practice")
                or raw.get("days_since_topic_practice")
            ),
            retention_risk=bool(
                twin.get("retention_risk") or raw.get("retention_risk")
            ),
            weak_topic=bool(twin.get("weak_topic") or raw.get("weak_topic")),
            recent_session_count=_optional_int(
                cad.get("recent_session_count")
                or raw.get("recent_session_count")
            ),
            streak_days=_optional_int(
                cad.get("streak_days") or raw.get("streak_days")
            ),
            consecutive_partial_finishes=int(
                cad.get("consecutive_partial_finishes")
                or raw.get("consecutive_partial_finishes")
                or 0
            ),
            consecutive_strong_sittings=int(
                cad.get("consecutive_strong_sittings")
                or raw.get("consecutive_strong_sittings")
                or 0
            ),
            next_topic_title=str(
                raw.get("next_recommendation")
                or meta.get("next_recommendation")
                or ""
            ).strip(),
        )


@dataclass(frozen=True)
class LearningStrategyAdvice:
    """Deterministic educational strategy recommendation with WHY."""

    action: StrategyAction
    recommendation_title: str
    recommendation_body: str
    explanation: str
    spacing: SpacingDecision
    spacing_guidance: str
    momentum: MomentumPosture
    momentum_guidance: str
    confidence_guidance: str
    rule_id: str
    reason_codes: tuple[str, ...] = ()
    # Internal only — never surface these strings to learners.
    calibration: ConfidenceCalibration = ConfidenceCalibration.UNKNOWN
    topic_title: str = ""
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    def to_opaque(self) -> dict[str, Any]:
        """Founder / test projection — includes internal calibration."""
        return {
            "action": self.action.value,
            "recommendation_title": self.recommendation_title,
            "recommendation_body": self.recommendation_body,
            "explanation": self.explanation,
            "spacing": self.spacing.value,
            "spacing_guidance": self.spacing_guidance,
            "momentum": self.momentum.value,
            "momentum_guidance": self.momentum_guidance,
            "confidence_guidance": self.confidence_guidance,
            "rule_id": self.rule_id,
            "reason_codes": list(self.reason_codes),
            "calibration": self.calibration.value,
            "topic_title": self.topic_title,
        }

    def student_projection(self) -> dict[str, str]:
        """Student-safe fields only — no calibration labels."""
        return {
            "recommendation_title": self.recommendation_title,
            "recommendation_body": self.recommendation_body,
            "explanation": self.explanation,
            "spacing_guidance": self.spacing_guidance,
            "momentum_guidance": self.momentum_guidance,
            "confidence_guidance": self.confidence_guidance,
        }


def _practice_counts(opaque: dict[str, Any]) -> dict[str, int]:
    if (
        opaque.get("practice_correct") is not None
        or opaque.get("practice_incorrect") is not None
    ):
        correct = int(opaque.get("practice_correct") or 0)
        incorrect = int(opaque.get("practice_incorrect") or 0)
        attempted = int(
            opaque.get("practice_attempted")
            or (correct + incorrect + int(opaque.get("practice_unscored") or 0))
        )
        return {
            "correct": max(0, correct),
            "incorrect": max(0, incorrect),
            "attempted": max(0, attempted),
            "unscored": int(opaque.get("practice_unscored") or 0),
        }
    correct = incorrect = attempted = unscored = 0
    for obs in opaque.get("observations") or ():
        if not isinstance(obs, dict):
            continue
        tid = str(obs.get("type_id") or "")
        payload = obs.get("payload") or {}
        if tid == "EV-RT-07":
            correct += 1
            attempted += 1
        elif tid == "EV-RT-08":
            incorrect += 1
            attempted += 1
        elif tid == "EV-RT-40":
            attempted += 1
            if payload.get("scored_correct") is True or payload.get("correct") is True:
                correct += 1
            elif (
                payload.get("scored_correct") is False
                or payload.get("correct") is False
            ):
                incorrect += 1
        elif tid in {"EV-RT-06", "EV-RT-09"}:
            attempted += 1
            unscored += 1
    return {
        "correct": correct,
        "incorrect": incorrect,
        "attempted": attempted,
        "unscored": unscored,
    }


def _type_ids(opaque: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for obs in opaque.get("observations") or ():
        if isinstance(obs, dict) and obs.get("type_id"):
            ids.add(str(obs["type_id"]))
    for tid in opaque.get("observation_type_ids") or ():
        ids.add(str(tid))
    return ids


def _finish_verdict(opaque: dict[str, Any], meta: dict[str, Any]) -> str:
    review = opaque.get("finish_review")
    if isinstance(review, dict):
        verdict = str(review.get("verdict") or "").strip().lower()
        if verdict:
            return verdict
    raw = str(
        meta.get("finish_review")
        or opaque.get("finish_review_verdict")
        or ""
    ).strip().lower()
    if raw in {"yes", "partially", "no"}:
        return raw
    type_ids = _type_ids(opaque)
    if "EV-RT-23" in type_ids:
        return "yes"
    if "EV-RT-24" in type_ids:
        return "partially"
    if "EV-RT-25" in type_ids:
        return "no"
    return raw


def _reported_confidence(
    opaque: dict[str, Any], twin: dict[str, Any]
) -> float | None:
    for key in ("reported_confidence", "concept_confidence", "confidence"):
        if opaque.get(key) is not None:
            try:
                value = float(opaque[key])
            except (TypeError, ValueError):
                continue
            if value > 1.0:
                value = value / 100.0
            return max(0.0, min(1.0, value))
    for obs in opaque.get("observations") or ():
        if not isinstance(obs, dict):
            continue
        if str(obs.get("type_id") or "") != "EV-RT-12":
            continue
        payload = obs.get("payload") or {}
        raw = payload.get("confidence")
        if raw is None:
            raw = payload.get("score")
        if raw is None:
            continue
        try:
            value = float(raw)
        except (TypeError, ValueError):
            continue
        if value > 1.0:
            value = value / 100.0
        return max(0.0, min(1.0, value))
    if twin.get("confidence_score") is not None:
        try:
            value = float(twin["confidence_score"])
        except (TypeError, ValueError):
            return None
        if value > 1.0:
            value = value / 100.0
        return max(0.0, min(1.0, value))
    return None


def _string_tuple(value: Any) -> tuple[str, ...]:
    if not value:
        return ()
    if isinstance(value, str):
        text = value.strip()
        return (text,) if text else ()
    out: list[str] = []
    for item in value:
        text = str(item).strip()
        if text:
            out.append(text)
    return tuple(out)


def _truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
