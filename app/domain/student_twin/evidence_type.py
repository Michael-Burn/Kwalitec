"""Lawful evidence types that may update the Student Digital Twin.

Evidence only — never curriculum content, PDFs, or AI responses.
"""

from __future__ import annotations

from enum import StrEnum


class EvidenceType(StrEnum):
    """Observable learning evidence categories."""

    ACTIVITY_COMPLETED = "activity_completed"
    ASSESSMENT_OUTCOME = "assessment_outcome"
    PRACTICE_RESULT = "practice_result"
    REFLECTION = "reflection"
    SELF_ASSESSMENT = "self_assessment"
    RECALL_PERFORMANCE = "recall_performance"
    CONFIDENCE_RATING = "confidence_rating"
    TIME_ON_TASK = "time_on_task"
    SESSION_COMPLETION = "session_completion"
    MISSION_COMPLETION = "mission_completion"
    REVISION_OUTCOME = "revision_outcome"


def resolve_evidence_type(value: EvidenceType | str) -> EvidenceType:
    """Resolve a string or enum to EvidenceType."""
    if isinstance(value, EvidenceType):
        return value
    token = (value or "").strip().lower()
    try:
        return EvidenceType(token)
    except ValueError as exc:
        raise ValueError(f"unknown evidence type: {value!r}") from exc


# Outcome polarity for deterministic mastery updates (positive / negative / neutral).
POSITIVE_OUTCOMES = frozenset({"pass", "success", "correct", "strong", "high"})
NEGATIVE_OUTCOMES = frozenset({"fail", "failure", "incorrect", "weak", "low"})
NEUTRAL_OUTCOMES = frozenset({"partial", "skip", "unknown", "neutral", "medium"})
