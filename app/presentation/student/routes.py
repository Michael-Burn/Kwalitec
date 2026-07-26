"""HTTP routes for the Student Experience UI.

Thin Flask layer: auth → views → templates.
Educational authority stays in Student Experience application services.
"""

from __future__ import annotations

import logging

from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.application.student_experience.exceptions import (
    PortUnavailable,
    StudentExperienceError,
)
from app.application.student_experience.recommendation_commitment import (
    RecommendationCommitmentService,
)
from app.domain.student_experience.experience_workspace import ExperienceSurface
from app.presentation.student import student_bp
from app.presentation.student.factory import get_experience_composition
from app.presentation.student.forms import (
    BeginRevisionForm,
    DeferCommitmentForm,
    ReflectionAckForm,
    StartSessionForm,
)
from app.presentation.student.views import load_page, start_todays_session

logger = logging.getLogger(__name__)


def _current_tip_payload() -> dict:
    """Read today's tip projection for commitment recording (pass-through)."""
    from app.presentation.student.factory import get_experience_service

    try:
        dash = get_experience_service().get_dashboard(
            str(current_user.id),
            surface="home",
            include_all_surfaces=False,
        )
        home = getattr(dash, "home", None)
        if home is None:
            return {}
        tip: dict = {
            "title": home.recommendation_title or "",
            "topic_title": home.recommendation_title or "",
            "summary": home.recommendation_summary or "",
            "category": "Study",
            "priority": "Medium",
            "reason": "",
            "why_recommended": "",
            "expected_benefit": "",
            "review_point": "",
            "suggested_next_action": "",
            "generated_at": home.recommendation_title or "",
        }
        expl = home.explanation
        if expl is not None:
            tip["reason"] = expl.timeliness_line or expl.why_recommended or ""
            tip["why_recommended"] = expl.why_recommended or ""
            tip["expected_benefit"] = expl.expected_benefit or ""
            tip["review_point"] = expl.review_point or ""
            tip["suggested_next_action"] = expl.suggested_next_action or ""
        commitment = getattr(home, "commitment", None)
        key = getattr(commitment, "recommendation_key", "") or ""
        if "|" in key:
            tip["generated_at"] = key.split("|", 1)[1]
        return tip
    except Exception:  # noqa: BLE001 — fail-open for preference path
        logger.warning("commitment_tip_payload_failed", exc_info=True)
        return {}


@student_bp.get("/")
@login_required
def home():
    """Student Home — what to do next, and why."""
    from app.services.alpha_onboarding_service import AlphaOnboardingService
    from app.services.presentation_telemetry_service import (
        EVENT_DASHBOARD_OPENED,
        PresentationTelemetryService,
    )
    from app.services.welcome_service import WelcomeService

    # B8 (PX-003): Student Home is the canonical post-login landing surface
    # under SOLE_RUNTIME — mirror the same first-time onboarding gate
    # `dashboard.index` already applies, so onboarding is guaranteed exactly
    # once regardless of which home a student's flag configuration resolves
    # to (see app/presentation/consolidation.py).
    if AlphaOnboardingService.should_show(current_user):
        return redirect(url_for("alpha.onboarding"))

    page = load_page(ExperienceSurface.HOME)
    PresentationTelemetryService.record(
        EVENT_DASHBOARD_OPENED,
        user_id=current_user.id,
        path="/student/",
        context={"surface": "home"},
    )
    form = StartSessionForm()
    defer_form = DeferCommitmentForm()
    reflection_form = ReflectionAckForm()
    if page.home:
        form.mission_id.data = page.home.mission_id
        form.session_id.data = page.home.session_id
        if page.home.commitment:
            form.recommendation_key.data = (
                page.home.commitment.recommendation_key or ""
            )
            defer_form.recommendation_key.data = (
                page.home.commitment.recommendation_key or ""
            )
            reflection_form.recommendation_key.data = (
                page.home.commitment.recommendation_key or ""
            )
    return render_template(
        "student/home.html",
        title=page.shell.page_title,
        page=page,
        form=form,
        defer_form=defer_form,
        reflection_form=reflection_form,
        show_welcome=WelcomeService.should_show(current_user),
    )


