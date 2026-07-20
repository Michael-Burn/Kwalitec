"""MissionEnricher — enrich MissionSpecification presentation only.

Architecture Source
    AI-001 Educational Enrichment Layer
Concept
    Mission Enricher

Depends on AIProvider (dependency inversion). Never mutates or replaces
educational decisions on the MissionSpecification.
"""

from __future__ import annotations

from domain.mission_generation.mission_specification import MissionSpecification
from domain.student_experience.student_experience import StudentExperience
from infrastructure.ai.models.enhanced_mission import EnhancedMission
from infrastructure.ai.prompting.mission_prompt_builder import MissionPromptBuilder
from infrastructure.ai.providers.ai_provider import AIProvider, AIProviderError


class MissionEnricher:
    """Orchestrate mission presentation enrichment via an AIProvider."""

    def __init__(
        self,
        provider: AIProvider,
        *,
        prompt_builder: MissionPromptBuilder | None = None,
    ) -> None:
        if not isinstance(provider, AIProvider):
            raise AIProviderError("provider must implement AIProvider")
        self._provider = provider
        self._prompt_builder = prompt_builder or MissionPromptBuilder()

    @property
    def provider(self) -> AIProvider:
        return self._provider

    def enrich(
        self,
        mission: MissionSpecification,
        experience: StudentExperience,
    ) -> EnhancedMission:
        """Enrich mission presentation without changing educational decisions.

        Args:
            mission: Educational OS MissionSpecification (immutable truth).
            experience: StudentExperience presentation context.

        Returns:
            EnhancedMission wrapping the original specification plus enrichment.
        """
        prompt = self._prompt_builder.build(mission, experience)
        response = self._provider.complete(prompt)
        enhanced = EnhancedMission.from_enrichment(
            mission,
            response,
            provider_name=self._provider.name,
        )
        _assert_educational_fields_unchanged(mission, enhanced)
        return enhanced


def _assert_educational_fields_unchanged(
    original: MissionSpecification,
    enhanced: EnhancedMission,
) -> None:
    """Guardrail: enrichment must preserve Educational OS decision fields."""
    if enhanced.specification is not original:
        raise AIProviderError(
            "EnhancedMission must retain the original MissionSpecification"
        )
    if enhanced.objective is not original.objective:
        raise AIProviderError("enrichment must not change mission objective")
    if enhanced.priority is not original.priority:
        raise AIProviderError("enrichment must not change mission priority")
    if enhanced.duration is not original.duration:
        raise AIProviderError("enrichment must not change mission duration")
    if enhanced.sequence is not original.sequence:
        raise AIProviderError("enrichment must not change mission sequence")
    if enhanced.educational_rationale != original.educational_rationale:
        raise AIProviderError(
            "enrichment must not change mission educational rationale"
        )
