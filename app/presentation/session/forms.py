"""WTForms for Learning Session Experience POST actions."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import (
    HiddenField,
    RadioField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, Optional


class BeginSessionForm(FlaskForm):
    """Start Session from Overview (same verb family as Home)."""

    session_id = HiddenField(validators=[DataRequired(), Length(max=128)])
    mission_id = HiddenField(validators=[Optional(), Length(max=128)])
    submit = SubmitField("Start Session")


class PauseSessionForm(FlaskForm):
    """Pause Study Session — safe leave without completing."""

    session_id = HiddenField(validators=[DataRequired(), Length(max=128)])
    submit = SubmitField("Pause Session")


class ResumeSessionForm(FlaskForm):
    """Resume a paused Study Session."""

    session_id = HiddenField(validators=[DataRequired(), Length(max=128)])
    submit = SubmitField("Resume Session")


class ChecklistItemForm(FlaskForm):
    """Toggle a plan-checklist item."""

    session_id = HiddenField(validators=[DataRequired(), Length(max=128)])
    item_id = HiddenField(validators=[DataRequired(), Length(max=64)])
    done = HiddenField(validators=[Optional(), Length(max=8)])
    submit = SubmitField("Update")


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
    reflection_note = TextAreaField(
        "Your reflection",
        validators=[Optional(), Length(max=2000)],
    )
    submit = SubmitField("Continue to Summary")


class FinishReviewForm(FlaskForm):
    """Explicit Finish Review — Yes / Partially / No (LXP-003)."""

    session_id = HiddenField(validators=[DataRequired(), Length(max=128)])
    completion_status = RadioField(
        "Did you complete today's planned study?",
        choices=[
            ("yes", "Yes"),
            ("partially", "Partially"),
            ("no", "No"),
        ],
        validators=[DataRequired()],
    )
    notes = TextAreaField(
        "Optional notes",
        validators=[Optional(), Length(max=2000)],
    )
    submit = SubmitField("Finish Session")


class CompleteSessionForm(FlaskForm):
    """Complete session and return home (rollback path without finish review)."""

    session_id = HiddenField(validators=[DataRequired(), Length(max=128)])
    submit = SubmitField("Return Home")
