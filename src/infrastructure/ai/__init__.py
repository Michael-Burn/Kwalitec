"""Educational Enrichment Layer — AI presentation enrichment only.

AI-001: Enrich MissionSpecification and RecommendationSpecification wording
without changing educational decisions.

The Educational Operating System remains the sole source of educational truth.
Providers may improve wording, examples, analogies, tone, worked examples, and
revision tips. They must never alter objective, priority, duration, sequence,
or educational rationale.
"""

from __future__ import annotations

from infrastructure.ai.enrichment.mission_enricher import MissionEnricher
from infrastructure.ai.enrichment.recommendation_enricher import RecommendationEnricher
from infrastructure.ai.models.enhanced_mission import EnhancedMission
from infrastructure.ai.models.enhanced_recommendation import EnhancedRecommendation
from infrastructure.ai.prompting.mission_prompt_builder import MissionPromptBuilder
from infrastructure.ai.prompting.prompt_builder import PromptBuilder
from infrastructure.ai.prompting.recommendation_prompt_builder import (
    RecommendationPromptBuilder,
)
from infrastructure.ai.providers.ai_provider import (
    AIProvider,
    AIProviderError,
    AIProviderNotConfiguredError,
    EnrichmentResponse,
    PromptDocument,
    parse_enrichment_payload,
)
from infrastructure.ai.providers.anthropic_provider import AnthropicProvider
from infrastructure.ai.providers.gemini_provider import GeminiProvider
from infrastructure.ai.providers.openai_provider import OpenAIProvider

__all__ = [
    "AIProvider",
    "AIProviderError",
    "AIProviderNotConfiguredError",
    "AnthropicProvider",
    "EnhancedMission",
    "EnhancedRecommendation",
    "EnrichmentResponse",
    "GeminiProvider",
    "MissionEnricher",
    "MissionPromptBuilder",
    "OpenAIProvider",
    "PromptBuilder",
    "PromptDocument",
    "RecommendationEnricher",
    "RecommendationPromptBuilder",
    "parse_enrichment_payload",
]
