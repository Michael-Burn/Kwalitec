"""Shared vendor provider helpers for educational enrichment."""

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


class VendorAIProvider(AIProvider):
    """Base class for HTTP/SDK-backed enrichment providers.

    Concrete vendors differ only by ``name`` and default ``model``. Completion
    is delegated to an injected ``CompletionTransport`` so the enrichment
    contract stays provider-independent and testable without network calls.
    """

    def __init__(
        self,
        *,
        transport: CompletionTransport | None = None,
        model: str | None = None,
    ) -> None:
        self._transport = transport
        self._model = (model or self.default_model).strip()
        if not self._model:
            raise AIProviderError(f"{self.name} model must be non-empty")

    @property
    def default_model(self) -> str:
        raise NotImplementedError

    @property
    def model(self) -> str:
        return self._model

    def complete(self, prompt: PromptDocument) -> EnrichmentResponse:
        if not isinstance(prompt, PromptDocument):
            raise AIProviderError("prompt must be a PromptDocument")
        if self._transport is None:
            raise AIProviderNotConfiguredError(
                f"{self.name} provider has no completion transport configured"
            )
        try:
            raw = self._transport.complete(
                system=prompt.system,
                user=prompt.user,
                model=self._model,
            )
        except AIProviderError:
            raise
        except Exception as exc:  # noqa: BLE001 — vendor transport boundary
            raise AIProviderError(
                f"{self.name} completion failed: {exc}"
            ) from exc
        if not isinstance(raw, str):
            raise AIProviderError(f"{self.name} transport must return a string")
        return parse_enrichment_payload(raw)
