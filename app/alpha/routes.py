"""Routes for Internal Alpha infrastructure — ALPHA-001."""

from __future__ import annotations

import logging

from flask import (
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required

from app.alpha import alpha_bp
from app.alpha.forms import (
    ExplanationClearForm,
    MissionHelpfulForm,
    ReportProblemForm,
    SuggestImprovementForm,
    TelemetryIngestForm,
)
from app.services.alpha_feedback_service import (
    KIND_EXPLANATION_CLEAR,
    KIND_MISSION_HELPFUL,
    KIND_REPORT_PROBLEM,
    KIND_SUGGEST_IMPROVEMENT,
    AlphaFeedbackService,
)
from app.services.alpha_onboarding_service import AlphaOnboardingService
from app.services.presentation_telemetry_service import (
    CLIENT_EVENTS,
    EVENT_FEEDBACK_SUBMITTED,
    PresentationTelemetryService,
)
from app.services.release_info_service import ReleaseInfoService

logger = logging.getLogger(__name__)


@alpha_bp.get("/onboarding")
@login_required
def onboarding():
    """Lightweight product onboarding for Internal Alpha participants."""
    steps = AlphaOnboardingService.steps()
    state = AlphaOnboardingService.state_for(current_user)
    return render_template(
        "alpha/onboarding.html",
        title="Welcome to Kwalitec",
        steps=steps,
        state=state,
    )


@alpha_bp.post("/onboarding/complete")
@login_required
def onboarding_complete():
    """Mark product onboarding complete."""
    AlphaOnboardingService.complete(current_user.id)
    flash("You're set — open today's mission when you're ready.", "success")
    return redirect(url_for("dashboard.index"))


@alpha_bp.post("/onboarding/skip")
@login_required
def onboarding_skip():
    """Skip onboarding; still reachable from Help."""
    AlphaOnboardingService.skip(current_user.id)
    return redirect(url_for("dashboard.index"))


@alpha_bp.get("/help")
@login_required
def help_centre():
    """Student-facing support tools and release information."""
    release = ReleaseInfoService.current()
    return render_template(
        "alpha/help.html",
        title="Help & Support",
        release=release,
        report_form=ReportProblemForm(),
        suggest_form=SuggestImprovementForm(),
    )


@alpha_bp.route("/feedback/mission-helpful", methods=["GET", "POST"])
@login_required
def feedback_mission_helpful():
    """Was this mission helpful?"""
    form = MissionHelpfulForm()
    if request.method == "GET":
        form.mission_id.data = request.args.get("mission_id", "")
        form.surface.data = request.args.get("surface", "mission")
    return _handle_feedback(
        form=form,
        kind=KIND_MISSION_HELPFUL,
        template="alpha/feedback_mission_helpful.html",
        title="Was this mission helpful?",
    )


@alpha_bp.route("/feedback/explanation-clear", methods=["GET", "POST"])
@login_required
def feedback_explanation_clear():
    """Was this explanation clear?"""
    form = ExplanationClearForm()
    if request.method == "GET":
        form.mission_id.data = request.args.get("mission_id", "")
        form.surface.data = request.args.get("surface", "explanation")
    return _handle_feedback(
        form=form,
        kind=KIND_EXPLANATION_CLEAR,
        template="alpha/feedback_explanation_clear.html",
        title="Was this explanation clear?",
    )


@alpha_bp.route("/feedback/report-problem", methods=["GET", "POST"])
@login_required
def feedback_report_problem():
    """Report a problem."""
    form = ReportProblemForm()
    if request.method == "GET":
        form.mission_id.data = request.args.get("mission_id", "")
        form.surface.data = request.args.get("surface", "support")
        form.reference_id.data = request.args.get("ref", "")
        if form.reference_id.data and not form.message.data:
            form.message.data = f"Error reference: {form.reference_id.data}\n"
    return _handle_feedback(
        form=form,
        kind=KIND_REPORT_PROBLEM,
        template="alpha/feedback_report_problem.html",
        title="Report a problem",
        include_reference=True,
    )


@alpha_bp.route("/feedback/suggest", methods=["GET", "POST"])
@login_required
def feedback_suggest():
    """Suggest an improvement."""
    form = SuggestImprovementForm()
    if request.method == "GET":
        form.mission_id.data = request.args.get("mission_id", "")
        form.surface.data = request.args.get("surface", "support")
    return _handle_feedback(
        form=form,
        kind=KIND_SUGGEST_IMPROVEMENT,
        template="alpha/feedback_suggest.html",
        title="Suggest an improvement",
    )


@alpha_bp.post("/telemetry")
@login_required
def telemetry_ingest():
    """Accept allowed client-side presentation telemetry events."""
    form = TelemetryIngestForm()
    if not form.validate_on_submit():
        return jsonify({"ok": False, "error": "invalid"}), 400

    event_type = (form.event_type.data or "").strip().lower()
    if event_type not in CLIENT_EVENTS:
        return jsonify({"ok": False, "error": "event_not_allowed"}), 400

    PresentationTelemetryService.record(
        event_type,
        user_id=current_user.id,
        resource_type=(form.resource_type.data or None),
        resource_id=(form.resource_id.data or None),
        path=request.path,
        context={"surface": form.surface.data} if form.surface.data else None,
    )
    return jsonify({"ok": True})


def _handle_feedback(
    *,
    form,
    kind: str,
    template: str,
    title: str,
    include_reference: bool = False,
):
    if form.validate_on_submit():
        mission_raw = (form.mission_id.data or "").strip()
        mission_id = int(mission_raw) if mission_raw.isdigit() else None
        message = form.message.data
        if include_reference and getattr(form, "reference_id", None):
            ref = (form.reference_id.data or "").strip()
            if ref and message and ref not in message:
                message = f"{message}\n\nError reference: {ref}"
            elif ref and not message:
                message = f"Error reference: {ref}"

        result = AlphaFeedbackService.submit(
            user_id=current_user.id,
            kind=kind,
            rating=getattr(form, "rating", None).data
            if hasattr(form, "rating")
            else None,
            message=message,
            mission_id=mission_id,
            surface=(form.surface.data or None),
        )
        if not result.ok:
            flash(result.error or "Could not save feedback.", "warning")
            return render_template(template, title=title, form=form)

        PresentationTelemetryService.record(
            EVENT_FEEDBACK_SUBMITTED,
            user_id=current_user.id,
            resource_type="alpha_feedback",
            resource_id=result.submission_id,
            path=request.path,
            context={"kind": kind},
        )
        flash("Thank you — your feedback helps Internal Alpha.", "success")
        next_url = request.args.get("next") or url_for("dashboard.index")
        if (
            isinstance(next_url, str)
            and next_url.startswith("/")
            and not next_url.startswith("//")
        ):
            return redirect(next_url)
        return redirect(url_for("dashboard.index"))

    return render_template(template, title=title, form=form)
