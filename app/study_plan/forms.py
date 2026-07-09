"""Forms for the exam-aware Study Plan Wizard."""

from __future__ import annotations

from datetime import date

from flask_wtf import FlaskForm
from wtforms import (
    HiddenField,
    IntegerField,
    RadioField,
    SelectField,
    StringField,
    SubmitField,
    validators,
)
from wtforms.fields import DateField
from wtforms.validators import Optional

from app.services import examination_catalogue as catalogue


# ─────────────────────────────────────────────────────────────────────────────
# Step 1 — Examination category
# ─────────────────────────────────────────────────────────────────────────────


class ExamCategoryForm(FlaskForm):
    """Step 1: Select the examination category."""

    exam_category = RadioField(
        "Examination",
        choices=catalogue.get_category_choices(),
        validators=[validators.DataRequired("Please select an examination.")],
    )
    submit = SubmitField("Next")


# ─────────────────────────────────────────────────────────────────────────────
# Step 2 — Paper / subject
# ─────────────────────────────────────────────────────────────────────────────


class ExamPaperForm(FlaskForm):
    """Step 2: Select the paper or enter a free-text subject."""

    exam_paper = RadioField(
        "Paper / Subject",
        choices=[],  # populated dynamically in the route
        validators=[Optional()],
    )
    free_text_subject = StringField(
        "Subject",
        validators=[Optional(), validators.Length(max=255)],
    )
    submit = SubmitField("Next")


# ─────────────────────────────────────────────────────────────────────────────
# Step 3 — Sitting & exam date
# ─────────────────────────────────────────────────────────────────────────────


class ExamSittingForm(FlaskForm):
    """Step 3: Select exam sitting and date."""

    exam_sitting = SelectField(
        "Sitting",
        choices=[],  # populated dynamically in the route
        validators=[validators.DataRequired("Please select a sitting.")],
    )
    exam_date = DateField(
        "Exam Date",
        format="%Y-%m-%d",
        validators=[validators.DataRequired("Exam date is required.")],
    )
    submit = SubmitField("Next")

    def validate_exam_date(form, field):
        """Validate that the exam date is in the future."""
        if field.data <= date.today():
            raise validators.ValidationError("Exam date must be in the future.")


# ─────────────────────────────────────────────────────────────────────────────
# Step 4 — Current position
# ─────────────────────────────────────────────────────────────────────────────


class CurrentPositionForm(FlaskForm):
    """Step 4: Where are you currently?"""

    current_position = RadioField(
        "Current Position",
        choices=[
            ("not_started", "I haven't started"),
            ("learning", "I've started but I'm still learning new material"),
            ("completed", "I've completed the syllabus once"),
            ("revising", "I'm currently revising"),
        ],
        validators=[validators.DataRequired("Please select your current position.")],
    )
    current_topic = StringField(
        "What topic are you currently studying?",
        validators=[Optional(), validators.Length(max=255)],
    )
    submit = SubmitField("Next")


# ─────────────────────────────────────────────────────────────────────────────
# Step 5 — Study availability & session length
# ─────────────────────────────────────────────────────────────────────────────


class StudyAvailabilityForm(FlaskForm):
    """Step 5: How much time can you realistically study?"""

    weekday_study_minutes = IntegerField(
        "Weekdays (minutes per day)",
        validators=[
            validators.DataRequired("Weekday study time is required."),
            validators.NumberRange(
                min=15, max=480, message="Study time must be between 15 and 480 minutes."
            ),
        ],
    )
    weekend_study_minutes = IntegerField(
        "Weekend (minutes per day)",
        validators=[
            validators.DataRequired("Weekend study time is required."),
            validators.NumberRange(
                min=15, max=480, message="Study time must be between 15 and 480 minutes."
            ),
        ],
    )
    preferred_session_minutes = RadioField(
        "Preferred study session length",
        choices=[(30, "30 minutes"), (45, "45 minutes"), (60, "60 minutes"),
                 (90, "90 minutes"), (120, "120 minutes")],
        coerce=int,
        default=60,
        validators=[validators.DataRequired()],
    )
    submit = SubmitField("Next")


# ─────────────────────────────────────────────────────────────────────────────
# Step 6 — Learning style
# ─────────────────────────────────────────────────────────────────────────────


class StudyPreferenceForm(FlaskForm):
    """Step 6: How do you prefer to learn?"""

    study_preference = RadioField(
        "Learning Style",
        choices=[
            ("Reading First", "Reading First"),
            ("Questions First", "Questions First"),
            ("Mixed", "Mixed"),
        ],
        default="Mixed",
        validators=[validators.DataRequired()],
    )
    submit = SubmitField("Next")


# ─────────────────────────────────────────────────────────────────────────────
# Step 7 — Target result
# ─────────────────────────────────────────────────────────────────────────────


class TargetResultForm(FlaskForm):
    """Step 7: What result are you aiming for?"""

    target_grade = RadioField(
        "Target Result",
        choices=[],  # populated dynamically in the route
        validators=[validators.DataRequired("Please select a target result.")],
    )
    submit = SubmitField("Create Study Plan")


# ─────────────────────────────────────────────────────────────────────────────
# Step 8 — Review
# ─────────────────────────────────────────────────────────────────────────────


class StudyPlanReviewForm(FlaskForm):
    """Final step: Review and confirm study plan."""

    confirm = RadioField(
        "Does everything look correct?",
        choices=[
            ("yes", "Yes, create my study plan"),
            ("no", "No, let me make changes"),
        ],
        default="yes",
        validators=[validators.DataRequired()],
    )
    submit = SubmitField("Confirm")