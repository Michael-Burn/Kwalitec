"""Prompt generation tests for AI-001 Educational Enrichment Layer."""

from __future__ import annotations

from infrastructure.ai.prompting.mission_prompt_builder import (
    PURPOSE as MISSION_PURPOSE,
)
from infrastructure.ai.prompting.mission_prompt_builder import MissionPromptBuilder
from infrastructure.ai.prompting.prompt_builder import ENRICHMENT_CONSTRAINTS
from infrastructure.ai.prompting.recommendation_prompt_builder import (
    PURPOSE as RECOMMENDATION_PURPOSE,
)
from infrastructure.ai.prompting.recommendation_prompt_builder import (
    RecommendationPromptBuilder,
)
from tests.education_os.infrastructure.ai.helpers import aligned_enrichment_inputs


def test_mission_prompt_is_deterministic() -> None:
    mission, _recommendations, experience = aligned_enrichment_inputs()
    builder = MissionPromptBuilder()
    first = builder.build(mission, experience)
    second = builder.build(mission, experience)
    assert first == second
    assert first.purpose == MISSION_PURPOSE
    assert first.system == second.system
    assert first.user == second.user


def test_recommendation_prompt_is_deterministic() -> None:
    _mission, recommendations, experience = aligned_enrichment_inputs()
    builder = RecommendationPromptBuilder()
    first = builder.build(recommendations, experience)
    second = builder.build(recommendations, experience)
    assert first == second
    assert first.purpose == RECOMMENDATION_PURPOSE


def test_mission_prompt_includes_constraints_and_educational_fields() -> None:
    mission, _recommendations, experience = aligned_enrichment_inputs()
    prompt = MissionPromptBuilder().build(mission, experience)
    assert ENRICHMENT_CONSTRAINTS in prompt.system
    assert "MUST NOT change objective" in prompt.system
    assert mission.objective.statement in prompt.user
    assert mission.priority.band.value in prompt.user
    assert str(mission.duration.planned_minutes) in prompt.user
    assert mission.educational_rationale in prompt.user
    assert mission.sequence.tasks[0].label in prompt.user
    assert experience.motivation.tone.value in prompt.user


def test_recommendation_prompt_includes_constraints_and_decisions() -> None:
    _mission, recommendations, experience = aligned_enrichment_inputs()
    prompt = RecommendationPromptBuilder().build(recommendations, experience)
    assert ENRICHMENT_CONSTRAINTS in prompt.system
    assert "MUST NOT" in prompt.system
    assert recommendations.educational_rationale in prompt.user
    assert recommendations.primary.reason.statement in prompt.user
    assert recommendations.primary.expected_outcome in prompt.user
    assert "Do not change recommendations" in prompt.user
    assert experience.presentation_narrative in prompt.user
