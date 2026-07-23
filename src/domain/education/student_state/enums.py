"""Student Educational State domain enumerations.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
    EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md
Concept
    Subject Status / Mastery Band / Educational Health Band
"""

from __future__ import annotations

from enum import StrEnum


class SubjectStatus(StrEnum):
    """Coarse study posture of a subject within a student's current state.

    Status is supplied state, not a computed diagnosis.
    """

    NOT_STARTED = "not_started"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"


class MasteryBand(StrEnum):
    """Qualitative mastery band recorded for a competency or as a summary.

    Bands are supplied state. This aggregate does not estimate, infer, or
    diagnose mastery from evidence — it only stores what it is given.
    """

    UNKNOWN = "unknown"
    NOT_STARTED = "not_started"
    DEVELOPING = "developing"
    SECURE = "secure"
    MASTERED = "mastered"


class EducationalHealthBand(StrEnum):
    """Qualitative overall educational health band.

    Supplied state describing the student's current educational posture —
    never computed by probabilistic estimation inside this aggregate.
    """

    UNKNOWN = "unknown"
    CRITICAL = "critical"
    AT_RISK = "at_risk"
    STABLE = "stable"
    THRIVING = "thriving"
