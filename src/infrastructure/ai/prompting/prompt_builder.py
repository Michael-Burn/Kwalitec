"""PromptBuilder — shared deterministic enrichment prompt helpers.

Architecture Source
    AI-001 Educational Enrichment Layer
Concept
    Prompt Builder
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from infrastructure.ai.providers.ai_provider import PromptDocument

# Fixed constraint block — identical across all enrichment prompts.
ENRICHMENT_CONSTRAINTS: str = (
    "You enrich educational presentation only.\n"
    "You MUST NOT change objective, priority, duration, sequence, or "
    "educational rationale.\n"
    "You MUST NOT make educational decisions.\n"
    "You MUST NOT rewrite the mission or change recommendations.\n"
    "You may only improve wording, generate examples, create analogies, "
    "adapt tone, produce worked examples, and generate revision tips.\n"
    "Respond with a single JSON object containing keys: "
    "improved_wording (string), examples (array of strings), "
    "analogies (array of strings), adapted_tone (string), "
    "worked_examples (array of strings), revision_tips (array of strings)."
)


class PromptBuilder(ABC):
    """Base builder for deterministic enrichment prompts."""

    @abstractmethod
    def build(self, *args: object, **kwargs: object) -> PromptDocument:
        """Build a PromptDocument from Educational OS outputs."""

    @staticmethod
    def system_preamble(*, role: str) -> str:
        """Return the shared system instructions for enrichment."""
        cleaned = role.strip()
        return (
            f"You are a presentation enrichment assistant for {cleaned}.\n"
            f"{ENRICHMENT_CONSTRAINTS}"
        )

    @staticmethod
    def format_lines(title: str, items: tuple[str, ...] | list[str]) -> str:
        """Render a titled bullet list deterministically."""
        if not items:
            return f"{title}:\n- (none)"
        body = "\n".join(f"- {item}" for item in items)
        return f"{title}:\n{body}"
