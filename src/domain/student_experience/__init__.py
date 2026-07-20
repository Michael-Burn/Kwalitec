"""Student Experience Engine — presentation from Educational OS outputs.

EXP-001: Convert MissionSpecification, StudyPlan, ProgressReport, and
RecommendationSpecification into a StudentExperience for learner engagement.

Responsibilities: learning streaks, achievements, session summaries, progress
celebrations, motivational messaging, review reminders, milestone recognition.

Pure presentation domain only. No educational decisions, no AI, no prompting,
no randomness, no persistence, Flask, ORM, HTTP, or DTOs. Recommendations are
referenced, never modified.
"""

from __future__ import annotations

from domain.student_experience.achievement import Achievement
from domain.student_experience.celebration import Celebration
from domain.student_experience.enums import (
    AchievementKind,
    CelebrationKind,
    MilestoneKind,
    MotivationTone,
    ReminderKind,
    StreakBand,
)
from domain.student_experience.experience_generator import (
    ExperienceGenerator,
    consecutive_run_ending_at,
    longest_consecutive_run,
    streak_band_for,
)
from domain.student_experience.ids import (
    AchievementId,
    CelebrationId,
    MotivationId,
    ReminderId,
    SessionSummaryId,
    StudentExperienceId,
)
from domain.student_experience.learning_streak import LearningStreak
from domain.student_experience.motivation import Motivation
from domain.student_experience.reminder import Reminder
from domain.student_experience.session_summary import SessionSummary
from domain.student_experience.student_experience import StudentExperience

__all__ = [
    # Aggregate
    "StudentExperience",
    "SessionSummary",
    "LearningStreak",
    "Achievement",
    "Celebration",
    "Motivation",
    "Reminder",
    # Identities
    "StudentExperienceId",
    "AchievementId",
    "CelebrationId",
    "MotivationId",
    "ReminderId",
    "SessionSummaryId",
    # Enums
    "AchievementKind",
    "CelebrationKind",
    "MotivationTone",
    "ReminderKind",
    "StreakBand",
    "MilestoneKind",
    # Generator
    "ExperienceGenerator",
    "streak_band_for",
    "consecutive_run_ending_at",
    "longest_consecutive_run",
]
