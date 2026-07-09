"""Study Plan blueprint routes — exam-aware wizard."""

from __future__ import annotations

import logging
from datetime import date

from flask import Blueprint, flash, redirect, render_template, session, url_for
from flask_login import current_user, login_required

from app.services import examination_catalogue as catalogue
from app.services.study_plan_service import StudyPlanService
from app.study_plan.forms import (
    CurrentPositionForm,
    ExamCategoryForm,
    ExamPaperForm,
    ExamSittingForm,
    StudyAvailabilityForm,
    StudyPlanReviewForm,
    StudyPreferenceForm,
    TargetResultForm,
)

logger = logging.getLogger(__name__)

study_plan_bp = Blueprint("study_plan", __name__, url_prefix="/study-plan")

TOTAL_STEPS = 7

# Step titles used for progress display
STEP_TITLES = {
    1: "Examination",
    2: "Paper / Subject",
    3: "Exam Date",
    4: "Current Position",
    5: "Availability",
    6: "Learning Style",
    7: "Target",
    8: "Review",
}


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def _position_label(code: str) -> str:
    """Map a current_position code to a human-readable label."""
    return {
        "not_started": "I haven't started",
        "learning": "Learning new material",
        "completed": "Completed the syllabus once",
        "revising": "Currently revising",
    }.get(code, code)


def _build_current_stage(position: str, topic: str | None) -> str:
    """Combine position and topic into a single current_stage string.

    The existing StudyPlan.current_stage column is reused so no schema change
    is required for the position data.
    """
    label = _position_label(position)
    if position == "learning" and topic:
        return f"{label}: {topic}"
    return label


def _parse_current_stage(current_stage: str) -> tuple[str, str]:
    """Split a stored current_stage back into (position_code, topic)."""
    if not current_stage:
        return "not_started", ""
    if current_stage.startswith("I haven't started"):
        return "not_started", ""
    if current_stage.startswith("Learning new material"):
        topic = ""
        if ": " in current_stage:
            topic = current_stage.split(": ", 1)[1]
        return "learning", topic
    if current_stage.startswith("Completed the syllabus once"):
        return "completed", ""
    if current_stage.startswith("Currently revising"):
        return "revising", ""
    return "learning", current_stage


# ─────────────────────────────────────────────────────────────────────────────
# Index
# ─────────────────────────────────────────────────────────────────────────────


@study_plan_bp.get("/")
@login_required
def index():
    """Redirect to the active study plan or wizard if none exists."""
    active_plan = StudyPlanService.get_user_active_plan(current_user.id)
    if active_plan:
        return redirect(url_for("study_plan.view_plan", study_plan_id=active_plan.id))
    return redirect(url_for("study_plan.wizard_step", step=1))


# ─────────────────────────────────────────────────────────────────────────────
# Wizard — GET
# ─────────────────────────────────────────────────────────────────────────────


@study_plan_bp.get("/wizard/<int:step>")
@login_required
def wizard_step(step: int):
    """Handle a specific step of the study plan wizard."""
    if step < 1 or step > TOTAL_STEPS:
        return redirect(url_for("study_plan.wizard_step", step=1))

    if step == 1:
        return _handle_step_1()
    elif step == 2:
        return _handle_step_2()
    elif step == 3:
        return _handle_step_3()
    elif step == 4:
        return _handle_step_4()
    elif step == 5:
        return _handle_step_5()
    elif step == 6:
        return _handle_step_6()
    elif step == 7:
        return _handle_step_7()
    return redirect(url_for("study_plan.wizard_step", step=1))


# ─────────────────────────────────────────────────────────────────────────────
# Wizard — POST
# ─────────────────────────────────────────────────────────────────────────────


@study_plan_bp.post("/wizard/<int:step>")
@login_required
def wizard_step_post(step: int):
    """Handle form submission for a wizard step."""
    if step < 1 or step > TOTAL_STEPS:
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
    return redirect(url_for("study_plan.wizard_step", step=1))


# ─────────────────────────────────────────────────────────────────────────────
# Step 1 — Examination category
# ─────────────────────────────────────────────────────────────────────────────


