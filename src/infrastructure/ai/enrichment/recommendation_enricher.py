"""RecommendationEnricher — enrich RecommendationSpecification presentation.

Architecture Source
    AI-001 Educational Enrichment Layer
Concept
    Recommendation Enricher

Depends on AIProvider (dependency inversion). Never mutates or replaces
educational recommendation decisions.
"""

from __future__ import annotations

from domain.recommendation.recommendation_specification import (
    RecommendationSpecification,
)
from domain.student_experience.student_experience import StudentExperience
from infrastructure.ai.models.enhanced_recommendation import EnhancedRecommendation
from infrastructure.ai.prompting.recommendation_prompt_builder import (
    RecommendationPromptBuilder,
)
from infrastructure.ai.providers.ai_provider import AIProvider, AIProviderError


class RecommendationEnricher:
    """Orchestrate recommendation presentation enrichment via an AIProvider."""

    def __init__(
        self,
        provider: AIProvider,
        *,
        prompt_builder: RecommendationPromptBuilder | None = None,
    ) -> None:
        if not isinstance(provider, AIProvider):
            raise AIProviderError("provider must implement AIProvider")
        self._provider = provider
        self._prompt_builder = prompt_builder or RecommendationPromptBuilder()

    @property
    def provider(self) -> AIProvider:
        return self._provider

    def enrich(
        self,
        recommendations: RecommendationSpecification,
        experience: StudentExperience,
    ) -> EnhancedRecommendation:
        """Enrich recommendation presentation without changing decisions.

        Args:
            recommendations: Educational OS RecommendationSpecification.
            experience: StudentExperience presentation context.

        Returns:
            EnhancedRecommendation wrapping the original specification plus
            enrichment.
        """
        prompt = self._prompt_builder.build(recommendations, experience)
        response = self._provider.complete(prompt)
        enhanced = EnhancedRecommendation.from_enrichment(
            recommendations,
            response,
            provider_name=self._provider.name,
        )
        _assert_educational_fields_unchanged(recommendations, enhanced)
        return enhanced


def _assert_educational_fields_unchanged(
    original: RecommendationSpecification,
    enhanced: EnhancedRecommendation,
) -> None:
    """Guardrail: enrichment must preserve Educational OS decisions."""
    if enhanced.specification is not original:
        raise AIProviderError(
            "EnhancedRecommendation must retain the original "
            "RecommendationSpecification"
        )
    if enhanced.recommendations is not original.recommendations:
        raise AIProviderError("enrichment must not change recommendations")
    if enhanced.educational_rationale != original.educational_rationale:
        raise AIProviderError(
            "enrichment must not change recommendation educational rationale"
        )
    if enhanced.primary is not original.primary:
        raise AIProviderError("enrichment must not change primary recommendation")
