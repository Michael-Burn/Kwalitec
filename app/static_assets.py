"""Centralized static asset URL helpers (IAHF-005).

Templates should prefer ``versioned_static(...)`` over raw
``url_for('static', ...)`` so every asset receives the same cache-bust
fingerprint from ``STATIC_ASSET_VERSION``.
"""

from __future__ import annotations

from typing import Any

from flask import current_app, url_for


def versioned_static(
    filename: str,
    *,
    endpoint: str = "static",
    **values: Any,
) -> str:
    """Return a cache-busted URL for a static asset.

    Calls ``url_for`` for ``endpoint`` and appends ``?v=<STATIC_ASSET_VERSION>``.

    Args:
        filename: Path relative to the static folder (e.g. ``branding/logo-icon.svg``).
        endpoint: Flask static endpoint (default ``static``; blueprint static
            endpoints such as ``founder_dashboard.static`` are supported).
        **values: Extra ``url_for`` keyword arguments (e.g. ``_external=True``).

    Returns:
        Absolute or relative URL including the configured asset version query.
    """
    values.setdefault("v", current_app.config["STATIC_ASSET_VERSION"])
    return url_for(endpoint, filename=filename, **values)