def _handle_step_1():
    """Display exam category selection form."""
    form = ExamCategoryForm()
    wizard_data = session.get("wizard_data", {})
    if "exam_category" in wizard_data:
        form.exam_category.data = wizard_data["exam_category"]
    categories = catalogue.get_categories()
    return render_template(
        "study_plan/wizard_step_1.html",
        form=form,
        step=1,
        total_steps=TOTAL_STEPS,
        step_title=STEP_TITLES[1],
        categories=categories,
    )


def _handle_step_1_post():
    """Process exam category selection form."""
    form = ExamCategoryForm()
    if form.validate_on_submit():
        session["wizard_data"]["exam_category"] = form.exam_category.data
        # Clear downstream data when category changes
        for key in ("exam_paper", "free_text_subject", "exam_sitting",
                    "exam_date", "target_grade"):
            session["wizard_data"].pop(key, None)
        session.modified = True
        return redirect(url_for("study_plan.wizard_step", step=2))
    categories = catalogue.get_categories()
    return render_template(
        "study_plan/wizard_step_1.html",
        form=form,
        step=1,
        total_steps=TOTAL_STEPS,
        step_title=STEP_TITLES[1],
        categories=categories,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Step 2 — Paper / subject
# ─────────────────────────────────────────────────────────────────────────────


def _handle_step_2():
    """Display paper/subject selection form."""
    wizard_data = session.get("wizard_data", {})
    category_code = wizard_data.get("exam_category")
    if not category_code:
        flash("Please complete the wizard from the beginning.", "info")
        return redirect(url_for("study_plan.wizard_step", step=1))

    form = ExamPaperForm()
    category = catalogue.get_category(category_code)
    if not category:
        flash("Invalid examination category. Please start again.", "warning")
        return redirect(url_for("study_plan.wizard_step", step=1))

    if not category.free_text_subject:
        form.exam_paper.choices = catalogue.get_paper_choices(category_code)
        if "exam_paper" in wizard_data:
            form.exam_paper.data = wizard_data["exam_paper"]
    if "free_text_subject" in wizard_data:
        form.free_text_subject.data = wizard_data["free_text_subject"]

    return render_template(
        "study_plan/wizard_step_2.html",
        form=form,
        step=2,
        total_steps=TOTAL_STEPS,
        step_title=STEP_TITLES[2],
        category=category,
    )


def _handle_step_2_post():
    """Process paper/subject selection form."""
    wizard_data = session.get("wizard_data", {})
    category_code = wizard_data.get("exam_category")
    if not category_code:
        flash("Please complete the wizard from the beginning.", "info")
        return redirect(url_for("study_plan.wizard_step", step=1))

    form = ExamPaperForm()
    category = catalogue.get_category(category_code)
    if not category:
        flash("Invalid examination category. Please start again.", "warning")
        return redirect(url_for("study_plan.wizard_step", step=1))

    if category.free_text_subject:
        if form.free_text_subject.validate(form) and form.free_text_subject.data.strip():
            session["wizard_data"]["free_text_subject"] = form.free_text_subject.data.strip()
            session["wizard_data"].pop("exam_paper", None)
            session.modified = True
            return redirect(url_for("study_plan.wizard_step", step=3))
        form.free_text_subject.errors = ["Please enter your subject."]
    else:
        form.exam_paper.choices = catalogue.get_paper_choices(category_code)
        if form.exam_paper.validate(form) and form.exam_paper.data:
            session["wizard_data"]["exam_paper"] = form.exam_paper.data
            session["wizard_data"].pop("free_text_subject", None)
            session.modified = True
            return redirect(url_for("study_plan.wizard_step", step=3))
        form.exam_paper.errors = ["Please select a paper."]

    return render_template(
        "study_plan/wizard_step_2.html",
        form=form,
        step=2,
        total_steps=TOTAL_STEPS,
        step_title=STEP_TITLES[2],
        category=category,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Step 3 — Sitting & exam date
# ─────────────────────────────────────────────────────────────────────────────


def _handle_step_3():
    """Display exam sitting/date form."""
    wizard_data = session.get("wizard_data", {})
    category_code = wizard_data.get("exam_category")
    if not category_code:
        flash("Please complete the wizard from the beginning.", "info")
        return redirect(url_for("study_plan.wizard_step", step=1))

    form = ExamSittingForm()
    form.exam_sitting.choices = catalogue.get_sitting_choices(category_code)
    if "exam_sitting" in wizard_data:
        form.exam_sitting.data = wizard_data["exam_sitting"]
    if "exam_date" in wizard_data:
        form.exam_date.data = wizard_data["exam_date"]
    return render_template(
        "study_plan/wizard_step_3.html",
        form=form,
        step=3,
        total_steps=TOTAL_STEPS,
        step_title=STEP_TITLES[3],
    )


def _handle_step_3_post():
    """Process exam sitting/date form."""
    wizard_data = session.get("wizard_data", {})
    category_code = wizard_data.get("exam_category")
    if not category_code:
        flash("Please complete the wizard from the beginning.", "info")
        return redirect(url_for("study_plan.wizard_step", step=1))

    form = ExamSittingForm()
    form.exam_sitting.choices = catalogue.get_sitting_choices(category_code)
    if form.validate_on_submit():
        session["wizard_data"]["exam_sitting"] = form.exam_sitting.data
        exam_date = form.exam_date.data
        if hasattr(exam_date, "isoformat"):
            session["wizard_data"]["exam_date"] = exam_date.isoformat()
        else:
            session["wizard_data"]["exam_date"] = str(exam_date)
        session.modified = True
        return redirect(url_for("study_plan.wizard_step", step=4))
    return render_template(
        "study_plan/wizard_step_3.html",
        form=form,
        step=3,
        total_steps=TOTAL_STEPS,
        step_title=STEP_TITLES[3],
    )


# ─────────────────────────────────────────────────────────────────────────────
# Step 4 — Current position
# ─────────────────────────────────────────────────────────────────────────────


def _handle_step_4():
    """Display current position form."""
    form = CurrentPositionForm()
    wizard_data = session.get("wizard_data", {})
    if "current_position" in wizard_data:
        form.current_position.data = wizard_data["current_position"]
    if "current_topic" in wizard_data:
        form.current_topic.data = wizard_data["current_topic"]
    return render_template(
        "study_plan/wizard_step_4.html",
        form=form,
        step=4,
        total_steps=TOTAL_STEPS,
        step_title=STEP_TITLES[4],
    )


def _handle_step_4_post():
    """Process current position form."""
    form = CurrentPositionForm()
    if form.validate_on_submit():
        session["wizard_data"]["current_position"] = form.current_position.data
        session["wizard_data"]["current_topic"] = (
            form.current_topic.data.strip() if form.current_topic.data else ""
        )
        session.modified = True
        return redirect(url_for("study_plan.wizard_step", step=5))
    return render_template(
        "study_plan/wizard_step_4.html",
        form=form,
        step=4,
        total_steps=TOTAL_STEPS,
        step_title=STEP_TITLES[4],
    )


# ─────────────────────────────────────────────────────────────────────────────
# Step 5 — Study availability & session length
# ─────────────────────────────────────────────────────────────────────────────


def _handle_step_5():
    """Display study availability form."""
    form = StudyAvailabilityForm()
    wizard_data = session.get("wizard_data", {})
    if "weekday_study_minutes" in wizard_data:
        form.weekday_study_minutes.data = wizard_data["weekday_study_minutes"]
    if "weekend_study_minutes" in wizard_data:
        form.weekend_study_minutes.data = wizard_data["weekend_study_minutes"]
    if "preferred_session_minutes" in wizard_data:
        form.preferred_session_minutes.data = wizard_data["preferred_session_minutes"]
    return render_template(
        "study_plan/wizard_step_5.html",
        form=form,
        step=5,
        total_steps=TOTAL_STEPS,
        step_title=STEP_TITLES[5],
    )


def _handle_step_5_post():
    """Process study availability form."""
    form = StudyAvailabilityForm()
    if form.validate_on_submit():
        session["wizard_data"]["weekday_study_minutes"] = form.weekday_study_minutes.data
        session["wizard_data"]["weekend_study_minutes"] = form.weekend_study_minutes.data
        session["wizard_data"]["preferred_session_minutes"] = form.preferred_session_minutes.data
        session.modified = True
        return redirect(url_for("study_plan.wizard_step", step=6))
    return render_template(
        "study_plan/wizard_step_5.html",
        form=form,
        step=5,
        total_steps=TOTAL_STEPS,
        step_title=STEP_TITLES[5],
    )


# ─────────────────────────────────────────────────────────────────────────────
# Step 6 — Learning style
# ─────────────────────────────────────────────────────────────────────────────


def _handle_step_6():
    """Display study preference form."""
    form = StudyPreferenceForm()
    wizard_data = session.get("wizard_data", {})
    if "study_preference" in wizard_data:
        form.study_preference.data = wizard_data["study_preference"]
    else:
        form.study_preference.data = "Mixed"
    return render_template(
        "study_plan/wizard_step_6.html",
        form=form,
        step=6,
        total_steps=TOTAL_STEPS,
        step_title=STEP_TITLES[6],
    )


def _handle_step_6_post():
    """Process study preference form."""
    form = StudyPreferenceForm()
    if form.validate_on_submit():
        session["wizard_data"]["study_preference"] = form.study_preference.data
        session.modified = True
        return redirect(url_for("study_plan.wizard_step", step=7))
    return render_template(
        "study_plan/wizard_step_6.html",
        form=form,
        step=6,
        total_steps=TOTAL_STEPS,
        step_title=STEP_TITLES[6],
    )


# ─────────────────────────────────────────────────────────────────────────────
# Step 7 — Target result
# ─────────────────────────────────────────────────────────────────────────────


def _handle_step_7():
    """Display target result form."""
    wizard_data = session.get("wizard_data", {})
    category_code = wizard_data.get("exam_category")
    if not category_code:
        flash("Please complete the wizard from the beginning.", "info")
        return redirect(url_for("study_plan.wizard_step", step=1))

    form = TargetResultForm()
    form.target_grade.choices = catalogue.get_target_choices(category_code)
    if "target_grade" in wizard_data:
        form.target_grade.data = wizard_data["target_grade"]
    return render_template(
        "study_plan/wizard_step_7.html",
        form=form,
        step=7,
        total_steps=TOTAL_STEPS,
        step_title=STEP_TITLES[7],
    )


def _handle_step_7_post():
    """Process target result form and redirect to review."""
    wizard_data = session.get("wizard_data", {})
    category_code = wizard_data.get("exam_category")
    if not category_code:
        flash("Please complete the wizard from the beginning.", "info")
        return redirect(url_for("study_plan.wizard_step", step=1))

    form = TargetResultForm()
    form.target_grade.choices = catalogue.get_target_choices(category_code)
    if form.validate_on_submit():
        session["wizard_data"]["target_grade"] = form.target_grade.data
        session.modified = True
        return redirect(url_for("study_plan.review"))
    return render_template(
        "study_plan/wizard_step_7.html",
        form=form,
        step=7,
        total_steps=TOTAL_STEPS,
        step_title=STEP_TITLES[7],
    )


# ─────────────────────────────────────────────────────────────────────────────
# Review
# ─────────────────────────────────────────────────────────────────────────────


@study_plan_bp.get("/review")
@login_required
def review():
    """Review the study plan before creation."""
    wizard_data = session.get("wizard_data", {})

    if not wizard_data or "exam_category" not in wizard_data:
        flash("Please complete the wizard from the beginning.", "info")
        return redirect(url_for("study_plan.wizard_step", step=1))

    review_data = _build_review_data(wizard_data)
    form = StudyPlanReviewForm()
    return render_template(
        "study_plan/review.html",
        form=form,
        wizard_data=wizard_data,
        review_data=review_data,
        step=8,
        total_steps=TOTAL_STEPS + 1,
        step_title=STEP_TITLES[8],
    )


@study_plan_bp.post("/review")
@login_required
def review_post():
    """Handle study plan creation."""
    wizard_data = session.get("wizard_data", {})

    if not wizard_data or "exam_category" not in wizard_data:
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
            "exam_category", "exam_sitting", "exam_date",
            "weekday_study_minutes", "weekend_study_minutes",
            "current_position", "study_preference", "target_grade",
        ]
        missing = [f for f in required_fields if f not in wizard_data or not wizard_data[f]]
        if missing:
            flash(
                f"Missing required fields: {', '.join(missing)}. Please restart the wizard.",
                "danger",
            )
            session.pop("wizard_data", None)
            return redirect(url_for("study_plan.wizard_step", step=1))

        # Build the exam_name from category + paper/subject
        category_code = wizard_data["exam_category"]
        if catalogue.is_free_text_subject(category_code):
            paper_or_subject = wizard_data.get("free_text_subject", "")
        else:
            paper_or_subject = wizard_data.get("exam_paper", "")
        exam_name = catalogue.format_exam_name(category_code, paper_or_subject)

        # Build current_stage from position + topic
        current_stage = _build_current_stage(
            wizard_data["current_position"],
            wizard_data.get("current_topic") or None,
        )

        # Create the study plan
        try:
            exam_date_str = wizard_data["exam_date"]
            if isinstance(exam_date_str, str):
                exam_date = date.fromisoformat(exam_date_str)
            else:
                exam_date = exam_date_str

            preferred_session = int(wizard_data.get("preferred_session_minutes", 60))

            study_plan = StudyPlanService.create_study_plan(
                user_id=current_user.id,
                exam_name=exam_name,
                exam_sitting=wizard_data["exam_sitting"],
                exam_date=exam_date,
                weekday_study_minutes=int(wizard_data["weekday_study_minutes"]),
                weekend_study_minutes=int(wizard_data["weekend_study_minutes"]),
                current_stage=current_stage,
                study_preference=wizard_data["study_preference"],
                target_grade=wizard_data["target_grade"],
                preferred_session_minutes=preferred_session,
            )

            session.pop("wizard_data", None)

            logger.info("Study plan %d created for user %s", study_plan.id, current_user.id)
            flash("Study plan created successfully!", "success")
            return redirect(url_for("study_plan.view_plan", study_plan_id=study_plan.id))
        except ValueError as e:
            logger.warning("Study plan creation failed: %s", e)
            flash(str(e), "danger")
            form.confirm.errors = [str(e)]

    review_data = _build_review_data(wizard_data)
    return render_template(
        "study_plan/review.html",
        form=form,
        wizard_data=wizard_data,
        review_data=review_data,
        step=8,
        total_steps=TOTAL_STEPS + 1,
        step_title=STEP_TITLES[8],
    )


def _build_review_data(wizard_data: dict) -> dict:
    """Build a structured dict for the review template sections."""
    category_code = wizard_data.get("exam_category", "")
    category = catalogue.get_category(category_code)

    # Paper / subject display
    if catalogue.is_free_text_subject(category_code):
        paper_label = wizard_data.get("free_text_subject", "")
    else:
        paper_label = wizard_data.get("exam_paper", "")

    exam_name = catalogue.format_exam_name(category_code, paper_label) if paper_label else ""

    # Exam date + days remaining
    exam_date_str = wizard_data.get("exam_date", "")
    days_remaining = None
    exam_date_display = exam_date_str
    if exam_date_str:
        try:
            exam_date = date.fromisoformat(exam_date_str) if isinstance(exam_date_str, str) else exam_date_str
            exam_date_display = exam_date.strftime("%B %d, %Y")
            days_remaining = (exam_date - date.today()).days
        except (ValueError, TypeError):
            pass

    # Current position
    position_code = wizard_data.get("current_position", "")
    position_label = _position_label(position_code)
    current_topic = wizard_data.get("current_topic", "")

    return {
        "category": category,
        "category_code": category_code,
        "paper_label": paper_label,
        "exam_name": exam_name,
        "exam_sitting": wizard_data.get("exam_sitting", ""),
        "exam_date_display": exam_date_display,
        "days_remaining": days_remaining,
        "position_label": position_label,
        "current_topic": current_topic,
        "weekday_study_minutes": wizard_data.get("weekday_study_minutes", ""),
        "weekend_study_minutes": wizard_data.get("weekend_study_minutes", ""),
        "preferred_session_minutes": wizard_data.get("preferred_session_minutes", ""),
        "study_preference": wizard_data.get("study_preference", ""),
        "target_grade": wizard_data.get("target_grade", ""),
    }


# ─────────────────────────────────────────────────────────────────────────────
# View & list plans
# ─────────────────────────────────────────────────────────────────────────────


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