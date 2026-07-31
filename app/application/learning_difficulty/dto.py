"""Learning Difficulty & Cognitive Load DTOs (KWP-009).

Models how educationally demanding a topic is for a learner.
Internal bands and load levels never reach students as labels —
only natural pacing / intensity recommendations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from app.application.learning_strategy.dto import StrategyEvidenceInput


class ObjectiveComplexity(StrEnum):
    """Curriculum / authored topic complexity — not learner-specific."""

    LIGHT = "light"
    MODERATE = "moderate"
    DEMANDING = "demanding"
    INTENSIVE = "intensive"
    UNKNOWN = "unknown"


class ObservedDifficulty(StrEnum):
    """How difficult the topic has been *for this learner*."""

    LIGHT = "light"
    MODERATE = "moderate"
    DEMANDING = "demanding"
    VERY_DEMANDING = "very_demanding"
    UNKNOWN = "unknown"


class LearningEffort(StrEnum):
    """Estimated educational effort implied by evidence."""

    LOW = "low"
    STEADY = "steady"
    HIGH = "high"
    VERY_HIGH = "very_high"


class EducationalPacing(StrEnum):
    """Suggested educational pace relative to current journey."""

    HOLD = "hold"
    SLOW = "slow"
    MAINTAIN = "maintain"
    ACCELERATE = "accelerate"


class SessionIntensity(StrEnum):
    """How intense the recent / current sitting pattern is."""

    LIGHT = "light"
    STANDARD = "standard"
    HEAVY = "heavy"
    OVERLOADED = "overloaded"


class RevisionPressure(StrEnum):
    """Pressure to revisit / reinforce rather than advance."""

    NONE = "none"
    LIGHT = "light"
    ELEVATED = "elevated"
    URGENT = "urgent"


class LoadRecommendation(StrEnum):
    """Student-facing educational load recommendations (titles, not scores)."""

    CONTINUE = "continue"
    REDUCE_SESSION_LENGTH = "reduce_session_length"
    INCREASE_SPACING = "increase_spacing"
    DECREASE_SPACING = "decrease_spacing"
    TAKE_CONSOLIDATION_SESSION = "take_consolidation_session"
    SPLIT_TOPIC = "split_topic"
    INCREASE_CHALLENGE = "increase_challenge"
    MAINTAIN_PACE = "maintain_pace"


# Founder / audit labels only — never student copy.
OBJECTIVE_COMPLEXITY_LABELS: dict[ObjectiveComplexity, str] = {
    ObjectiveComplexity.LIGHT: "Light",
    ObjectiveComplexity.MODERATE: "Moderate",
    ObjectiveComplexity.DEMANDING: "Demanding",
    ObjectiveComplexity.INTENSIVE: "Intensive",
    ObjectiveComplexity.UNKNOWN: "Unknown",
}

OBSERVED_DIFFICULTY_LABELS: dict[ObservedDifficulty, str] = {
    ObservedDifficulty.LIGHT: "Light",
    ObservedDifficulty.MODERATE: "Moderate",
    ObservedDifficulty.DEMANDING: "Demanding",
    ObservedDifficulty.VERY_DEMANDING: "Very demanding",
    ObservedDifficulty.UNKNOWN: "Unknown",
}

LOAD_RECOMMENDATION_TITLES: dict[LoadRecommendation, str] = {
    LoadRecommendation.CONTINUE: "Continue",
    LoadRecommendation.REDUCE_SESSION_LENGTH: "Reduce Session Length",
    LoadRecommendation.INCREASE_SPACING: "Increase Spacing",
    LoadRecommendation.DECREASE_SPACING: "Decrease Spacing",
    LoadRecommendation.TAKE_CONSOLIDATION_SESSION: "Take Consolidation Session",
    LoadRecommendation.SPLIT_TOPIC: "Split Topic",
    LoadRecommendation.INCREASE_CHALLENGE: "Increase Challenge",
    LoadRecommendation.MAINTAIN_PACE: "Maintain Pace",
}

# Map CKG / authored difficulty strings → objective complexity.
_AUTHED_DIFFICULTY_MAP: dict[str, ObjectiveComplexity] = {
    "foundational": ObjectiveComplexity.LIGHT,
    "foundation": ObjectiveComplexity.LIGHT,
    "easy": ObjectiveComplexity.LIGHT,
    "light": ObjectiveComplexity.LIGHT,
    "introductory": ObjectiveComplexity.LIGHT,
    "intermediate": ObjectiveComplexity.MODERATE,
    "moderate": ObjectiveComplexity.MODERATE,
    "medium": ObjectiveComplexity.MODERATE,
    "advanced": ObjectiveComplexity.DEMANDING,
    "demanding": ObjectiveComplexity.DEMANDING,
    "hard": ObjectiveComplexity.DEMANDING,
    "capstone": ObjectiveComplexity.INTENSIVE,
    "intensive": ObjectiveComplexity.INTENSIVE,
    "expert": ObjectiveComplexity.INTENSIVE,
}


@dataclass(frozen=True)
class DifficultyEvidenceInput:
    """Opaque educational facts for difficulty / load modelling.

    Reuses StrategyEvidenceInput fields; adds duration, attempt history,
    reflection density, and optional authored topic complexity when present.
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
    # Difficulty / load enrichments (optional; never invented).
    authored_difficulty: str = ""
    session_duration_minutes: int | None = None
    topic_attempt_count: int = 0
    reinforcement_session_count: int = 0
    reflection_count: int = 0
    recovered_after_misses: bool = False
    recovered_after_difficult: bool = False
    partial_completion: bool = False

    @classmethod
    def from_strategy_input(
        cls,
        strategy: StrategyEvidenceInput,
        *,
        enrichments: dict[str, Any] | None = None,
    ) -> DifficultyEvidenceInput:
        """Lift StrategyEvidenceInput plus optional difficulty enrichments."""
        extra = dict(enrichments or {})
        return cls(
            topic_title=strategy.topic_title,
            learning_objectives=strategy.learning_objectives,
            practice_correct=strategy.practice_correct,
            practice_incorrect=strategy.practice_incorrect,
            practice_attempted=strategy.practice_attempted,
            practice_unscored=strategy.practice_unscored,
            finish_verdict=strategy.finish_verdict,
            progress_advanced=strategy.progress_advanced,
            mission_completed=strategy.mission_completed,
            has_reflection=strategy.has_reflection,
            abandoned=strategy.abandoned,
            reported_confidence=strategy.reported_confidence,
            twin_confidence_band=strategy.twin_confidence_band,
            days_since_topic_practice=strategy.days_since_topic_practice,
            retention_risk=strategy.retention_risk,
            weak_topic=strategy.weak_topic,
            recent_session_count=strategy.recent_session_count,
            streak_days=strategy.streak_days,
            consecutive_partial_finishes=strategy.consecutive_partial_finishes,
            consecutive_strong_sittings=strategy.consecutive_strong_sittings,
            next_topic_title=strategy.next_topic_title,
            authored_difficulty=str(
                extra.get("authored_difficulty")
                or extra.get("difficulty")
                or extra.get("difficulty_band")
                or ""
            )
            .strip()
            .lower(),
            session_duration_minutes=_optional_int(
                extra.get("session_duration_minutes")
                or extra.get("actual_duration_minutes")
            ),
            topic_attempt_count=int(extra.get("topic_attempt_count") or 0),
            reinforcement_session_count=int(
                extra.get("reinforcement_session_count") or 0
            ),
            reflection_count=int(extra.get("reflection_count") or 0),
            recovered_after_misses=bool(extra.get("recovered_after_misses")),
            recovered_after_difficult=bool(
                extra.get("recovered_after_difficult")
            ),
            partial_completion=bool(extra.get("partial_completion")),
        )

    @classmethod
    def from_opaque(
        cls,
        opaque: dict[str, Any] | None = None,
        *,
        metadata: dict[str, Any] | None = None,
        twin_signals: dict[str, Any] | None = None,
        cadence: dict[str, Any] | None = None,
    ) -> DifficultyEvidenceInput:
        """Build from sitting opaque summary — reuses StrategyEvidenceInput."""
        strategy = StrategyEvidenceInput.from_opaque(
            opaque,
            metadata=metadata,
            twin_signals=twin_signals,
            cadence=cadence,
        )
        raw = dict(opaque or {})
        twin = dict(twin_signals or {})
        cad = dict(cadence or {})
        meta = dict(metadata or {})
        shape = _load_shape(raw, meta=meta, twin=twin, cadence=cad)
        return cls.from_strategy_input(strategy, enrichments=shape)


