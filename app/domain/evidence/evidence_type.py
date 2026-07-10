"""Learning Evidence type vocabulary from the Learning Evidence Model.

Evidence types are the type-level catalogue kinds. They are distinct from
``EvidenceCategory``, which organises high-level groups. Types do not assign
numerical weights or scores.
"""

from __future__ import annotations

from enum import Enum


class EvidenceType(str, Enum):
    """Canonical Learning Evidence type vocabulary.

    Values are stable snake_case identifiers aligned with the Learning Evidence
    Model catalogue. Adding a member here does not require architectural changes
    elsewhere in the domain package — specialised transformers may map
    validated candidates onto these types without editing the coordinator.
    """

    STUDY_SESSION = "study_session"
    TOPIC_STARTED = "topic_started"
    TOPIC_COMPLETED = "topic_completed"
    QUESTION_ATTEMPT = "question_attempt"
    QUESTION_CORRECT = "question_correct"
    QUESTION_INCORRECT = "question_incorrect"
    QUESTION_DIFFICULTY = "question_difficulty"
    QUIZ_COMPLETED = "quiz_completed"
    MOCK_EXAM = "mock_exam"
    PAST_PAPER_ATTEMPT = "past_paper_attempt"
    MISSION_COMPLETED = "mission_completed"
    MISSION_MISSED = "mission_missed"
    REVISION_SESSION = "revision_session"
    FLASHCARD_REVIEW = "flashcard_review"
    CONFIDENCE_RATING = "confidence_rating"
    HINT_REQUESTED = "hint_requested"
    TIME_ON_TASK = "time_on_task"
    SESSION_ABANDONED = "session_abandoned"
    STUDY_BREAK = "study_break"
    DAILY_CHECK_IN = "daily_check_in"
    PLAN_RESCHEDULED = "plan_rescheduled"
    SKIPPED_SESSION = "skipped_session"
    MANUAL_GOAL_CHANGE = "manual_goal_change"
    EXAM_DATE_CHANGE = "exam_date_change"
    READINESS_REVIEW = "readiness_review"
    AI_TUTOR_INTERACTION = "ai_tutor_interaction"
    REFLECTION_JOURNAL = "reflection_journal"
    RECOMMENDATION_DECISION = "recommendation_decision"
    DIAGNOSTIC_ASSESSMENT = "diagnostic_assessment"
    NOTIFICATION_ENGAGEMENT = "notification_engagement"
    POST_EXAM_OUTCOME = "post_exam_outcome"
