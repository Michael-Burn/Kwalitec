"""Observation, attempt, and evidence enumerations.

Architecture Source
    knowledge/product/AP-002/EVIDENCE_MODEL.md
    knowledge/product/AP-002/SCORING_MODEL.md
"""

from __future__ import annotations

from enum import StrEnum


class ObservationKind(StrEnum):
    """Kinds of immutable facts the Assessment Engine may record.

    These classify what happened — never Twin mastery inferences.
    Mapping into Twin ObservationKind / AP-001 events is deferred.
    """

    QUESTION_ANSWERED = "question_answered"
    QUIZ_COMPLETED = "quiz_completed"
    REFLECTION_CAPTURED = "reflection_captured"
    FORMULA_REVIEWED = "formula_reviewed"
    WORKED_SOLUTION_REVIEWED = "worked_solution_reviewed"
    SESSION_ABANDONED = "session_abandoned"


class AttemptOutcome(StrEnum):
    """Deterministic evaluation label for a committed attempt (evidence only)."""

    CORRECT = "correct"
    PARTIAL = "partial"
    INCORRECT = "incorrect"
    SKIPPED = "skipped"
    ABANDONED = "abandoned"
    UNCODED = "uncoded"


class EvidenceSource(StrEnum):
    """Provenance class for assessment evidence packaging."""

    ASSESSMENT_ENGINE = "assessment_engine"
    STUDENT_RESPONSE = "student_response"
    INSTRUMENT_METADATA = "instrument_metadata"
    SESSION_SUMMARY = "session_summary"


class ConfidenceBand(StrEnum):
    """Coarse band derived from a 1–5 confidence rating (soft signal)."""

    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class DifficultyBand(StrEnum):
    """Ordered difficulty band for selection — not prestige judgement."""

    INTRODUCTORY = "introductory"
    STANDARD = "standard"
    STRETCH = "stretch"


class EvidenceStrengthBand(StrEnum):
    """Evidence strength band for observation packaging (SCORING_MODEL §8)."""

    THIN = "thin"
    MODERATE = "moderate"
    STRONG = "strong"
