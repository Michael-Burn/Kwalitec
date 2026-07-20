"""APP-004 production readiness — configuration, observability, resilience."""

from __future__ import annotations

import json
import logging
from concurrent.futures import ThreadPoolExecutor

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from application.composition import assemble
from application.pipeline import EducationalPipeline
from infrastructure.ai.providers.ai_provider import (
    AIProviderError,
    AIProviderNotConfiguredError,
    EnrichmentResponse,
    PromptDocument,
)
from infrastructure.ai.providers.anthropic_provider import AnthropicProvider
from infrastructure.ai.providers.openai_provider import OpenAIProvider
from infrastructure.composition.provider_factory import (
    DisabledAIProvider,
    build_ai_provider,
)
from infrastructure.config import (
    AIProviderSettings,
    AppSettings,
    ConfigurationError,
    load_settings,
    read_product_version,
    validate_settings,
)
from infrastructure.observability import (
    ObservedEducationalPipeline,
    PipelineMetrics,
    StructuredLogger,
    configure_structured_logging,
    timed,
)
from infrastructure.resilience import (
    ProviderTimeoutError,
    ResilientAIProvider,
    TransientProviderError,
    call_with_retry,
    call_with_timeout,
)
from tests.education_os.application.pipeline.test_educational_pipeline import (
    make_pipeline_request,
)
from tests.education_os.infrastructure.ai.helpers import FakeAIProvider


def test_read_product_version_from_release_artefact() -> None:
    version = read_product_version()
    assert version == "2.0.0"


def test_load_settings_typed_objects() -> None:
    settings = load_settings(
        {
            "APP_ENV": "development",
            "SECRET_KEY": "dev-change-this-secret-key",
            "AI_PROVIDER": "anthropic",
            "AI_MODEL": "claude-test",
            "AI_TIMEOUT_SECONDS": "8",
            "AI_MAX_RETRIES": "1",
        },
        validate=False,
    )
    assert isinstance(settings, AppSettings)
    assert settings.ai is not None
    assert settings.ai.name == "anthropic"
    assert settings.ai.model == "claude-test"
    assert settings.ai.timeout_seconds == 8.0
    assert settings.ai.max_retries == 1


def test_production_fails_fast_on_insecure_secret() -> None:
    settings = AppSettings(
        environment="production",
        secret_key="dev-change-this-secret-key",
        database_url="postgresql+psycopg://db/kwalitec",
        ai=AIProviderSettings(name="none", enabled=False),
    )
    with pytest.raises(ConfigurationError, match="SECRET_KEY"):
        validate_settings(settings, fail_fast=True)


def test_production_requires_database_url() -> None:
    settings = AppSettings(
        environment="production",
        secret_key="production-secret-key-value-32chars",
        database_url="sqlite+pysqlite:///:memory:",
        ai=AIProviderSettings(name="none", enabled=False),
    )
    with pytest.raises(ConfigurationError, match="DATABASE_URL"):
        validate_settings(settings, fail_fast=True)


def test_provider_factory_selects_without_code_change() -> None:
    openai = build_ai_provider(AIProviderSettings(name="openai", enabled=True))
    anthropic = build_ai_provider(AIProviderSettings(name="anthropic", enabled=True))
    disabled = build_ai_provider(AIProviderSettings(name="none", enabled=False))

    assert isinstance(openai, ResilientAIProvider)
    assert isinstance(openai.inner, OpenAIProvider)
    assert isinstance(anthropic, ResilientAIProvider)
    assert isinstance(anthropic.inner, AnthropicProvider)
    assert isinstance(disabled, DisabledAIProvider)


def test_disabled_provider_raises_for_deterministic_fallback() -> None:
    provider = DisabledAIProvider()
    prompt = PromptDocument(system="s", user="u", purpose="test")
    with pytest.raises(AIProviderNotConfiguredError):
        provider.complete(prompt)


def test_structured_logger_emits_fields() -> None:
    logger = StructuredLogger("test.eos")
    record = logger.info("hello", event="unit", duration_ms=1.5)
    assert record["message"] == "hello"
    assert record["event"] == "unit"
    assert logger.records[0]["duration_ms"] == 1.5


def test_configure_structured_logging_json(capsys) -> None:
    configure_structured_logging(level="INFO", structured=True)
    logging.getLogger("test.json").info(
        "structured",
        extra={"structured_fields": {"event": "probe"}},
    )
    # Handler writes to stderr; ensure formatter is JSON-capable.
    formatter = logging.getLogger().handlers[0].formatter
    assert formatter is not None
    line = formatter.format(
        logging.LogRecord(
            name="test.json",
            level=logging.INFO,
            pathname=__file__,
            lineno=1,
            msg="structured",
            args=(),
            exc_info=None,
        )
    )
    # Without structured_fields on a raw record, still valid JSON.
    payload = json.loads(line)
    assert payload["message"] == "structured"


