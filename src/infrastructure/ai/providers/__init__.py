"""AI provider package — vendor adapters for educational enrichment."""

from __future__ import annotations

from infrastructure.ai.providers.ai_provider import (
    AIProvider,
    AIProviderError,
    AIProviderNotConfiguredError,
    CompletionTransport,
    EnrichmentResponse,
    PromptDocument,
    parse_enrichment_payload,
)
from infrastructure.ai.providers.anthropic_provider import AnthropicProvider
from infrastructure.ai.providers.gemini_provider import GeminiProvider
from infrastructure.ai.providers.openai_provider import OpenAIProvider

__all__ = [
    "AIProvider",
    "AIProviderError",
    "AIProviderNotConfiguredError",
    "AnthropicProvider",
    "CompletionTransport",
    "EnrichmentResponse",
    "GeminiProvider",
    "OpenAIProvider",
    "PromptDocument",
    "parse_enrichment_payload",
]
