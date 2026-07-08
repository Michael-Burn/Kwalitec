"""Study Plan blueprint routes."""

from __future__ import annotations

import logging
from datetime import date

from flask import Blueprint, flash, redirect, render_template, session, url_for
from flask_login import current_user, login_required

from app.services.study_plan_service import StudyPlanService
from app.study_plan.forms import (
    CurrentStageForm,
    ExamSelectionForm,
    ExamSittingForm,
    StudyAvailabilityForm,
    StudyPlanReviewForm,
    StudyPreferenceForm,
    TargetGradeForm,
    UnavailableDaysForm,
)

logger = logging.getLogger(__name__)

study_plan_bp = Blueprint("study_plan", __name__, url_prefix="/study-plan")


@study_plan_bp.get("/")
@login_required
def index():
    """Redirect to the active study plan or wizard if none exists."""
    active_plan = StudyPlanService.get_user_active_plan(current_user.id)
    if active_plan:
        return redirect(url_for("study_plan.view_plan", study_plan_id=active_plan.id))
    return redirect(url_for("study_plan.wizard_step", step=1))


@study_plan_bp.get("/wizard/<int:step>")
@login_required
def wizard_step(step: int):
    """Handle a specific step of the study plan wizard."""
    if step < 1 or step > 7:
        return redirect(url_for("study_plan.wizard_step", step=1))

    # Render the appropriate step
    if step == 1:
        return _handle_step_1_exam_selection()
    elif step == 2:
        return _handle_step_2_exam_sitting()
    elif step == 3:
        return _handle_step_3_current_stage()
    elif step == 4:
        return _handle_step_4_study_availability()
    elif step == 5:
        return _handle_step_5_unavailable_days()
    elif step == 6:
        return _handle_step_6_study_preference()
    elif step == 7:
        return _handle_step_7_target_grade()
    else:
        return redirect(url_for("study_plan.wizard_step", step=1))


@study_plan_bp.post("/wizard/<int:step>")
@login_required
def wizard_step_post(step: int):
    """Handle form submission for a wizard step."""
    if step < 1 or step > 7:
        return redirect(url_for("study_plan.wizard_step", step=1))

    if "wizard_data" not in session:
        session["wizard_data"] = {}

    if step == 1:
        return _handle_step_1_post()
    elif step == 2:
        return _handle_step_2_post()
    elif step == 3:
        return _handle_step_3_post()
    elif step == 4:
        return _handle_step_4_post()
    elif step == 5:
        return _handle_step_5_post()
    elif step == 6:
        return _handle_step_6_post()
    elif step == 7:
        return _handle_step_7_post()
    else:
        return redirect(url_for("study_plan.wizard_step", step=1))


def _handle_step_1_exam_selection():
    """Display exam selection form."""
    form = ExamSelectionForm()
    wizard_data = session.get("wizard_data", {})
    if "exam_name" in wizard_data:
        form.exam_name.data = wizard_data["exam_name"]
    return render_template("study_plan/wizard_step_1.html", form=form, step=1, total_steps=7)


def _handle_step_1_post():
    """Process exam selection form."""
    form = ExamSelectionForm()
    if form.validate_on_submit():
        session["wizard_data"]["exam_name"] = form.exam_name.data
        session.modified = True
        return redirect(url_for("study_plan.wizard_step", step=2))
    return render_template("study_plan/wizard_step_1.html", form=form, step=1, total_steps=7)


def _handle_step_2_exam_sitting():
    """Display exam sitting form."""
    form = ExamSittingForm()
    wizard_data = session.get("wizard_data", {})
    if "exam_sitting" in wizard_data:
        form.exam_sitting.data = wizard_data["exam_sitting"]
    if "exam_date" in wizard_data:
        form.exam_date.data = wizard_data["exam_date"]
    return render_template("study_plan/wizard_step_2.html", form=form, step=2, total_steps=7)


