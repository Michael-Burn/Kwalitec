"""EnhancedRecommendation — RecommendationSpecification plus enrichment.

Architecture Source
    AI-001 Educational Enrichment Layer
Concept
    Enhanced Recommendation

Recommendation decisions (ordered recommendations, priorities, reasons,
outcomes, educational rationale) always come from the original
RecommendationSpecification. Enrichment never rewrites those decisions.
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.recommendation.recommendation import Recommendation
from domain.recommendation.recommendation_specification import (
    RecommendationSpecification,
)
from infrastructure.ai.providers.ai_provider import (
    AIProviderError,
    EnrichmentResponse,
)


@dataclass(frozen=True, slots=True)
class EnhancedRecommendation:
    """Immutable enrichment wrapper around a RecommendationSpecification.

    The ``specification`` reference is the Educational OS truth. Enrichment
    fields are presentation-only.
    """

    specification: RecommendationSpecification
    improved_wording: str
    examples: tuple[str, ...]
    analogies: tuple[str, ...]
    adapted_tone: str
    worked_examples: tuple[str, ...]
    revision_tips: tuple[str, ...]
    provider_name: str

    def __post_init__(self) -> None:
        if not isinstance(self.specification, RecommendationSpecification):
            raise AIProviderError(
                "specification must be a RecommendationSpecification"
            )
        object.__setattr__(
            self,
            "improved_wording",
            _require_text(self.improved_wording, "improved_wording"),
        )
        object.__setattr__(
            self,
            "adapted_tone",
            _require_text(self.adapted_tone, "adapted_tone"),
        )
        object.__setattr__(
            self,
            "provider_name",
            _require_text(self.provider_name, "provider_name"),
        )
        for field_name in (
            "examples",
            "analogies",
            "worked_examples",
            "revision_tips",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, tuple):
                raise AIProviderError(f"{field_name} must be a tuple of strings")
            for item in value:
                if not isinstance(item, str) or not item.strip():
                    raise AIProviderError(
                        f"{field_name} must contain non-empty strings"
                    )
            object.__setattr__(
                self,
                field_name,
                tuple(item.strip() for item in value),
            )

    @classmethod
    def from_enrichment(
        cls,
        specification: RecommendationSpecification,
        enrichment: EnrichmentResponse,
        *,
        provider_name: str,
    ) -> EnhancedRecommendation:
        """Map a provider-independent EnrichmentResponse onto recommendations."""
        if not isinstance(enrichment, EnrichmentResponse):
            raise AIProviderError("enrichment must be an EnrichmentResponse")
        return cls(
            specification=specification,
            improved_wording=enrichment.improved_wording,
            examples=enrichment.examples,
            analogies=enrichment.analogies,
            adapted_tone=enrichment.adapted_tone,
            worked_examples=enrichment.worked_examples,
            revision_tips=enrichment.revision_tips,
            provider_name=provider_name,
        )

    # --- Educational OS passthrough (never enrichment-owned) ---------------

    @property
    def recommendations(self) -> tuple[Recommendation, ...]:
        return self.specification.recommendations

    @property
    def educational_rationale(self) -> str:
        return self.specification.educational_rationale

    @property
    def primary(self) -> Recommendation:
        return self.specification.primary

    @property
    def specification_id(self):
        return self.specification.specification_id

    @property
    def student_id(self) -> str:
        return self.specification.student_id

    @property
    def mission_id(self):
        return self.specification.mission_id


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise AIProviderError(f"{field_name} must be a string")
    cleaned = value.strip()
    if not cleaned:
        raise AIProviderError(f"{field_name} must be non-empty")
    return cleaned
