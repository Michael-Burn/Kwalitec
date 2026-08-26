"""WTForms for Assessment Delivery POST actions."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import (
    HiddenField,
    IntegerField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class StartAssessmentForm(FlaskForm):
    """Start a new learning check from the entry surface."""

    instrument_id = HiddenField(validators=[Optional(), Length(max=128)])
    submit = SubmitField("Start learning check")


class BeginAssessmentForm(FlaskForm):
    session_id = HiddenField(validators=[DataRequired(), Length(max=128)])
    submit = SubmitField("Begin")


class RespondAssessmentForm(FlaskForm):
    """Capture a learner response (format validated in delivery strategies)."""

    session_id = HiddenField(validators=[DataRequired(), Length(max=128)])
    question_id = HiddenField(validators=[DataRequired(), Length(max=128)])
    selected_option = StringField(validators=[Optional(), Length(max=128)])
    selected_options = SelectMultipleField(
        choices=[], validators=[Optional()], coerce=str
    )
    linked_concepts = SelectMultipleField(
        choices=[], validators=[Optional()], coerce=str
    )
    entered_value = StringField(validators=[Optional(), Length(max=64)])
    entered_expression = StringField(validators=[Optional(), Length(max=500)])
    entered_text = TextAreaField(validators=[Optional(), Length(max=4000)])
    entered_steps = TextAreaField(validators=[Optional(), Length(max=8000)])
    reflection_text = TextAreaField(validators=[Optional(), Length(max=4000)])
    confidence = IntegerField(
        validators=[Optional(), NumberRange(min=1, max=5)],
    )
    response_time_ms = HiddenField(validators=[Optional(), Length(max=32)])
    submit = SubmitField("Save answer")


class NavigateAssessmentForm(FlaskForm):
    session_id = HiddenField(validators=[DataRequired(), Length(max=128)])
    direction = HiddenField(validators=[DataRequired(), Length(max=16)])
    submit = SubmitField("Continue")


class PauseAssessmentForm(FlaskForm):
    session_id = HiddenField(validators=[DataRequired(), Length(max=128)])
    submit = SubmitField("Pause")


class ResumeAssessmentForm(FlaskForm):
    session_id = HiddenField(validators=[DataRequired(), Length(max=128)])
    submit = SubmitField("Resume")


class CompleteAssessmentForm(FlaskForm):
    session_id = HiddenField(validators=[DataRequired(), Length(max=128)])
    submit = SubmitField("Finish check")


class CancelAssessmentForm(FlaskForm):
    session_id = HiddenField(validators=[DataRequired(), Length(max=128)])
    submit = SubmitField("Leave check")


class HintAssessmentForm(FlaskForm):
    session_id = HiddenField(validators=[DataRequired(), Length(max=128)])
    question_id = HiddenField(validators=[DataRequired(), Length(max=128)])
    submit = SubmitField("Show hint")


class ConfidenceSelectForm(FlaskForm):
    """Optional standalone confidence control (kept for template reuse)."""

    confidence = SelectField(
        choices=[
            ("1", "1: Not sure"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5: Very sure"),
        ],
        validators=[Optional()],
    )
