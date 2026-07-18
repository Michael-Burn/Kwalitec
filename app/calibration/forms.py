"""Forms for Alpha Student Calibration (Capability 3.8.1).

Closed declaration fields only — never mastery, readiness, or recommendation
inputs. Presentation maps these into the Application Calibration Contract.
"""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    RadioField,
    SelectMultipleField,
    SubmitField,
    validators,
)
from wtforms.widgets import CheckboxInput, ListWidget


class MultiCheckboxField(SelectMultipleField):
    """Multi-select rendered as checkboxes."""

    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class AlphaCalibrationForm(FlaskForm):
    """Minimal Alpha Calibration — educational history declarations only."""

    previously_studied = RadioField(
        "Have you studied this paper before?",
        choices=[
            ("first_time", "No — I'm starting from scratch"),
            ("previously_studied", "Yes — I've studied this before"),
        ],
        validators=[validators.DataRequired("Please tell us your starting point.")],
    )
    core_reading_completed = RadioField(
        "Have you completed the Core Reading?",
        choices=[
            ("none", "Not yet / not applicable"),
            ("whole_paper", "Yes — whole paper (declared)"),
        ],
        default="none",
        validators=[validators.DataRequired()],
    )
    previous_attempts_count = IntegerField(
        "How many times have you sat this paper before?",
        default=0,
        validators=[
            validators.Optional(),
            validators.NumberRange(
                min=0, max=20, message="Attempts must be between 0 and 20."
            ),
        ],
    )
    study_objective = RadioField(
        "What are you aiming for now?",
        choices=[
            ("first_sit", "First learning / first sit"),
            ("revision", "Revision after Core Reading"),
            ("finish_remaining", "Finish remaining sections"),
            ("resit", "Re-sit / another attempt"),
        ],
        default="first_sit",
        validators=[validators.DataRequired()],
    )
    completed_sections = MultiCheckboxField(
        "Sections you've already covered (declared)",
        choices=[],  # populated in the route from curriculum when available
        validators=[validators.Optional()],
    )
    confirm = RadioField(
        "Confirm these are your declarations — not Estimated Knowledge",
        choices=[
            ("yes", "Yes — record what I declared and continue"),
        ],
        default="yes",
        validators=[validators.DataRequired()],
    )
    submit = SubmitField("Create my study profile")
    skip_beginner = SubmitField("I'm starting from scratch — skip detail")
    abandon = SubmitField("Continue without declaring history")
