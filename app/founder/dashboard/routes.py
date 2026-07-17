"""Founder Command Centre HTTP routes (IAHF-003 / POP-002).

Single Founder operational home under ``/founder``. Legacy Research
Command Centre URLs redirect here for compatibility.
"""

from __future__ import annotations

from flask import render_template, request, url_for
from flask_login import current_user

from app.founder.dashboard import founder_dashboard_bp
from app.founder.dashboard.access import founder_required, is_founder_user
from app.founder.dashboard.feedback_handlers import (
    handle_award_founders_circle,
    handle_feedback_request,
    handle_finding_detail,
    handle_review_submission,
)
from app.founder.dashboard.nav import COMMAND_CENTRE_NAV, active_section_id
from app.founder.dashboard.services.command_centre_service import (
    CommandCentreService,
    build_operations_page,
)
from app.founder.dashboard.vision_handlers import (
    handle_remove_relation,
    handle_vision_edit,
    handle_vision_entry,
    handle_vision_export,
    handle_vision_journal,
    handle_vision_new,
    handle_vision_timeline,
)
from app.services.founder_research_service import (
    WORKFLOW_LABELS,
    FounderResearchService,
    InboxFilters,
)
from app.services.internal_alpha_status_service import InternalAlphaStatusService
from app.services.research_insight_service import (
    TIME_WINDOW_7_DAYS,
    TIME_WINDOW_LABELS,
)


def _overview_service() -> CommandCentreService:
    return CommandCentreService(founder_user_id=current_user.id)


@founder_dashboard_bp.app_context_processor
def inject_founder_nav() -> dict:
    """Expose Founder nav visibility and Command Centre section chrome."""
    endpoint = request.endpoint if request else None
    return {
        "show_founder_nav": is_founder_user(),
        "command_centre_nav": COMMAND_CENTRE_NAV,
        "command_centre_section": active_section_id(endpoint),
        "is_founder_command_centre": bool(
            endpoint and endpoint.startswith("founder_dashboard.")
        ),
    }


@founder_dashboard_bp.get("/")
@founder_dashboard_bp.get("")
@founder_required
def index():
    """Founder Command Centre Overview — the sole Founder home."""
    overview = _overview_service().build_overview()
    return render_template(
        "founder_dashboard/overview.html",
        title="Founder Command Centre",
        overview=overview,
    )


@founder_dashboard_bp.get("/attention")
@founder_required
def attention():
    """Triage queue: outstanding reviews and high-severity findings."""
    items = _overview_service().list_attention_items()
    return render_template(
        "founder_dashboard/attention.html",
        title="Attention",
        items=items,
    )


@founder_dashboard_bp.route("/feedback", methods=["GET", "POST"])
@founder_required
def feedback():
    """Product Check-in inbox and submission workflow (live SoT)."""
    return handle_feedback_request()


@founder_dashboard_bp.get("/findings")
@founder_required
def findings():
    """Product Findings list."""
    severity = (request.args.get("severity") or "").strip() or None
    status = (request.args.get("status") or "").strip() or None
    findings_list = FounderResearchService.list_findings(
        severity=severity,
        status=status,
        limit=100,
    )
    return render_template(
        "founder_dashboard/findings.html",
        title="Findings",
        findings=findings_list,
        severity=severity or "",
        status=status or "",
        workflow_labels=WORKFLOW_LABELS,
    )


@founder_dashboard_bp.route(
    "/findings/<int:finding_id>", methods=["GET", "POST"]
)
@founder_required
def finding_detail(finding_id: int):
    """Product Finding detail."""
    return handle_finding_detail(finding_id)


@founder_dashboard_bp.get("/research")
@founder_required
def research():
    """Research insights and product health (read/decide)."""
    time_window = (request.args.get("time_window") or TIME_WINDOW_7_DAYS).strip()
    if time_window not in TIME_WINDOW_LABELS:
        time_window = TIME_WINDOW_7_DAYS
    context = FounderResearchService.build_dashboard_context(
        InboxFilters(),
        time_window=time_window,
    )
    return render_template(
        "founder_dashboard/research.html",
        title="Research",
        context=context,
        time_window=time_window,
        time_window_labels=TIME_WINDOW_LABELS,
    )


