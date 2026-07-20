"""Shared helpers for AI-001 Educational Enrichment Layer tests."""

from __future__ import annotations

import json

from domain.mission_generation import MissionSpecification
from domain.recommendation import RecommendationSpecification
from domain.student_experience import StudentExperience
from infrastructure.ai.providers.ai_provider import (
    AIProvider,
    EnrichmentResponse,
    PromptDocument,
)
from tests.domain.student_experience.experience_engine_helpers import (
    generate_experience,
    make_experience_inputs,
)


def sample_enrichment_payload(**overrides: object) -> dict[str, object]:
    """Canonical provider-independent enrichment JSON."""
    payload: dict[str, object] = {
        "improved_wording": (
            "Clarify the core idea with a calm, step-by-step explanation."
        ),
        "examples": (
            "Work a short numerical example before the full exercise.",
            "Restate the definition in your own words.",
        ),
        "analogies": (
            "Think of the rule as a checklist you apply in the same order.",
        ),
        "adapted_tone": "steady and encouraging",
        "worked_examples": (
            "Given inputs A and B, apply the rule, then check the boundary case.",
        ),
        "revision_tips": (
            "Revisit the definition after one successful attempt.",
            "Compare today's example with yesterday's mistake pattern.",
        ),
    }
    payload.update(overrides)
    return payload


def sample_enrichment_json(**overrides: object) -> str:
    return json.dumps(sample_enrichment_payload(**overrides))


def sample_enrichment_response(**overrides: object) -> EnrichmentResponse:
    data = sample_enrichment_payload(**overrides)
    return EnrichmentResponse(
        improved_wording=str(data["improved_wording"]),
        examples=tuple(data["examples"]),  # type: ignore[arg-type]
        analogies=tuple(data["analogies"]),  # type: ignore[arg-type]
        adapted_tone=str(data["adapted_tone"]),
        worked_examples=tuple(data["worked_examples"]),  # type: ignore[arg-type]
        revision_tips=tuple(data["revision_tips"]),  # type: ignore[arg-type]
    )


class FakeCompletionTransport:
    """Deterministic transport returning fixed enrichment JSON."""

    def __init__(self, payload: str | None = None) -> None:
        self.payload = payload or sample_enrichment_json()
        self.calls: list[dict[str, str]] = []

    def complete(self, *, system: str, user: str, model: str) -> str:
        self.calls.append({"system": system, "user": user, "model": model})
        return self.payload


class FakeAIProvider(AIProvider):
    """In-memory provider for contract and enrichment tests."""

    def __init__(
        self,
        *,
        name: str = "fake",
        response: EnrichmentResponse | None = None,
    ) -> None:
        self._name = name
        self._response = response or sample_enrichment_response()
        self.prompts: list[PromptDocument] = []

    @property
    def name(self) -> str:
        return self._name

    def complete(self, prompt: PromptDocument) -> EnrichmentResponse:
        self.prompts.append(prompt)
        return self._response


def aligned_enrichment_inputs() -> tuple[
    MissionSpecification,
    RecommendationSpecification,
    StudentExperience,
]:
    mission, _plan, _progress, recommendations = make_experience_inputs()
    experience = generate_experience(
        mission=mission,
        study_plan=_plan,
        progress=_progress,
        recommendations=recommendations,
    )
    return mission, recommendations, experience
