"""RecommendationPromptBuilder — deterministic recommendation enrichment prompts.

Architecture Source
    AI-001 Educational Enrichment Layer
Concept
    Recommendation Prompt Builder
"""

from __future__ import annotations

from domain.recommendation.recommendation_specification import (
    RecommendationSpecification,
)
from domain.student_experience.student_experience import StudentExperience
from infrastructure.ai.prompting.prompt_builder import PromptBuilder
from infrastructure.ai.providers.ai_provider import PromptDocument

PURPOSE = "recommendation_enrichment"


class RecommendationPromptBuilder(PromptBuilder):
    """Build deterministic prompts for RecommendationSpecification enrichment.

    Same specification and experience always yield the same PromptDocument.
    Recommendation decisions are quoted for context and must not be changed.
    """

    def build(
        self,
        recommendations: RecommendationSpecification,
        experience: StudentExperience,
    ) -> PromptDocument:
        if not isinstance(recommendations, RecommendationSpecification):
            raise TypeError(
                "recommendations must be a RecommendationSpecification"
            )
        if not isinstance(experience, StudentExperience):
            raise TypeError("experience must be a StudentExperience")
        if recommendations.student_id != experience.student_id:
            raise ValueError(
                "recommendations and experience must share the same student_id"
            )
        if (
            recommendations.specification_id
            != experience.recommendation_specification_id
        ):
            raise ValueError(
                "recommendations and experience must reference the same "
                "recommendation_specification_id"
            )

        system = self.system_preamble(
            role="learner recommendation presentation"
        )
        recommendation_lines = tuple(
            (
                f"{index}. [{item.category.value}] "
                f"priority={item.priority.band.value}/"
                f"{item.priority.urgency.value}; "
                f"reason={item.reason.statement}; "
                f"expected_outcome={item.expected_outcome}; "
                f"confidence={item.confidence.level.value}"
            )
            for index, item in enumerate(recommendations.recommendations, start=1)
        )
        user = "\n".join(
            (
                "Enrich the following RecommendationSpecification for learner "
                "presentation.",
                "",
                f"specification_id: {recommendations.specification_id.value}",
                f"student_id: {recommendations.student_id}",
                f"mission_id: {recommendations.mission_id.value}",
                f"educational_rationale: {recommendations.educational_rationale}",
                self.format_lines("recommendations", recommendation_lines),
                "",
                "StudentExperience context (presentation only):",
                f"experience_id: {experience.experience_id.value}",
                f"motivation_tone: {experience.motivation.tone.value}",
                f"motivation_message: {experience.motivation.message}",
                f"presentation_narrative: {experience.presentation_narrative}",
                "",
                "Do not change recommendations, priorities, categories, reasons, "
                "expected outcomes, or educational rationale. Enrich presentation "
                "only.",
            )
        )
        return PromptDocument(system=system, user=user, purpose=PURPOSE)