def _handle_step_2_post():
    """Process exam sitting form."""
    form = ExamSittingForm()
    if form.validate_on_submit():
        session["wizard_data"]["exam_sitting"] = form.exam_sitting.data
        # Store date as ISO format string for reliable session serialization
        exam_date = form.exam_date.data
        if hasattr(exam_date, "isoformat"):
            session["wizard_data"]["exam_date"] = exam_date.isoformat()
        else:
            session["wizard_data"]["exam_date"] = str(exam_date)
        session.modified = True
        return redirect(url_for("study_plan.wizard_step", step=3))
    return render_template("study_plan/wizard_step_2.html", form=form, step=2, total_steps=7)


def _handle_step_3_current_stage():
    """Display current stage form."""
    form = CurrentStageForm()
    wizard_data = session.get("wizard_data", {})
    if "current_stage" in wizard_data:
        form.current_stage.data = wizard_data["current_stage"]
    return render_template("study_plan/wizard_step_3.html", form=form, step=3, total_steps=7)


def _handle_step_3_post():
    """Process current stage form."""
    form = CurrentStageForm()
    if form.validate_on_submit():
        session["wizard_data"]["current_stage"] = form.current_stage.data
        session.modified = True
        return redirect(url_for("study_plan.wizard_step", step=4))
    return render_template("study_plan/wizard_step_3.html", form=form, step=3, total_steps=7)


def _handle_step_4_study_availability():
    """Display study availability form."""
    form = StudyAvailabilityForm()
    wizard_data = session.get("wizard_data", {})
    if "weekday_study_minutes" in wizard_data:
        form.weekday_study_minutes.data = wizard_data["weekday_study_minutes"]
    if "weekend_study_minutes" in wizard_data:
        form.weekend_study_minutes.data = wizard_data["weekend_study_minutes"]
    return render_template("study_plan/wizard_step_4.html", form=form, step=4, total_steps=7)


def _handle_step_4_post():
    """Process study availability form."""
    form = StudyAvailabilityForm()
    if form.validate_on_submit():
        session["wizard_data"]["weekday_study_minutes"] = form.weekday_study_minutes.data
        session["wizard_data"]["weekend_study_minutes"] = form.weekend_study_minutes.data
        session.modified = True
        return redirect(url_for("study_plan.wizard_step", step=5))
    return render_template("study_plan/wizard_step_4.html", form=form, step=4, total_steps=7)


def _handle_step_5_unavailable_days():
    """Display unavailable days form."""
    form = UnavailableDaysForm()
    wizard_data = session.get("wizard_data", {})
    if "available_days" in wizard_data:
        form.available_days.data = wizard_data["available_days"]
    else:
        form.available_days.data = "all"
    return render_template("study_plan/wizard_step_5.html", form=form, step=5, total_steps=7)


def _handle_step_5_post():
    """Process unavailable days form."""
    form = UnavailableDaysForm()
    if form.validate_on_submit():
        session["wizard_data"]["available_days"] = form.available_days.data
        session.modified = True
        return redirect(url_for("study_plan.wizard_step", step=6))
    return render_template("study_plan/wizard_step_5.html", form=form, step=5, total_steps=7)


def _handle_step_6_study_preference():
    """Display study preference form."""
    form = StudyPreferenceForm()
    wizard_data = session.get("wizard_data", {})
    if "study_preference" in wizard_data:
        form.study_preference.data = wizard_data["study_preference"]
    else:
        form.study_preference.data = "Mixed"
    return render_template("study_plan/wizard_step_6.html", form=form, step=6, total_steps=7)


def _handle_step_6_post():
    """Process study preference form."""
    form = StudyPreferenceForm()
    if form.validate_on_submit():
        session["wizard_data"]["study_preference"] = form.study_preference.data
        session.modified = True
        return redirect(url_for("study_plan.wizard_step", step=7))
    return render_template("study_plan/wizard_step_6.html", form=form, step=6, total_steps=7)


def _handle_step_7_target_grade():
    """Display target grade form."""
    form = TargetGradeForm()
    wizard_data = session.get("wizard_data", {})
    if "target_grade" in wizard_data:
        form.target_grade.data = wizard_data["target_grade"]
    return render_template("study_plan/wizard_step_7.html", form=form, step=7, total_steps=7)


