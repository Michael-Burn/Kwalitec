"""Typed configuration and startup validation for the Educational OS.

Architecture Source
    APP-004 Production Readiness & Version 2 Release

Secrets are loaded only from environment / configuration objects.
No educational decisions live here.
"""

from __future__ import annotations

from infrastructure.config.settings import (
    AIProviderSettings,
    AppSettings,
    ConfigurationError,
    load_settings,
    read_product_version,
    validate_settings,
)

__all__ = [
    "AIProviderSettings",
    "AppSettings",
    "ConfigurationError",
    "load_settings",
    "read_product_version",
    "validate_settings",
]
