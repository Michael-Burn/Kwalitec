"""Forms for the Study Plan Wizard."""

from __future__ import annotations

from datetime import date, timedelta

from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    RadioField,
    StringField,
    SubmitField,
    validators,
)
from wtforms.fields import DateField


class ExamSelectionForm(FlaskForm):
    """Step 1: Select the examination."""

    exam_name = RadioField(
        "Examination",
        choices=[
            ("A-Level", "A-Level"),
            ("GCSE", "GCSE"),
            ("IB", "International Baccalaureate (IB)"),
            ("Cambridge", "Cambridge University"),
            ("Oxford", "Oxford University"),
            ("Professional Exam", "Professional Certification"),
            ("Other", "Other"),
        ],
        validators=[validators.DataRequired("Please select an examination.")],
    )
    submit = SubmitField("Next")


class ExamSittingForm(FlaskForm):
    """Step 2: Select exam sitting/date."""

    exam_sitting = StringField(
        "Exam Sitting",
        description="e.g., June 2026, January 2027",
        validators=[
            validators.DataRequired("Exam sitting is required."),
            validators.Length(min=4, max=50),
        ],
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


class CurrentStageForm(FlaskForm):
    """Step 3: Enter current study position."""

    current_stage = StringField(
        "Current Study Position",
        description="e.g., Chapter 3, Unit 2, Topic: Photosynthesis",
        validators=[
            validators.DataRequired("Current study position is required."),
            validators.Length(min=2, max=255),
        ],
    )
    submit = SubmitField("Next")


class StudyAvailabilityForm(FlaskForm):
    """Step 4: Enter weekday/weekend study availability."""

    weekday_study_minutes = IntegerField(
        "Weekday Study Time (minutes)",
        description="How many minutes per weekday can you study?",
        validators=[
            validators.DataRequired("Weekday study time is required."),
            validators.NumberRange(
                min=15, max=480, message="Study time must be between 15 and 480 minutes."
            ),
        ],
    )
    weekend_study_minutes = IntegerField(
        "Weekend Study Time (minutes)",
        description="How many minutes per weekend day can you study?",
        validators=[
            validators.DataRequired("Weekend study time is required."),
            validators.NumberRange(
                min=15, max=480, message="Study time must be between 15 and 480 minutes."
            ),
        ],
    )
    submit = SubmitField("Next")


class UnavailableDaysForm(FlaskForm):
    """Step 5: Select unavailable days."""

    # Note: This form would typically be handled with checkboxes in JavaScript
    # For now, we'll accept all days as available and handle unavailable days
    # through a separate mechanism (could be stored in a future feature)
    available_days = RadioField(
        "Availability",
        choices=[
            ("all", "Study all days of the week"),
            ("weekdays", "Study only weekdays"),
            ("custom", "Select specific days (coming soon)"),
        ],
        default="all",
    )
    submit = SubmitField("Next")


class StudyPreferenceForm(FlaskForm):
    """Step 6: Select study preference."""

    study_preference = RadioField(
        "How would you prefer to study?",
        choices=[
            ("Reading First", "Reading First - Read material first, then practice questions"),
            ("Questions First", "Questions First - Start with practice questions, then read"),
            ("Mixed", "Mixed - Alternate between reading and questions"),
        ],
        default="Mixed",
        validators=[validators.DataRequired()],
    )
    submit = SubmitField("Next")


class TargetGradeForm(FlaskForm):
    """Step 7: Select target grade."""

    target_grade = RadioField(
        "Target Grade",
        choices=[
            ("A", "A - Excellence"),
            ("B", "B - Very Good"),
            ("C", "C - Good"),
            ("D", "D - Satisfactory"),
            ("Pass", "Pass - Acceptable"),
            ("Distinction", "Distinction"),
            ("Merit", "Merit"),
        ],
        validators=[validators.DataRequired("Please select a target grade.")],
    )
    submit = SubmitField("Create Study Plan")


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
