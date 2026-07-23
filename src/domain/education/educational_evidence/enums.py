"""Educational Evidence domain enumerations.

Architecture Source
    STUDENT_DIGITAL_TWIN.md (Learning Evidence Model)
Concept
    Evidence Type / Evidence Source Kind / Learning Environment Kind /
    Evidence Weight Band
"""

from __future__ import annotations

from enum import StrEnum


class EvidenceType(StrEnum):
    """Educational meaning captured by a single piece of evidence.

    Evidence types classify *what happened educationally*. They are never a
    diagnosis, a mastery estimate, or a recommendation — this bounded
    context only transforms student interactions into evidence.
    """

    QUESTION_ANSWERED = "question_answered"
    QUESTION_INCORRECT = "question_incorrect"
    REFLECTION_RECORDED = "reflection_recorded"
    MISSION_COMPLETED = "mission_completed"
    MISSION_ABANDONED = "mission_abandoned"
    STUDY_SESSION_STARTED = "study_session_started"
    STUDY_SESSION_COMPLETED = "study_session_completed"
    HINT_REQUESTED = "hint_requested"
    REVIEW_COMPLETED = "review_completed"
    CHECKPOINT_REACHED = "checkpoint_reached"
    CONFIDENCE_REPORTED = "confidence_reported"
    GOAL_ACHIEVED = "goal_achieved"
    TIME_INVESTED = "time_invested"
    SUBJECT_VISITED = "subject_visited"
    COMPETENCY_PRACTISED = "competency_practised"


class EvidenceSourceKind(StrEnum):
    """Provenance class of an educational evidence observation."""

    STUDENT_ACTION = "student_action"
    SYSTEM_OBSERVATION = "system_observation"
    SELF_REPORT = "self_report"


class LearningEnvironmentKind(StrEnum):
    """Setting in which the underlying student interaction took place."""

    MISSION = "mission"
    STUDY_SESSION = "study_session"
    REVIEW = "review"
    DIAGNOSTIC = "diagnostic"
    FREE_PRACTICE = "free_practice"
    REFLECTION_PROMPT = "reflection_prompt"
    CHECKPOINT_GATE = "checkpoint_gate"
    GOAL_TRACKING = "goal_tracking"


class EvidenceWeightBand(StrEnum):
    """Qualitative band derived deterministically from an evidence weight.

    The band is always computed from the numeric magnitude — never supplied
    independently — so weight and band can never disagree.
    """

    NEGLIGIBLE = "negligible"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    DECISIVE = "decisive"
