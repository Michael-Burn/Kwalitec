"""Provider contract tests for AI-001 Educational Enrichment Layer."""

from __future__ import annotations

import pytest

from infrastructure.ai.providers.ai_provider import (
    AIProvider,
    AIProviderError,
    AIProviderNotConfiguredError,
    EnrichmentResponse,
    PromptDocument,
    parse_enrichment_payload,
)
from infrastructure.ai.providers.anthropic_provider import AnthropicProvider
from infrastructure.ai.providers.gemini_provider import GeminiProvider
from infrastructure.ai.providers.openai_provider import OpenAIProvider
from tests.education_os.infrastructure.ai.helpers import (
    FakeAIProvider,
    FakeCompletionTransport,
    sample_enrichment_json,
    sample_enrichment_response,
)

PROVIDER_TYPES = (OpenAIProvider, AnthropicProvider, GeminiProvider)


def _prompt() -> PromptDocument:
    return PromptDocument(
        system="Enrich presentation only.",
        user="Improve wording for this learner-facing summary.",
        purpose="mission_enrichment",
    )


@pytest.mark.parametrize("provider_cls", PROVIDER_TYPES)
def test_vendor_providers_implement_ai_provider_contract(provider_cls) -> None:
    transport = FakeCompletionTransport()
    provider = provider_cls(transport=transport)
    assert isinstance(provider, AIProvider)
    assert provider.name
    result = provider.complete(_prompt())
    assert isinstance(result, EnrichmentResponse)
    assert result.improved_wording
    assert result.adapted_tone
    assert transport.calls
    assert transport.calls[0]["model"] == provider.model


@pytest.mark.parametrize("provider_cls", PROVIDER_TYPES)
def test_vendor_providers_require_transport(provider_cls) -> None:
    provider = provider_cls()
    with pytest.raises(AIProviderNotConfiguredError):
        provider.complete(_prompt())


@pytest.mark.parametrize("provider_cls", PROVIDER_TYPES)
def test_vendor_providers_share_enrichment_shape(provider_cls) -> None:
    expected = sample_enrichment_response()
    transport = FakeCompletionTransport(sample_enrichment_json())
    provider = provider_cls(transport=transport)
    result = provider.complete(_prompt())
    assert result == expected


def test_fake_provider_contract() -> None:
    provider: AIProvider = FakeAIProvider()
    result = provider.complete(_prompt())
    assert provider.name == "fake"
    assert isinstance(result, EnrichmentResponse)


def test_parse_enrichment_payload_accepts_fenced_json() -> None:
    raw = "Here is enrichment:\n```json\n" + sample_enrichment_json() + "\n```\n"
    result = parse_enrichment_payload(raw)
    assert result.improved_wording.startswith("Clarify")


def test_parse_enrichment_payload_rejects_incomplete_json() -> None:
    with pytest.raises(AIProviderError):
        parse_enrichment_payload('{"improved_wording": "only"}')


def test_provider_names_are_distinct() -> None:
    names = {cls(transport=FakeCompletionTransport()).name for cls in PROVIDER_TYPES}
    assert names == {"openai", "anthropic", "gemini"}