@dataclass(frozen=True)
class DifficultyProfile:
    """Deterministic difficulty / load profile for one sitting or topic."""

    objective_complexity: ObjectiveComplexity
    observed_difficulty: ObservedDifficulty
    learning_effort: LearningEffort
    educational_pacing: EducationalPacing
    session_intensity: SessionIntensity
    revision_pressure: RevisionPressure
    recommendation: LoadRecommendation
    recommendation_title: str
    guidance: str
    explanation: str
    rule_id: str
    # Internal load points for founder analytics (0–100 scale, not product).
    load_points: int = 0
    evidence_codes: tuple[str, ...] = ()
    topic_title: str = ""
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    def to_opaque(self) -> dict[str, Any]:
        """Founder / test projection — includes internal bands."""
        return {
            "objective_complexity": self.objective_complexity.value,
            "observed_difficulty": self.observed_difficulty.value,
            "learning_effort": self.learning_effort.value,
            "educational_pacing": self.educational_pacing.value,
            "session_intensity": self.session_intensity.value,
            "revision_pressure": self.revision_pressure.value,
            "recommendation": self.recommendation.value,
            "recommendation_title": self.recommendation_title,
            "guidance": self.guidance,
            "explanation": self.explanation,
            "rule_id": self.rule_id,
            "load_points": self.load_points,
            "evidence_codes": list(self.evidence_codes),
            "topic_title": self.topic_title,
        }

    def student_projection(self) -> dict[str, str]:
        """Student-safe fields only — no band / load labels."""
        return {
            "recommendation_title": self.recommendation_title,
            "guidance": self.guidance,
            "explanation": self.explanation,
        }


