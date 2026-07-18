"""Single product version source of truth (PTP-005 / QS-001 / IAHF-005)."""

from __future__ import annotations

import os
from importlib.metadata import PackageNotFoundError, version

# Canonical student-facing product version — keep in sync with pyproject.toml.
_FALLBACK_VERSION = "1.0.0"

try:
    APP_VERSION = version("kwalitec")
except PackageNotFoundError:
    APP_VERSION = _FALLBACK_VERSION

# Unified product identity line (PTP-000 §8.3 / PTP-005 F-4, F-5).
PRODUCT_TAGLINE = (
    "Adaptive study planner and honest practice tracker for professional exams."
)

# IAHF-005 — single cache-bust fingerprint for all static asset URLs.
# Bump when shipping changes under app/static/ (or blueprint static folders)
# so browsers refetch branding, CSS, JS, and icons after deploy.
# Override with STATIC_ASSET_VERSION env var when needed.
_DEFAULT_STATIC_ASSET_VERSION = f"{APP_VERSION}-RC2.1"
STATIC_ASSET_VERSION = os.getenv(
    "STATIC_ASSET_VERSION", _DEFAULT_STATIC_ASSET_VERSION
).strip() or _DEFAULT_STATIC_ASSET_VERSION
