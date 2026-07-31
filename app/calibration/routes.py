"""Student Calibration routes — SB-001A deprecated student UI.

Student-facing Calibration redirects to Baseline. Application Twin-birth
modules remain available for Baseline reuse.
"""

from __future__ import annotations

import logging

from flask import flash, redirect, url_for
from flask_login import current_user, login_required

from app.calibration import calibration_bp
from app.models.study_plan import StudyPlan
from app.services.study_plan_service import StudyPlanService

logger = logging.getLogger(__name__)


def _load_owned_plan(study_plan_id: int) -> StudyPlan | None:
    from app.extensions import db

    plan = db.session.get(StudyPlan, study_plan_id)
    if plan is None or plan.user_id != current_user.id:
        return None
    return plan


@calibration_bp.get("/after-plan/<int:study_plan_id>")
@login_required
def start(study_plan_id: int):
    """Deprecated — redirect to Baseline for this study plan."""
    plan = _load_owned_plan(study_plan_id)
    if plan is None:
        flash("Study plan not found.", "warning")
        return redirect(url_for("study_plan.index"))
    flash(
        "Educational history now starts with Baseline — continuing there.",
        "info",
    )
    return redirect(
        url_for("student_baseline.for_plan", study_plan_id=study_plan_id)
    )


@calibration_bp.post("/after-plan/<int:study_plan_id>")
@login_required
def submit(study_plan_id: int):
    """Deprecated POST — redirect to Baseline."""
    return redirect(
        url_for("student_baseline.for_plan", study_plan_id=study_plan_id)
    )


@calibration_bp.get("/resume")
@login_required
def resume():
    """Deprecated resume — open Baseline for the active plan when present."""
    plan = StudyPlanService.get_user_active_plan(current_user.id)
    if plan is None:
        flash("Choose your exam to begin Baseline.", "info")
        return redirect(url_for("study_plan.wizard_step", step=1))
    return redirect(
        url_for("student_baseline.for_plan", study_plan_id=plan.id)
    )