def map_authored_difficulty(raw: str) -> ObjectiveComplexity:
    """Map authored / CKG difficulty strings to ObjectiveComplexity."""
    key = (raw or "").strip().lower()
    if not key:
        return ObjectiveComplexity.UNKNOWN
    return _AUTHED_DIFFICULTY_MAP.get(key, ObjectiveComplexity.UNKNOWN)


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _load_shape(
    opaque: dict[str, Any],
    *,
    meta: dict[str, Any],
    twin: dict[str, Any],
    cadence: dict[str, Any],
) -> dict[str, Any]:
    """Derive duration / attempt / reflection signals from opaque facts."""
    duration = _optional_int(
        opaque.get("session_duration_minutes")
        or opaque.get("actual_duration_minutes")
        or meta.get("session_duration_minutes")
        or meta.get("actual_duration_minutes")
    )
    topic_attempts = int(
        twin.get("topic_attempt_count")
        or opaque.get("topic_attempt_count")
        or cadence.get("topic_attempt_count")
        or 0
    )
    reinforcement = int(
        twin.get("reinforcement_session_count")
        or opaque.get("reinforcement_session_count")
        or cadence.get("reinforcement_session_count")
        or 0
    )
    # If topic was practised more than once recently, treat as reinforcement.
    if reinforcement == 0 and topic_attempts > 1:
        reinforcement = topic_attempts - 1

    reflection_count = int(opaque.get("reflection_count") or 0)
    type_ids: set[str] = set()
    for obs in opaque.get("observations") or ():
        if isinstance(obs, dict) and obs.get("type_id"):
            type_ids.add(str(obs["type_id"]))
    for tid in opaque.get("observation_type_ids") or ():
        type_ids.add(str(tid))
    if "EV-RT-10" in type_ids:
        reflection_count = max(reflection_count, 1)
    if opaque.get("has_reflection"):
        reflection_count = max(reflection_count, 1)

    recovered = bool(
        opaque.get("recovered_after_misses")
        or twin.get("recovered_after_misses")
    )
    correct = int(opaque.get("practice_correct") or 0)
    incorrect = int(opaque.get("practice_incorrect") or 0)
    if not recovered and correct > 0 and incorrect > 0 and correct >= incorrect:
        recovered = True

    recovered_difficult = bool(
        opaque.get("recovered_after_difficult")
        or twin.get("recovered_after_difficult")
        or (recovered and incorrect >= 2)
    )

    finish = str(
        (opaque.get("finish_review") or {}).get("verdict")
        if isinstance(opaque.get("finish_review"), dict)
        else opaque.get("finish_review_verdict") or meta.get("finish_review") or ""
    ).strip().lower()
    partial = (
        finish == "partially"
        or "EV-RT-24" in type_ids
        or bool(opaque.get("partial_completion"))
    )

    authored = str(
        twin.get("difficulty")
        or twin.get("difficulty_band")
        or twin.get("authored_difficulty")
        or opaque.get("difficulty")
        or opaque.get("difficulty_band")
        or opaque.get("authored_difficulty")
        or meta.get("difficulty")
        or ""
    ).strip().lower()

    return {
        "authored_difficulty": authored,
        "session_duration_minutes": duration,
        "topic_attempt_count": topic_attempts,
        "reinforcement_session_count": reinforcement,
        "reflection_count": reflection_count,
        "recovered_after_misses": recovered,
        "recovered_after_difficult": recovered_difficult,
        "partial_completion": partial,
    }
