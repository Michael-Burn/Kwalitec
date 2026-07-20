"""Timeout and retry policy for transient AI provider failures."""

from __future__ import annotations

import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturesTimeoutError
from typing import TypeVar

from infrastructure.ai.providers.ai_provider import (
    AIProvider,
    AIProviderError,
    AIProviderNotConfiguredError,
    EnrichmentResponse,
    PromptDocument,
)

T = TypeVar("T")


class TransientProviderError(AIProviderError):
    """Raised for retryable provider failures (network blips, 429/5xx, etc.)."""


class ProviderTimeoutError(AIProviderError):
    """Raised when a provider call exceeds the configured timeout."""


def call_with_timeout(fn: Callable[[], T], timeout_seconds: float) -> T:
    """Execute ``fn`` in a worker thread and fail if it exceeds ``timeout_seconds``."""
    if timeout_seconds <= 0:
        raise ProviderTimeoutError("timeout_seconds must be > 0")
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(fn)
        try:
            return future.result(timeout=timeout_seconds)
        except FuturesTimeoutError as exc:
            future.cancel()
            raise ProviderTimeoutError(
                f"provider call exceeded {timeout_seconds}s"
            ) from exc


def call_with_retry(
    fn: Callable[[], T],
    *,
    max_retries: int,
    backoff_seconds: float,
    is_transient: Callable[[BaseException], bool] | None = None,
    on_retry: Callable[[int, BaseException], None] | None = None,
) -> T:
    """Retry ``fn`` on transient failures with linear backoff."""
    if max_retries < 0:
        raise AIProviderError("max_retries must be >= 0")
    predicate = is_transient or _default_is_transient
    attempt = 0
    while True:
        try:
            return fn()
        except AIProviderNotConfiguredError:
            raise
        except Exception as exc:
            if attempt >= max_retries or not predicate(exc):
                raise
            attempt += 1
            if on_retry is not None:
                on_retry(attempt, exc)
            if backoff_seconds > 0:
                time.sleep(backoff_seconds * attempt)


def _default_is_transient(exc: BaseException) -> bool:
    if isinstance(exc, ProviderTimeoutError | TransientProviderError):
        return True
    if isinstance(exc, AIProviderNotConfiguredError):
        return False
    if isinstance(exc, AIProviderError):
        message = str(exc).casefold()
        return any(
            token in message
            for token in (
                "timeout",
                "temporar",
                "unavailable",
                "429",
                "502",
                "503",
                "504",
            )
        )
    return False


class ResilientAIProvider(AIProvider):
    """Wrap an AIProvider with timeout handling and transient retry policy."""

    def __init__(
        self,
        provider: AIProvider,
        *,
        timeout_seconds: float = 15.0,
        max_retries: int = 2,
        backoff_seconds: float = 0.25,
        on_retry: Callable[[int, BaseException], None] | None = None,
        on_timeout: Callable[[], None] | None = None,
    ) -> None:
        if not isinstance(provider, AIProvider):
            raise AIProviderError("provider must implement AIProvider")
        self._provider = provider
        self._timeout_seconds = timeout_seconds
        self._max_retries = max_retries
        self._backoff_seconds = backoff_seconds
        self._on_retry = on_retry
        self._on_timeout = on_timeout

    @property
    def name(self) -> str:
        return self._provider.name

    @property
    def inner(self) -> AIProvider:
        return self._provider

    def complete(self, prompt: PromptDocument) -> EnrichmentResponse:
        def _once() -> EnrichmentResponse:
            try:
                return call_with_timeout(
                    lambda: self._provider.complete(prompt),
                    self._timeout_seconds,
                )
            except ProviderTimeoutError:
                if self._on_timeout is not None:
                    self._on_timeout()
                raise

        return call_with_retry(
            _once,
            max_retries=self._max_retries,
            backoff_seconds=self._backoff_seconds,
            on_retry=self._on_retry,
        )
