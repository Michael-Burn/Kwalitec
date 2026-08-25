"""Domain tests for Educational Experience Engine (EX-001)."""

from __future__ import annotations

from datetime import datetime

import pytest

from app.domain.educational_experience_engine.engine import EducationalExperienceEngine
from app.domain.educational_experience_engine.experience import ExperienceModel
from app.domain.educational_experience_engine.presentation import urgency_for
from app.domain.educational_experience_engine.surfaces import (
    CoachConversationContext,
    DailyMissionExperience,
    DashboardPriorityCard,
    RevisionPlannerEntry,
    StudySessionBriefing,
)
from app.domain.educational_experience_engine.urgency import UrgencyLevel
from app.domain.educational_experience_engine.version import EXPERIENCE_VERSION
from app.domain.educational_reasoning_engine.decision import EducationalDecision
from app.domain.educational_reasoning_engine.decision_type import (
    DecisionType,
    ExpectedOutcome,
)

AS_OF = datetime(2026, 7, 28, 12, 0, 0)


def _decision(
    *,
    decision_type: str = DecisionType.STUDY_NEW.value,
    priority: float = 0.6,
    outcome: str = ExpectedOutcome.INTRODUCE_NODE.value,
    prereqs: tuple[str, ...] = (),
    target: str = "CS1.LO1",
) -> EducationalDecision:
    return EducationalDecision(
        decision_id="ere-dec-1",
        instance_id="sci-1",
        decision_type=decision_type,
        curriculum_target=target,
        priority=priority,
        rank_position=1,
        rationale_summary="Incomplete path at syllabus index 0 with evidence.",
        prerequisite_chain=prereqs,
        estimated_effort_minutes=30,
        expected_educational_outcome=outcome,
        supporting_belief_ids=("tie-1",),
        supporting_curriculum_refs=(target,),
        supporting_evidence_ids=("lee-1",),
        applied_rule_ids=("incomplete_curriculum_paths",),
        reasoned_at=AS_OF,
    )


def test_experience_model_requires_core_fields() -> None:
    decision = _decision()
    experience = EducationalExperienceEngine().present(decision)
    with pytest.raises(ValueError, match="title"):
        ExperienceModel(
            experience_id=experience.experience_id,
            instance_id=experience.instance_id,
            title="  ",
            summary=experience.summary,
            educational_rationale=experience.educational_rationale,
            estimated_effort=experience.estimated_effort,
            expected_outcome=experience.expected_outcome,
            urgency=experience.urgency,
            prerequisite_explanation=experience.prerequisite_explanation,
            motivational_framing=experience.motivational_framing,
            next_steps=experience.next_steps,
            curriculum_area=experience.curriculum_area,
            trace=experience.trace,
            presented_at=experience.presented_at,
        )


def test_same_decision_yields_identical_experience() -> None:
    engine = EducationalExperienceEngine()
    decision = _decision()
    first = engine.present(decision, presented_at=AS_OF)
    second = engine.present(decision, presented_at=AS_OF)
    assert first == second
    assert first.experience_version == EXPERIENCE_VERSION
    assert first.trace.decision_id == decision.decision_id
    # Student-facing why is catalogue-derived — never EI-007 audit text.
    assert first.educational_rationale != decision.rationale_summary
    assert "LO1" in first.educational_rationale
    assert "incomplete curriculum path" in first.educational_rationale.lower()


