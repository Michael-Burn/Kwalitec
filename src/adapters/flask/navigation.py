"""Student-flow navigation — action keys → adapter paths.

Routing concern only. Maps presentation ``action_key`` values to Flask adapter
URL paths. Never contains educational logic.
"""

from __future__ import annotations

from urllib.parse import urlencode

# Canonical student journey paths (V4-004 / PX-002 continuous journey).
LOGIN_PATH = "/eos/login/"
DASHBOARD_PATH = "/eos/dashboard/"
HOME_PATH = "/eos/home/"
MISSION_PATH = "/eos/mission/"
WORKSPACE_PATH = "/eos/workspace/"
SESSION_PATH = "/eos/session/"
REFLECTION_PATH = "/eos/reflection/"
JOURNEY_PATH = "/eos/journey/"
READINESS_PATH = "/eos/readiness/"
COACH_PATH = "/eos/coach/"
ONBOARDING_PATH = "/eos/onboarding/"

_ACTION_PATHS: dict[str, str] = {
    "begin_session": SESSION_PATH,
    "continue_mission": MISSION_PATH,
    "resume_session": SESSION_PATH,
    "view_mission": MISSION_PATH,
    "view_progress": JOURNEY_PATH,
    "return_home": DASHBOARD_PATH,
    "open_reflection": REFLECTION_PATH,
    "review_reflection": REFLECTION_PATH,
    "prepare_checkpoint": MISSION_PATH,
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
        "home": with_query(HOME_PATH, student_id=sid or None),
        "mission": with_query(MISSION_PATH, student_id=sid or None),
        "workspace": with_query(WORKSPACE_PATH, student_id=sid or None),
        "session": with_query(
            SESSION_PATH, student_id=sid or None, session_id=sess or None
        ),
        "reflection": with_query(
            REFLECTION_PATH, student_id=sid or None, session_id=sess or None
        ),
        "journey": with_query(JOURNEY_PATH, student_id=sid or None),
        "readiness": with_query(READINESS_PATH, student_id=sid or None),
        "coach": with_query(COACH_PATH, student_id=sid or None),
        "onboarding": with_query(ONBOARDING_PATH, student_id=sid or None),
        "begin_session": with_query(
            SESSION_PATH, student_id=sid or None, session_id=sess or None
        ),
        "continue_mission": with_query(MISSION_PATH, student_id=sid or None),
        "resume_session": with_query(
            SESSION_PATH, student_id=sid or None, session_id=sess or None
        ),
        "open_reflection": with_query(
            REFLECTION_PATH, student_id=sid or None, session_id=sess or None
        ),
        "review_reflection": with_query(
            REFLECTION_PATH, student_id=sid or None, session_id=sess or None
        ),
        "prepare_checkpoint": with_query(MISSION_PATH, student_id=sid or None),
        "return_home": with_query(DASHBOARD_PATH, student_id=sid or None),
        "view_progress": with_query(JOURNEY_PATH, student_id=sid or None),
    }


def primary_cta_href(
    action_key: str | None,
    *,
    student_id: str = "",
    session_id: str = "",
) -> str:
    """Resolve the primary CTA href for the student's current learning state."""
    nav = student_flow_nav(student_id=student_id, session_id=session_id)
    key = (action_key or "").strip() or "begin_session"
    if key in nav:
        return nav[key]
    return with_query(
        path_for_action(key),
        student_id=student_id or None,
        session_id=session_id or None,
    )