def _handle_step_7_post():
    """Process target grade form and redirect to review."""
    form = TargetGradeForm()
    if form.validate_on_submit():
        session["wizard_data"]["target_grade"] = form.target_grade.data
        session.modified = True
        return redirect(url_for("study_plan.review"))
    return render_template("study_plan/wizard_step_7.html", form=form, step=7, total_steps=7)


@study_plan_bp.get("/review")
@login_required
def review():
    """Review the study plan before creation."""
    wizard_data = session.get("wizard_data", {})

    if not wizard_data or "exam_name" not in wizard_data:
        flash("Please complete the wizard from the beginning.", "info")
        return redirect(url_for("study_plan.wizard_step", step=1))

    form = StudyPlanReviewForm()
    return render_template(
        "study_plan/review.html", form=form, wizard_data=wizard_data, step=8, total_steps=8
    )


@study_plan_bp.post("/review")
@login_required
def review_post():
    """Handle study plan creation."""
    wizard_data = session.get("wizard_data", {})

    if not wizard_data or "exam_name" not in wizard_data:
        flash("Please complete the wizard from the beginning.", "info")
        return redirect(url_for("study_plan.wizard_step", step=1))

    form = StudyPlanReviewForm()
    if form.validate_on_submit():
        if form.confirm.data == "no":
            session.pop("wizard_data", None)
            flash("Wizard cancelled. You can start over anytime.", "info")
            return redirect(url_for("study_plan.wizard_step", step=1))

        # Validate all required fields are present
        required_fields = [
            "exam_name", "exam_sitting", "exam_date",
            "weekday_study_minutes", "weekend_study_minutes",
            "current_stage", "study_preference", "target_grade",
        ]
        missing = [f for f in required_fields if f not in wizard_data or not wizard_data[f]]
        if missing:
            flash(f"Missing required fields: {', '.join(missing)}. Please restart the wizard.", "danger")
            session.pop("wizard_data", None)
            return redirect(url_for("study_plan.wizard_step", step=1))

        # Create the study plan
        try:
            # Convert exam_date string from session to date object
            exam_date_str = wizard_data["exam_date"]
            if isinstance(exam_date_str, str):
                exam_date = date.fromisoformat(exam_date_str)
            else:
                exam_date = exam_date_str

            study_plan = StudyPlanService.create_study_plan(
                user_id=current_user.id,
                exam_name=wizard_data["exam_name"],
                exam_sitting=wizard_data["exam_sitting"],
                exam_date=exam_date,
                weekday_study_minutes=int(wizard_data["weekday_study_minutes"]),
                weekend_study_minutes=int(wizard_data["weekend_study_minutes"]),
                current_stage=wizard_data["current_stage"],
                study_preference=wizard_data["study_preference"],
                target_grade=wizard_data["target_grade"],
            )

            # Clear wizard data from session
            session.pop("wizard_data", None)

            logger.info("Study plan %d created for user %s", study_plan.id, current_user.id)
            flash("Study plan created successfully!", "success")
            return redirect(url_for("study_plan.view_plan", study_plan_id=study_plan.id))
        except ValueError as e:
            logger.warning("Study plan creation failed: %s", e)
            flash(str(e), "danger")
            form.confirm.errors = [str(e)]

    return render_template(
        "study_plan/review.html", form=form, wizard_data=wizard_data, step=8, total_steps=8
    )


@study_plan_bp.get("/<int:study_plan_id>")
@login_required
def view_plan(study_plan_id: int):
    """View a study plan."""
    from app.models.study_plan import StudyPlan

    study_plan = StudyPlan.query.get(study_plan_id)

    if not study_plan:
        flash("Study plan not found.", "warning")
        return redirect(url_for("study_plan.index"))

    if study_plan.user_id != current_user.id:
        flash("You can only view your own study plans.", "danger")
        return redirect(url_for("study_plan.index"))

    return render_template("study_plan/view.html", study_plan=study_plan)


@study_plan_bp.get("/plans/all")
@login_required
def list_plans():
    """List all study plans for the user."""
    plans = StudyPlanService.get_user_plans(current_user.id)
    return render_template("study_plan/list.html", plans=plans)