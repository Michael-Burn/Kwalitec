"""Immutable per-step declaration payloads.

Each payload records what the student declared. None of these types encode
mastery, readiness, recommendations, or mission plans.
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.onboarding.enums import (
    ConfidenceBand,
    CoreReadingDeclaration,
    DiagnosticChoice,
    ExamSittingIntent,
    IfoaPathway,
    PriorStudyPosture,
    StudyHabitPreference,
)
from domain.onboarding.errors import OnboardingValidationError


@dataclass(frozen=True, slots=True)
class WelcomePayload:
    """Welcome acknowledgement — invitation only."""

    acknowledged: bool

    def validate(self) -> None:
        if not self.acknowledged:
            raise OnboardingValidationError(
                "welcome must be acknowledged to continue",
                step="welcome",
                field="acknowledged",
            )


@dataclass(frozen=True, slots=True)
class IfoaProfilePayload:
    """IFoA pathway and paper scope declaration."""

    pathway: IfoaPathway
    exam_paper: str
    intended_sitting_label: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "exam_paper", (self.exam_paper or "").strip())
        object.__setattr__(
            self,
            "intended_sitting_label",
            (self.intended_sitting_label or "").strip(),
        )

    def validate(self) -> None:
        if not self.exam_paper:
            raise OnboardingValidationError(
                "exam paper is required",
                step="ifoa_profile",
                field="exam_paper",
            )


@dataclass(frozen=True, slots=True)
class ExamHistoryPayload:
    """Prior study and attempt history declaration."""

    prior_study: PriorStudyPosture
    core_reading: CoreReadingDeclaration
    previous_attempts: int
    sitting_intent: ExamSittingIntent

    def validate(self) -> None:
        if self.previous_attempts < 0:
            raise OnboardingValidationError(
                "previous attempts cannot be negative",
                step="exam_history",
                field="previous_attempts",
            )
        if self.previous_attempts > 20:
            raise OnboardingValidationError(
                "previous attempts must be at most 20",
                step="exam_history",
                field="previous_attempts",
            )
        if (
            self.prior_study is PriorStudyPosture.FIRST_TIME
            and self.previous_attempts > 0
        ):
            raise OnboardingValidationError(
                "first-time posture cannot declare previous attempts",
                step="exam_history",
                field="previous_attempts",
            )


@dataclass(frozen=True, slots=True)
class WeeklyAvailabilityPayload:
    """Declared weekly study capacity — not a generated study plan."""

    weekday_minutes: int
    weekend_minutes: int
    preferred_session_minutes: int

    def validate(self) -> None:
        for field, value in (
            ("weekday_minutes", self.weekday_minutes),
            ("weekend_minutes", self.weekend_minutes),
            ("preferred_session_minutes", self.preferred_session_minutes),
        ):
            if value < 0:
                raise OnboardingValidationError(
                    f"{field} cannot be negative",
                    step="weekly_availability",
                    field=field,
                )
        if not 15 <= self.preferred_session_minutes <= 240:
            raise OnboardingValidationError(
                "preferred session minutes must be between 15 and 240",
                step="weekly_availability",
                field="preferred_session_minutes",
            )
        if self.weekday_minutes + self.weekend_minutes <= 0:
            raise OnboardingValidationError(
                "at least some weekly availability is required",
                step="weekly_availability",
                field="weekday_minutes",
            )


@dataclass(frozen=True, slots=True)
class ConfidencePayload:
    """Self-reported confidence — declaration only."""

    band: ConfidenceBand
    notes: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "notes", (self.notes or "").strip())

    def validate(self) -> None:
        if len(self.notes) > 500:
            raise OnboardingValidationError(
                "confidence notes must be at most 500 characters",
                step="confidence",
                field="notes",
            )


@dataclass(frozen=True, slots=True)
class StudyHabitsPayload:
    """Study habit preference — not mission planning."""

    preference: StudyHabitPreference
    typical_start_time: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "typical_start_time",
            (self.typical_start_time or "").strip(),
        )

    def validate(self) -> None:
        if self.typical_start_time and len(self.typical_start_time) > 32:
            raise OnboardingValidationError(
                "typical start time is too long",
                step="study_habits",
                field="typical_start_time",
            )


@dataclass(frozen=True, slots=True)
class OptionalDiagnosticPayload:
    """Optional diagnostic invitation — never runs diagnostic logic here."""

    choice: DiagnosticChoice

    def validate(self) -> None:
        # Any closed choice is structurally valid; skip is allowed.
        return None


@dataclass(frozen=True, slots=True)
class ReviewPayload:
    """Explicit confirmation that declarations may be submitted."""

    confirmed: bool

    def validate(self) -> None:
        if not self.confirmed:
            raise OnboardingValidationError(
                "review confirmation is required to complete onboarding",
                step="review",
                field="confirmed",
            )


StepPayload = (
    WelcomePayload
    | IfoaProfilePayload
    | ExamHistoryPayload
    | WeeklyAvailabilityPayload
    | ConfidencePayload
    | StudyHabitsPayload
    | OptionalDiagnosticPayload
    | ReviewPayload
)
