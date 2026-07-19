"""HTTP routes for the Student Experience UI.

Thin Flask layer: auth → views → templates.
Educational authority stays in Student Experience application services.
"""

from __future__ import annotations

import logging

from flask import flash, redirect, render_template, url_for
from flask_login import login_required

from app.application.student_experience.exceptions import (
    PortUnavailable,
    StudentExperienceError,
)
from app.domain.student_experience.experience_workspace import ExperienceSurface
from app.presentation.student import student_bp
from app.presentation.student.factory import get_experience_composition
from app.presentation.student.forms import BeginRevisionForm, StartSessionForm
from app.presentation.student.views import load_page, start_todays_session

logger = logging.getLogger(__name__)


@student_bp.get("/")
@login_required
def home():
    """Student Home — what to do next, and why."""
    page = load_page(ExperienceSurface.HOME)
    form = StartSessionForm()
    if page.home:
        form.mission_id.data = page.home.mission_id
        form.session_id.data = page.home.session_id
    return render_template(
        "student/home.html",
        title=page.shell.page_title,
        page=page,
        form=form,
    )


@student_bp.get("/journey")
@login_required
def journey():
    """Journey — roadmap without curriculum graph jargon."""
    page = load_page(ExperienceSurface.JOURNEY)
    return render_template(
        "student/journey.html",
        title=page.shell.page_title,
        page=page,
    )


@student_bp.get("/revision")
@login_required
def revision():
    """Revision — highest-value revision from Adaptive Decision."""
    page = load_page(ExperienceSurface.REVISION)
    form = BeginRevisionForm()
    if page.revision and page.revision.primary:
        form.option_id.data = page.revision.primary.option_id
    return render_template(
        "student/revision.html",
        title=page.shell.page_title,
        page=page,
        form=form,
    )


@student_bp.get("/history")
@login_required
def history():
    """History — educational progress, not activity logs."""
    page = load_page(ExperienceSurface.HISTORY)
    return render_template(
        "student/history.html",
        title=page.shell.page_title,
        page=page,
    )


@student_bp.get("/profile")
@login_required
def profile():
    """Profile — examination, preferences, goals, settings."""
    page = load_page(ExperienceSurface.PROFILE)
    return render_template(
        "student/profile.html",
        title=page.shell.page_title,
        page=page,
    )


@student_bp.post("/session/start")
@login_required
def start_session():
    """Primary Home CTA — start Today's Session via Experience."""
    form = StartSessionForm()
    if not form.validate_on_submit():
        flash("Could not start today's session. Please try again.", "warning")
        return redirect(url_for("student.home"))
    mission_id = (form.mission_id.data or "").strip() or None
    session_id = (form.session_id.data or "").strip() or None
    try:
        handle = start_todays_session(
            mission_id=mission_id, session_id=session_id
        )
    except PortUnavailable:
        flash(
            "Today's Session is temporarily unavailable. Please try again shortly.",
            "warning",
        )
        return redirect(url_for("student.home"))
    except StudentExperienceError as exc:
        logger.warning("Start session failed: %s", exc)
        flash("Could not start today's session.", "warning")
        return redirect(url_for("student.home"))

    topic = handle.topic_title or "your topic"
    flash(f"Session started: {topic}.", "success")
    # Version 2 learning loop completes via Mission → Twin → Adaptive;
    # return to Student Home with refreshed production projections.
    return redirect(url_for("student.home"))


@student_bp.post("/revision/begin")
@login_required
def begin_revision():
    """Primary Revision CTA — begin revision via session start."""
    form = BeginRevisionForm()
    if not form.validate_on_submit():
        flash("Could not begin revision. Please try again.", "warning")
        return redirect(url_for("student.revision"))
    mission_id = (form.mission_id.data or "").strip() or None
    session_id = (form.session_id.data or "").strip() or None
    try:
        handle = start_todays_session(
            mission_id=mission_id, session_id=session_id
        )
    except PortUnavailable:
        flash(
            "Revision session is temporarily unavailable. Please try again shortly.",
            "warning",
        )
        return redirect(url_for("student.revision"))
    except StudentExperienceError as exc:
        logger.warning("Begin revision failed: %s", exc)
        flash("Could not begin revision.", "warning")
        return redirect(url_for("student.revision"))

    flash(
        f"Revision started: {handle.topic_title or 'selected topic'}.",
        "success",
    )
    composition = get_experience_composition()
    if composition is not None:
        composition.emit_revision_started(
            str(handle.student_id),
            option_id=(form.option_id.data or "").strip() or None,
        )
    return redirect(url_for("student.home"))
