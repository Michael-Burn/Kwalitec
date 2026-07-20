"""OpenAI enrichment provider.

Architecture Source
    AI-001 Educational Enrichment Layer
Concept
    OpenAI Provider
"""

from __future__ import annotations

from infrastructure.ai.providers._vendor import VendorAIProvider


class OpenAIProvider(VendorAIProvider):
    """OpenAI-backed presentation enrichment provider.

    Requires an injected ``CompletionTransport``. Does not make educational
    decisions; maps vendor completions into EnrichmentResponse only.
    """

    @property
    def name(self) -> str:
        return "openai"

    @property
    def default_model(self) -> str:
        return "gpt-4o-mini"
