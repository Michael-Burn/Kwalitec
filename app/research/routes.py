"""Routes for RIP-001 Daily Reflection & Product Check-in and RIP-002 recognition.

Founder operational surfaces live under ``/founder`` (IAHF-003). Legacy
``/research/founder*`` paths redirect into the Founder Command Centre.
"""

from __future__ import annotations

import logging

from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from app.founder.dashboard.access import founder_required
from app.research import research_bp
from app.research.forms import ProductCheckinForm
from app.services.contributor_recognition_service import (
    BADGE_LABELS,
    ContributorRecognitionService,
)
from app.services.research_feedback_service import (
    SOURCE_SETTINGS,
    SOURCE_STUDY_SESSION,
    ResearchFeedbackService,
)

logger = logging.getLogger(__name__)


def _parse_optional_int(raw: str | None) -> int | None:
    if raw is None or raw == "":
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


@research_bp.route("/checkin", methods=["GET", "POST"])
@login_required
def checkin():
    """Optional Daily Reflection & Product Check-in form."""
    source = request.args.get("source") or request.form.get("submission_source")
    if source not in {SOURCE_STUDY_SESSION, SOURCE_SETTINGS}:
        source = SOURCE_SETTINGS

    mission_id = _parse_optional_int(
        request.args.get("mission_id") or request.form.get("mission_id")
    )
    study_plan_id = _parse_optional_int(
        request.args.get("study_plan_id") or request.form.get("study_plan_id")
    )

    # Primary post-study entry: soft invitation gate (settings always open).
    if request.method == "GET" and source == SOURCE_STUDY_SESSION:
        eligibility = ResearchFeedbackService.is_eligible_for_invitation(
            current_user.id,
            mission_id=mission_id,
        )
        if not eligibility.eligible:
            flash(
                "Product Check-in is available after some study activity today.",
                "info",
            )
            return redirect(url_for("dashboard.index"))
        if mission_id is None and eligibility.mission is not None:
            mission_id = eligibility.mission.id
        if study_plan_id is None and eligibility.study_plan is not None:
            study_plan_id = eligibility.study_plan.id

    form = ProductCheckinForm()
    if request.method == "GET":
        form.submission_source.data = source
        form.mission_id.data = str(mission_id) if mission_id is not None else ""
        form.study_plan_id.data = (
            str(study_plan_id) if study_plan_id is not None else ""
        )

    if form.validate_on_submit():
        try:
            result = ResearchFeedbackService.submit_checkin(
                current_user.id,
                experience_rating=form.experience_rating.data,
                feature_helped_most=form.feature_helped_most.data,
                friction_area=form.friction_area.data,
                confidence_rating=form.confidence_rating.data,
                return_intent=form.return_intent.data,
                submission_source=form.submission_source.data,
                free_text=form.free_text.data,
                classification=form.classification.data,
                study_plan_id=_parse_optional_int(form.study_plan_id.data),
                mission_id=_parse_optional_int(form.mission_id.data),
            )
        except ValueError as exc:
            flash(str(exc), "danger")
            return render_template(
                "research/checkin.html",
                title="Product Check-in",
                form=form,
                source=form.submission_source.data or source,
            )
        if result.newly_earned_badges:
            session["rip002_new_badges"] = list(result.newly_earned_badges)
        return redirect(url_for("research.thank_you"))

    return render_template(
        "research/checkin.html",
        title="Product Check-in",
        form=form,
        source=source,
    )


@research_bp.get("/thank-you")
@login_required
def thank_you():
    """Thank-you screen after a completed Product Check-in."""
    journey = ContributorRecognitionService.get_journey_summary(current_user.id)
    new_badges = session.pop("rip002_new_badges", [])
    new_badge_labels = [
        BADGE_LABELS[slug] for slug in new_badges if slug in BADGE_LABELS
    ]
    return render_template(
        "research/thank_you.html",
        title="Thank you",
        journey=journey,
        new_badge_labels=new_badge_labels,
    )


@research_bp.get("/dismiss")
@login_required
def dismiss():
    """Skip the optional Product Check-in without penalty."""
    return redirect(url_for("dashboard.index"))


@research_bp.route("/founder", methods=["GET", "POST"])
@founder_required
def founder_command_centre():
    """Deprecated — redirects into Founder Command Centre Feedback."""
    code = 307 if request.method == "POST" else 302
    return redirect(
        url_for("founder_dashboard.feedback", **request.args.to_dict()),
        code=code,
    )


@research_bp.route("/founder/finding/<int:finding_id>", methods=["GET", "POST"])
@founder_required
def founder_finding_detail(finding_id: int):
    """Deprecated — redirects into Founder Command Centre Findings."""
    code = 307 if request.method == "POST" else 302
    return redirect(
        url_for(
            "founder_dashboard.finding_detail",
            finding_id=finding_id,
            **request.args.to_dict(),
        ),
        code=code,
    )


@research_bp.route(
    "/founder/review/<int:submission_id>",
    methods=["GET", "POST"],
)
@founder_required
def founder_review_submission(submission_id: int):
    """Deprecated — redirects into Founder Feedback review."""
    code = 307 if request.method == "POST" else 302
    return redirect(
        url_for(
            "founder_dashboard.review_submission",
            submission_id=submission_id,
            **request.args.to_dict(),
        ),
        code=code,
    )


@research_bp.post("/founder/award-founders-circle/<int:user_id>")
@founder_required
def founder_award_founders_circle(user_id: int):
    """Deprecated — redirects into Founder Participants award action."""
    return redirect(
        url_for(
            "founder_dashboard.award_founders_circle",
            user_id=user_id,
        ),
        code=307,
    )
