"""Construct AI providers from typed configuration (composition-root helper).

Architecture Source
    APP-004 Production Readiness & Version 2 Release

Lives under ``infrastructure.composition`` so production provider constructors
remain inside the composition root (APP-003). Provider *selection* is driven by
``AIProviderSettings`` — swap vendors via environment without editing callers.
"""

from __future__ import annotations

from infrastructure.ai.providers.ai_provider import (
    AIProvider,
    AIProviderError,
    AIProviderNotConfiguredError,
    CompletionTransport,
    EnrichmentResponse,
    PromptDocument,
)
from infrastructure.ai.providers.anthropic_provider import AnthropicProvider
from infrastructure.ai.providers.gemini_provider import GeminiProvider
from infrastructure.ai.providers.openai_provider import OpenAIProvider
from infrastructure.config.settings import AIProviderSettings, ConfigurationError
from infrastructure.resilience.retry import ResilientAIProvider


class DisabledAIProvider(AIProvider):
    """Provider used when enrichment is disabled via configuration.

    Completions raise so enrichers / pipeline fall back to deterministic views.
    """

    @property
    def name(self) -> str:
        return "none"

    def complete(self, prompt: PromptDocument) -> EnrichmentResponse:
        raise AIProviderNotConfiguredError("AI enrichment is disabled by configuration")


def build_ai_provider(
    settings: AIProviderSettings,
    *,
    transport: CompletionTransport | None = None,
) -> AIProvider:
    """Build an AI provider from settings, wrapping with timeout/retry policy.

    Provider name is selected by ``AI_PROVIDER`` / ``EOS_AI_PROVIDER`` without
    editing composition-root callers. Secrets come only from settings.

    Args:
        settings: Typed provider settings.
        transport: Optional completion transport (tests / SDK adapters).

    Returns:
        Configured ``AIProvider`` (possibly resilient wrapper).

    Raises:
        ConfigurationError: When the provider name is unknown.
    """
    if not settings.enabled or settings.name == "none":
        return DisabledAIProvider()

    provider = _construct_vendor(settings, transport=transport)
    return ResilientAIProvider(
        provider,
        timeout_seconds=settings.timeout_seconds,
        max_retries=settings.max_retries,
        backoff_seconds=settings.retry_backoff_seconds,
    )


def _construct_vendor(
    settings: AIProviderSettings,
    *,
    transport: CompletionTransport | None,
) -> AIProvider:
    model = settings.model
    # API keys remain on settings for transport adapters; vendor classes accept
    # only transport + model so secrets never appear in provider source.
    _ = settings.api_key
    try:
        if settings.name == "openai":
            return OpenAIProvider(transport=transport, model=model)
        if settings.name == "anthropic":
            return AnthropicProvider(transport=transport, model=model)
        if settings.name == "gemini":
            return GeminiProvider(transport=transport, model=model)
    except AIProviderError as exc:
        raise ConfigurationError(str(exc)) from exc
    raise ConfigurationError(f"unsupported AI provider: {settings.name!r}")
