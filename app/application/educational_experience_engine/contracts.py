"""Runtime integration contracts for Educational Experience Engine (EX-001).

UI components and presentation adapters consume Experience Models through
these interfaces. Controllers and templates must not duplicate educational
logic — they call these contracts only.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from app.domain.educational_experience_engine.experience import ExperienceModel
from app.domain.educational_experience_engine.surfaces import (
    CoachConversationContext,
    DailyMissionExperience,
    DashboardPriorityCard,
    RevisionPlannerEntry,
    StudySessionBriefing,
)
from app.domain.educational_reasoning_engine.decision import EducationalDecision


@runtime_checkable
class ExperienceModelConsumer(Protocol):
    """Any student surface that renders a canonical ExperienceModel."""

    def render_experience(self, experience: ExperienceModel) -> object:
        """Bind an ExperienceModel into a UI-specific view structure."""


@runtime_checkable
class DailyMissionExperiencePort(Protocol):
    """Contract for Daily Mission presentation consumers."""

    def present_daily_mission(
        self, decision: EducationalDecision
    ) -> DailyMissionExperience:
        """Transform one Educational Decision into a Daily Mission model."""


@runtime_checkable
class CoachExperiencePort(Protocol):
    """Contract for AI Coach conversation grounding."""

    def present_coach_context(
        self, decision: EducationalDecision
    ) -> CoachConversationContext:
        """Transform one Educational Decision into Coach conversation context."""


@runtime_checkable
class DashboardExperiencePort(Protocol):
    """Contract for Dashboard priority card consumers."""

    def present_dashboard_card(
        self, decision: EducationalDecision
    ) -> DashboardPriorityCard:
        """Transform one Educational Decision into a Dashboard priority card."""


@runtime_checkable
class RevisionPlannerExperiencePort(Protocol):
    """Contract for Revision Planner entry consumers."""

    def present_revision_entry(
        self, decision: EducationalDecision
    ) -> RevisionPlannerEntry:
        """Transform one Educational Decision into a Revision Planner entry."""


@runtime_checkable
class StudySessionExperiencePort(Protocol):
    """Contract for study session briefing consumers."""

    def present_session_briefing(
        self, decision: EducationalDecision
    ) -> StudySessionBriefing:
        """Transform one Educational Decision into a study session briefing."""


@runtime_checkable
class ExperienceEnginePort(Protocol):
    """Full Experience Engine contract for orchestrators and adapters."""

    def present(self, decision: EducationalDecision) -> ExperienceModel:
        """Build the canonical ExperienceModel from an Educational Decision."""

    def present_daily_mission(
        self, decision: EducationalDecision
    ) -> DailyMissionExperience: ...

    def present_coach_context(
        self, decision: EducationalDecision
    ) -> CoachConversationContext: ...

    def present_dashboard_card(
        self, decision: EducationalDecision
    ) -> DashboardPriorityCard: ...

    def present_revision_entry(
        self, decision: EducationalDecision
    ) -> RevisionPlannerEntry: ...

    def present_session_briefing(
        self, decision: EducationalDecision
    ) -> StudySessionBriefing: ...
