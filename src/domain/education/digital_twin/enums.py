"""Educational Digital Twin domain enumerations.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
    EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md
Concept
    Twin Status / Mastery / Retention / Misconception Presence / Trajectory
"""

from __future__ import annotations

from enum import StrEnum


class TwinStatus(StrEnum):
    """Lifecycle status of an EducationalDigitalTwin aggregate.

    The Twin remembers educational state. ACTIVE accepts memory updates;
    ARCHIVED is terminal and preserves history without further mutation.
    """

    ACTIVE = "active"
    ARCHIVED = "archived"


class LearnerActivityStatus(StrEnum):
    """Coarse activity posture recorded on LearnerState.

    This is remembered posture, not a diagnosis or priority decision.
    """

    ENGAGED = "engaged"
    IDLE = "idle"
    PAUSED = "paused"
    JOURNEY_COMPLETE = "journey_complete"


class MasteryBand(StrEnum):
    """Qualitative mastery band stored as educational memory.

    Bands are recorded beliefs supplied by authorised writers. The Twin does
    not invent, diagnose, or interpret mastery from raw evidence.
    """

    UNKNOWN = "unknown"
    NASCENT = "nascent"
    DEVELOPING = "developing"
    PROFICIENT = "proficient"
    MASTERED = "mastered"


class RetentionBand(StrEnum):
    """Qualitative retention band stored as educational memory.

    Retention describes remembered durability of learning — not a scheduling
    recommendation and not a diagnosis.
    """

    UNKNOWN = "unknown"
    FADING = "fading"
    FRAGILE = "fragile"
    STABLE = "stable"
    DURABLE = "durable"


class MisconceptionPresence(StrEnum):
    """Recorded presence of a misconception within Twin memory.

    Presence is remembered state. The Twin does not create hypotheses or
    diagnose misconceptions; it only stores presence updates it is given.
    """

    SUSPECTED = "suspected"
    ACTIVE = "active"
    DORMANT = "dormant"
    CLEARED = "cleared"


class TwinUpdateKind(StrEnum):
    """Kinds of Twin memory updates that emit TwinUpdated events."""

    EVIDENCE_RECORDED = "evidence_recorded"
    INTERVENTION_RECORDED = "intervention_recorded"
    MASTERY_UPDATED = "mastery_updated"
    RETENTION_UPDATED = "retention_updated"
    CONFIDENCE_UPDATED = "confidence_updated"
    CONCEPT_STATE_UPDATED = "concept_state_updated"
    MISCONCEPTION_STATE_UPDATED = "misconception_state_updated"
    LEARNER_STATE_UPDATED = "learner_state_updated"
    ARCHIVED = "archived"


class TrajectoryPointKind(StrEnum):
    """Kinds of points appended to the LearningTrajectory memory spine."""

    CREATED = "created"
    EVIDENCE = "evidence"
    INTERVENTION = "intervention"
    MASTERY = "mastery"
    RETENTION = "retention"
    CONFIDENCE = "confidence"
    CONCEPT = "concept"
    MISCONCEPTION = "misconception"
    LEARNER = "learner"
    ARCHIVE = "archive"
