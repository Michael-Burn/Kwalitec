"""Learning Diagnostics DTOs (KWP-008).

Internal diagnostic categories identify probable learning *causes*.
Students never see category labels — only guidance and cause explanations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from app.application.learning_strategy.dto import StrategyEvidenceInput


class DiagnosticCategory(StrEnum):
    """Internal cause categories — never render these names to students."""

    CONCEPTUAL_MISUNDERSTANDING = "conceptual_misunderstanding"
    PREREQUISITE_WEAKNESS = "prerequisite_weakness"
    FORMULA_RECALL_WEAKNESS = "formula_recall_weakness"
    CALCULATION_ACCURACY = "calculation_accuracy"
    READING_INTERPRETATION = "reading_interpretation"
    EXAM_TECHNIQUE = "exam_technique"
    CONFIDENCE_MISMATCH = "confidence_mismatch"
    RETENTION_DECAY = "retention_decay"
    INCONSISTENT_PRACTICE = "inconsistent_practice"
    IMPROVING_UNDERSTANDING = "improving_understanding"
    STRONG_PERFORMANCE = "strong_performance"
    INSUFFICIENT_SIGNAL = "insufficient_signal"


# Founder / audit labels only — not student copy.
DIAGNOSTIC_CATEGORY_LABELS: dict[DiagnosticCategory, str] = {
    DiagnosticCategory.CONCEPTUAL_MISUNDERSTANDING: "Conceptual misunderstanding",
    DiagnosticCategory.PREREQUISITE_WEAKNESS: "Prerequisite weakness",
    DiagnosticCategory.FORMULA_RECALL_WEAKNESS: "Formula recall weakness",
    DiagnosticCategory.CALCULATION_ACCURACY: "Calculation accuracy",
    DiagnosticCategory.READING_INTERPRETATION: "Reading interpretation",
    DiagnosticCategory.EXAM_TECHNIQUE: "Exam technique",
    DiagnosticCategory.CONFIDENCE_MISMATCH: "Confidence mismatch",
    DiagnosticCategory.RETENTION_DECAY: "Retention decay",
    DiagnosticCategory.INCONSISTENT_PRACTICE: "Inconsistent practice",
    DiagnosticCategory.IMPROVING_UNDERSTANDING: "Improving understanding",
    DiagnosticCategory.STRONG_PERFORMANCE: "Strong performance",
    DiagnosticCategory.INSUFFICIENT_SIGNAL: "Insufficient signal",
}


@dataclass(frozen=True)
class DiagnosticEvidenceInput:
    """Opaque educational facts for cause diagnosis.

    Built from sitting opaque summaries and optional Twin / cadence
    enrichments. Reuses StrategyEvidenceInput fields; adds practice-shape
    and topic-relationship signals when present.
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
    # Topic relationship enrichments (optional; never invented).
    prerequisite_title: str = ""
    dependent_topic_title: str = ""
    strong_prerequisite: bool = False
    # Practice-shape aggregates from activity / observation payloads.
    numeric_incorrect: int = 0
    numeric_correct: int = 0
    mcq_incorrect: int = 0
    short_structured_incorrect: int = 0
    reading_completed: bool = False
    reading_skipped: bool = False
    common_mistake_hints: tuple[str, ...] = ()
    practice_hints: tuple[str, ...] = ()
    # Multi-attempt pattern within a sitting (when observed).
    recovered_after_misses: bool = False

    @classmethod
    def from_strategy_input(
        cls,
        strategy: StrategyEvidenceInput,
        *,
        enrichments: dict[str, Any] | None = None,
    ) -> DiagnosticEvidenceInput:
        """Lift StrategyEvidenceInput plus optional diagnostic enrichments."""
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
            prerequisite_title=str(
                extra.get("prerequisite_title") or ""
            ).strip(),
            dependent_topic_title=str(
                extra.get("dependent_topic_title") or ""
            ).strip(),
            strong_prerequisite=bool(extra.get("strong_prerequisite")),
            numeric_incorrect=int(extra.get("numeric_incorrect") or 0),
            numeric_correct=int(extra.get("numeric_correct") or 0),
            mcq_incorrect=int(extra.get("mcq_incorrect") or 0),
            short_structured_incorrect=int(
                extra.get("short_structured_incorrect") or 0
            ),
            reading_completed=bool(extra.get("reading_completed")),
            reading_skipped=bool(extra.get("reading_skipped")),
            common_mistake_hints=_string_tuple(extra.get("common_mistake_hints")),
            practice_hints=_string_tuple(extra.get("practice_hints")),
            recovered_after_misses=bool(extra.get("recovered_after_misses")),
        )

    @classmethod
    def from_opaque(
        cls,
        opaque: dict[str, Any] | None = None,
        *,
        metadata: dict[str, Any] | None = None,
        twin_signals: dict[str, Any] | None = None,
        cadence: dict[str, Any] | None = None,
    ) -> DiagnosticEvidenceInput:
        """Build from sitting opaque summary — reuses StrategyEvidenceInput."""
        strategy = StrategyEvidenceInput.from_opaque(
            opaque,
            metadata=metadata,
            twin_signals=twin_signals,
            cadence=cadence,
        )
        raw = dict(opaque or {})
        twin = dict(twin_signals or {})
        shape = _practice_shape(raw)
        return cls.from_strategy_input(
            strategy,
            enrichments={
                "prerequisite_title": (
                    twin.get("prerequisite_title")
                    or twin.get("likely_prerequisite_title")
                    or raw.get("prerequisite_title")
                    or ""
                ),
                "dependent_topic_title": (
                    twin.get("dependent_topic_title")
                    or raw.get("dependent_topic_title")
                    or ""
                ),
                "strong_prerequisite": bool(
                    twin.get("strong_prerequisite")
                    or raw.get("strong_prerequisite")
                ),
                "numeric_incorrect": shape["numeric_incorrect"],
                "numeric_correct": shape["numeric_correct"],
                "mcq_incorrect": shape["mcq_incorrect"],
                "short_structured_incorrect": shape["short_structured_incorrect"],
                "reading_completed": shape["reading_completed"],
                "reading_skipped": shape["reading_skipped"],
                "common_mistake_hints": shape["common_mistake_hints"],
                "practice_hints": shape["practice_hints"],
                "recovered_after_misses": shape["recovered_after_misses"],
            },
        )


