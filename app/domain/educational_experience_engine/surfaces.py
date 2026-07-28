"""Surface-specific experience projections (EX-001).

Each surface model is derived from the same ExperienceModel / Educational
Decision. Surfaces never invent educational actions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.domain.educational_experience_engine.experience import ExperienceModel


@dataclass(frozen=True)
class DailyMissionExperience:
    """Presentation model for Daily Mission surfaces."""

    experience_id: str
    decision_id: str
    mission_title: str
    mission_summary: str
    why_this_mission: str
    curriculum_target: str
    curriculum_area: str
    estimated_minutes: int
    estimated_effort_label: str
    expected_outcome: str
    urgency: str
    prerequisite_note: str
    motivational_line: str
    task_steps: tuple[str, ...]
    experience_version: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "experience_id": self.experience_id,
            "decision_id": self.decision_id,
            "mission_title": self.mission_title,
            "mission_summary": self.mission_summary,
            "why_this_mission": self.why_this_mission,
            "curriculum_target": self.curriculum_target,
            "curriculum_area": self.curriculum_area,
            "estimated_minutes": self.estimated_minutes,
            "estimated_effort_label": self.estimated_effort_label,
            "expected_outcome": self.expected_outcome,
            "urgency": self.urgency,
            "prerequisite_note": self.prerequisite_note,
            "motivational_line": self.motivational_line,
            "task_steps": list(self.task_steps),
            "experience_version": self.experience_version,
        }

    @classmethod
    def from_experience(cls, experience: ExperienceModel) -> DailyMissionExperience:
        return cls(
            experience_id=experience.experience_id,
            decision_id=experience.trace.decision_id,
            mission_title=experience.title,
            mission_summary=experience.summary,
            why_this_mission=experience.educational_rationale,
            curriculum_target=experience.trace.curriculum_target,
            curriculum_area=experience.curriculum_area,
            estimated_minutes=experience.estimated_effort.minutes,
            estimated_effort_label=experience.estimated_effort.label,
            expected_outcome=experience.expected_outcome,
            urgency=experience.urgency,
            prerequisite_note=experience.prerequisite_explanation,
            motivational_line=experience.motivational_framing,
            task_steps=experience.next_steps,
            experience_version=experience.experience_version,
        )


@dataclass(frozen=True)
class CoachConversationContext:
    """Presentation model for AI Coach conversation grounding."""

    experience_id: str
    decision_id: str
    focus_title: str
    coach_opening: str
    educational_why: str
    curriculum_target: str
    curriculum_area: str
    estimated_minutes: int
    expected_outcome: str
    urgency: str
    prerequisite_note: str
    talking_points: tuple[str, ...]
    suggested_prompts: tuple[str, ...]
    experience_version: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "experience_id": self.experience_id,
            "decision_id": self.decision_id,
            "focus_title": self.focus_title,
            "coach_opening": self.coach_opening,
            "educational_why": self.educational_why,
            "curriculum_target": self.curriculum_target,
            "curriculum_area": self.curriculum_area,
            "estimated_minutes": self.estimated_minutes,
            "expected_outcome": self.expected_outcome,
            "urgency": self.urgency,
            "prerequisite_note": self.prerequisite_note,
            "talking_points": list(self.talking_points),
            "suggested_prompts": list(self.suggested_prompts),
            "experience_version": self.experience_version,
        }

    @classmethod
    def from_experience(
        cls, experience: ExperienceModel
    ) -> CoachConversationContext:
        prompts = (
            f"Why is {experience.curriculum_area} the right focus now?",
            "What should I do first in this study block?",
            "How will I know this session helped?",
        )
        return cls(
            experience_id=experience.experience_id,
            decision_id=experience.trace.decision_id,
            focus_title=experience.title,
            coach_opening=(
                f"{experience.motivational_framing} "
                f"Today's focus: {experience.title}."
            ),
            educational_why=experience.educational_rationale,
            curriculum_target=experience.trace.curriculum_target,
            curriculum_area=experience.curriculum_area,
            estimated_minutes=experience.estimated_effort.minutes,
            expected_outcome=experience.expected_outcome,
            urgency=experience.urgency,
            prerequisite_note=experience.prerequisite_explanation,
            talking_points=experience.next_steps,
            suggested_prompts=prompts,
            experience_version=experience.experience_version,
        )


@dataclass(frozen=True)
class DashboardPriorityCard:
    """Presentation model for Dashboard priority cards."""

    experience_id: str
    decision_id: str
    card_title: str
    card_summary: str
    why_label: str
    curriculum_target: str
    curriculum_area: str
    effort_label: str
    expected_outcome: str
    urgency: str
    rank_position: int
    priority: float
    cta_label: str
    experience_version: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "experience_id": self.experience_id,
            "decision_id": self.decision_id,
            "card_title": self.card_title,
            "card_summary": self.card_summary,
            "why_label": self.why_label,
            "curriculum_target": self.curriculum_target,
            "curriculum_area": self.curriculum_area,
            "effort_label": self.effort_label,
            "expected_outcome": self.expected_outcome,
            "urgency": self.urgency,
            "rank_position": self.rank_position,
            "priority": self.priority,
            "cta_label": self.cta_label,
            "experience_version": self.experience_version,
        }

    @classmethod
    def from_experience(cls, experience: ExperienceModel) -> DashboardPriorityCard:
        return cls(
            experience_id=experience.experience_id,
            decision_id=experience.trace.decision_id,
            card_title=experience.title,
            card_summary=experience.summary,
            why_label=experience.educational_rationale,
            curriculum_target=experience.trace.curriculum_target,
            curriculum_area=experience.curriculum_area,
            effort_label=experience.estimated_effort.label,
            expected_outcome=experience.expected_outcome,
            urgency=experience.urgency,
            rank_position=experience.trace.rank_position,
            priority=experience.trace.priority,
            cta_label=_cta_for_urgency(experience.urgency),
            experience_version=experience.experience_version,
        )


@dataclass(frozen=True)
class RevisionPlannerEntry:
    """Presentation model for Revision Planner entries."""

    experience_id: str
    decision_id: str
    entry_title: str
    entry_summary: str
    educational_why: str
    curriculum_target: str
    curriculum_area: str
    estimated_minutes: int
    estimated_effort_label: str
    expected_outcome: str
    urgency: str
    prerequisite_note: str
    revision_steps: tuple[str, ...]
    is_revision_action: bool
    experience_version: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "experience_id": self.experience_id,
            "decision_id": self.decision_id,
            "entry_title": self.entry_title,
            "entry_summary": self.entry_summary,
            "educational_why": self.educational_why,
            "curriculum_target": self.curriculum_target,
            "curriculum_area": self.curriculum_area,
            "estimated_minutes": self.estimated_minutes,
            "estimated_effort_label": self.estimated_effort_label,
            "expected_outcome": self.expected_outcome,
            "urgency": self.urgency,
            "prerequisite_note": self.prerequisite_note,
            "revision_steps": list(self.revision_steps),
            "is_revision_action": self.is_revision_action,
            "experience_version": self.experience_version,
        }

    @classmethod
    def from_experience(cls, experience: ExperienceModel) -> RevisionPlannerEntry:
        dtype = experience.trace.decision_type
        return cls(
            experience_id=experience.experience_id,
            decision_id=experience.trace.decision_id,
            entry_title=experience.title,
            entry_summary=experience.summary,
            educational_why=experience.educational_rationale,
            curriculum_target=experience.trace.curriculum_target,
            curriculum_area=experience.curriculum_area,
            estimated_minutes=experience.estimated_effort.minutes,
            estimated_effort_label=experience.estimated_effort.label,
            expected_outcome=experience.expected_outcome,
            urgency=experience.urgency,
            prerequisite_note=experience.prerequisite_explanation,
            revision_steps=experience.next_steps,
            is_revision_action=dtype
            in {"revise", "strengthen_confidence", "satisfy_prerequisite"},
            experience_version=experience.experience_version,
        )


@dataclass(frozen=True)
class StudySessionBriefing:
    """Presentation model for study session briefings."""

    experience_id: str
    decision_id: str
    briefing_title: str
    briefing_summary: str
    educational_why: str
    curriculum_target: str
    curriculum_area: str
    estimated_minutes: int
    estimated_effort_label: str
    expected_outcome: str
    urgency: str
    prerequisite_note: str
    motivational_line: str
    session_steps: tuple[str, ...]
    success_signal: str
    experience_version: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "experience_id": self.experience_id,
            "decision_id": self.decision_id,
            "briefing_title": self.briefing_title,
            "briefing_summary": self.briefing_summary,
            "educational_why": self.educational_why,
            "curriculum_target": self.curriculum_target,
            "curriculum_area": self.curriculum_area,
            "estimated_minutes": self.estimated_minutes,
            "estimated_effort_label": self.estimated_effort_label,
            "expected_outcome": self.expected_outcome,
            "urgency": self.urgency,
            "prerequisite_note": self.prerequisite_note,
            "motivational_line": self.motivational_line,
            "session_steps": list(self.session_steps),
            "success_signal": self.success_signal,
            "experience_version": self.experience_version,
        }

    @classmethod
    def from_experience(cls, experience: ExperienceModel) -> StudySessionBriefing:
        return cls(
            experience_id=experience.experience_id,
            decision_id=experience.trace.decision_id,
            briefing_title=experience.title,
            briefing_summary=experience.summary,
            educational_why=experience.educational_rationale,
            curriculum_target=experience.trace.curriculum_target,
            curriculum_area=experience.curriculum_area,
            estimated_minutes=experience.estimated_effort.minutes,
            estimated_effort_label=experience.estimated_effort.label,
            expected_outcome=experience.expected_outcome,
            urgency=experience.urgency,
            prerequisite_note=experience.prerequisite_explanation,
            motivational_line=experience.motivational_framing,
            session_steps=experience.next_steps,
            success_signal=experience.expected_outcome,
            experience_version=experience.experience_version,
        )


def _cta_for_urgency(urgency: str) -> str:
    mapping = {
        "critical": "Start now",
        "high": "Continue today",
        "moderate": "Plan this block",
        "low": "Review when ready",
    }
    return mapping.get(urgency, "Continue")
