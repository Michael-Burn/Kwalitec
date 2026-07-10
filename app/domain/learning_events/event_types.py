"""Recognised Learning Event types.

Extensible catalogue of discrete occurrences that may become Learning Evidence.
Adding a member here does not require architectural changes elsewhere in the
domain package — consumers should treat unknown future members as first-class
types once declared.
"""

from __future__ import annotations

from enum import Enum


class LearningEventType(str, Enum):
    """Canonical Learning Event type vocabulary for Epic 1.

    Values are stable snake_case identifiers suitable for later persistence and
    explainability trails without coupling this package to infrastructure.
    """

    STUDY_SESSION_STARTED = "study_session_started"
    STUDY_SESSION_COMPLETED = "study_session_completed"
    TOPIC_STARTED = "topic_started"
    TOPIC_COMPLETED = "topic_completed"
    QUESTION_ATTEMPTED = "question_attempted"
    QUESTION_CORRECT = "question_correct"
    QUESTION_INCORRECT = "question_incorrect"
    QUIZ_COMPLETED = "quiz_completed"
    MOCK_COMPLETED = "mock_completed"
    REVISION_COMPLETED = "revision_completed"
    MISSION_COMPLETED = "mission_completed"
    MISSION_MISSED = "mission_missed"
    CONFIDENCE_UPDATED = "confidence_updated"
    STUDY_SESSION_SKIPPED = "study_session_skipped"
