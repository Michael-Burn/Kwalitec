"""SessionSummary — presentation summary of recent learning activity.

Architecture Source
    EXP-001 Student Experience Engine
Concept
    Session Summary
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.mission_generation.ids import MissionSpecificationId
from domain.recommendation.enums import RecommendationCategory
from domain.student_experience.ids import SessionSummaryId


@dataclass(frozen=True, slots=True)
class SessionSummary(EducationalValueObject):
    """Immutable presentation summary of mission work and progress signals.

    Echoes educational facts for learner-facing closure. Never claims mastery
    from session completion and never rewrites recommendations.
    """

    summary_id: SessionSummaryId
    mission_id: MissionSpecificationId
    objective_statement: str
    planned_minutes: int
    completed_mission_count: int
    mastery_trend_label: str
    confidence_trend_label: str
    next_focus_category: RecommendationCategory
    next_focus_preview: str
    honesty_note: str

    def _validate(self) -> None:
        if not isinstance(self.summary_id, SessionSummaryId):
            raise EducationalInvariantViolation(
                "summary_id must be a SessionSummaryId",
                invariant="SessionSummary.summary_id.type",
            )
        if not isinstance(self.mission_id, MissionSpecificationId):
            raise EducationalInvariantViolation(
                "mission_id must be a MissionSpecificationId",
                invariant="SessionSummary.mission_id.type",
            )
        object.__setattr__(
            self,
            "objective_statement",
            require_non_empty_text(self.objective_statement, "objective_statement"),
        )
        if not isinstance(self.planned_minutes, int) or isinstance(
            self.planned_minutes, bool
        ):
            raise EducationalInvariantViolation(
                "planned_minutes must be an integer",
                invariant="SessionSummary.planned_minutes.type",
            )
        if self.planned_minutes <= 0:
            raise EducationalInvariantViolation(
                "planned_minutes must be positive",
                invariant="SessionSummary.planned_minutes.positive",
            )
        if not isinstance(self.completed_mission_count, int) or isinstance(
            self.completed_mission_count, bool
        ):
            raise EducationalInvariantViolation(
                "completed_mission_count must be an integer",
                invariant="SessionSummary.completed_mission_count.type",
            )
        if self.completed_mission_count < 0:
            raise EducationalInvariantViolation(
                "completed_mission_count must be non-negative",
                invariant="SessionSummary.completed_mission_count.non_negative",
            )
        for name, value in (
            ("mastery_trend_label", self.mastery_trend_label),
            ("confidence_trend_label", self.confidence_trend_label),
            ("next_focus_preview", self.next_focus_preview),
            ("honesty_note", self.honesty_note),
        ):
            object.__setattr__(
                self,
                name,
                require_non_empty_text(value, name),
            )
        if not isinstance(self.next_focus_category, RecommendationCategory):
            raise EducationalInvariantViolation(
                "next_focus_category must be a RecommendationCategory",
                invariant="SessionSummary.next_focus_category.type",
            )
        lowered = self.honesty_note.casefold()
        if "not mastery" not in lowered and "not a mastery" not in lowered:
            raise EducationalInvariantViolation(
                "honesty_note must state that finishing is not mastery",
                invariant="SessionSummary.honesty_note.no_mastery_claim",
            )
