"""View helpers for Adaptive Assessment / Quick Check routes."""

from __future__ import annotations

from flask import session, url_for
from flask_login import current_user

from app.application.adaptive_assessment.quick_check_contracts import (
    QuickCheckMissionReturnContract,
)
from app.application.adaptive_assessment.quick_check_experience import (
    QuickCheckExperienceService,
    QuickCheckSurfaceSnapshot,
)
from app.presentation.adaptive_assessment.factory import get_service
from app.presentation.adaptive_assessment.view_models import (
    QuickCheckPageViewModel,
    page_from_snapshot,
)

_RETURN_ENDPOINT_KEY = "qc_return_endpoint"
_RETURN_SESSION_KEY = "qc_return_session_id"
_MISSION_ACK_KEY = "qc_mission_ack"


def student_id() -> str:
    return str(current_user.id)


def service() -> QuickCheckExperienceService:
    return get_service()


def remember_return(
    *,
    return_endpoint: str = "",
    return_session_id: str = "",
) -> None:
    """Persist Mission return targets in the Flask session."""
    if return_endpoint:
        session[_RETURN_ENDPOINT_KEY] = return_endpoint.strip()
    if return_session_id:
        session[_RETURN_SESSION_KEY] = return_session_id.strip()


def pop_mission_ack() -> str:
    """Consume a one-shot Mission acknowledgement message."""
    return str(session.pop(_MISSION_ACK_KEY, "") or "")


def stash_mission_ack(message: str) -> None:
    session[_MISSION_ACK_KEY] = message


def resolve_return_url(
    *,
    return_endpoint: str = "",
    return_session_id: str = "",
    mission_ref: str = "",
) -> str:
    """Build a safe local return URL back into the Mission experience."""
    endpoint = (
        return_endpoint.strip()
        or str(session.get(_RETURN_ENDPOINT_KEY) or "").strip()
    )
    session_id = (
        return_session_id.strip()
        or str(session.get(_RETURN_SESSION_KEY) or "").strip()
    )
    allowed = {
        "session.overview",
        "session.activity",
        "mission.study_session",
        "student.home",
        "mission.missions",
    }
    if endpoint in allowed:
        try:
            if endpoint.startswith("session.") and session_id:
                return url_for(endpoint, session_id=session_id)
            if endpoint == "mission.study_session" and mission_ref.isdigit():
                return url_for(endpoint, mission_id=int(mission_ref))
            if endpoint in {"student.home", "mission.missions"}:
                return url_for(endpoint)
        except Exception:
            pass
    # Fallbacks: session experience if we have an id, else student home.
    if session_id:
        try:
            return url_for("session.activity", session_id=session_id)
        except Exception:
            pass
    if mission_ref.isdigit():
        try:
            return url_for(
                "mission.study_session", mission_id=int(mission_ref)
            )
        except Exception:
            pass
    return url_for("student.home")


def page_for(
    snapshot: QuickCheckSurfaceSnapshot,
    *,
    return_endpoint: str = "",
    return_session_id: str = "",
) -> QuickCheckPageViewModel:
    endpoint = (
        return_endpoint
        or str(session.get(_RETURN_ENDPOINT_KEY) or "")
    )
    sid = return_session_id or str(session.get(_RETURN_SESSION_KEY) or "")
    return page_from_snapshot(
        snapshot,
        return_endpoint=endpoint,
        return_session_id=sid,
    )


def apply_mission_return(ack: QuickCheckMissionReturnContract) -> str:
    """Stash acknowledgement and return the redirect URL helper inputs."""
    stash_mission_ack(ack.acknowledgement)
    return ack.acknowledgement