@dataclass(frozen=True)
class DiagnosticFinding:
    """One probable learning cause with student-safe guidance."""

    category: DiagnosticCategory
    guidance: str
    explanation: str
    rule_id: str
    evidence_codes: tuple[str, ...] = ()
    focus_topic: str = ""
    related_topic: str = ""
    # Internal polarity for confidence mismatch (never shown as label).
    mismatch_polarity: str = ""

    def to_opaque(self) -> dict[str, Any]:
        return {
            "category": self.category.value,
            "guidance": self.guidance,
            "explanation": self.explanation,
            "rule_id": self.rule_id,
            "evidence_codes": list(self.evidence_codes),
            "focus_topic": self.focus_topic,
            "related_topic": self.related_topic,
            "mismatch_polarity": self.mismatch_polarity,
        }


@dataclass(frozen=True)
class LearningDiagnosticsReport:
    """Deterministic diagnostic report — causes, not scores."""

    primary: DiagnosticFinding
    supporting: tuple[DiagnosticFinding, ...] = ()
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    @property
    def category(self) -> DiagnosticCategory:
        return self.primary.category

    @property
    def guidance(self) -> str:
        return self.primary.guidance

    @property
    def explanation(self) -> str:
        return self.primary.explanation

    @property
    def findings(self) -> tuple[DiagnosticFinding, ...]:
        return (self.primary, *self.supporting)

    def to_opaque(self) -> dict[str, Any]:
        return {
            "primary": self.primary.to_opaque(),
            "supporting": [f.to_opaque() for f in self.supporting],
            "category": self.primary.category.value,
            "guidance": self.primary.guidance,
            "explanation": self.primary.explanation,
        }

    def student_projection(self) -> dict[str, str]:
        """Student-safe fields only — no category labels."""
        return {
            "guidance": self.primary.guidance,
            "explanation": self.primary.explanation,
        }


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


