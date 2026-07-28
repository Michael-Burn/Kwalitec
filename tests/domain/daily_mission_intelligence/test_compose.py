"""Domain tests for Daily Mission Intelligence (ILE-004)."""

from __future__ import annotations

import pytest

from app.domain.daily_mission_intelligence import (
    DailyMissionEvidenceInput,
    MissionLifecyclePhase,
    MissionOptimisationAxis,
    compose_daily_mission,
    empty_mission_brief,
)
from app.domain.daily_mission_intelligence.invariants import (
    assert_mission_speech_safe,
)
from app.domain.decision_journal.enums import QualitativeConfidence


class TestComposeDailyMission:
    def test_composes_full_brief(self):
        brief = compose_daily_mission(
            DailyMissionEvidenceInput(
                title="Revise equity valuation",
                why_recommended="Recent practice looks fragile on equity.",
                timeliness_line="Your plan places this focus today.",
                supporting_evidence=(
                    "Two short sessions this week were uneven.",
                    "Next syllabus topics depend on this base.",
                ),
                estimated_effort="About 25 minutes",
                expected_benefit="A steadier base for later topics.",
                completion_loop_line="Evidence from today's loop is recorded.",
                confidence_label="Emerging confidence",
                uncertainty="Limited evidence remains on harder items.",
                alternative_titles=("Skip ahead to derivatives",),
                recommendation_key="equity|2026-07-28",
            )
        )
        assert brief.has_mission
        assert brief.title == "Revise equity valuation"
        assert "fragile" in brief.educational_purpose
        assert "today" in brief.why_today.lower()
        assert "derivatives" in brief.why_not_something_else.lower()
        assert len(brief.supporting_evidence) == 2
        assert brief.estimated_effort == "About 25 minutes"
        assert "steadier" in brief.expected_learning_outcome
        assert "recorded" in brief.what_happens_after_completion.lower()
        prompt = brief.reflection_prompt.lower()
        assert "mission" in prompt or "today" in prompt
        assert brief.mission_confidence == "Emerging confidence"
        assert brief.uncertainty
        assert brief.mission_explanation
        assert brief.skip_consequence
        assert brief.optimisation_axis_label == "Learning value"
        assert brief.lifecycle_phase == MissionLifecyclePhase.CREATED
        assert brief.qualitative_confidence == QualitativeConfidence.EMERGING

    def test_empty_without_title(self):
        brief = compose_daily_mission({})
        assert brief.empty
        assert not brief.has_mission
        assert brief.qualitative_confidence == QualitativeConfidence.INSUFFICIENT

    def test_honest_refusal_yields_empty(self):
        brief = compose_daily_mission(
            {
                "title": "Something",
                "honest_refusal": True,
                "confidence_label": "Not enough evidence yet",
            }
        )
        assert brief.empty
        assert "Not enough evidence" in brief.educational_purpose

    def test_mapping_input(self):
        brief = compose_daily_mission(
            {
                "title": "Practice duration matching",
                "why_recommended": "Supports later liability topics.",
                "supporting_evidence": "One uneven attempt yesterday.",
                "expected_benefit": "Clearer grasp of the method.",
            }
        )
        assert brief.has_mission
        assert brief.supporting_evidence == ("One uneven attempt yesterday.",)

    def test_forbids_engagement_theatre(self):
        with pytest.raises(ValueError, match="engagement"):
            compose_daily_mission(
                {
                    "title": "Open the app",
                    "why_recommended": "Boost engagement with a streak.",
                }
            )

    def test_forbids_engine_leakage(self):
        with pytest.raises(ValueError, match="digital twin"):
            assert_mission_speech_safe(
                "Based on your digital twin state",
                field="purpose",
            )

    def test_empty_helper(self):
        brief = empty_mission_brief()
        assert brief.empty
        assert brief.lifecycle_phase == MissionLifecyclePhase.CREATED

    def test_optimisation_axes_are_educational(self):
        axes = {a.value for a in MissionOptimisationAxis}
        assert "learning_value" in axes
        assert "engagement" not in axes
        assert "streak" not in axes
