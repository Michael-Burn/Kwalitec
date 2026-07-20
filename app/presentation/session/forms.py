"""WTForms for Learning Session Experience POST actions."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class BeginSessionForm(FlaskForm):
    """Begin Session from Overview."""

    session_id = HiddenField(validators=[DataRequired(), Length(max=128)])
    mission_id = HiddenField(validators=[Optional(), Length(max=128)])
    submit = SubmitField("Begin Session")


class SubmitAnswerForm(FlaskForm):
    """Submit an activity response."""

    session_id = HiddenField(validators=[DataRequired(), Length(max=128)])
    activity_id = HiddenField(validators=[DataRequired(), Length(max=128)])
    response = TextAreaField(
        "Your answer",
        validators=[DataRequired(), Length(min=1, max=8000)],
    )
    submit = SubmitField("Submit Answer")


class AdvanceActivityForm(FlaskForm):
    """Advance to the next activity."""

    session_id = HiddenField(validators=[DataRequired(), Length(max=128)])
    submit = SubmitField("Continue")


class ContinueReflectionForm(FlaskForm):
    """Continue from reflection to summary."""

    session_id = HiddenField(validators=[DataRequired(), Length(max=128)])
    reflection_note = StringField(
        "Reflection note",
        validators=[Optional(), Length(max=2000)],
    )
    submit = SubmitField("Continue to Summary")


class CompleteSessionForm(FlaskForm):
    """Complete session and return home."""

    session_id = HiddenField(validators=[DataRequired(), Length(max=128)])
    submit = SubmitField("Return Home")