def test_surfaces_consume_same_decision_consistently() -> None:
    engine = EducationalExperienceEngine()
    decision = _decision(
        decision_type=DecisionType.REVISE.value,
        priority=0.8,
        outcome=ExpectedOutcome.RESTORE_RETENTION.value,
    )
    experience = engine.present(decision, presented_at=AS_OF)
    mission = engine.to_daily_mission(decision, presented_at=AS_OF)
    coach = engine.to_coach_context(decision, presented_at=AS_OF)
    card = engine.to_dashboard_card(decision, presented_at=AS_OF)
    revision = engine.to_revision_entry(decision, presented_at=AS_OF)
    briefing = engine.to_session_briefing(decision, presented_at=AS_OF)

    assert isinstance(mission, DailyMissionExperience)
    assert isinstance(coach, CoachConversationContext)
    assert isinstance(card, DashboardPriorityCard)
    assert isinstance(revision, RevisionPlannerEntry)
    assert isinstance(briefing, StudySessionBriefing)

    decision_ids = {
        mission.decision_id,
        coach.decision_id,
        card.decision_id,
        revision.decision_id,
        briefing.decision_id,
        experience.trace.decision_id,
    }
    assert decision_ids == {decision.decision_id}

    titles = {
        mission.mission_title,
        coach.focus_title,
        card.card_title,
        revision.entry_title,
        briefing.briefing_title,
        experience.title,
    }
    assert len(titles) == 1

    expected_why = experience.educational_rationale
    whys = {
        mission.why_this_mission,
        coach.educational_why,
        card.why_label,
        revision.educational_why,
        briefing.educational_why,
        experience.educational_rationale,
    }
    assert whys == {expected_why}
    assert expected_why != decision.rationale_summary
    assert "revision" in expected_why.lower()
    assert revision.is_revision_action is True


def test_internal_rationale_summary_never_reaches_student_why() -> None:
    """Bug 1: EI-007 audit strings must not leak into educational_rationale."""
    decision = EducationalDecision(
        decision_id="ere-dec-bug1",
        instance_id="sci-1",
        decision_type=DecisionType.CONTINUE_PATH.value,
        curriculum_target="CS1",
        priority=0.5,
        rank_position=1,
        rationale_summary=(
            "Rank 1 continue_path on CS1 with priority 0.5000 "
            "via rules [study_continuity] (ere.v1)."
        ),
        prerequisite_chain=(),
        estimated_effort_minutes=25,
        expected_educational_outcome=ExpectedOutcome.MAINTAIN_MOMENTUM.value,
        supporting_belief_ids=("tie-1",),
        supporting_curriculum_refs=("CS1",),
        supporting_evidence_ids=("lee-1",),
        applied_rule_ids=("study_continuity",),
        reasoned_at=AS_OF,
    )
    experience = EducationalExperienceEngine().present(decision, presented_at=AS_OF)
    mission = EducationalExperienceEngine().to_daily_mission(
        decision, presented_at=AS_OF
    )
    assert experience.educational_rationale != decision.rationale_summary
    assert "rank" not in experience.educational_rationale.lower()
    assert "priority" not in experience.educational_rationale.lower()
    assert "study_continuity" not in experience.educational_rationale
    assert "ere.v1" not in experience.educational_rationale
    assert mission.why_this_mission == experience.educational_rationale
    assert "CS1" in experience.educational_rationale
    assert "momentum" in experience.educational_rationale.lower()


def test_explainability_preserved() -> None:
    experience = EducationalExperienceEngine().present(_decision(prereqs=("CS1.LO0",)))
    assert experience.educational_rationale
    assert experience.curriculum_area
    assert experience.expected_outcome
    assert experience.estimated_effort.minutes == 30
    assert experience.trace.supporting_belief_ids == ("tie-1",)
    assert experience.trace.supporting_evidence_ids == ("lee-1",)
    assert experience.trace.applied_rule_ids
    assert "prerequisite" in experience.prerequisite_explanation.lower()


def test_urgency_mapping_is_presentation_only() -> None:
    assert urgency_for(priority=0.9, decision_type=DecisionType.STUDY_NEW.value) == (
        UrgencyLevel.CRITICAL
    )
    assert urgency_for(priority=0.6, decision_type=DecisionType.REVISE.value) == (
        UrgencyLevel.CRITICAL
    )
    assert urgency_for(
        priority=0.5, decision_type=DecisionType.SATISFY_PREREQUISITE.value
    ) == UrgencyLevel.HIGH
    assert (
        urgency_for(
            priority=0.2,
            decision_type=DecisionType.CONTINUE_PATH.value,
        )
        == UrgencyLevel.LOW
    )


def test_engine_does_not_mutate_decision() -> None:
    decision = _decision()
    before = decision.to_dict()
    EducationalExperienceEngine().present(decision)
    assert decision.to_dict() == before
