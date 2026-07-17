"""Shared Founder Feedback section request helpers (IAHF-003).

Extracted so Feedback lives under the Founder Command Centre while
deprecated `/research/founder*` URLs can redirect without duplicating logic.
"""

from __future__ import annotations

from datetime import date

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user

from app.services.contributor_recognition_service import (
    BADGE_LABELS,
    ContributorRecognitionService,
)
from app.services.founder_research_service import (
    WORKFLOW_LABELS,
    FounderResearchService,
    InboxFilters,
)
from app.services.research_insight_service import (
    TIME_WINDOW_7_DAYS,
    TIME_WINDOW_LABELS,
)

FEEDBACK_ENDPOINT = "founder_dashboard.feedback"
FINDING_DETAIL_ENDPOINT = "founder_dashboard.finding_detail"
REVIEW_ENDPOINT = "founder_dashboard.review_submission"
PARTICIPANTS_ENDPOINT = "founder_dashboard.participants"


def parse_optional_int(raw: str | None) -> int | None:
    if raw is None or raw == "":
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


def parse_optional_date(raw: str | None) -> date | None:
    if raw is None or not str(raw).strip():
        return None
    try:
        return date.fromisoformat(str(raw).strip())
    except ValueError:
        return None


def parse_submission_ids(raw: str | None) -> tuple[int, ...]:
    if raw is None or not str(raw).strip():
        return ()
    ids: list[int] = []
    for part in str(raw).split(","):
        part = part.strip()
        if not part:
            continue
        try:
            ids.append(int(part))
        except ValueError:
            continue
    return tuple(ids)


def filters_from_request() -> InboxFilters:
    """Build inbox filters from query string parameters."""
    return InboxFilters(
        version=(request.args.get("version") or "").strip() or None,
        badge=(request.args.get("badge") or "").strip() or None,
        feature=(request.args.get("feature") or "").strip() or None,
        severity=(request.args.get("severity") or "").strip() or None,
        status=(request.args.get("status") or "").strip() or None,
        classification=(request.args.get("classification") or "").strip() or None,
        date_from=parse_optional_date(request.args.get("date_from")),
        date_to=parse_optional_date(request.args.get("date_to")),
        submission_source=(request.args.get("submission_source") or "").strip()
        or None,
        keyword=(request.args.get("keyword") or "").strip() or None,
        student=(request.args.get("student") or "").strip() or None,
    )


def redirect_to_feedback(**kwargs: object):
    return redirect(url_for(FEEDBACK_ENDPOINT, **kwargs))


