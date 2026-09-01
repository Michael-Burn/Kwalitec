"""Single product version source of truth (PTP-005 / QS-001 / IAHF-005)."""

from __future__ import annotations

import os
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from app.brand_identity import PRODUCT_DESCRIPTOR

# Canonical student-facing product version — keep in sync with VERSION / pyproject.toml.
_FALLBACK_VERSION = "2.0.0-beta.1"
_VERSION_FILE = Path(__file__).resolve().parents[1] / "VERSION"


def _read_app_version() -> str:
    """Prefer repository VERSION so pre-release labels stay human-readable."""
    try:
        text = _VERSION_FILE.read_text(encoding="utf-8").strip()
    except OSError:
        text = ""
    if text:
        return text
    try:
        return version("kwalitec")
    except PackageNotFoundError:
        return _FALLBACK_VERSION


APP_VERSION = _read_app_version()

# Unified product identity line (PTP-000 §8.3 / PTP-005 F-4, F-5 / PX-001 / PX-005).
# Single source: brand_identity.PRODUCT_DESCRIPTOR (PX-B-038).
PRODUCT_TAGLINE = PRODUCT_DESCRIPTOR

# IAHF-005 — single cache-bust fingerprint for all static asset URLs.
# Bump when shipping changes under app/static/ (or blueprint static folders)
# so browsers refetch branding, CSS, JS, and icons after deploy.
# Override with STATIC_ASSET_VERSION env var when needed.
_DEFAULT_STATIC_ASSET_VERSION = f"{APP_VERSION}-g5"
STATIC_ASSET_VERSION = os.getenv(
    "STATIC_ASSET_VERSION", _DEFAULT_STATIC_ASSET_VERSION
).strip() or _DEFAULT_STATIC_ASSET_VERSION
