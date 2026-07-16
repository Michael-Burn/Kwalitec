"""Single product version source of truth (PTP-005 / QS-001)."""

from __future__ import annotations

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