def handle_feedback_request():
    """Process GET/POST for the Feedback section (live Product Check-in inbox)."""
    from app.research.forms import (
        FounderNoteForm,
        ProductFindingForm,
        ResearchInboxFilterForm,
        StatusTransitionForm,
    )

    filter_form = ResearchInboxFilterForm()
    note_form = FounderNoteForm()
    transition_form = StatusTransitionForm()
    finding_form = ProductFindingForm()

    filters = filters_from_request()
    selected_id = parse_optional_int(request.args.get("submission"))
    inbox_page = parse_optional_int(request.args.get("page")) or 1
    time_window = (request.args.get("time_window") or TIME_WINDOW_7_DAYS).strip()
    if time_window not in TIME_WINDOW_LABELS:
        time_window = TIME_WINDOW_7_DAYS
    custom_date_from = parse_optional_date(request.args.get("custom_date_from"))
    custom_date_to = parse_optional_date(request.args.get("custom_date_to"))
    current_release = (request.args.get("current_release") or "").strip() or None
    previous_release = (request.args.get("previous_release") or "").strip() or None

    if request.method == "POST":
        action = request.form.get("action")
        submission_id = parse_optional_int(request.form.get("submission_id"))

        if action == "filter" and filter_form.validate_on_submit():
            return redirect(
                url_for(
                    FEEDBACK_ENDPOINT,
                    version=filter_form.version.data or None,
                    badge=filter_form.badge.data or None,
                    feature=filter_form.feature.data or None,
                    severity=filter_form.severity.data or None,
                    status=filter_form.status.data or None,
                    classification=filter_form.classification.data or None,
                    date_from=filter_form.date_from.data or None,
                    date_to=filter_form.date_to.data or None,
                    submission_source=filter_form.submission_source.data or None,
                    keyword=filter_form.keyword.data or None,
                    student=filter_form.student.data or None,
                    submission=submission_id,
                )
            )

        if submission_id is not None:
            try:
                if action == "helpful":
                    FounderResearchService.apply_founder_marks(
                        submission_id, current_user.id, helpful=True
                    )
                    flash("Marked helpful.", "success")
                elif action == "insightful":
                    FounderResearchService.apply_founder_marks(
                        submission_id, current_user.id, insightful=True
                    )
                    flash("Marked insightful.", "success")
                elif action == "accept":
                    FounderResearchService.transition_submission_status(
                        submission_id, current_user.id, "accepted"
                    )
                    flash("Feedback accepted.", "success")
                elif action == "reject":
                    FounderResearchService.transition_submission_status(
                        submission_id, current_user.id, "rejected"
                    )
                    flash("Feedback rejected.", "info")
                elif action == "clarify":
                    FounderResearchService.transition_submission_status(
                        submission_id,
                        current_user.id,
                        "clarification_requested",
                    )
                    flash("Clarification requested.", "info")
                elif action == "plan":
                    FounderResearchService.transition_submission_status(
                        submission_id, current_user.id, "planned"
                    )
                    flash("Feedback planned.", "success")
                elif action == "implement":
                    result = FounderResearchService.transition_submission_status(
                        submission_id, current_user.id, "implemented"
                    )
                    if result.newly_earned_badges:
                        flash("Implemented. Product Shaper awarded.", "success")
                    else:
                        flash("Feedback marked implemented.", "success")
                elif action == "release":
                    FounderResearchService.transition_submission_status(
                        submission_id, current_user.id, "released"
                    )
                    flash("Feedback released.", "success")
                elif action == "verify":
                    FounderResearchService.transition_submission_status(
                        submission_id, current_user.id, "verified"
                    )
                    flash("Feedback verified.", "success")
                elif action == "under_review":
                    FounderResearchService.transition_submission_status(
                        submission_id, current_user.id, "under_review"
                    )
                    flash("Moved to under review.", "success")
                elif action == "note" and note_form.validate_on_submit():
                    FounderResearchService.add_founder_note(
                        submission_id,
                        current_user.id,
                        note_form.note_text.data,
                    )
                    flash("Note added.", "success")
                elif action == "transition" and transition_form.validate_on_submit():
                    FounderResearchService.transition_submission_status(
                        submission_id,
                        current_user.id,
                        transition_form.to_status.data,
                        rationale=transition_form.rationale.data,
                    )
                    flash("Status updated.", "success")
            except ValueError as exc:
                flash(str(exc), "danger")

            return redirect_to_feedback(
                submission=submission_id,
                **{k: v for k, v in request.args.items()},
            )

        if action == "create_finding" and finding_form.validate_on_submit():
            try:
                finding = FounderResearchService.create_product_finding(
                    current_user.id,
                    title=finding_form.title.data,
                    summary=finding_form.summary.data,
                    severity=finding_form.severity.data,
                    feature_area=finding_form.feature_area.data,
                    status=finding_form.status.data,
                    target_release=finding_form.target_release.data,
                    notes=finding_form.notes.data,
                    linked_submission_ids=parse_submission_ids(
                        finding_form.linked_submission_ids.data
                    ),
                )
                flash(f"Finding created: {finding.title}", "success")
                return redirect(
                    url_for(FINDING_DETAIL_ENDPOINT, finding_id=finding.id)
                )
            except ValueError as exc:
                flash(str(exc), "danger")

    if request.method == "GET":
        filter_form.version.data = filters.version or ""
        filter_form.badge.data = filters.badge or ""
        filter_form.feature.data = filters.feature or ""
        filter_form.severity.data = filters.severity or ""
        filter_form.status.data = filters.status or ""
        filter_form.classification.data = filters.classification or ""
        filter_form.date_from.data = (
            filters.date_from.isoformat() if filters.date_from else ""
        )
        filter_form.date_to.data = (
            filters.date_to.isoformat() if filters.date_to else ""
        )
        filter_form.submission_source.data = filters.submission_source or ""
        filter_form.keyword.data = filters.keyword or ""
        filter_form.student.data = filters.student or ""

    context = FounderResearchService.build_dashboard_context(
        filters,
        selected_submission_id=selected_id,
        time_window=time_window,
        custom_date_from=custom_date_from,
        custom_date_to=custom_date_to,
        current_release=current_release,
        previous_release=previous_release,
        inbox_page=inbox_page,
    )

    return render_template(
        "founder_dashboard/feedback.html",
        title="Feedback",
        context=context,
        filter_form=filter_form,
        note_form=note_form,
        transition_form=transition_form,
        finding_form=finding_form,
        workflow_labels=WORKFLOW_LABELS,
        badge_labels=BADGE_LABELS,
        time_window=time_window,
        time_window_labels=TIME_WINDOW_LABELS,
        custom_date_from=custom_date_from.isoformat() if custom_date_from else "",
        custom_date_to=custom_date_to.isoformat() if custom_date_to else "",
        current_release=current_release or "",
        previous_release=previous_release or "",
        feedback_endpoint=FEEDBACK_ENDPOINT,
        finding_detail_endpoint=FINDING_DETAIL_ENDPOINT,
    )


