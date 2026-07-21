"""Student-flow navigation — action keys → adapter paths.

Routing concern only. Maps presentation ``action_key`` values to Flask adapter
URL paths. Never contains educational logic.
"""

from __future__ import annotations

from urllib.parse import urlencode

# Canonical student journey paths (V4-004).
LOGIN_PATH = "/eos/login/"
DASHBOARD_PATH = "/eos/dashboard/"
MISSION_PATH = "/eos/mission/"
SESSION_PATH = "/eos/session/"
REFLECTION_PATH = "/eos/reflection/"
ONBOARDING_PATH = "/eos/onboarding/"

_ACTION_PATHS: dict[str, str] = {
    "begin_session": SESSION_PATH,
    "continue_mission": MISSION_PATH,
    "view_mission": MISSION_PATH,
    "view_progress": DASHBOARD_PATH,
    "return_home": DASHBOARD_PATH,
    "open_reflection": REFLECTION_PATH,
    "start_onboarding": ONBOARDING_PATH,
}


def path_for_action(action_key: str | None, *, default: str = DASHBOARD_PATH) -> str:
    """Resolve a presentation action key to an adapter path."""
    key = (action_key or "").strip()
    if not key:
        return default
    return _ACTION_PATHS.get(key, default)


def with_query(path: str, **params: str | None) -> str:
    """Append non-empty query parameters to a path."""
    filtered = {
        key: value
        for key, value in params.items()
        if value is not None and str(value).strip()
    }
    if not filtered:
        return path
    separator = "&" if "?" in path else "?"
    return f"{path}{separator}{urlencode(filtered)}"


def student_flow_nav(*, student_id: str = "", session_id: str = "") -> dict[str, str]:
    """Build the standard student-journey link set for templates."""
    sid = (student_id or "").strip()
    sess = (session_id or "").strip()
    return {
        "login": LOGIN_PATH,
        "dashboard": with_query(DASHBOARD_PATH, student_id=sid or None),
        "mission": with_query(MISSION_PATH, student_id=sid or None),
        "session": with_query(
            SESSION_PATH, student_id=sid or None, session_id=sess or None
        ),
        "reflection": with_query(
            REFLECTION_PATH, student_id=sid or None, session_id=sess or None
        ),
        "onboarding": with_query(ONBOARDING_PATH, student_id=sid or None),
        "begin_session": with_query(
            SESSION_PATH, student_id=sid or None, session_id=sess or None
        ),
        "return_home": with_query(DASHBOARD_PATH, student_id=sid or None),
    }
