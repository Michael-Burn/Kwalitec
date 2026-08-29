"""WTForms for Learning Session Experience POST actions."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import (
    HiddenField,
    RadioField,
    StringField,
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
    """Submit an activity response (textarea or MCQ choice id)."""

    session_id = HiddenField(validators=[DataRequired(), Length(max=128)])
    activity_id = HiddenField(validators=[DataRequired(), Length(max=128)])
    response = TextAreaField(
        "Your answer",
        validators=[Optional(), Length(min=1, max=8000)],
    )
    choice = StringField(
        "Your choice",
        validators=[Optional(), Length(max=64)],
    )
    submit = SubmitField("Submit Answer")

    def resolved_response(self) -> str:
        """Prefer MCQ choice id when posted; otherwise free-text response."""
        choice = (self.choice.data or "").strip()
        if choice:
            return choice
        return (self.response.data or "").strip()

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators=extra_validators):
            return False
        if not self.resolved_response():
            self.response.errors.append("A response is required.")
            return False
        return True


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
    confidence_rating = RadioField(
        "Confidence",
        choices=[
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
        ],
        validators=[Optional()],
    )
    submit = SubmitField("Continue to Summary")

    def resolved_confidence_rating(self) -> int | None:
        """Return 1-5 when a valid rating was posted; otherwise None."""
        raw = (self.confidence_rating.data or "").strip()
        if not raw:
            return None
        try:
            value = int(raw)
        except (TypeError, ValueError):
            return None
        if 1 <= value <= 5:
            return value
        return None


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
