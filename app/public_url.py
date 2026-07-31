"""Public base-URL helpers for production / custom-domain deployments.

``APP_URL`` is the canonical public origin (scheme + host[+port], no path).
It drives sitemap/robots absolute links and OG/canonical metadata.  During an
HTTP request, Flask URL generation still prefers the live Host (via ProxyFix);
``APP_URL`` is the operator-configured source of truth for the preferred
public domain.
"""

from __future__ import annotations

from urllib.parse import urlsplit, urlunsplit

from flask import current_app, has_request_context, request


def normalize_app_url(raw: str | None) -> str:
    """Return a normalised origin (no trailing slash, no path/query).

    Empty or whitespace-only input yields ``""``.
    """
    value = (raw or "").strip()
    if not value:
        return ""
    if "://" not in value:
        value = f"https://{value}"
    parts = urlsplit(value)
    if not parts.netloc:
        return ""
    # Drop path/query/fragment — APP_URL is origin-only.
    return urlunsplit((parts.scheme or "https", parts.netloc, "", "", "")).rstrip(
        "/"
    )


def configured_app_url() -> str:
    """Return the configured ``APP_URL`` origin, or ``""`` when unset."""
    return normalize_app_url(current_app.config.get("APP_URL"))


def public_base_url() -> str:
    """Return the preferred public origin for absolute links.

    Preference order:
    1. Configured ``APP_URL``
    2. Current request URL root (ProxyFix-aware Host + scheme)
    3. Empty string when neither is available
    """
    configured = configured_app_url()
    if configured:
        return configured
    if has_request_context():
        return request.url_root.rstrip("/")
    return ""


def absolute_public_url(path: str = "/") -> str:
    """Join ``path`` onto the public origin.

    ``path`` should start with ``/``. Relative paths are coerced.
    """
    base = public_base_url()
    if not path.startswith("/"):
        path = f"/{path}"
    if not base:
        return path
    return f"{base}{path}"


def host_from_app_url(raw: str | None = None) -> str | None:
    """Extract hostname (no port) from an APP_URL-style origin."""
    origin = normalize_app_url(raw) if raw is not None else ""
    if raw is None:
        try:
            origin = configured_app_url()
        except RuntimeError:
            return None
    if not origin:
        return None
    return urlsplit(origin).hostname
