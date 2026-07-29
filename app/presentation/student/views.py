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
    """Load a surface page via Student Experience dashboard projection.

    PX-001: when the student has an active Runtime C enrolment, Home and
    Journey are projected from Runtime C educational outputs (EQ-001).
    Runtime A remains the default path for students without Runtime C.
    """
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

    runtime_c_page = _try_runtime_c_page(sid, surface_key)
    if runtime_c_page is not None:
        return runtime_c_page

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


def _try_runtime_c_page(sid: str, surface_key: str) -> StudentPageViewModel | None:
    """Return a Runtime C educational page when the student is enrolled.

    RI-001: when Educational Intelligence Preferred Authority is available,
    skip Runtime C educational selection and let Runtime A/Home consume
    Experience Models via the recommendation bridge. Runtime C remains
    Temporary compatibility only — no new educational reasoning here.
    """
    if surface_key not in {"home", "journey"}:
        return None
    try:
        user_id = int(sid)
    except (TypeError, ValueError):
        return None
    if _ri001_preferred_authority_available(user_id):
        return None
    try:
        from app.application.educational_experience import (
            EducationalExperienceService,
        )
        from app.presentation.student.educational_view_models import (
            page_from_educational_experience,
        )

        experience = EducationalExperienceService().load_for_user(user_id)
        if experience is None:
            return None
        return page_from_educational_experience(experience, surface=surface_key)
    except Exception:  # noqa: BLE001 — fail open to Runtime A
        logger.warning(
            "runtime_c_educational_page_failed surface=%s",
            surface_key,
            exc_info=True,
        )
        return None


def _ri001_preferred_authority_available(user_id: int) -> bool:
    """True when SCI + Educational Decisions exist for Preferred Authority."""
    try:
        from app.application.runtime_integration import (
            build_runtime_integration_service,
        )

        return build_runtime_integration_service().has_educational_intelligence(user_id)
    except Exception:  # noqa: BLE001
        return False


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
        # SOP-001 — one question per surface.
        "home": "What should I do now?",
        "journey": "Where am I?",
        "revision": "What deserves my attention?",
        "history": "What have I accomplished?",
        "profile": "Configure how Kwalitec works for you.",
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
