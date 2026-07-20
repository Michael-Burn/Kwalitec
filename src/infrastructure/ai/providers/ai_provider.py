"""AIProvider — vendor-neutral contract for educational enrichment.

Architecture Source
    AI-001 Educational Enrichment Layer
Concept
    AI Provider Abstraction

Providers produce presentation enrichment only. Educational decisions remain
owned by the Educational Operating System.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol


class AIProviderError(Exception):
    """Raised when an AI provider fails to produce enrichment."""


class AIProviderNotConfiguredError(AIProviderError):
    """Raised when a provider has no completion transport configured."""


@dataclass(frozen=True, slots=True)
class PromptDocument:
    """Immutable prompt payload sent to an AI provider.

    Prompts are built deterministically from Educational OS outputs. They
    instruct the model to enrich presentation only.
    """

    system: str
    user: str
    purpose: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "system", _require_text(self.system, "system"))
        object.__setattr__(self, "user", _require_text(self.user, "user"))
        object.__setattr__(self, "purpose", _require_text(self.purpose, "purpose"))


@dataclass(frozen=True, slots=True)
class EnrichmentResponse:
    """Provider-independent enrichment payload.

    All vendors must map their raw completions into this shape so enrichers
    and Enhanced* models remain provider-agnostic.
    """

    improved_wording: str
    examples: tuple[str, ...]
    analogies: tuple[str, ...]
    adapted_tone: str
    worked_examples: tuple[str, ...]
    revision_tips: tuple[str, ...]

    def __post_init__(self) -> None:
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
        for field_name in (
            "examples",
            "analogies",
            "worked_examples",
            "revision_tips",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, tuple):
                raise AIProviderError(f"{field_name} must be a tuple of strings")
            cleaned: list[str] = []
            for item in value:
                if not isinstance(item, str):
                    raise AIProviderError(f"{field_name} must contain strings")
                text = item.strip()
                if text:
                    cleaned.append(text)
            object.__setattr__(self, field_name, tuple(cleaned))


class CompletionTransport(Protocol):
    """Injectable completion backend for vendor providers.

    Infrastructure supplies HTTP/SDK transports. Tests inject fakes. Providers
    must not embed educational decision logic in transports.
    """

    def complete(self, *, system: str, user: str, model: str) -> str:
        """Return raw model text (preferably JSON matching EnrichmentResponse)."""


class AIProvider(ABC):
    """Abstract AI provider for educational presentation enrichment.

    Implementations may call external vendors. They must never diagnose,
    prioritise, select strategies, rewrite missions, or change recommendations.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Stable provider identifier (e.g. ``openai``, ``anthropic``)."""

    @abstractmethod
    def complete(self, prompt: PromptDocument) -> EnrichmentResponse:
        """Produce provider-independent enrichment from a prompt document.

        Args:
            prompt: Deterministic enrichment prompt.

        Returns:
            Structured enrichment payload shared across all vendors.

        Raises:
            AIProviderError: When completion or parsing fails.
            AIProviderNotConfiguredError: When no transport is available.
        """


def parse_enrichment_payload(raw: str) -> EnrichmentResponse:
    """Parse vendor-agnostic JSON (or fenced JSON) into EnrichmentResponse.

    Args:
        raw: Model completion text.

    Returns:
        Validated EnrichmentResponse.

    Raises:
        AIProviderError: When the payload is missing, invalid JSON, or incomplete.
    """
    if raw is None:
        raise AIProviderError("enrichment payload is missing")
    text = raw.strip()
    if not text:
        raise AIProviderError("enrichment payload is empty")

    candidate = _extract_json_object(text)
    try:
        data = json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise AIProviderError("enrichment payload is not valid JSON") from exc

    if not isinstance(data, dict):
        raise AIProviderError("enrichment payload must be a JSON object")

    return EnrichmentResponse(
        improved_wording=_require_string(data, "improved_wording"),
        adapted_tone=_require_string(data, "adapted_tone"),
        examples=_require_string_list(data, "examples"),
        analogies=_require_string_list(data, "analogies"),
        worked_examples=_require_string_list(data, "worked_examples"),
        revision_tips=_require_string_list(data, "revision_tips"),
    )


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise AIProviderError(f"{field_name} must be a string")
    cleaned = value.strip()
    if not cleaned:
        raise AIProviderError(f"{field_name} must be non-empty")
    return cleaned


def _extract_json_object(text: str) -> str:
    """Prefer a fenced ```json block; otherwise the first {...} span."""
    lowered = text.casefold()
    fence = "```json"
    if fence in lowered:
        start = lowered.index(fence) + len(fence)
        end = text.find("```", start)
        if end != -1:
            return text[start:end].strip()
    begin = text.find("{")
    finish = text.rfind("}")
    if begin != -1 and finish != -1 and finish > begin:
        return text[begin : finish + 1]
    return text


def _require_string(data: dict[str, Any], key: str) -> str:
    if key not in data:
        raise AIProviderError(f"enrichment payload missing field: {key}")
    value = data[key]
    if not isinstance(value, str):
        raise AIProviderError(f"enrichment field {key} must be a string")
    cleaned = value.strip()
    if not cleaned:
        raise AIProviderError(f"enrichment field {key} must be non-empty")
    return cleaned


def _require_string_list(data: dict[str, Any], key: str) -> tuple[str, ...]:
    if key not in data:
        raise AIProviderError(f"enrichment payload missing field: {key}")
    value = data[key]
    if not isinstance(value, list):
        raise AIProviderError(f"enrichment field {key} must be a list")
    items: list[str] = []
    for item in value:
        if not isinstance(item, str):
            raise AIProviderError(f"enrichment field {key} must contain strings")
        cleaned = item.strip()
        if cleaned:
            items.append(cleaned)
    return tuple(items)
