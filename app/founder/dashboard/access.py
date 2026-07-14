"""Founder / administrator access helpers for FOS-004."""

from __future__ import annotations

import os
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from flask import abort, current_app
from flask_login import current_user, login_required

F = TypeVar("F", bound=Callable[..., Any])


def founder_emails() -> frozenset[str]:
    """Return normalised Founder / administrator email addresses.

    Sources (merged):
    - ``ADMIN_EMAIL`` (canonical bootstrap administrator)
    - ``FOUNDER_EMAILS`` comma-separated list
    - ``FOUNDER_EMAILS`` app config (tests)
    """
    emails: set[str] = set()
    admin = (os.getenv("ADMIN_EMAIL") or "").strip().lower()
    if admin:
        emails.add(admin)

    env_founders = (os.getenv("FOUNDER_EMAILS") or "").strip()
    if env_founders:
        emails.update(e.strip().lower() for e in env_founders.split(",") if e.strip())

    try:
        cfg = current_app.config.get("FOUNDER_EMAILS")
    except RuntimeError:
        cfg = None
    if isinstance(cfg, str) and cfg.strip():
        emails.update(e.strip().lower() for e in cfg.split(",") if e.strip())
    elif isinstance(cfg, list | tuple | set | frozenset):
        emails.update(str(e).strip().lower() for e in cfg if str(e).strip())

    return frozenset(emails)


def is_founder_user(user: Any | None = None) -> bool:
    """Return whether ``user`` is an authorised Founder / administrator."""
    candidate = user if user is not None else current_user
    if candidate is None or not getattr(candidate, "is_authenticated", False):
        return False
    email = str(getattr(candidate, "email", "") or "").strip().lower()
    if not email:
        return False
    return email in founder_emails()


def founder_required(view: F) -> F:
    """Require authentication and Founder / administrator access."""

    @wraps(view)
    @login_required
    def wrapped(*args: Any, **kwargs: Any):
        if not is_founder_user(current_user):
            abort(403)
        return view(*args, **kwargs)

    return wrapped  # type: ignore[return-value]
