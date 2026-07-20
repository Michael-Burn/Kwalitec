"""Enrichment mapping tests for AI-001 Educational Enrichment Layer."""

from __future__ import annotations

from infrastructure.ai.enrichment.mission_enricher import MissionEnricher
from infrastructure.ai.enrichment.recommendation_enricher import (
    RecommendationEnricher,
)
from infrastructure.ai.models.enhanced_mission import EnhancedMission
from infrastructure.ai.models.enhanced_recommendation import EnhancedRecommendation
from infrastructure.ai.providers.openai_provider import OpenAIProvider
from tests.education_os.infrastructure.ai.helpers import (
    FakeAIProvider,
    FakeCompletionTransport,
    aligned_enrichment_inputs,
    sample_enrichment_response,
)


def test_mission_enricher_maps_response_without_changing_decisions() -> None:
    mission, _recommendations, experience = aligned_enrichment_inputs()
    enrichment = sample_enrichment_response(
        improved_wording="Clearer mission wording for the learner.",
    )
    enricher = MissionEnricher(FakeAIProvider(response=enrichment))
    enhanced = enricher.enrich(mission, experience)

    assert isinstance(enhanced, EnhancedMission)
    assert enhanced.specification is mission
    assert enhanced.objective is mission.objective
    assert enhanced.priority is mission.priority
    assert enhanced.duration is mission.duration
    assert enhanced.sequence is mission.sequence
    assert enhanced.educational_rationale == mission.educational_rationale
    assert enhanced.improved_wording == enrichment.improved_wording
    assert enhanced.examples == enrichment.examples
    assert enhanced.analogies == enrichment.analogies
    assert enhanced.adapted_tone == enrichment.adapted_tone
    assert enhanced.worked_examples == enrichment.worked_examples
    assert enhanced.revision_tips == enrichment.revision_tips
    assert enhanced.provider_name == "fake"


def test_recommendation_enricher_maps_response_without_changing_decisions() -> None:
    _mission, recommendations, experience = aligned_enrichment_inputs()
    enrichment = sample_enrichment_response(
        adapted_tone="encouraging and precise",
    )
    enricher = RecommendationEnricher(FakeAIProvider(response=enrichment))
    enhanced = enricher.enrich(recommendations, experience)

    assert isinstance(enhanced, EnhancedRecommendation)
    assert enhanced.specification is recommendations
    assert enhanced.recommendations is recommendations.recommendations
    assert enhanced.primary is recommendations.primary
    assert enhanced.educational_rationale == recommendations.educational_rationale
    assert enhanced.adapted_tone == "encouraging and precise"
    assert enhanced.provider_name == "fake"


def test_enrichment_is_provider_independent() -> None:
    mission, recommendations, experience = aligned_enrichment_inputs()
    transport = FakeCompletionTransport()
    openai_mission = MissionEnricher(OpenAIProvider(transport=transport)).enrich(
        mission, experience
    )
    fake_mission = MissionEnricher(FakeAIProvider()).enrich(mission, experience)

    assert openai_mission.improved_wording == fake_mission.improved_wording
    assert openai_mission.examples == fake_mission.examples
    assert openai_mission.objective is mission.objective
    assert fake_mission.objective is mission.objective

    openai_rec = RecommendationEnricher(
        OpenAIProvider(transport=FakeCompletionTransport())
    ).enrich(recommendations, experience)
    fake_rec = RecommendationEnricher(FakeAIProvider()).enrich(
        recommendations, experience
    )
    assert openai_rec.revision_tips == fake_rec.revision_tips
    assert openai_rec.recommendations is recommendations.recommendations


def test_enhanced_mission_from_enrichment_factory() -> None:
    mission, _recommendations, _experience = aligned_enrichment_inputs()
    enrichment = sample_enrichment_response()
    enhanced = EnhancedMission.from_enrichment(
        mission, enrichment, provider_name="openai"
    )
    assert enhanced.provider_name == "openai"
    assert enhanced.specification is mission
