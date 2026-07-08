"""Forms for mission review and learning recording."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, TextAreaField, validators
from wtforms.validators import DataRequired, Optional, ValidationError


class MissionReviewForm(FlaskForm):
    """Form for reviewing a completed mission and recording learning."""

    duration_minutes = IntegerField(
        "Time Spent (minutes)",
        validators=[
            DataRequired(),
            validators.NumberRange(min=1, max=600, message="Must be between 1 and 600 minutes"),
        ],
        render_kw={"placeholder": "e.g., 45", "min": 1, "max": 600},
    )

    questions_attempted = IntegerField(
        "Questions Attempted",
        validators=[Optional(), validators.NumberRange(min=0)],
        render_kw={"placeholder": "e.g., 10"},
    )

    questions_correct = IntegerField(
        "Questions Correct",
        validators=[Optional(), validators.NumberRange(min=0)],
        render_kw={"placeholder": "e.g., 8"},
    )

    confidence_before = SelectField(
        "Confidence Before",
        choices=[
            ("Not Started", "Not Sure"),
            ("Low", "Not Confident"),
            ("Medium", "Somewhat Confident"),
            ("High", "Confident"),
            ("Mastered", "Very Confident"),
        ],
        validators=[DataRequired()],
    )

    confidence_after = SelectField(
        "Confidence After",
        choices=[
            ("Not Started", "Not Sure"),
            ("Low", "Not Confident"),
            ("Medium", "Somewhat Confident"),
            ("High", "Confident"),
            ("Mastered", "Very Confident"),
        ],
        validators=[DataRequired()],
    )

    notes = TextAreaField(
        "Notes",
        validators=[Optional()],
        render_kw={
            "placeholder": "What did you learn? What was difficult?",
            "rows": 4,
        },
    )

    def validate_questions_correct(self, field):
        """Validate that correct <= attempted."""
        if (
            self.questions_correct.data is not None
            and self.questions_attempted.data is not None
        ):
            if self.questions_correct.data > self.questions_attempted.data:
                raise ValidationError(
                    "Questions correct cannot exceed questions attempted."
                )


class MistakeForm(FlaskForm):
    """Form for recording a single mistake."""

    mistake_type = SelectField(
        "Type of Mistake",
        choices=[
            ("", "-- Select --"),
            ("Calculation", "Calculation Error"),
            ("Concept", "Conceptual Misunderstanding"),
            ("Misconception", "Misconception"),
            ("Careless", "Careless Error"),
            ("Misreading", "Misread Question"),
            ("Method", "Wrong Method"),
            ("Other", "Other"),
        ],
        validators=[DataRequired()],
    )

    description = TextAreaField(
        "What Went Wrong?",
        validators=[
            DataRequired(message="Please describe the mistake."),
            validators.Length(min=10, max=500),
        ],
        render_kw={
            "placeholder": "Explain what you did wrong and why...",
            "rows": 3,
        },
    )

    correct_solution = TextAreaField(
        "Correct Solution",
        validators=[Optional(), validators.Length(max=500)],
        render_kw={
            "placeholder": "What's the correct approach or answer?",
            "rows": 3,
        },
    )
