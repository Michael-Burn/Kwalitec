"""Onboarding domain enumerations.

Collect structured educational evidence only. Values are declarations —
never mastery scores, readiness bands, or recommendations.
"""

from __future__ import annotations

from enum import StrEnum


class OnboardingStatus(StrEnum):
    """Lifecycle status of an onboarding session."""

    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class OnboardingStep(StrEnum):
    """Ordered first-run collection steps.

    ``BUILD_STUDENT_TWIN`` and ``DASHBOARD_REDIRECT`` are terminal system
    stages after the student confirms Review — not questionnaire forms.
    """

    WELCOME = "welcome"
    IFOA_PROFILE = "ifoa_profile"
    EXAM_HISTORY = "exam_history"
    WEEKLY_AVAILABILITY = "weekly_availability"
    CONFIDENCE = "confidence"
    STUDY_HABITS = "study_habits"
    OPTIONAL_DIAGNOSTIC = "optional_diagnostic"
    REVIEW = "review"
    BUILD_STUDENT_TWIN = "build_student_twin"
    DASHBOARD_REDIRECT = "dashboard_redirect"


class IfoaPathway(StrEnum):
    """Coarse IFoA pathway declaration."""

    CORE_PRINCIPLES = "core_principles"
    CORE_PRACTICES = "core_practices"
    SPECIALIST = "specialist"
    OTHER = "other"
    UNSURE = "unsure"


class ExamSittingIntent(StrEnum):
    """Declared sitting intention (history / objective, not prediction)."""

    FIRST_SIT = "first_sit"
    RESIT = "resit"
    REVISION = "revision"
    FINISH_REMAINING = "finish_remaining"


class PriorStudyPosture(StrEnum):
    """Whether the student has previously engaged with the paper."""

    FIRST_TIME = "first_time"
    PREVIOUSLY_STUDIED = "previously_studied"


class CoreReadingDeclaration(StrEnum):
    """Declared Core Reading coverage — not measured mastery."""

    NONE = "none"
    PARTIAL = "partial"
    WHOLE_PAPER = "whole_paper"


class ConfidenceBand(StrEnum):
    """Self-reported confidence band — declaration only, not readiness."""

    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    UNSURE = "unsure"


class StudyHabitPreference(StrEnum):
    """Preferred study approach — preference, not a mission plan."""

    READING_FIRST = "reading_first"
    QUESTIONS_FIRST = "questions_first"
    MIXED = "mixed"
    UNSURE = "unsure"


class DiagnosticChoice(StrEnum):
    """Optional diagnostic invitation response."""

    SKIPPED = "skipped"
    ACCEPTED = "accepted"
    DECLINED = "declined"


# Collection steps the student fills; excludes terminal system stages.
COLLECTION_STEPS: tuple[OnboardingStep, ...] = (
    OnboardingStep.WELCOME,
    OnboardingStep.IFOA_PROFILE,
    OnboardingStep.EXAM_HISTORY,
    OnboardingStep.WEEKLY_AVAILABILITY,
    OnboardingStep.CONFIDENCE,
    OnboardingStep.STUDY_HABITS,
    OnboardingStep.OPTIONAL_DIAGNOSTIC,
    OnboardingStep.REVIEW,
)

STEP_LABELS: dict[OnboardingStep, str] = {
    OnboardingStep.WELCOME: "Welcome",
    OnboardingStep.IFOA_PROFILE: "IFoA Profile",
    OnboardingStep.EXAM_HISTORY: "Exam History",
    OnboardingStep.WEEKLY_AVAILABILITY: "Weekly Availability",
    OnboardingStep.CONFIDENCE: "Confidence",
    OnboardingStep.STUDY_HABITS: "Study Habits",
    OnboardingStep.OPTIONAL_DIAGNOSTIC: "Optional Diagnostic",
    OnboardingStep.REVIEW: "Review",
    OnboardingStep.BUILD_STUDENT_TWIN: "Build Student Twin",
    OnboardingStep.DASHBOARD_REDIRECT: "Dashboard",
}
