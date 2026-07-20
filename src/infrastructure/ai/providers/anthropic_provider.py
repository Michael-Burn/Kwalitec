"""Anthropic enrichment provider.

Architecture Source
    AI-001 Educational Enrichment Layer
Concept
    Anthropic Provider
"""

from __future__ import annotations

from infrastructure.ai.providers._vendor import VendorAIProvider


class AnthropicProvider(VendorAIProvider):
    """Anthropic-backed presentation enrichment provider.

    Requires an injected ``CompletionTransport``. Does not make educational
    decisions; maps vendor completions into EnrichmentResponse only.
    """

    @property
    def name(self) -> str:
        return "anthropic"

    @property
    def default_model(self) -> str:
        return "claude-3-5-haiku-latest"
