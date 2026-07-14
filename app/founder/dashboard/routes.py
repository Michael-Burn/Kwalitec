"""Founder Dashboard HTTP routes (FOS-004)."""

from __future__ import annotations

from flask import render_template

from app.founder.dashboard import founder_dashboard_bp
from app.founder.dashboard.access import founder_required, is_founder_user
from app.founder.dashboard.services import FounderDashboardService


def _service() -> FounderDashboardService:
    """Build the default dashboard service (live Founder providers)."""
    return FounderDashboardService()


@founder_dashboard_bp.get("/")
@founder_dashboard_bp.get("")
@founder_required
def index():
    """Render the Founder Operating System executive dashboard."""
    page = _service().build_page()
    return render_template(
        "founder_dashboard/index.html",
        title="Founder Operating System",
        page=page,
        overview=page.overview,
    )


@founder_dashboard_bp.app_context_processor
def inject_founder_nav() -> dict[str, bool]:
    """Expose Founder nav visibility to all templates."""
    return {"show_founder_nav": is_founder_user()}
