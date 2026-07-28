"""Decision Journal enumerations (ILE-002).

Learner-facing educational memory states. Values are product vocabulary —
never Twin, ranking, or engine labels.
"""

from __future__ import annotations

from enum import StrEnum


class EntryKind(StrEnum):
    """Significant educational interaction kinds recorded in the journal."""

    MISSION_RECOMMENDATION = "mission_recommendation"
    QUICK_CHECK_RECOMMENDATION = "quick_check_recommendation"
    REVISION_RECOMMENDATION = "revision_recommendation"
    RECOVERY_RECOMMENDATION = "recovery_recommendation"
    LEARNING_MILESTONE = "learning_milestone"
    EDUCATIONAL_REFLECTION = "educational_reflection"


class JournalLifecycleStatus(StrEnum):
    """Lifecycle of one Decision Journal entry.

    Recommended → Accepted | Deferred → Evidence evolves → Reflection →
    Outcome → Archived. History is never rewritten; evidence appends.
    """

    RECOMMENDED = "recommended"
    ACCEPTED = "accepted"
    DEFERRED = "deferred"
    EVIDENCE_EVOLVING = "evidence_evolving"
    REFLECTED = "reflected"
    OUTCOME_RECORDED = "outcome_recorded"
    ARCHIVED = "archived"


class QualitativeConfidence(StrEnum):
    """ILE-011 qualitative confidence — never numeric scores."""

    INSUFFICIENT = "insufficient"
    OBSERVATION_ONLY = "observation_only"
    EMERGING = "emerging"
    RELIABLE = "reliable"
    HIGH = "high"


class StudentAction(StrEnum):
    """What the learner chose in response to guidance."""

    NONE_YET = "none_yet"
    ACCEPTED = "accepted"
    DEFERRED = "deferred"
    DISMISSED = "dismissed"


class ReflectionStatus(StrEnum):
    """Whether reflection has closed the educational loop."""

    PENDING = "pending"
    REFLECTED = "reflected"
    NOT_APPLICABLE = "not_applicable"
