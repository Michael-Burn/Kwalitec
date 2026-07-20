"""Evidence Interpretation domain enumerations.

Architecture Source
    EDUCATIONAL_EVIDENCE_MODEL.md /
    CAPABILITY_4_8_2_EDUCATIONAL_EVIDENCE_ANALYSIS.md
Concept
    Pattern Kind / Interpretation Status / Educational Scope Kind
"""

from __future__ import annotations

from enum import StrEnum


class PatternKind(StrEnum):
    """Kinds of interpreted educational patterns.

    Patterns describe repeated observational structure. They never diagnose,
    recommend, or prioritise learning actions.
    """

    REPEATED_RETRIEVAL_FAILURE = "repeated_retrieval_failure"
    REPEATED_TRANSFER_FAILURE = "repeated_transfer_failure"
    REPEATED_CONFIDENCE_MISMATCH = "repeated_confidence_mismatch"
    REPEATED_MISCONCEPTION_INDICATOR = "repeated_misconception_indicator"
    REPEATED_PROCEDURAL_ERROR = "repeated_procedural_error"
    REPEATED_REFLECTION_THEME = "repeated_reflection_theme"
    EVIDENCE_CONSISTENCY = "evidence_consistency"
    EVIDENCE_SUFFICIENCY = "evidence_sufficiency"
    TREND_STABILITY = "trend_stability"


class InterpretationStatus(StrEnum):
    """Lifecycle status of an Interpretation aggregate.

    Interpretation remains observational pattern memory. INVALIDATED voids
    interpretive trust without diagnosing; REVISED records lawful correction of
    pattern detail; MERGED marks an interpretation absorbed into another.
    """

    ACTIVE = "active"
    REVISED = "revised"
    INVALIDATED = "invalidated"
    MERGED = "merged"


class EducationalScopeKind(StrEnum):
    """Grain of educational scope identified by an interpretation."""

    CONCEPT = "concept"
    LEARNING_OBJECTIVE = "learning_objective"
    LEARNING_EPISODE = "learning_episode"
    LEARNING_DIMENSION = "learning_dimension"
    CROSS_CONCEPT = "cross_concept"
    SESSION_WINDOW = "session_window"
