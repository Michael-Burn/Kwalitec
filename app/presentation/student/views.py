"""View helpers — load snapshots and assemble page view models.

Routes stay thin: call these helpers, then render templates.
No educational calculations live here.

V1S-007 / A9 — Educational Runtime Singularity: when a student has a Runtime C
enrolment, Home / Journey / Session execute exclusively through the Educational
Runtime. Missing SCI is ensured or surfaced — never a Runtime A fallback.
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

    PX-001 / V1S-007: Runtime C enrolment owns Home and Journey exclusively.
    Students without Runtime C still use the legacy Experience projection
    (TEMPORARY — RI-002 retirement); enrolled Runtime C students never fall
    through to Runtime A mastery theatre.
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

    # V1S-007: Runtime C enrolment present but page unavailable → readiness
    # message, never Runtime A.
    if _has_runtime_c_enrolment(sid) and surface_key in {"home", "journey"}:
        flash(
            "Your educational workspace is not ready yet. "
            "Please try again shortly.",
            "warning",
        )
        return _empty_page(surface_key)

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


def _has_runtime_c_enrolment(sid: str) -> bool:
    """True when the student has an active or completed Runtime C enrolment."""
    try:
        user_id = int(sid)
    except (TypeError, ValueError):
        return False
    try:
        from app.application.educational_experience import (
            EducationalExperienceService,
        )

        return (
            EducationalExperienceService().find_enrolment_for_experience(user_id)
            is not None
        )
    except Exception:  # noqa: BLE001
        return False


def _try_runtime_c_page(sid: str, surface_key: str) -> StudentPageViewModel | None:
    """Return a Runtime C educational page when the student is enrolled.

    V1S-005 DF-002: Runtime C enrolment wins so ProgressEngine remains the
    sole progress truth for dogfood. RI-001 Preferred Authority must not
    divert enrolled Runtime C students onto Runtime A mastery theatre.

    V1S-007: ensure SCI before projection; never fail open to Runtime A.
    """
    if surface_key not in {"home", "journey"}:
        return None
    try:
        user_id = int(sid)
    except (TypeError, ValueError):
        return None
    try:
        from app.application.educational_experience import (
            EducationalExperienceService,
        )
        from app.application.educational_runtime_engine import ensure_active_sci
        from app.presentation.student.educational_view_models import (
            page_from_educational_experience,
        )

        experience = EducationalExperienceService().load_for_user(user_id)
        if experience is None:
            return None
        if experience.is_runtime_c and experience.subject_code:
            ensure_active_sci(
                student_id=user_id,
                subject_code=experience.subject_code,
                correlation_id=f"v1s007-home-{user_id}",
                require=False,
            )
        return page_from_educational_experience(
            experience, surface=surface_key
        )
    except Exception:  # noqa: BLE001 — caller decides Runtime A vs readiness
        logger.warning(
            "runtime_c_educational_page_failed surface=%s",
            surface_key,
            exc_info=True,
        )
        return None


def start_todays_session(
    *,
    mission_id: str | None = None,
    session_id: str | None = None,
):
    """Request Today's Session start through Student Runtime.

    V1S-007 / A9: Runtime C enrolments execute exclusively through the
    Educational Runtime + Learning Session spine. SCI is ensured before
    session start. Session never falls through to Runtime A / PlanningService
    for enrolled Runtime C students.
    """
    sid = student_id()
    runtime_c_binding = _try_runtime_c_session_start(
        sid, mission_id=mission_id, session_id=session_id
    )
    if runtime_c_binding is not None:
        return runtime_c_binding

    if _has_runtime_c_enrolment(sid):
        from app.application.educational_runtime_engine import (
            EducationalPrerequisiteMissing,
        )

        raise EducationalPrerequisiteMissing(
            "Your learning session could not start in the Educational Runtime. "
            "Please return to Home and try again. Study will not continue on "
            "the legacy path.",
            missing_prerequisite="educational_runtime_session",
        )

    # TEMPORARY (RI-002): students without Runtime C enrolment still use the
    # legacy Experience Mission port. Not a Runtime C → Runtime A fallback.
    composition = get_experience_composition()
    if composition is not None:
        composition.ensure_learner(sid)
    service = get_experience_service()
    return service.start_session(
        sid,
        mission_id=mission_id or None,
        session_id=session_id or None,
    )


def _try_runtime_c_session_start(
    sid: str,
    *,
    mission_id: str | None,
    session_id: str | None,
):
    """Start/resume LearningSessionRuntime for published-curriculum students."""
    from app.application.config.v2_flags import resolve_v2_feature_flags
    from app.domain.student_experience.experience_session import (
        ExperienceSession,
        ExperienceSessionStatus,
    )

    flags = resolve_v2_feature_flags()
    if not flags.SR_SESSION_PRIMARY:
        return None
    try:
        user_id = int(sid)
    except (TypeError, ValueError):
        return None

    from app.application.educational_experience import EducationalExperienceService
    from app.application.educational_runtime_engine import ensure_active_sci
    from app.application.student_runtime import (
        MissionNotAcceptable,
        SessionSpineUnavailable,
        StudentRuntimeCoordinator,
    )
    from app.infrastructure.adapters.learning_session.persistence import (
        LearningSessionPersistenceAdapter,
    )
    from app.presentation.session.factory import get_session_experience_composition

    experience = EducationalExperienceService().load_for_user(user_id)
    if experience is None or not experience.is_runtime_c:
        return None

    # V1S-007: SCI is mandatory before session ownership — create or raise.
    subject = (experience.subject_code or "").strip().upper()
    if subject:
        ensure_active_sci(
            student_id=user_id,
            subject_code=subject,
            correlation_id=f"v1s007-session-{user_id}",
            require=True,
        )

    mid = (mission_id or "").strip()
    if not mid and experience.mission is not None:
        mid = experience.mission.mission_instance_id
    if not mid:
        from app.application.educational_runtime_engine import (
            EducationalPrerequisiteMissing,
        )

        raise EducationalPrerequisiteMissing(
            "Today's mission is not ready yet. Return to Home and refresh "
            "before starting a session.",
            missing_prerequisite="daily_mission",
            subject_code=subject or None,
        )

    session_composition = get_session_experience_composition()
    store = session_composition.store if session_composition is not None else None
    persistence = LearningSessionPersistenceAdapter(store=store)
    overview_writer = (
        session_composition.runtime if session_composition is not None else None
    )

    coordinator = StudentRuntimeCoordinator(
        persistence=persistence,
        session_overview_writer=overview_writer,
        flags=flags,
    )

    topic_title = ""
    minutes = None
    if experience.mission is not None:
        topic_title = experience.mission.topic_title or experience.mission.title
        minutes = experience.mission.estimated_duration_minutes or None

    try:
        if session_id or (
            experience.mission is not None
            and (experience.mission.status or "").lower() == "accepted"
        ):
            try:
                binding = coordinator.resume_session(
                    user_id=user_id,
                    session_id=session_id,
                    mission_instance_id=mid,
                )
            except SessionSpineUnavailable:
                binding = coordinator.accept_and_start_session(
                    user_id=user_id,
                    mission_instance_id=mid,
                    topic_title=topic_title,
                    estimated_minutes=minutes,
                )
        else:
            binding = coordinator.accept_and_start_session(
                user_id=user_id,
                mission_instance_id=mid,
                topic_title=topic_title,
                estimated_minutes=minutes,
            )
    except (SessionSpineUnavailable, MissionNotAcceptable) as exc:
        logger.warning("runtime_c_session_spine_failed: %s", exc)
        raise

    return ExperienceSession.create(
        binding.session_id,
        sid,
        status=ExperienceSessionStatus.IN_PROGRESS,
        mission_id=binding.mission_instance_id,
        session_id=binding.session_id,
        topic_title=binding.topic_title,
        estimated_minutes=binding.estimated_minutes,
        started_at="",
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
        "journey": "Syllabus",
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
