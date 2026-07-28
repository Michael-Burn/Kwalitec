"""DTOs for Educational Experience Engine services (EX-001)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.domain.educational_experience_engine.experience import ExperienceModel
from app.domain.educational_experience_engine.surfaces import (
    CoachConversationContext,
    DailyMissionExperience,
    DashboardPriorityCard,
    RevisionPlannerEntry,
    StudySessionBriefing,
)
from app.domain.educational_reasoning_engine.decision import EducationalDecision


@dataclass(frozen=True)
class SurfaceBundle:
    """All surface projections derived from one Educational Decision."""

    experience: ExperienceModel
    daily_mission: DailyMissionExperience
    coach: CoachConversationContext
    dashboard_card: DashboardPriorityCard
    revision_entry: RevisionPlannerEntry
    session_briefing: StudySessionBriefing

    def to_dict(self) -> dict[str, Any]:
        return {
            "experience": self.experience.to_dict(),
            "daily_mission": self.daily_mission.to_dict(),
            "coach": self.coach.to_dict(),
            "dashboard_card": self.dashboard_card.to_dict(),
            "revision_entry": self.revision_entry.to_dict(),
            "session_briefing": self.session_briefing.to_dict(),
        }


@dataclass(frozen=True)
class ExperiencePortfolio:
    """Ordered experience projections for an SCI decision set."""

    instance_id: str
    experience_version: str
    reasoning_version: str
    surfaces: tuple[SurfaceBundle, ...] = field(default_factory=tuple)

    @property
    def count(self) -> int:
        return len(self.surfaces)

    def to_dict(self) -> dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "experience_version": self.experience_version,
            "reasoning_version": self.reasoning_version,
            "count": self.count,
            "surfaces": [s.to_dict() for s in self.surfaces],
        }


@dataclass(frozen=True)
class DecisionExperienceRequest:
    """Explicit request envelope for experience transformation."""

    decision: EducationalDecision
    curriculum_area: str | None = None

    def __post_init__(self) -> None:
        if self.decision is None:
            raise ValueError("decision is required")
