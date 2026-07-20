"""Typed application settings loaded from the environment.

Architecture Source
    APP-004 Production Readiness & Version 2 Release
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
VERSION_FILE = REPO_ROOT / "VERSION"

# Insecure defaults that must never ship as production secrets.
_INSECURE_SECRET_KEYS = frozenset(
    {
        "",
        "dev-change-this-secret-key",
        "change-this-secret-key",
        "changeme",
        "secret",
    }
)

_VALID_ENVIRONMENTS = frozenset({"development", "production", "testing"})
_VALID_AI_PROVIDERS = frozenset({"openai", "anthropic", "gemini", "none"})


class ConfigurationError(ValueError):
    """Raised when configuration is missing or unsafe for the target environment."""


@dataclass(frozen=True, slots=True)
class AIProviderSettings:
    """Provider selection and resilience knobs — no vendor SDKs required at import."""

    name: str = "openai"
    model: str | None = None
    api_key: str | None = None
    enabled: bool = True
    timeout_seconds: float = 15.0
    max_retries: int = 2
    retry_backoff_seconds: float = 0.25

    def __post_init__(self) -> None:
        name = (self.name or "").strip().lower()
        if name not in _VALID_AI_PROVIDERS:
            raise ConfigurationError(
                "AI_PROVIDER must be one of "
                f"{sorted(_VALID_AI_PROVIDERS)}; got {self.name!r}"
            )
        object.__setattr__(self, "name", name)
        if self.timeout_seconds <= 0:
            raise ConfigurationError("AI_TIMEOUT_SECONDS must be > 0")
        if self.max_retries < 0:
            raise ConfigurationError("AI_MAX_RETRIES must be >= 0")
        if self.retry_backoff_seconds < 0:
            raise ConfigurationError("AI_RETRY_BACKOFF_SECONDS must be >= 0")


@dataclass(frozen=True, slots=True)
class AppSettings:
    """Immutable typed configuration for the Educational Operating System runtime."""

    environment: str = "development"
    secret_key: str = "dev-change-this-secret-key"
    database_url: str = "sqlite+pysqlite:///:memory:"
    log_level: str = "INFO"
    structured_logging: bool = True
    ai: AIProviderSettings | None = None
    version: str = "2.0.0"
    testing: bool = False

    def __post_init__(self) -> None:
        env = (self.environment or "").strip().lower()
        if env not in _VALID_ENVIRONMENTS:
            raise ConfigurationError(
                "APP_ENV must be one of "
                f"{sorted(_VALID_ENVIRONMENTS)}; got {self.environment!r}"
            )
        object.__setattr__(self, "environment", env)
        if self.ai is None:
            object.__setattr__(self, "ai", AIProviderSettings())
        object.__setattr__(self, "log_level", (self.log_level or "INFO").upper())
        object.__setattr__(self, "version", (self.version or "").strip() or "2.0.0")

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def is_testing(self) -> bool:
        return self.testing or self.environment == "testing"


def read_product_version(*, default: str = "2.0.0") -> str:
    """Read the product version from the VERSION release artefact."""
    try:
        text = VERSION_FILE.read_text(encoding="utf-8").strip()
    except OSError:
        return default
    return text or default


def load_settings(
    environ: Mapping[str, str] | None = None,
    *,
    validate: bool = True,
) -> AppSettings:
    """Load typed settings from the process environment (or a mapping).

    Args:
        environ: Optional mapping; defaults to ``os.environ``.
        validate: When True, fail-fast on configuration errors for the environment.

    Returns:
        Immutable ``AppSettings``.

    Raises:
        ConfigurationError: When required values are missing or unsafe.
    """
    env = environ if environ is not None else os.environ
    environment = _first(env, "APP_ENV", "FLASK_ENV") or "development"
    testing_flag = _truthy(env.get("TESTING", ""))
    if testing_flag and environment == "development":
        environment = "testing"

    ai_name = (env.get("AI_PROVIDER") or env.get("EOS_AI_PROVIDER") or "openai").strip()
    ai_enabled = not _truthy(env.get("AI_ENRICHMENT_DISABLED", ""))
    if ai_name.lower() == "none":
        ai_enabled = False

    api_key = _first(
        env,
        "AI_API_KEY",
        "EOS_AI_API_KEY",
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "GEMINI_API_KEY",
        "GOOGLE_API_KEY",
    )

    settings = AppSettings(
        environment=environment,
        secret_key=env.get("SECRET_KEY", "dev-change-this-secret-key"),
        database_url=(
            _first(env, "EOS_DATABASE_URL", "DATABASE_URL")
            or "sqlite+pysqlite:///:memory:"
        ),
        log_level=env.get("LOG_LEVEL", "INFO"),
        structured_logging=_truthy(env.get("STRUCTURED_LOGGING", "1")),
        ai=AIProviderSettings(
            name=ai_name,
            model=_first(env, "AI_MODEL", "EOS_AI_MODEL"),
            api_key=api_key,
            enabled=ai_enabled,
            timeout_seconds=_float(env, "AI_TIMEOUT_SECONDS", 15.0),
            max_retries=_int(env, "AI_MAX_RETRIES", 2),
            retry_backoff_seconds=_float(env, "AI_RETRY_BACKOFF_SECONDS", 0.25),
        ),
        version=env.get("APP_VERSION") or read_product_version(),
        testing=testing_flag,
    )

    if validate:
        validate_settings(settings, fail_fast=True)
    return settings


def validate_settings(
    settings: AppSettings,
    *,
    fail_fast: bool = True,
) -> tuple[str, ...]:
    """Validate settings for the target environment.

    Production fails fast on missing secrets and insecure defaults.
    Development / testing collect warnings but do not raise unless ``fail_fast``
    and the environment is production.
    """
    errors: list[str] = []

    if settings.is_production:
        if settings.secret_key.strip().lower() in _INSECURE_SECRET_KEYS:
            errors.append(
                "SECRET_KEY must be set to a strong non-default value in production"
            )
        if settings.database_url.startswith("sqlite+pysqlite:///:memory:"):
            errors.append(
                "DATABASE_URL / EOS_DATABASE_URL must be set in production"
            )
        if settings.ai and settings.ai.enabled and settings.ai.name != "none":
            if not (settings.ai.api_key or "").strip():
                errors.append(
                    "AI_API_KEY (or vendor-specific key) is required when "
                    f"AI_PROVIDER={settings.ai.name} is enabled in production"
                )

    if settings.ai and settings.ai.enabled and settings.ai.name == "none":
        errors.append(
            "AI_PROVIDER=none cannot be enabled; set AI_ENRICHMENT_DISABLED=1"
        )

    if fail_fast and errors and settings.is_production:
        raise ConfigurationError("; ".join(errors))
    return tuple(errors)


def _first(env: Mapping[str, str], *keys: str) -> str | None:
    for key in keys:
        value = env.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return None


def _truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _float(env: Mapping[str, str], key: str, default: float) -> float:
    raw = env.get(key)
    if raw is None or not str(raw).strip():
        return default
    try:
        return float(raw)
    except ValueError as exc:
        raise ConfigurationError(f"{key} must be a number") from exc


def _int(env: Mapping[str, str], key: str, default: int) -> int:
    raw = env.get(key)
    if raw is None or not str(raw).strip():
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise ConfigurationError(f"{key} must be an integer") from exc
