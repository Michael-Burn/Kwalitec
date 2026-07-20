"""Evidence domain enumerations.

Architecture Source
    EDUCATIONAL_EVIDENCE_MODEL.md /
    CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md
Concept
    Evidence Item Kind / Source Kind / Record Status / Strength Level
"""

from __future__ import annotations

from enum import StrEnum


class EvidenceItemKind(StrEnum):
    """Kinds of educational observation items.

    These classify *what was observed*, never a diagnosis or recommendation.
    """

    QUESTION_RESPONSE = "question_response"
    REFLECTION = "reflection"
    WORKED_EXAMPLE_OUTCOME = "worked_example_outcome"
    RETRIEVAL_ATTEMPT = "retrieval_attempt"
    TRANSFER_ATTEMPT = "transfer_attempt"
    HINT_USAGE = "hint_usage"


class EvidenceSourceKind(StrEnum):
    """Provenance class of an educational evidence source."""

    STUDENT_ACTION = "student_action"
    ASSESSMENT = "assessment"
    REFLECTION_CAPTURE = "reflection_capture"
    SYSTEM_OBSERVATION = "system_observation"
    LEARNING_EPISODE = "learning_episode"


class EvidenceRecordStatus(StrEnum):
    """Lifecycle status of an EvidenceRecord aggregate.

    Evidence remains observational memory. INVALIDATED voids trust without
    deleting history; AMENDED records lawful correction of observational detail;
    MERGED marks a record whose items were absorbed into another.
    """

    ACTIVE = "active"
    AMENDED = "amended"
    INVALIDATED = "invalidated"
    MERGED = "merged"


class EvidenceStrengthLevel(StrEnum):
    """Epistemic strength of educational evidence.

    Derived from Educational Evidence Model quality levels (engagement →
    high-confidence assessment). Strength is observational warrant — not a
    mastery, readiness, or priority score.
    """

    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"
    VERY_STRONG = "very_strong"
