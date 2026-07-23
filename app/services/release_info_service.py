"""Release / build information for Internal Alpha — ALPHA-001.

Assembles version, build date, environment, optional commit, and support
contact for settings and support surfaces. Presentation only.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import UTC, datetime
from functools import lru_cache

from app.brand_identity import INTERNAL_ALPHA_BUILD_LABEL, INTERNAL_ALPHA_LABEL
from app.services.internal_alpha_status_service import INTERNAL_ALPHA_VERSION
from app.version import APP_VERSION

DEFAULT_SUPPORT_CONTACT = "alpha-support@kwalitec.com"


@dataclass(frozen=True)
class ReleaseInfo:
    """Student- and founder-facing release metadata."""

    app_version: str
    build_date: str
    environment: str
    commit: str | None
    support_contact: str
    build_number: str
    internal_alpha_version: str
    internal_alpha_label: str
    build_label: str


class ReleaseInfoService:
    """Compose release information from env and package metadata."""

    @staticmethod
    def current() -> ReleaseInfo:
        """Return the current release info snapshot."""
        return ReleaseInfo(
            app_version=APP_VERSION,
            build_date=_build_date(),
            environment=_environment_name(),
            commit=_commit_sha(),
            support_contact=_support_contact(),
            build_number=_build_number(),
            internal_alpha_version=INTERNAL_ALPHA_VERSION,
            internal_alpha_label=INTERNAL_ALPHA_LABEL,
            build_label=INTERNAL_ALPHA_BUILD_LABEL,
        )


def _environment_name() -> str:
    flask_env = os.getenv("FLASK_ENV", "development").strip().lower()
    app_env = os.getenv("APP_ENV", flask_env).strip().lower() or "development"
    return app_env


def _build_number() -> str:
    raw = os.environ.get("KWALITEC_BUILD_NUMBER", "").strip()
    return raw or "local"


def _support_contact() -> str:
    raw = os.environ.get("KWALITEC_SUPPORT_CONTACT", "").strip()
    return raw or DEFAULT_SUPPORT_CONTACT


def _build_date() -> str:
    raw = os.environ.get("KWALITEC_BUILD_DATE", "").strip()
    if raw:
        return raw
    # Fallback: process start day in UTC (stable for a running instance).
    return _process_start_date()


@lru_cache(maxsize=1)
def _process_start_date() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d")


def _commit_sha() -> str | None:
    for key in ("KWALITEC_GIT_COMMIT", "RENDER_GIT_COMMIT", "SOURCE_VERSION"):
        raw = os.environ.get(key, "").strip()
        if raw:
            return raw[:40]
    return None
