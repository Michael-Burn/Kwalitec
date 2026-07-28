"""Adapter purity and cross-surface consistency tests (RI-001)."""

from __future__ import annotations

from datetime import datetime

from app.application.educational_experience_engine.experience_service import (
    ExperienceTransformationService,
)
from app.application.runtime_integration import (
    map_coach_context,
    map_daily_mission,
    map_dashboard_recommendation,
    map_revision_entry,
    map_session_briefing,
)
from app.domain.educational_reasoning_engine.decision import EducationalDecision
from app.domain.educational_reasoning_engine.decision_type import (
    DecisionType,
    ExpectedOutcome,
)
from app.domain.educational_reasoning_engine.version import REASONING_VERSION

AS_OF = datetime(2026, 7, 28, 12, 0, 0)


def _decision() -> EducationalDecision:
    return EducationalDecision(
        decision_id="ere-dec-ri001",
        instance_id="sci-ri001",
        decision_type=DecisionType.STUDY_NEW.value,
        curriculum_target="CS1.LO1",
        priority=0.7,
        rank_position=1,
        rationale_summary="Study new incomplete learning objective.",
        prerequisite_chain=(),
        estimated_effort_minutes=25,
        expected_educational_outcome=ExpectedOutcome.INTRODUCE_NODE.value,
        supporting_belief_ids=("tie-1",),
        supporting_curriculum_refs=("CS1.LO1",),
        supporting_evidence_ids=("lee-1",),
        applied_rule_ids=("incomplete_curriculum_paths",),
        reasoned_at=AS_OF,
        reasoning_version=REASONING_VERSION,
    )


def test_adapters_share_decision_id_and_why() -> None:
    bundle = ExperienceTransformationService().present_all_surfaces(
        _decision(), presented_at=AS_OF
    )
    dashboard = map_dashboard_recommendation(bundle)
    mission = map_daily_mission(bundle.daily_mission)
    coach = map_coach_context(bundle.coach)
    revision = map_revision_entry(bundle.revision_entry)
    session = map_session_briefing(bundle.session_briefing)

    decision_ids = {
        dashboard["decision_id"],
        mission["decision_id"],
        coach["decision_id"],
        revision["decision_id"],
        session["decision_id"],
    }
    assert decision_ids == {"ere-dec-ri001"}

    why_values = {
        dashboard["why_recommended"],
        mission["why_this_mission"],
        coach["educational_why"],
        revision["educational_why"],
        session["educational_why"],
    }
    assert why_values == {"Study new incomplete learning objective."}

    assert dashboard["curriculum_target"] == "CS1.LO1"
    assert mission["curriculum_target"] == session["curriculum_target"] == "CS1.LO1"


def test_adapters_do_not_mutate_experience_model() -> None:
    decision = _decision()
    bundle = ExperienceTransformationService().present_all_surfaces(
        decision, presented_at=AS_OF
    )
    before = bundle.experience.educational_rationale
    map_dashboard_recommendation(bundle)
    map_daily_mission(bundle.daily_mission)
    assert bundle.experience.educational_rationale == before
    assert decision.rationale_summary == before