def _practice_shape(opaque: dict[str, Any]) -> dict[str, Any]:
    """Derive practice-shape and reading signals from opaque sitting facts."""
    numeric_incorrect = int(opaque.get("numeric_incorrect") or 0)
    numeric_correct = int(opaque.get("numeric_correct") or 0)
    mcq_incorrect = int(opaque.get("mcq_incorrect") or 0)
    short_incorrect = int(opaque.get("short_structured_incorrect") or 0)
    mistakes: list[str] = []
    hints: list[str] = []
    reading_completed = bool(opaque.get("reading_completed"))
    reading_skipped = bool(opaque.get("reading_skipped"))
    recovered = bool(opaque.get("recovered_after_misses"))

    type_ids: set[str] = set()
    for obs in opaque.get("observations") or ():
        if not isinstance(obs, dict):
            continue
        tid = str(obs.get("type_id") or "")
        if tid:
            type_ids.add(tid)
        payload = obs.get("payload") or {}
        if not isinstance(payload, dict):
            continue
        rtype = str(
            payload.get("response_type") or payload.get("practice_response_type") or ""
        ).strip().lower()
        scored_correct = payload.get("scored_correct")
        if scored_correct is None:
            scored_correct = payload.get("correct")
        if tid == "EV-RT-07" or scored_correct is True:
            if rtype == "numeric":
                numeric_correct += 1
        if tid == "EV-RT-08" or scored_correct is False:
            if rtype == "numeric":
                numeric_incorrect += 1
            elif rtype == "mcq":
                mcq_incorrect += 1
            elif rtype in {"short_structured", "short"}:
                short_incorrect += 1
        mistake = str(payload.get("common_mistake") or "").strip()
        if mistake:
            mistakes.append(mistake)
        for hint in payload.get("hints") or ():
            text = str(hint).strip()
            if text:
                hints.append(text)

    if "EV-RT-03" in type_ids:
        reading_completed = True
    elif "EV-RT-02" in type_ids and "EV-RT-03" not in type_ids:
        reading_skipped = True
    # Also inspect activity stages when observation types are thin.
    for raw in opaque.get("activities") or opaque.get("activity_items") or ():
        if not isinstance(raw, dict):
            continue
        stage = str(raw.get("stage") or raw.get("activity_type") or "").lower()
        done = bool(
            raw.get("completed")
            or raw.get("done")
            or str(raw.get("status") or "").lower() == "completed"
        )
        if stage in {"reading", "read"}:
            if done:
                reading_completed = True
            else:
                reading_skipped = True
        rtype = str(raw.get("response_type") or "").strip().lower()
        scored = raw.get("scored_correct")
        if scored is None:
            scored = raw.get("correct")
        if scored is False:
            if rtype == "numeric":
                numeric_incorrect += 1
            elif rtype == "mcq":
                mcq_incorrect += 1
            elif rtype in {"short_structured", "short"}:
                short_incorrect += 1
        elif scored is True and rtype == "numeric":
            numeric_correct += 1
        mistake = str(raw.get("common_mistake") or "").strip()
        if mistake:
            mistakes.append(mistake)
        for hint in raw.get("hints") or ():
            text = str(hint).strip()
            if text:
                hints.append(text)

    correct = int(opaque.get("practice_correct") or 0)
    incorrect = int(opaque.get("practice_incorrect") or 0)
    if not recovered and correct > 0 and incorrect > 0 and correct >= incorrect:
        recovered = True

    return {
        "numeric_incorrect": numeric_incorrect,
        "numeric_correct": numeric_correct,
        "mcq_incorrect": mcq_incorrect,
        "short_structured_incorrect": short_incorrect,
        "reading_completed": reading_completed,
        "reading_skipped": reading_skipped,
        "common_mistake_hints": tuple(mistakes[:6]),
        "practice_hints": tuple(hints[:8]),
        "recovered_after_misses": recovered,
    }