def handle_finding_detail(finding_id: int):
    """Product finding detail under Findings."""
    from app.research.forms import StatusTransitionForm

    detail = FounderResearchService.get_finding_detail(finding_id)
    if detail is None:
        flash("Finding not found.", "danger")
        return redirect(url_for("founder_dashboard.findings"))

    transition_form = StatusTransitionForm()
    if transition_form.validate_on_submit():
        try:
            FounderResearchService.transition_finding_status(
                finding_id,
                current_user.id,
                transition_form.to_status.data,
                rationale=transition_form.rationale.data,
                target_release=request.form.get("target_release"),
            )
            flash("Finding updated.", "success")
        except ValueError as exc:
            flash(str(exc), "danger")
        return redirect(url_for(FINDING_DETAIL_ENDPOINT, finding_id=finding_id))

    transition_form.to_status.data = detail.finding.status

    return render_template(
        "founder_dashboard/finding_detail.html",
        title=detail.finding.title,
        detail=detail,
        transition_form=transition_form,
        workflow_labels=WORKFLOW_LABELS,
        feedback_endpoint=FEEDBACK_ENDPOINT,
        finding_detail_endpoint=FINDING_DETAIL_ENDPOINT,
    )


def handle_review_submission(submission_id: int):
    """Standalone review form (secondary to inline Feedback actions)."""
    from app.research.forms import FounderFeedbackReviewForm

    form = FounderFeedbackReviewForm()
    if form.validate_on_submit():
        try:
            newly: tuple[str, ...] = ()
            if form.implemented.data:
                result = FounderResearchService.transition_submission_status(
                    submission_id,
                    current_user.id,
                    "implemented",
                )
                FounderResearchService.apply_founder_marks(
                    submission_id,
                    current_user.id,
                    helpful=bool(form.helpful.data),
                    insightful=bool(form.insightful.data),
                )
                newly = result.newly_earned_badges
            else:
                FounderResearchService.apply_founder_marks(
                    submission_id,
                    current_user.id,
                    helpful=bool(form.helpful.data),
                    insightful=bool(form.insightful.data),
                )
        except ValueError as exc:
            flash(str(exc), "danger")
            return redirect_to_feedback()

        if newly:
            labels = [BADGE_LABELS[slug] for slug in newly if slug in BADGE_LABELS]
            flash(
                f"Review saved. Product Shaper awarded: {', '.join(labels)}.",
                "success",
            )
        else:
            flash("Review saved.", "success")
        return redirect_to_feedback(submission=submission_id)

    return render_template(
        "founder_dashboard/review.html",
        title="Review Feedback",
        form=form,
        submission_id=submission_id,
        feedback_endpoint=FEEDBACK_ENDPOINT,
        review_endpoint=REVIEW_ENDPOINT,
    )


def handle_award_founders_circle(user_id: int):
    """Invitation-only Founder's Circle award."""
    badge = ContributorRecognitionService.award_founders_circle(
        user_id,
        current_user.id,
    )
    if badge is None:
        flash("Founder's Circle is already awarded to this student.", "info")
    else:
        flash("Founder's Circle awarded.", "success")
    return redirect(url_for(PARTICIPANTS_ENDPOINT))
