"""EnhancedMission — MissionSpecification plus presentation enrichment.

Architecture Source
    AI-001 Educational Enrichment Layer
Concept
    Enhanced Mission

Educational fields (objective, priority, duration, sequence, educational
rationale) are always taken from the original MissionSpecification. Enrichment
never rewrites those decisions.
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.mission_generation.mission_duration import MissionDuration
from domain.mission_generation.mission_objective import MissionObjective
from domain.mission_generation.mission_priority import MissionPriority
from domain.mission_generation.mission_sequence import MissionSequence
from domain.mission_generation.mission_specification import MissionSpecification
from infrastructure.ai.providers.ai_provider import (
    AIProviderError,
    EnrichmentResponse,
)


@dataclass(frozen=True, slots=True)
class EnhancedMission:
    """Immutable enrichment wrapper around a MissionSpecification.

    The ``specification`` reference is the Educational OS truth. Enrichment
    fields are presentation-only.
    """

    specification: MissionSpecification
    improved_wording: str
    examples: tuple[str, ...]
    analogies: tuple[str, ...]
    adapted_tone: str
    worked_examples: tuple[str, ...]
    revision_tips: tuple[str, ...]
    provider_name: str

    def __post_init__(self) -> None:
        if not isinstance(self.specification, MissionSpecification):
            raise AIProviderError("specification must be a MissionSpecification")
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
            cleaned = tuple(
                item.strip()
                for item in value
                if isinstance(item, str) and item.strip()
            )
            if len(cleaned) != len(value):
                # Reject non-string / blank entries rather than silently drop.
                for item in value:
                    if not isinstance(item, str) or not item.strip():
                        raise AIProviderError(
                            f"{field_name} must contain non-empty strings"
                        )
            object.__setattr__(self, field_name, cleaned)

    @classmethod
    def from_enrichment(
        cls,
        specification: MissionSpecification,
        enrichment: EnrichmentResponse,
        *,
        provider_name: str,
    ) -> EnhancedMission:
        """Map a provider-independent EnrichmentResponse onto a mission."""
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
    def objective(self) -> MissionObjective:
        return self.specification.objective

    @property
    def priority(self) -> MissionPriority:
        return self.specification.priority

    @property
    def duration(self) -> MissionDuration:
        return self.specification.duration

    @property
    def sequence(self) -> MissionSequence:
        return self.specification.sequence

    @property
    def educational_rationale(self) -> str:
        return self.specification.educational_rationale

    @property
    def mission_id(self):
        return self.specification.mission_id

    @property
    def student_id(self) -> str:
        return self.specification.student_id


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise AIProviderError(f"{field_name} must be a string")
    cleaned = value.strip()
    if not cleaned:
        raise AIProviderError(f"{field_name} must be non-empty")
    return cleaned
