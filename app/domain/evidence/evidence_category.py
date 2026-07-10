"""Evidence category vocabulary from the Learning Evidence Model.

Categories organise evidence kinds; they do not replace type-level semantics
or assign numerical weights.
"""

from __future__ import annotations

from enum import Enum


class EvidenceCategory(str, Enum):
    """High-level evidence categories for Evidence Candidates.

    Values are stable snake_case identifiers aligned with the Learning Evidence
    Model and Twin domain vocabulary. Adding a member here does not require
    architectural changes elsewhere in the domain package.
    """

    KNOWLEDGE = "knowledge"
    PERFORMANCE = "performance"
    BEHAVIOUR = "behaviour"
    TIME = "time"
    REVISION = "revision"
    CONFIDENCE = "confidence"
    PLANNING = "planning"
    ENGAGEMENT = "engagement"
    RETENTION = "retention"
    MOTIVATION = "motivation"


class EvidenceConfidenceLevel(str, Enum):
    """Qualitative confidence attached to an Evidence Candidate.

    Expresses how strongly downstream Twin updates *may* treat the candidate —
    not a numerical weight, score, or mastery estimate. Levels match the
    Learning Evidence Model confidence vocabulary.
    """

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"
