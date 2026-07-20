"""StudentExperience — presentation aggregate from Educational OS outputs.

Architecture Source
    EXP-001 Student Experience Engine
Concept
    Student Experience
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.mission_generation.ids import MissionSpecificationId
from domain.progress_evaluation.ids import ProgressReportId
from domain.recommendation.ids import RecommendationSpecificationId
from domain.student_experience.achievement import Achievement
from domain.student_experience.celebration import Celebration
from domain.student_experience.ids import StudentExperienceId
from domain.student_experience.learning_streak import LearningStreak
from domain.student_experience.motivation import Motivation
from domain.student_experience.reminder import Reminder
from domain.student_experience.session_summary import SessionSummary
from domain.study_planning.ids import StudyPlanId


@dataclass(frozen=True, slots=True)
class StudentExperience(EducationalValueObject):
    """Fully explainable learner experience projection.

    Converts Educational OS outputs into presentation constructs: streaks,
    achievements, celebrations, motivation, reminders, and session summary.
    Pure presentation — no educational decisions, persistence, AI, or
    recommendation mutation.
    """

    experience_id: StudentExperienceId
    student_id: str
    streak: LearningStreak
    achievements: tuple[Achievement, ...]
    celebrations: tuple[Celebration, ...]
    motivation: Motivation
    reminders: tuple[Reminder, ...]
    session_summary: SessionSummary
    presentation_narrative: str
    mission_id: MissionSpecificationId
    plan_id: StudyPlanId
    progress_report_id: ProgressReportId
    recommendation_specification_id: RecommendationSpecificationId

    def _validate(self) -> None:
        if not isinstance(self.experience_id, StudentExperienceId):
            raise EducationalInvariantViolation(
                "experience_id must be a StudentExperienceId",
                invariant="StudentExperience.experience_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_non_empty_text(self.student_id, "student_id"),
        )
        if not isinstance(self.streak, LearningStreak):
            raise EducationalInvariantViolation(
                "streak must be a LearningStreak",
                invariant="StudentExperience.streak.type",
            )
        if not isinstance(self.achievements, tuple):
            raise EducationalInvariantViolation(
                "achievements must be a tuple",
                invariant="StudentExperience.achievements.type",
            )
        seen_achievements: set[str] = set()
        for achievement in self.achievements:
            if not isinstance(achievement, Achievement):
                raise EducationalInvariantViolation(
                    "achievements must contain Achievement values",
                    invariant="StudentExperience.achievements.item_type",
                )
            if achievement.achievement_id.value in seen_achievements:
                raise EducationalInvariantViolation(
                    "achievement identities must be unique",
                    invariant="StudentExperience.achievements.unique",
                )
            seen_achievements.add(achievement.achievement_id.value)
        if not isinstance(self.celebrations, tuple):
            raise EducationalInvariantViolation(
                "celebrations must be a tuple",
                invariant="StudentExperience.celebrations.type",
            )
        seen_celebrations: set[str] = set()
        for celebration in self.celebrations:
            if not isinstance(celebration, Celebration):
                raise EducationalInvariantViolation(
                    "celebrations must contain Celebration values",
                    invariant="StudentExperience.celebrations.item_type",
                )
            if celebration.celebration_id.value in seen_celebrations:
                raise EducationalInvariantViolation(
                    "celebration identities must be unique",
                    invariant="StudentExperience.celebrations.unique",
                )
            seen_celebrations.add(celebration.celebration_id.value)
        if not isinstance(self.motivation, Motivation):
            raise EducationalInvariantViolation(
                "motivation must be a Motivation",
                invariant="StudentExperience.motivation.type",
            )
        if not isinstance(self.reminders, tuple):
            raise EducationalInvariantViolation(
                "reminders must be a tuple",
                invariant="StudentExperience.reminders.type",
            )
        seen_reminders: set[str] = set()
        for reminder in self.reminders:
            if not isinstance(reminder, Reminder):
                raise EducationalInvariantViolation(
                    "reminders must contain Reminder values",
                    invariant="StudentExperience.reminders.item_type",
                )
            if reminder.reminder_id.value in seen_reminders:
                raise EducationalInvariantViolation(
                    "reminder identities must be unique",
                    invariant="StudentExperience.reminders.unique",
                )
            seen_reminders.add(reminder.reminder_id.value)
        if not isinstance(self.session_summary, SessionSummary):
            raise EducationalInvariantViolation(
                "session_summary must be a SessionSummary",
                invariant="StudentExperience.session_summary.type",
            )
        object.__setattr__(
            self,
            "presentation_narrative",
            require_non_empty_text(
                self.presentation_narrative, "presentation_narrative"
            ),
        )
        if len(self.presentation_narrative) < 24:
            raise EducationalInvariantViolation(
                "presentation narrative must be substantive",
                invariant="StudentExperience.presentation_narrative.substantive",
            )
        for name, value, expected in (
            ("mission_id", self.mission_id, MissionSpecificationId),
            ("plan_id", self.plan_id, StudyPlanId),
            ("progress_report_id", self.progress_report_id, ProgressReportId),
            (
                "recommendation_specification_id",
                self.recommendation_specification_id,
                RecommendationSpecificationId,
            ),
        ):
            if not isinstance(value, expected):
                raise EducationalInvariantViolation(
                    f"{name} must be a {expected.__name__}",
                    invariant=f"StudentExperience.{name}.type",
                )

    def achievement_count(self) -> int:
        return len(self.achievements)

    def reminder_count(self) -> int:
        return len(self.reminders)

    def celebration_count(self) -> int:
        return len(self.celebrations)

    def has_achievement_kind(self, kind: object) -> bool:
        return any(item.kind is kind for item in self.achievements)

    def has_reminder_kind(self, kind: object) -> bool:
        return any(item.kind is kind for item in self.reminders)
