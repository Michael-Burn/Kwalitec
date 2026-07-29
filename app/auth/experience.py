"""FV-001B — Experience Selection helpers (navigation only).

Dual-access users (Console + Student Experience) choose explicitly after
login. Preference storage is device-local (versioned localStorage) — no DB.
"""

from __future__ import annotations

from typing import Any

from flask import url_for


def can_access_both_experiences(user: Any | None = None) -> bool:
    """True when the user may use Console and Student Experience.

    Founder / Administrator / console.access operators can enter Student OS
    deliberately. Student-only identities cannot access Console, so they
    skip Experience Selection.
    """
    from app.founder.dashboard.access import is_founder_user

    return bool(is_founder_user(user))


def experience_selection_url(*, switch: bool = False) -> str:
    """URL for the Experience Selection page."""
    if switch:
        return url_for("auth.experience_selection", switch="1")
    return url_for("auth.experience_selection")


def founder_console_url() -> str:
    """Founder Console home URL."""
    return url_for("founder_dashboard.index")


def student_experience_url() -> str:
    """Student Experience home URL (Education OS)."""
    return url_for("student.home")