@student_bp.get("/journey")
@login_required
def journey():
    """Journey — topic progress toward exam readiness."""
    from app.services.presentation_telemetry_service import (
        EVENT_JOURNEY_OPENED,
        PresentationTelemetryService,
    )

    page = load_page(ExperienceSurface.JOURNEY)
    PresentationTelemetryService.record(
        EVENT_JOURNEY_OPENED,
        user_id=current_user.id,
        path="/student/journey",
        context={"surface": "journey"},
    )
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
    """Primary Home CTA — start Today's Session via Experience.

    EP-008.3 Pattern A: also records conscious commitment (preference only).
    """
    form = StartSessionForm()
    if not form.validate_on_submit():
        flash(
            "We couldn't start today's session. Please try again.",
            "warning",
        )
        return redirect(url_for("student.home"))
    mission_id = (form.mission_id.data or "").strip() or None
    session_id = (form.session_id.data or "").strip() or None
    tip = _current_tip_payload()
    try:
        # Record commitment before / with start (Pattern A).
        if (form.record_commitment.data or "1") != "0" and tip.get("title"):
            RecommendationCommitmentService.confirm_commitment(
                current_user.id,
                tip,
                session_id=session_id,
            )
        handle = start_todays_session(
            mission_id=mission_id, session_id=session_id
        )
        RecommendationCommitmentService.mark_session_started(
            current_user.id,
            tip=tip,
            session_id=handle.session_id or session_id,
        )
    except PortUnavailable:
        flash(
            "Today's Session is temporarily unavailable. Please try again shortly.",
            "warning",
        )
        return redirect(url_for("student.home"))
    except StudentExperienceError as exc:
        logger.warning("Start session failed: %s", exc)
        flash(
            "We couldn't start today's session. Please try again from Home.",
            "warning",
        )
        return redirect(url_for("student.home"))

    from app.services.presentation_telemetry_service import (
        EVENT_MISSION_STARTED,
        PresentationTelemetryService,
    )

    PresentationTelemetryService.record(
        EVENT_MISSION_STARTED,
        user_id=current_user.id,
        resource_type="session",
        resource_id=handle.session_id or session_id,
        path="/student/session/start",
        context={"mission_id": mission_id or ""},
    )

    topic = handle.topic_title or "your topic"
    flash(f"Session started: {topic}. Entering your study environment.", "success")
    # Hand off into Session Experience (V2-019).
    target_session_id = handle.session_id or session_id
    if target_session_id:
        return redirect(
            url_for("session.overview", session_id=target_session_id)
        )
    return redirect(url_for("student.home"))


@student_bp.post("/commitment/defer")
@login_required
def defer_commitment():
    """Honest deferral — catalogue reason; no ranking change."""
    form = DeferCommitmentForm()
    if not form.validate_on_submit():
        flash("We couldn't save that just now. Please try again.", "warning")
        return redirect(url_for("student.home"))
    tip = _current_tip_payload()
    RecommendationCommitmentService.defer_commitment(
        current_user.id,
        tip,
        reason_code=form.reason_code.data or "not_today",
        reason_note=form.reason_note.data or "",
    )
    flash(
        "Your study plan continues — we'll meet you when you're ready.",
        "info",
    )
    return redirect(url_for("student.home"))


@student_bp.post("/commitment/reflection/ack")
@login_required
def acknowledge_reflection():
    """Advance C3 → C4 after viewing completion reflection."""
    form = ReflectionAckForm()
    if not form.validate_on_submit():
        return redirect(url_for("student.home"))
    RecommendationCommitmentService.acknowledge_reflection(
        current_user.id,
        recommendation_key=(form.recommendation_key.data or "").strip(),
    )
    return redirect(url_for("student.home"))


@student_bp.post("/revision/begin")
@login_required
def begin_revision():
    """Primary Revision CTA — begin revision via session start."""
    form = BeginRevisionForm()
    if not form.validate_on_submit():
        flash("We couldn't begin revision. Please try again.", "warning")
        return redirect(url_for("student.revision"))
    mission_id = (form.mission_id.data or "").strip() or None
    session_id = (form.session_id.data or "").strip() or None
    try:
        handle = start_todays_session(
            mission_id=mission_id, session_id=session_id
        )
    except PortUnavailable:
        flash(
            "Revision is temporarily unavailable. Please try again shortly.",
            "warning",
        )
        return redirect(url_for("student.revision"))
    except StudentExperienceError as exc:
        logger.warning("Begin revision failed: %s", exc)
        flash(
            "We couldn't begin revision. Please try again from this page.",
            "warning",
        )
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
    target_session_id = handle.session_id or session_id
    if target_session_id:
        return redirect(
            url_for("session.overview", session_id=target_session_id)
        )
    return redirect(url_for("student.home"))
