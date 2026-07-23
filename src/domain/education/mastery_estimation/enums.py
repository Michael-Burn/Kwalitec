"""Mastery Estimation domain enumerations.

Architecture Source
    KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md
    STUDENT_DIGITAL_TWIN.md
    KNOWLEDGE_DEPENDENCY_MODEL.md
Concept
    Mastery Band / Learning Stability Band / Knowledge Gap Kind /
    Knowledge Gap Severity / Assessment Reason Code

Every band here is always *computed* deterministically by the Mastery
Estimation Engine from evidence, student state, and knowledge graph
structure. They are distinct from same-named vocabulary elsewhere — for
example ``domain.education.student_state.enums.MasteryBand`` records a
*supplied* posture, never a computed estimate. This context does not
import, or assume equivalence with, that type.
"""

from __future__ import annotations

from enum import StrEnum


class MasteryBand(StrEnum):
    """Qualitative band computed deterministically from a mastery magnitude.

    ``NOT_ASSESSED`` is reserved for competencies with no relevant evidence
    at all — it is never inferred from a low magnitude, only from the
    absence of evidence.
    """

    NOT_ASSESSED = "not_assessed"
    NOT_STARTED = "not_started"
    DEVELOPING = "developing"
    SECURE = "secure"
    MASTERED = "mastered"


class LearningStabilityBand(StrEnum):
    """Qualitative band describing the volatility of a mastery signal.

    ``INSUFFICIENT_DATA`` is reserved for fewer than two evidence points —
    variance is not a meaningful measurement below that.
    """

    INSUFFICIENT_DATA = "insufficient_data"
    VOLATILE = "volatile"
    MODERATE = "moderate"
    STABLE = "stable"


class KnowledgeGapKind(StrEnum):
    """Origin of a knowledge gap identified by the estimator.

    ``WEAK_EVIDENCE`` gaps are discovered directly from a competency's own
    supporting evidence. ``WEAK_PREREQUISITE`` gaps are discovered through
    the knowledge graph: a structural prerequisite of the competency is
    itself weak.
    """

    WEAK_EVIDENCE = "weak_evidence"
    WEAK_PREREQUISITE = "weak_prerequisite"


class KnowledgeGapSeverity(StrEnum):
    """Qualitative severity of an identified knowledge gap."""

    MINOR = "minor"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"


class AssessmentReasonCode(StrEnum):
    """Structured, machine-readable reason attached to an assessment.

    Reason codes are structured domain information describing *why* an
    assessment took its shape — never natural language explanation text.
    """

    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    STRONG_POSITIVE_EVIDENCE = "strong_positive_evidence"
    STRONG_NEGATIVE_EVIDENCE = "strong_negative_evidence"
    CONTRADICTORY_EVIDENCE = "contradictory_evidence"
    WEAK_PREREQUISITE = "weak_prerequisite"
    STABLE_PERFORMANCE = "stable_performance"
    VOLATILE_PERFORMANCE = "volatile_performance"
    RECENT_EVIDENCE_DOMINANT = "recent_evidence_dominant"
    STALE_EVIDENCE = "stale_evidence"
