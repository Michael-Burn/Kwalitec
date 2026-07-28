"""Educational Experience transformation services (EX-001).

Converts Educational Decisions into structured presentation models for
student-facing surfaces. Does not reason educationally, mutate decisions,
or bypass the Educational Reasoning Engine.
"""

from __future__ import annotations

from datetime import datetime

from app.application.educational_experience_engine.dto import (
    DecisionExperienceRequest,
    ExperiencePortfolio,
    SurfaceBundle,
)
from app.application.educational_experience_engine.exceptions import (
    DecisionRequiredError,
)
from app.application.educational_reasoning_engine.dto import DecisionView
from app.application.educational_reasoning_engine.query_service import (
    DecisionQueryService,
)
from app.domain.educational_experience_engine.engine import EducationalExperienceEngine
from app.domain.educational_experience_engine.experience import ExperienceModel
from app.domain.educational_experience_engine.surfaces import (
    CoachConversationContext,
    DailyMissionExperience,
    DashboardPriorityCard,
    RevisionPlannerEntry,
    StudySessionBriefing,
)
from app.domain.educational_experience_engine.version import EXPERIENCE_VERSION
from app.domain.educational_reasoning_engine.decision import EducationalDecision
from app.domain.educational_reasoning_engine.version import REASONING_VERSION


class ExperienceTransformationService:
    """Transform Educational Decisions into surface experience models.

    Implements the ExperienceEnginePort contract. Controllers/templates must
    consume these outputs rather than re-deriving educational logic.
    """

    def __init__(
        self,
        engine: EducationalExperienceEngine | None = None,
        decision_query: DecisionQueryService | None = None,
    ) -> None:
        self._engine = engine or EducationalExperienceEngine()
        self._decision_query = decision_query or DecisionQueryService()

    def present(
        self,
        decision: EducationalDecision,
        *,
        presented_at: datetime | None = None,
        curriculum_area: str | None = None,
    ) -> ExperienceModel:
        """Build the canonical ExperienceModel from one Educational Decision."""
        self._require_decision(decision)
        return self._engine.present(
            decision,
            presented_at=presented_at,
            curriculum_area=curriculum_area,
        )

    def present_request(
        self,
        request: DecisionExperienceRequest,
        *,
        presented_at: datetime | None = None,
    ) -> ExperienceModel:
        return self.present(
            request.decision,
            presented_at=presented_at,
            curriculum_area=request.curriculum_area,
        )

    def present_daily_mission(
        self,
        decision: EducationalDecision,
        *,
        presented_at: datetime | None = None,
        curriculum_area: str | None = None,
    ) -> DailyMissionExperience:
        self._require_decision(decision)
        return self._engine.to_daily_mission(
            decision,
            presented_at=presented_at,
            curriculum_area=curriculum_area,
        )

    def present_coach_context(
        self,
        decision: EducationalDecision,
        *,
        presented_at: datetime | None = None,
        curriculum_area: str | None = None,
    ) -> CoachConversationContext:
        self._require_decision(decision)
        return self._engine.to_coach_context(
            decision,
            presented_at=presented_at,
            curriculum_area=curriculum_area,
        )

    def present_dashboard_card(
        self,
        decision: EducationalDecision,
        *,
        presented_at: datetime | None = None,
        curriculum_area: str | None = None,
    ) -> DashboardPriorityCard:
        self._require_decision(decision)
        return self._engine.to_dashboard_card(
            decision,
            presented_at=presented_at,
            curriculum_area=curriculum_area,
        )

    def present_revision_entry(
        self,
        decision: EducationalDecision,
        *,
        presented_at: datetime | None = None,
        curriculum_area: str | None = None,
    ) -> RevisionPlannerEntry:
        self._require_decision(decision)
        return self._engine.to_revision_entry(
            decision,
            presented_at=presented_at,
            curriculum_area=curriculum_area,
        )

    def present_session_briefing(
        self,
        decision: EducationalDecision,
        *,
        presented_at: datetime | None = None,
        curriculum_area: str | None = None,
    ) -> StudySessionBriefing:
        self._require_decision(decision)
        return self._engine.to_session_briefing(
            decision,
            presented_at=presented_at,
            curriculum_area=curriculum_area,
        )

    def present_all_surfaces(
        self,
        decision: EducationalDecision,
        *,
        presented_at: datetime | None = None,
        curriculum_area: str | None = None,
    ) -> SurfaceBundle:
        """Project one decision into every student-facing surface model."""
        experience = self.present(
            decision,
            presented_at=presented_at,
            curriculum_area=curriculum_area,
        )
        return SurfaceBundle(
            experience=experience,
            daily_mission=DailyMissionExperience.from_experience(experience),
            coach=CoachConversationContext.from_experience(experience),
            dashboard_card=DashboardPriorityCard.from_experience(experience),
            revision_entry=RevisionPlannerEntry.from_experience(experience),
            session_briefing=StudySessionBriefing.from_experience(experience),
        )

    def present_decision_view(
        self,
        view: DecisionView,
        *,
        presented_at: datetime | None = None,
        curriculum_area: str | None = None,
    ) -> SurfaceBundle:
        """Accept EI-007 DecisionView without using explanation for ranking."""
        return self.present_all_surfaces(
            view.decision,
            presented_at=presented_at,
            curriculum_area=curriculum_area,
        )

    def portfolio_for_instance(
        self,
        instance_id: str,
        *,
        limit: int | None = None,
        presented_at: datetime | None = None,
    ) -> ExperiencePortfolio:
        """Build ordered surface bundles from persisted Educational Decisions.

        Reads decisions via DecisionQueryService — never re-reasons.
        """
        decisions = self._decision_query.list_decisions(instance_id)
        if limit is not None:
            if limit < 1:
                decisions = ()
            else:
                decisions = decisions[:limit]

        bundles = tuple(
            self.present_decision_view(view, presented_at=presented_at)
            for view in decisions
        )
        reasoning_version = (
            decisions[0].decision.reasoning_version
            if decisions
            else REASONING_VERSION
        )
        return ExperiencePortfolio(
            instance_id=instance_id,
            experience_version=EXPERIENCE_VERSION,
            reasoning_version=reasoning_version,
            surfaces=bundles,
        )

    def explainable_presentation(self, decision: EducationalDecision) -> dict:
        """Compact explainable presentation preserving educational traceability.

        Students (via UI adapters) can see what/why/curriculum/outcome/effort.
        """
        experience = self.present(decision)
        return {
            "what_is_recommended": experience.title,
            "why_it_is_recommended": experience.educational_rationale,
            "curriculum_area": experience.curriculum_area,
            "curriculum_target": experience.trace.curriculum_target,
            "expected_learning_outcome": experience.expected_outcome,
            "estimated_effort": experience.estimated_effort.to_dict(),
            "urgency": experience.urgency,
            "prerequisite_explanation": experience.prerequisite_explanation,
            "next_steps": list(experience.next_steps),
            "motivational_framing": experience.motivational_framing,
            "trace": experience.trace.to_dict(),
            "experience_version": experience.experience_version,
        }

    @staticmethod
    def _require_decision(decision: EducationalDecision | None) -> None:
        if decision is None:
            raise DecisionRequiredError(
                "An Educational Decision is required — "
                "Experience Engine does not create decisions"
            )
