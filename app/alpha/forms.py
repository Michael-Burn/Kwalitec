"""WTForms for Internal Alpha feedback — ALPHA-001."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import HiddenField, RadioField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

from app.services.alpha_feedback_service import (
    KIND_EXPLANATION_CLEAR,
    KIND_MISSION_HELPFUL,
    KIND_REPORT_PROBLEM,
    KIND_SUGGEST_IMPROVEMENT,
    RATING_NO,
    RATING_YES,
)


class MissionHelpfulForm(FlaskForm):
    """Was this mission helpful?"""

    kind = HiddenField(default=KIND_MISSION_HELPFUL)
    mission_id = HiddenField()
    surface = HiddenField()
    rating = RadioField(
        "Was this mission helpful?",
        choices=[(RATING_YES, "Yes"), (RATING_NO, "No")],
        validators=[DataRequired(message="Please choose yes or no.")],
    )
    message = TextAreaField(
        "Optional note",
        validators=[Optional(), Length(max=500)],
        render_kw={"rows": 2, "maxlength": 500},
    )


class ExplanationClearForm(FlaskForm):
    """Was this explanation clear?"""

    kind = HiddenField(default=KIND_EXPLANATION_CLEAR)
    mission_id = HiddenField()
    surface = HiddenField()
    rating = RadioField(
        "Was this explanation clear?",
        choices=[(RATING_YES, "Yes"), (RATING_NO, "No")],
        validators=[DataRequired(message="Please choose yes or no.")],
    )
    message = TextAreaField(
        "Optional note",
        validators=[Optional(), Length(max=500)],
        render_kw={"rows": 2, "maxlength": 500},
    )


class ReportProblemForm(FlaskForm):
    """Report a problem during Internal Alpha."""

    kind = HiddenField(default=KIND_REPORT_PROBLEM)
    mission_id = HiddenField()
    surface = HiddenField()
    reference_id = StringField(
        "Error reference (optional)",
        validators=[Optional(), Length(max=64)],
    )
    message = TextAreaField(
        "What went wrong?",
        validators=[
            DataRequired(message="Please describe the problem."),
            Length(max=500),
        ],
        render_kw={"rows": 4, "maxlength": 500},
    )


class PrivateBetaFeedbackForm(FlaskForm):
    """PB-001 categorised student feedback with auto context capture."""

    category = SelectField(
        "What are you reporting?",
        choices=[],
        validators=[DataRequired(message="Please choose a category.")],
    )
    mission_id = HiddenField()
    current_screen = HiddenField()
    subject_code = HiddenField()
    browser = HiddenField()
    device = HiddenField()
    path = HiddenField()
    message = TextAreaField(
        "Tell us more",
        validators=[
            DataRequired(message="Please include a short message."),
            Length(max=1000),
        ],
        render_kw={"rows": 4, "maxlength": 1000},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from app.services.private_beta.feedback_service import (
            PrivateBetaFeedbackService,
        )

        self.category.choices = PrivateBetaFeedbackService.category_choices()


class SuggestImprovementForm(FlaskForm):
    """Suggest an improvement."""

    kind = HiddenField(default=KIND_SUGGEST_IMPROVEMENT)
    mission_id = HiddenField()
    surface = HiddenField()
    message = TextAreaField(
        "What would you improve?",
        validators=[
            DataRequired(message="Please share a short suggestion."),
            Length(max=500),
        ],
        render_kw={"rows": 4, "maxlength": 500},
    )


class TelemetryIngestForm(FlaskForm):
    """Client-side presentation telemetry ingest."""

    event_type = HiddenField(validators=[DataRequired()])
    resource_type = HiddenField()
    resource_id = HiddenField()
    surface = HiddenField()