@founder_dashboard_bp.get("/internal-alpha")
@founder_required
def internal_alpha():
    """Internal Alpha programme health — live Product Check-in SoT."""
    summary = FounderResearchService.get_internal_alpha_summary()
    changes = FounderResearchService.get_changes_since_yesterday()
    status = InternalAlphaStatusService.build_status(current_user.id)
    return render_template(
        "founder_dashboard/internal_alpha.html",
        title="Internal Alpha",
        summary=summary,
        changes=changes,
        alpha_status=status,
    )


@founder_dashboard_bp.get("/participants")
@founder_required
def participants():
    """Alpha participants roster and recognition."""
    rows = _overview_service().list_participants()
    return render_template(
        "founder_dashboard/participants.html",
        title="Participants",
        participants=rows,
    )


@founder_dashboard_bp.get("/operations")
@founder_required
def operations():
    """System & engineering readiness (FOS Operational State)."""
    page = build_operations_page()
    return render_template(
        "founder_dashboard/operations.html",
        title="Operations",
        page=page,
        overview=page.overview,
    )


@founder_dashboard_bp.get("/releases")
@founder_required
def releases():
    """Release identity and findings by target release."""
    status = InternalAlphaStatusService.build_status(current_user.id)
    findings_list = FounderResearchService.list_findings(limit=100)
    by_release: dict[str, list] = {}
    for finding in findings_list:
        label = (finding.target_release or "").strip() or "Unassigned"
        by_release.setdefault(label, []).append(finding)
    return render_template(
        "founder_dashboard/releases.html",
        title="Releases",
        alpha_status=status,
        findings_by_release=by_release,
    )


@founder_dashboard_bp.get("/vision")
@founder_required
def vision_journal():
    """Founder Vision Journal — strategic memory of product ideas."""
    return handle_vision_journal()


@founder_dashboard_bp.get("/vision/timeline")
@founder_required
def vision_timeline():
    """Chronological Vision Journal timeline."""
    return handle_vision_timeline()


@founder_dashboard_bp.route("/vision/new", methods=["GET", "POST"])
@founder_required
def vision_new():
    """Create a structured vision entry."""
    return handle_vision_new()


@founder_dashboard_bp.route("/vision/<int:entry_id>", methods=["GET", "POST"])
@founder_required
def vision_entry(entry_id: int):
    """Vision entry detail, relations, and promotion."""
    return handle_vision_entry(entry_id)


@founder_dashboard_bp.route(
    "/vision/<int:entry_id>/edit", methods=["GET", "POST"]
)
@founder_required
def vision_edit(entry_id: int):
    """Edit a vision entry."""
    return handle_vision_edit(entry_id)


@founder_dashboard_bp.get("/vision/export/<fmt>")
@founder_required
def vision_export(fmt: str):
    """Export Vision Journal (markdown, json, csv)."""
    return handle_vision_export(fmt)


@founder_dashboard_bp.post(
    "/vision/<int:entry_id>/relations/<int:relation_id>/remove"
)
@founder_required
def vision_remove_relation(entry_id: int, relation_id: int):
    """Remove a vision entry relationship."""
    return handle_remove_relation(relation_id, entry_id)


@founder_dashboard_bp.get("/settings")
@founder_required
def settings():
    """Founder settings bridge to product Settings / Internal Alpha."""
    status = InternalAlphaStatusService.build_status(current_user.id)
    return render_template(
        "founder_dashboard/settings.html",
        title="Founder Settings",
        alpha_status=status,
        product_settings_url=url_for("settings.index"),
    )


@founder_dashboard_bp.route(
    "/feedback/review/<int:submission_id>",
    methods=["GET", "POST"],
)
@founder_required
def review_submission(submission_id: int):
    """Optional standalone review form."""
    return handle_review_submission(submission_id)


@founder_dashboard_bp.post("/participants/award-founders-circle/<int:user_id>")
@founder_required
def award_founders_circle(user_id: int):
    """Award Founder's Circle from Participants."""
    return handle_award_founders_circle(user_id)
