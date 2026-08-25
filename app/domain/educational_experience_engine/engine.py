"""Educational Experience Engine core (EX-001).

Transforms Educational Decisions into Experience Models. Presentation only —
never creates, ranks, or mutates educational decisions.
"""

from __future__ import annotations

from datetime import datetime

from app.domain.educational_experience_engine.experience import (
    EffortPresentation,
    ExperienceModel,
    ExperienceTrace,
)
from app.domain.educational_experience_engine.presentation import (
    curriculum_area_label,
    educational_rationale_for,
    effort_label,
    motivation_for,
    next_steps_for,
    outcome_for,
    prerequisite_explanation,
    summary_for,
    title_for,
    urgency_for,
)
from app.domain.educational_experience_engine.surfaces import (
    CoachConversationContext,
    DailyMissionExperience,
    DashboardPriorityCard,
    RevisionPlannerEntry,
    StudySessionBriefing,
)
from app.domain.educational_experience_engine.version import EXPERIENCE_VERSION
from app.domain.educational_reasoning_engine.decision import EducationalDecision


class EducationalExperienceEngine:
    """Deterministic Decision → Experience transformation.

    Same Educational Decision (+ optional display overrides) always yields the
    same ExperienceModel for a fixed presentation version.
    """

    def __init__(self, *, experience_version: str = EXPERIENCE_VERSION) -> None:
        self.experience_version = experience_version

    def present(
        self,
        decision: EducationalDecision,
        *,
        presented_at: datetime | None = None,
        curriculum_area: str | None = None,
    ) -> ExperienceModel:
        """Build the canonical UI-agnostic ExperienceModel from a decision.

        Args:
            decision: Educational Decision from EI-007 (consumed read-only).
            presented_at: Presentation clock; defaults to decision.reasoned_at
                for determinism when callers do not inject a clock.
            curriculum_area: Optional human label; defaults to a deterministic
                shortening of ``decision.curriculum_target``.

        Returns:
            ExperienceModel preserving full educational explainability.
        """
        when = presented_at if presented_at is not None else decision.reasoned_at
        when = when.replace(tzinfo=None) if when.tzinfo else when
        area = (curriculum_area or "").strip() or curriculum_area_label(
            decision.curriculum_target
        )
        urgency = urgency_for(
            priority=decision.priority,
            decision_type=decision.decision_type,
        )
        minutes = int(decision.estimated_effort_minutes)
        trace = ExperienceTrace(
            decision_id=decision.decision_id,
            decision_type=decision.decision_type,
            curriculum_target=decision.curriculum_target,
            supporting_belief_ids=decision.supporting_belief_ids,
            supporting_curriculum_refs=decision.supporting_curriculum_refs,
            supporting_evidence_ids=decision.supporting_evidence_ids,
            applied_rule_ids=decision.applied_rule_ids,
            reasoning_version=decision.reasoning_version,
            priority=decision.priority,
            rank_position=decision.rank_position,
        )
        return ExperienceModel(
            experience_id=_experience_id(decision.decision_id),
            instance_id=decision.instance_id,
            title=title_for(decision.decision_type, decision.curriculum_target),
            summary=summary_for(decision.decision_type, area),
            # Student-facing why from presentation catalogues — never copy
            # EI-007 rationale_summary (internal audit / debug text).
            educational_rationale=educational_rationale_for(
                decision.decision_type, area
            ),
            estimated_effort=EffortPresentation(
                minutes=minutes,
                label=effort_label(minutes),
            ),
            expected_outcome=outcome_for(decision.expected_educational_outcome),
            urgency=urgency.value,
            prerequisite_explanation=prerequisite_explanation(
                decision_type=decision.decision_type,
                prerequisite_chain=decision.prerequisite_chain,
            ),
            motivational_framing=motivation_for(decision.decision_type),
            next_steps=next_steps_for(decision.decision_type),
            curriculum_area=area,
            trace=trace,
            presented_at=when,
            experience_version=self.experience_version,
        )

    def to_daily_mission(
        self,
        decision: EducationalDecision,
        *,
        presented_at: datetime | None = None,
        curriculum_area: str | None = None,
    ) -> DailyMissionExperience:
        return DailyMissionExperience.from_experience(
            self.present(
                decision,
                presented_at=presented_at,
                curriculum_area=curriculum_area,
            )
        )

    def to_coach_context(
        self,
        decision: EducationalDecision,
        *,
        presented_at: datetime | None = None,
        curriculum_area: str | None = None,
    ) -> CoachConversationContext:
        return CoachConversationContext.from_experience(
            self.present(
                decision,
                presented_at=presented_at,
                curriculum_area=curriculum_area,
            )
        )

    def to_dashboard_card(
        self,
        decision: EducationalDecision,
        *,
        presented_at: datetime | None = None,
        curriculum_area: str | None = None,
    ) -> DashboardPriorityCard:
        return DashboardPriorityCard.from_experience(
            self.present(
                decision,
                presented_at=presented_at,
                curriculum_area=curriculum_area,
            )
        )

    def to_revision_entry(
        self,
        decision: EducationalDecision,
        *,
        presented_at: datetime | None = None,
        curriculum_area: str | None = None,
    ) -> RevisionPlannerEntry:
        return RevisionPlannerEntry.from_experience(
            self.present(
                decision,
                presented_at=presented_at,
                curriculum_area=curriculum_area,
            )
        )

    def to_session_briefing(
        self,
        decision: EducationalDecision,
        *,
        presented_at: datetime | None = None,
        curriculum_area: str | None = None,
    ) -> StudySessionBriefing:
        return StudySessionBriefing.from_experience(
            self.present(
                decision,
                presented_at=presented_at,
                curriculum_area=curriculum_area,
            )
        )


def _experience_id(decision_id: str) -> str:
    return f"eee:{decision_id}"
