"""CoachContext — structured coaching context explaining Education OS decisions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.student_experience.coach.errors import CoachInvariantViolation
from application.student_experience.coach.ids import CoachId
from application.student_experience.coach.models.celebration_moments import (
    CelebrationMoments,
)
from application.student_experience.coach.models.explanation_cards import (
    ExplanationCards,
)


@dataclass(frozen=True, slots=True)
class FocusContext:
    """Current focus section — projected from home / workspace / mission."""

    headline: str
    reason: str
    mission_title: str | None = None
    action_label: str | None = None
    has_focus: bool = False

    def __post_init__(self) -> None:
        for name in ("headline", "reason"):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise CoachInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"FocusContext.{name}.required",
                )
            object.__setattr__(self, name, value)
        object.__setattr__(
            self, "mission_title", (self.mission_title or "").strip() or None
        )
        object.__setattr__(
            self, "action_label", (self.action_label or "").strip() or None
        )


@dataclass(frozen=True, slots=True)
class JourneyContext:
    """Learning journey section — projected from JourneySnapshot."""

    available: bool
    trajectory_message: str
    consistency_message: str
    habits_message: str
    weekly_missions_completed: int = 0
    current_streak_days: int = 0

    def __post_init__(self) -> None:
        for name in (
            "trajectory_message",
            "consistency_message",
            "habits_message",
        ):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise CoachInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"JourneyContext.{name}.required",
                )
            object.__setattr__(self, name, value)
        for name in ("weekly_missions_completed", "current_streak_days"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise CoachInvariantViolation(
                    f"{name} must be an integer >= 0",
                    invariant=f"JourneyContext.{name}.range",
                )


@dataclass(frozen=True, slots=True)
class ReadinessContext:
    """Readiness section — projected from ReadinessSnapshot."""

    available: bool
    readiness_label: str
    direction_message: str
    assessment_confidence_label: str
    risk_count: int = 0
    strength_count: int = 0
    days_remaining: int | None = None
    readiness_percent: float | None = None

    def __post_init__(self) -> None:
        for name in (
            "readiness_label",
            "direction_message",
            "assessment_confidence_label",
        ):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise CoachInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"ReadinessContext.{name}.required",
                )
            object.__setattr__(self, name, value)
        for name in ("risk_count", "strength_count"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise CoachInvariantViolation(
                    f"{name} must be an integer >= 0",
                    invariant=f"ReadinessContext.{name}.range",
                )


@dataclass(frozen=True, slots=True)
class MissionContext:
    """Current mission section — projected from workspace / execution / plan."""

    available: bool
    purpose: str
    progress_summary: str
    mission_title: str | None = None
    completion_percent: float | None = None
    objective_label: str | None = None

    def __post_init__(self) -> None:
        for name in ("purpose", "progress_summary"):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise CoachInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"MissionContext.{name}.required",
                )
            object.__setattr__(self, name, value)
        object.__setattr__(
            self, "mission_title", (self.mission_title or "").strip() or None
        )
        object.__setattr__(
            self, "objective_label", (self.objective_label or "").strip() or None
        )


@dataclass(frozen=True, slots=True)
class ImprovementItem:
    """One recent-improvement bullet projected from existing signals."""

    title: str
    message: str

    def __post_init__(self) -> None:
        for name in ("title", "message"):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise CoachInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"ImprovementItem.{name}.required",
                )
            object.__setattr__(self, name, value)


@dataclass(frozen=True, slots=True)
class RiskItem:
    """One current-risk bullet projected from readiness / evaluation."""

    title: str
    message: str

    def __post_init__(self) -> None:
        for name in ("title", "message"):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise CoachInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"RiskItem.{name}.required",
                )
            object.__setattr__(self, name, value)


@dataclass(frozen=True, slots=True)
class MilestoneItem:
    """One upcoming milestone projected from schedule / readiness / home."""

    title: str
    detail: str
    days_until: int | None = None

    def __post_init__(self) -> None:
        for name in ("title", "detail"):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise CoachInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"MilestoneItem.{name}.required",
                )
            object.__setattr__(self, name, value)


@dataclass(frozen=True, slots=True)
class CoachContext:
    """Immutable structured coaching context.

    Explains Education OS decisions. Never replaces them. Never invents
    mastery, recommendations, or missions. Never calls an LLM.
    """

    coach_id: CoachId
    student_id: str
    composed_at: datetime
    current_focus: FocusContext
    learning_journey: JourneyContext
    readiness: ReadinessContext
    current_mission: MissionContext
    recent_improvements: tuple[ImprovementItem, ...]
    current_risks: tuple[RiskItem, ...]
    upcoming_milestones: tuple[MilestoneItem, ...]
    explanation_cards: ExplanationCards
    celebration_moments: CelebrationMoments

    def __post_init__(self) -> None:
        if not isinstance(self.coach_id, CoachId):
            raise CoachInvariantViolation(
                "coach_id must be a CoachId",
                invariant="CoachContext.coach_id.type",
            )
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise CoachInvariantViolation(
                "student_id must be a non-empty string",
                invariant="CoachContext.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        if not isinstance(self.composed_at, datetime):
            raise CoachInvariantViolation(
                "composed_at must be a datetime",
                invariant="CoachContext.composed_at.type",
            )
        expected = {
            "current_focus": FocusContext,
            "learning_journey": JourneyContext,
            "readiness": ReadinessContext,
            "current_mission": MissionContext,
            "explanation_cards": ExplanationCards,
            "celebration_moments": CelebrationMoments,
        }
        for name, expected_type in expected.items():
            value = getattr(self, name)
            if not isinstance(value, expected_type):
                raise CoachInvariantViolation(
                    f"{name} must be a {expected_type.__name__}",
                    invariant=f"CoachContext.{name}.type",
                )
        improvements = tuple(self.recent_improvements or ())
        for item in improvements:
            if not isinstance(item, ImprovementItem):
                raise CoachInvariantViolation(
                    "recent_improvements must contain ImprovementItem instances",
                    invariant="CoachContext.recent_improvements.type",
                )
        object.__setattr__(self, "recent_improvements", improvements)
        risks = tuple(self.current_risks or ())
        for item in risks:
            if not isinstance(item, RiskItem):
                raise CoachInvariantViolation(
                    "current_risks must contain RiskItem instances",
                    invariant="CoachContext.current_risks.type",
                )
        object.__setattr__(self, "current_risks", risks)
        milestones = tuple(self.upcoming_milestones or ())
        for item in milestones:
            if not isinstance(item, MilestoneItem):
                raise CoachInvariantViolation(
                    "upcoming_milestones must contain MilestoneItem instances",
                    invariant="CoachContext.upcoming_milestones.type",
                )
        object.__setattr__(self, "upcoming_milestones", milestones)
