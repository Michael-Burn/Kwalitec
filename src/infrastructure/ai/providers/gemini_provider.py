"""Gemini enrichment provider.

Architecture Source
    AI-001 Educational Enrichment Layer
Concept
    Gemini Provider
"""

from __future__ import annotations

from infrastructure.ai.providers._vendor import VendorAIProvider


class GeminiProvider(VendorAIProvider):
    """Gemini-backed presentation enrichment provider.

    Requires an injected ``CompletionTransport``. Does not make educational
    decisions; maps vendor completions into EnrichmentResponse only.
    """

    @property
    def name(self) -> str:
        return "gemini"

    @property
    def default_model(self) -> str:
        return "gemini-2.0-flash"
