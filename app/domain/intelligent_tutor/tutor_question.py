"""Student questions posed to the Intelligent Tutor."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum


class TutorQuestionKind(StrEnum):
    """Educational topic the student is asking about.

    Classification is heuristic and deterministic. It does not invent
    educational decisions — it only routes explanation focus.
    """

    DAILY_MISSION = "daily_mission"
    KNOWLEDGE_GAP = "knowledge_gap"
    WEAK_CONCEPT = "weak_concept"
    PREREQUISITE = "prerequisite"
    LEARNING_PATH = "learning_path"
    RECOVERY_PLAN = "recovery_plan"
    STUDY_STRATEGY = "study_strategy"
    CONFIDENCE_TREND = "confidence_trend"
    MASTERY_CHANGE = "mastery_change"
    ASSESSMENT_FEEDBACK = "assessment_feedback"
    GENERAL = "general"


_KEYWORD_KINDS: tuple[tuple[tuple[str, ...], TutorQuestionKind], ...] = (
    (
        ("mission", "today", "daily plan", "what should i do"),
        TutorQuestionKind.DAILY_MISSION,
    ),
    (
        ("gap", "missing", "don't understand", "dont understand"),
        TutorQuestionKind.KNOWLEDGE_GAP,
    ),
    (
        ("weak", "struggling", "struggle", "hard for me"),
        TutorQuestionKind.WEAK_CONCEPT,
    ),
    (
        ("prerequisite", "prereq", "before i", "foundation"),
        TutorQuestionKind.PREREQUISITE,
    ),
    (("path", "roadmap", "sequence", "order"), TutorQuestionKind.LEARNING_PATH),
    (
        ("recovery", "catch up", "behind", "repair"),
        TutorQuestionKind.RECOVERY_PLAN,
    ),
    (
        ("strategy", "how to study", "study tip", "approach"),
        TutorQuestionKind.STUDY_STRATEGY,
    ),
    (("confidence", "sure", "uncertain"), TutorQuestionKind.CONFIDENCE_TREND),
    (
        ("mastery", "progress", "improving", "improved"),
        TutorQuestionKind.MASTERY_CHANGE,
    ),
    (
        ("feedback", "assessment", "quiz", "attempt", "score"),
        TutorQuestionKind.ASSESSMENT_FEEDBACK,
    ),
)


@dataclass(frozen=True)
class TutorQuestion:
    """One student question within a Tutor conversation."""

    question_id: str
    twin_id: str
    text: str
    kind: TutorQuestionKind = TutorQuestionKind.GENERAL
    concept_id: str = ""
    mission_id: str = ""
    session_id: str = ""
    asked_at: datetime | None = None

    def __post_init__(self) -> None:
        if not (self.question_id or "").strip():
            raise ValueError("question_id is required")
        if not (self.twin_id or "").strip():
            raise ValueError("twin_id is required")
        if not (self.text or "").strip():
            raise ValueError("question text is required")
        kind = (
            self.kind
            if isinstance(self.kind, TutorQuestionKind)
            else TutorQuestionKind(str(self.kind))
        )
        object.__setattr__(self, "kind", kind)
        object.__setattr__(self, "text", self.text.strip())
        when = self.asked_at
        if when is not None and when.tzinfo is not None:
            object.__setattr__(
                self, "asked_at", when.astimezone(UTC).replace(tzinfo=None)
            )


def classify_question(text: str) -> TutorQuestionKind:
    """Deterministically classify a question from keyword cues."""
    lowered = (text or "").strip().lower()
    if not lowered:
        return TutorQuestionKind.GENERAL
    for keywords, kind in _KEYWORD_KINDS:
        if any(token in lowered for token in keywords):
            return kind
    return TutorQuestionKind.GENERAL
