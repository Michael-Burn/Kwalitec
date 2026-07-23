"""View helpers — load snapshots and assemble page view models.

Routes stay thin: call these helpers, then render templates.
No educational calculations live here.
"""

from __future__ import annotations

import logging

from flask import flash
from flask_login import current_user

from app.application.student_experience.exceptions import (
    PortUnavailable,
    StudentExperienceError,
)
from app.domain.student_experience.experience_workspace import ExperienceSurface
from app.presentation.student.factory import (
    get_experience_composition,
    get_experience_service,
)
from app.presentation.student.view_models import (
    StudentPageViewModel,
    page_from_dashboard,
    shell_vm,
)

logger = logging.getLogger(__name__)


def student_id() -> str:
    """Stable student identity for Experience projections."""
    return str(current_user.id)


def load_page(surface: ExperienceSurface | str) -> StudentPageViewModel:
    """Load a surface page via Student Experience dashboard projection."""
    surface_key = (
        surface.value
        if isinstance(surface, ExperienceSurface)
        else str(surface).strip().lower()
    )
    sid = student_id()
    composition = get_experience_composition()
    if composition is not None:
        composition.ensure_learner(sid)
        composition.emit_surface_viewed(surface_key, sid)
    service = get_experience_service()
    try:
        # Home reuses sibling XP snapshots (journey / history / revision)
        # without duplicating educational projections.
        include_all = surface_key == "home"
        dash = service.get_dashboard(
            sid,
            surface=surface_key,
            include_all_surfaces=include_all,
        )
        return page_from_dashboard(dash, surface=surface_key)
    except PortUnavailable as exc:
        logger.info("Student experience port unavailable: %s", exc)
        flash(
            "Learning insights are temporarily unavailable. "
            "Please try again shortly.",
            "warning",
        )
        return _empty_page(surface_key)
    except StudentExperienceError as exc:
        logger.warning("Student experience error: %s", exc)
        flash(
            "We could not load this view right now. Please try again shortly.",
            "warning",
        )
        return _empty_page(surface_key)


def start_todays_session(
    *,
    mission_id: str | None = None,
    session_id: str | None = None,
):
    """Request Today's Session start through Student Experience."""
    sid = student_id()
    composition = get_experience_composition()
    if composition is not None:
        composition.ensure_learner(sid)
    service = get_experience_service()
    return service.start_session(
        sid,
        mission_id=mission_id or None,
        session_id=session_id or None,
    )


def _empty_page(surface: str) -> StudentPageViewModel:
    descriptions = {
        "home": "What you should do next, and why.",
        "journey": "Where you are on the path to exam readiness.",
        "revision": "The highest-value revision for today.",
        "history": "Your educational progress over time.",
        "profile": "Examination, preferences, goals, and account.",
    }
    titles = {
        "home": "Home",
        "journey": "Journey",
        "revision": "Revision",
        "history": "History",
        "profile": "Profile",
    }
    shell = shell_vm(
        active_surface=surface,
        page_title=titles.get(surface, surface.title()),
        page_description=descriptions.get(surface, ""),
    )
    return StudentPageViewModel(shell=shell)