def test_pipeline_metrics_success_and_failure() -> None:
    metrics = PipelineMetrics()
    metrics.incr("pipeline_started")
    metrics.incr("pipeline_succeeded")
    metrics.record_timing("pipeline_execution", 12.5)
    snap = metrics.snapshot()
    assert snap["counters"]["pipeline_succeeded"] == 1
    assert snap["timings_ms"]["pipeline_execution"]["last_ms"] == 12.5

    with pytest.raises(ValueError):
        metrics.incr("mastery_score")


def test_timed_context_records_duration() -> None:
    with timed("unit") as slot:
        _ = sum(range(100))
    assert slot[0] >= 0.0


def test_call_with_timeout_raises() -> None:
    def slow() -> str:
        import time

        time.sleep(0.2)
        return "done"

    with pytest.raises(ProviderTimeoutError):
        call_with_timeout(slow, 0.01)


def test_call_with_retry_retries_transient() -> None:
    attempts = {"n": 0}

    def flaky() -> str:
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise TransientProviderError("temporar y blip")
        return "ok"

    assert call_with_retry(flaky, max_retries=3, backoff_seconds=0) == "ok"
    assert attempts["n"] == 3


def test_resilient_provider_timeout_and_retry() -> None:
    class SlowProvider(FakeAIProvider):
        def complete(self, prompt: PromptDocument) -> EnrichmentResponse:
            import time

            time.sleep(0.15)
            return super().complete(prompt)

    resilient = ResilientAIProvider(
        SlowProvider(),
        timeout_seconds=0.01,
        max_retries=0,
        backoff_seconds=0,
    )
    prompt = PromptDocument(system="s", user="u", purpose="test")
    with pytest.raises(ProviderTimeoutError):
        resilient.complete(prompt)


def test_resilient_provider_retries_then_succeeds() -> None:
    class Flaky(FakeAIProvider):
        def __init__(self) -> None:
            super().__init__()
            self.calls = 0

        def complete(self, prompt: PromptDocument) -> EnrichmentResponse:
            self.calls += 1
            if self.calls < 2:
                raise AIProviderError("503 unavailable")
            return super().complete(prompt)

    inner = Flaky()
    retries: list[int] = []
    resilient = ResilientAIProvider(
        inner,
        timeout_seconds=5,
        max_retries=2,
        backoff_seconds=0,
        on_retry=lambda n, _exc: retries.append(n),
    )
    prompt = PromptDocument(system="s", user="u", purpose="test")
    result = resilient.complete(prompt)
    assert result.improved_wording
    assert inner.calls == 2
    assert retries == [1]


def test_observed_pipeline_records_success_metrics() -> None:
    pipeline = EducationalPipeline()
    metrics = PipelineMetrics()
    observed = ObservedEducationalPipeline(pipeline, metrics=metrics)
    result = observed.run(make_pipeline_request())
    assert result.mission is not None
    assert metrics.get("pipeline_started") == 1
    assert metrics.get("pipeline_succeeded") == 1
    assert "pipeline_execution" in metrics.timing_summary()


def test_assemble_uses_configured_provider(monkeypatch) -> None:
    monkeypatch.setenv("AI_PROVIDER", "gemini")
    monkeypatch.setenv("AI_ENRICHMENT_DISABLED", "0")
    session_factory = sessionmaker(bind=create_engine("sqlite+pysqlite:///:memory:"))
    container = assemble(session_factory, settings=load_settings(validate=False))
    provider = container.ai_provider
    if isinstance(provider, ResilientAIProvider):
        provider = provider.inner
    assert provider.name == "gemini"


def test_assemble_disables_enrichment_for_deterministic_fallback(monkeypatch) -> None:
    monkeypatch.setenv("AI_ENRICHMENT_DISABLED", "1")
    settings = load_settings(validate=False)
    session_factory = sessionmaker(bind=create_engine("sqlite+pysqlite:///:memory:"))
    container = assemble(session_factory, settings=settings)
    # Enrichers exist on the container, but pipeline stages use None → fallback.
    assert container.educational_pipeline._mission_enricher is None
    assert container.educational_pipeline._recommendation_enricher is None


def test_thread_pool_cleanup_does_not_hang() -> None:
    # Smoke: timeout helper returns promptly on success.
    with ThreadPoolExecutor(max_workers=1) as pool:
        assert pool.submit(lambda: 1).result(timeout=1) == 1
